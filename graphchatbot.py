import os
import json
import re
import subprocess
import dateparser
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Neo4jVector
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain_neo4j import Neo4jVector


# -------- CONFIG --------
DATA_PATH = "data.json"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# EMBEDDING_DIM = 384
NEO4J_URL = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "purva@1234"
COLLECTION_NAME = "vectorbot"

load_dotenv(".env.local")
DEFAULT_OLLAMA_MODEL = os.getenv("NEXT_PUBLIC_DEFAULT_MODEL", "Gemma3:1b")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    question: str
    model: str | None = None

def normalize_dates(text):
    parsed = dateparser.parse(text)
    return parsed.strftime("%Y-%m-%d") if parsed else text

def ask_ollama(prompt: str, model: str) -> str:
    result = subprocess.run(["ollama", "run", model], input=prompt.encode(), stdout=subprocess.PIPE)
    return result.stdout.decode().strip()

def load_json_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def json_to_text_entries(data):
    text_entries = []
    for item in data:
        text = (
            f"Location: {item.get('LocationCode', '')}, "
            f"Date: {item.get('RecordDate', '')}, Time: {item.get('Time', '')}, "
            f"Day: {item.get('DayOfWeek', '')}, Slot: {item.get('TimeSlot', '')}, "
            f"Floor: {item.get('Floor', '')}, Site: {item.get('SiteDetails', '')}, "
            f"Type: {item.get('DayType', '')}, "
            f"AccessControlCount: {item.get('AccessControlCount', '')}, "
            f"WiFiCount: {item.get('WiFiCount', '')}"
        )
        text_entries.append(text)
    return text_entries

def setup_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=LOCAL_MODEL_PATH)

    db = Neo4jVector.from_texts(
        texts=json_to_text_entries(load_json_data()),
        embedding=embeddings,
        url=NEO4J_URL,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database="neo4j",  # Optional if using default
        index_name="embedding_index",  # Optional name
        node_label="LogEntry",  # You can change this
        text_node_property="text",  # Must match property used internally
    )

    return db




def init_vector_store():
    raw_data = load_json_data()
    texts = json_to_text_entries(raw_data)
    metadata = raw_data

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Neo4jVector.from_texts(
        texts,
        embedding=embeddings,
        metadatas=metadata,
        url=NEO4J_URL,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database="neo4j",
        index_name=COLLECTION_NAME
    )
    return vectorstore.as_retriever(), raw_data

retriever, docs = init_vector_store()

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

def filter_logs(docs, query):
    query = query.lower()
    filters = {}

    date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", query)
    if date_match:
        filters["RecordDate"] = date_match.group(1)

    time_match = re.search(r"\b(\d{1,2}:\d{2}(?::\d{2})?)\b", query)
    if time_match:
        filters["Time"] = time_match.group(1)

    timeslot_match = re.search(r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})", query)
    if timeslot_match:
        filters["TimeSlot"] = f"{timeslot_match.group(1)}-{timeslot_match.group(2)}".replace(" ", "")

    for city in ["pune", "mumbai", "bangalore", "kalwa"]:
        if city in query:
            filters["LocationCode"] = city.upper()
            break

    floor_match = re.search(r"(\d+(?:st|nd|rd|th)\s+floor|ground floor)", query)
    if floor_match:
        filters["Floor"] = floor_match.group(1).title()

    for site in ["tech park", "innovation hub", "rnd building", "admin block"]:
        if site in query:
            filters["SiteDetails"] = site.title()
            break

    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        if day in query:
            filters["DayOfWeek"] = day.title()
            break

    for dtype in ["weekday", "weekend"]:
        if dtype in query:
            filters["DayType"] = dtype.title()
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
            elif k == "TimeSlot":
                slot = doc.get("TimeSlot", "").replace(" ", "").replace("–", "-")
                if slot.replace(" ", "") != v.replace(" ", ""):
                    match = False
                    break
            else:
                if str(doc.get(k, "")).lower() != v.lower():
                    match = False
                    break
        if match:
            filtered.append(doc)
    return filtered

@app.post("/query")
def query(req: QueryRequest):
    norm_q = normalize_dates(req.question).lower()
    filtered_docs = filter_logs(docs, norm_q)

    if not filtered_docs:
        results = retriever.get_relevant_documents(norm_q)
        results = [doc.page_content for doc in results]
    else:
        results = [doc_to_entry(d) for d in filtered_docs]

    prompt = f"""You are an expert log analyst. Use the following context to answer the question.

Relevant entries:
{chr(10).join(results)}

Question: {norm_q}
Answer:"""

    model_name = req.model or DEFAULT_OLLAMA_MODEL
    answer = ask_ollama(prompt, model_name)
    critique = ask_ollama(f"Critique the following answer:\n{answer}", model_name)

    return {"answer": answer, "critique": critique, "rewritten_query": norm_q}