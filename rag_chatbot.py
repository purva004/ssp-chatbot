import os
import json
import faiss
import numpy as np
import subprocess
import dateparser
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# -------- CONFIG --------
DATA_PATH = "data.json"
INDEX_PATH = "vector.index"
DOC_STORE_PATH = "data_store.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3:8b"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    question: str

# Simple conversation memory
conversation_memory = []

def normalize_dates(text):
    parsed = dateparser.parse(text)
    return parsed.strftime("%Y-%m-%d") if parsed else text

def ask_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    result = subprocess.run(["ollama", "run", model], input=prompt.encode(), stdout=subprocess.PIPE)
    return result.stdout.decode().strip()

def load_json_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def json_to_text_entries(data):
    result = []
    for d in data:
        date = d.get("RecordDate", "unknown date")
        time = d.get("Time", "")
        hour = int(datetime.strptime(time, "%H:%M:%S").hour) if time else None
        part = (
            "morning" if 5 <= hour < 12 else
            "afternoon" if 12 <= hour < 17 else
            "evening" if 17 <= hour < 21 else
            "night"
        ) if hour is not None else ""

        entry = f"""On {d.get("DayOfWeek", "")}, {date} at {d.get("SiteDetails", "")} ({d.get("Floor", "")}, {d.get("LocationCode", "").replace("LOC-IN-", "")}), 
        WiFi count: {d.get("WiFiCount", "N/A")}, Access count: {d.get("AccessControlCount", "N/A")}, Type: {d.get("DayType", "")}, TimeSlot: {d.get("TimeSlot", "")}. Part of day: {part}."""
        result.append(entry)
    return result

def build_index(text_data, model):
    vectors = model.encode(text_data, normalize_embeddings=True)
    index = faiss.IndexFlatIP(len(vectors[0]))
    index.add(np.array(vectors))
    faiss.write_index(index, INDEX_PATH)
    with open(DOC_STORE_PATH, "w") as f:
        json.dump(text_data, f)

def search(query, model, index, docs, top_k=3):
    qv = model.encode([query], normalize_embeddings=True)[0]
    D, I = index.search(np.array([qv]), top_k)
    return [docs[i] for i in I[0]]

# Init
def init_system():
    if not os.path.exists(INDEX_PATH):
        raw_data = load_json_data()
        entries = json_to_text_entries(raw_data)
        model = SentenceTransformer(EMBEDDING_MODEL)
        build_index(entries, model)

    index = faiss.read_index(INDEX_PATH)
    with open(DOC_STORE_PATH, "r") as f:
        docs = json.load(f)
    model = SentenceTransformer(EMBEDDING_MODEL)
    return index, docs, model

index, docs, embed_model = init_system()

@app.post("/query")
def query(req: QueryRequest):
    norm_q = normalize_dates(req.question).lower()

    # (3) Rewrite the query
    rewrite_prompt = f'Rewrite this for better clarity: "{norm_q}"'
    rewritten = ask_ollama(rewrite_prompt)

    # (2) Embed & search
    results = search(rewritten, embed_model, index, docs)

    # (1) Prompt engineering with memory
    memory = "\n".join([f"Q: {m['q']}\nA: {m['a']}" for m in conversation_memory[-5:]])
    prompt = f"""You are an expert log analyst. Use the following context to answer the question.

Previous Q&A:
{memory}

Relevant entries:
{chr(10).join(results)}

Question: {rewritten}
Answer:"""

    answer = ask_ollama(prompt)

    # (4) Store in memory
    conversation_memory.append({"q": req.question, "a": answer})
    if len(conversation_memory) > 5:
        conversation_memory.pop(0)

    # (5) Self-evaluation
    critique = ask_ollama(f"Critique the following answer:\n{answer}")

    return {"answer": answer, "critique": critique, "rewritten_query": rewritten}
