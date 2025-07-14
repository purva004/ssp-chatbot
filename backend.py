import os
import json
import re
import subprocess
import dateparser
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

# RAG imports
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Graph imports
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Neo4jVector
from langchain_neo4j import Neo4jVector

# CrewAI imports
import sys
sys.path.append('./crewAI')
from crewai_agent import run_crewai_query

# -------- CONFIG --------
DATA_PATH = "data.json"
INDEX_PATH = "vector.index"
DOC_STORE_PATH = "data_store.json"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_MODEL_PATH = "all-MiniLM-L6-v2"
NEO4J_URL = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "purva@1234"
COLLECTION_NAME = "vectorbot"

# Load environment variables
from dotenv import load_dotenv
load_dotenv(".env.local")
DEFAULT_OLLAMA_MODEL = os.getenv("NEXT_PUBLIC_DEFAULT_MODEL", "Gemma3:1b")

# Create FastAPI app
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Define request models
class QueryRequest(BaseModel):
    question: str
    model: str | None = None

class CrewQuery(BaseModel):
    query: str

# Helper functions
def normalize_dates(text):
    parsed = dateparser.parse(text)
    return parsed.strftime("%Y-%m-%d") if parsed else text

def ask_ollama(prompt: str, model: str) -> str:
    result = subprocess.run(["ollama", "run", model], input=prompt.encode(), stdout=subprocess.PIPE)
    return result.stdout.decode().strip()

def load_json_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Initialize systems
try:
    # RAG system initialization
    if not os.path.exists(INDEX_PATH):
        print("Building RAG index...")
        raw_data = load_json_data()
        entries = []
        for d in raw_data:
            date = d.get("RecordDate", "unknown date")
            time = d.get("Time", "")
            hour = int(datetime.strptime(time, "%H:%M:%S").hour) if time else None
            part = (
                "morning" if 5 <= hour < 12 else
                "afternoon" if 12 <= hour < 17 else
                "evening" if 17 <= hour < 21 else
                "night"
            ) if hour is not None else ""
            entry = f"""On {d.get("DayOfWeek", "")}, {date} at {d.get("SiteDetails", "")} ({d.get("Floor", "")}, {d.get("LocationCode", "").replace("LOC-IN-", "")}), WiFi count: {d.get("WiFiCount", "N/A")}, Access count: {d.get("AccessControlCount", "N/A")}, Type: {d.get("DayType", "")}, TimeSlot: {d.get("TimeSlot", "")}. Part of day: {part}."""
            entries.append(entry)
        
        model = SentenceTransformer(LOCAL_MODEL_PATH)
        vectors = model.encode(entries, normalize_embeddings=True)
        index = faiss.IndexFlatIP(len(vectors[0]))
        index.add(np.array(vectors))
        faiss.write_index(index, INDEX_PATH)
        with open(DOC_STORE_PATH, "w") as f:
            json.dump(raw_data, f)
    
    # Load RAG components
    rag_index = faiss.read_index(INDEX_PATH)
    with open(DOC_STORE_PATH, "r") as f:
        rag_docs = json.load(f)
    rag_model = SentenceTransformer(LOCAL_MODEL_PATH)
    
    # Graph system initialization
    embeddings = HuggingFaceEmbeddings(model_name=LOCAL_MODEL_PATH)
    graph_vectorstore = Neo4jVector.from_texts(
        texts=[],
        embedding=embeddings,
        url=NEO4J_URL,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database="neo4j",
        index_name="embedding_index",
        node_label="LogEntry",
        text_node_property="text",
    )
    graph_retriever = graph_vectorstore.as_retriever()
    graph_docs = load_json_data()
    
except Exception as e:
    print(f"Error initializing systems: {e}")
    rag_index = None
    rag_docs = []
    rag_model = None
    graph_retriever = None
    graph_docs = []

# RAG functions
def search_rag(query, model, index, docs, top_k=10):
    if not model or not index:
        return []
    qv = model.encode([query], normalize_embeddings=True)[0]
    if top_k > len(docs):
        top_k = len(docs)
    D, I = index.search(np.array([qv]), top_k)
    unique_indices = []
    seen = set()
    for i in I[0]:
        if i not in seen and i < len(docs):
            unique_indices.append(i)
            seen.add(i)
    return [docs[i] for i in unique_indices]

def filter_logs(docs, query):
    query = query.lower()
    filters = {}
    
    # Extract filters from query
    date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", query)
    if date_match:
        filters["RecordDate"] = date_match.group(1)
    
    for city in ["pune", "mumbai", "bangalore", "kalwa"]:
        if city in query:
            filters["LocationCode"] = city.upper()
            break
    
    filtered = []
    for doc in docs:
        match = True
        for k, v in filters.items():
            if k == "LocationCode":
                loc = doc.get("LocationCode", "").replace("LOC-IN-", "").upper()
                if loc != v:
                    match = False
                    break
            else:
                if str(doc.get(k, "")).lower() != v.lower():
                    match = False
                    break
        if match:
            filtered.append(doc)
    return filtered

def doc_to_entry(d):
    location = d.get("LocationCode", "").replace("LOC-IN-", "")
    date = d.get("RecordDate", "unknown date")
    time = d.get("Time", "")
    hour = int(datetime.strptime(time, "%H:%M:%S").hour) if time else None
    part = (
        "morning" if 5 <= hour < 12 else
        "afternoon" if 12 <= hour < 17 else
        "evening" if 17 <= hour < 21 else
        "night"
    ) if hour is not None else ""
    return (
        f"On {d.get('DayOfWeek', '')}, {date} at {d.get('SiteDetails', '')} "
        f"({d.get('Floor', '')}, {location}), WiFi count: {d.get('WiFiCount', 'N/A')}, "
        f"Access count: {d.get('AccessControlCount', 'N/A')}, Type: {d.get('DayType', '')}, "
        f"TimeSlot: {d.get('TimeSlot', '')}. Part of day: {part}."
    )

# RAG Endpoint
@app.post("/rag/query")
async def ask_rag(request: QueryRequest):
    try:
        norm_q = normalize_dates(request.question).lower()
        filtered_docs = filter_logs(rag_docs, norm_q)
        
        if not filtered_docs:
            results = search_rag(norm_q, rag_model, rag_index, rag_docs, top_k=10)
        else:
            results = [doc_to_entry(d) for d in filtered_docs]
        
        if not results:
            return {"answer": "No relevant information found."}
        
        prompt = f"""You are an expert log analyst. Use the following context to answer the question.

Relevant entries:
{chr(10).join(str(r) for r in results[:5])}

Question: {norm_q}
Answer:"""
        
        model_name = request.model or DEFAULT_OLLAMA_MODEL
        answer = ask_ollama(prompt, model_name)
        
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error processing RAG query: {str(e)}"}

# Graph Endpoint
@app.post("/graph/query")
async def ask_graph(request: QueryRequest):
    try:
        norm_q = normalize_dates(request.question).lower()
        filtered_docs = filter_logs(graph_docs, norm_q)
        
        if not filtered_docs and graph_retriever:
            results = graph_retriever.get_relevant_documents(norm_q)
            results = [doc.page_content for doc in results]
        else:
            results = [doc_to_entry(d) for d in filtered_docs]
        
        if not results:
            return {"answer": "No relevant information found."}
        
        prompt = f"""You are an expert log analyst. Use the following context to answer the question.

Relevant entries:
{chr(10).join(str(r) for r in results[:5])}

Question: {norm_q}
Answer:"""
        
        model_name = request.model or DEFAULT_OLLAMA_MODEL
        answer = ask_ollama(prompt, model_name)
        
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error processing Graph query: {str(e)}"}

# CrewAI Endpoint
@app.post("/crewai/query")
async def ask_crewai(query: CrewQuery):
    try:
        result = run_crewai_query(query.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CrewAI error: {str(e)}")

# Health Check Endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Unified Backend"}

