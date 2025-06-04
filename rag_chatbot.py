import os
import json
import faiss
import numpy as np
import subprocess
import dateparser
import re
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

def build_index(text_data, model, original_data):
    vectors = model.encode(text_data, normalize_embeddings=True)
    index = faiss.IndexFlatIP(len(vectors[0]))
    index.add(np.array(vectors))
    faiss.write_index(index, INDEX_PATH)
    # Save original JSON objects for filtering
    with open(DOC_STORE_PATH, "w") as f:
        json.dump(original_data, f)

def search(query, model, index, docs, top_k=None):
    qv = model.encode([query], normalize_embeddings=True)[0]
    if top_k is None or top_k > len(docs):
        top_k = len(docs)
    D, I = index.search(np.array([qv]), top_k)
    # Remove duplicates and keep only valid indices
    unique_indices = []
    seen = set()
    for i in I[0]:
        if i not in seen and i < len(docs):
            unique_indices.append(i)
            seen.add(i)
    return [docs[i] for i in unique_indices]

def filter_logs(docs, query):
    # Lowercase for case-insensitive matching
    query = query.lower()
    filters = {}

    # Extract date (YYYY-MM-DD)
    date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", query)
    if date_match:
        filters["RecordDate"] = date_match.group(1)

    # Extract time (HH:MM or HH:MM:SS)
    time_match = re.search(r"\b(\d{1,2}:\d{2}(?::\d{2})?)\b", query)
    if time_match:
        filters["Time"] = time_match.group(1)

    # Extract TimeSlot (HH:MM - HH:MM)
    timeslot_match = re.search(r"\b(\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2})\b", query)
    if timeslot_match:
        filters["TimeSlot"] = timeslot_match.group(1).replace(" ", "")

    # Extract location (city name, e.g., pune, mumbai, bangalore, kalwa)
    for city in ["pune", "mumbai", "bangalore", "kalwa"]:
        if city in query:
            filters["LocationCode"] = city.upper()
            break

    # Extract floor (e.g., "2nd Floor", "Ground Floor", etc.)
    floor_match = re.search(r"(\d+(?:st|nd|rd|th)\s+floor|ground floor)", query)
    if floor_match:
        filters["Floor"] = floor_match.group(1).title()

    # Extract SiteDetails (e.g., "Tech Park", "Innovation Hub", etc.)
    for site in ["tech park", "innovation hub", "rnd building", "admin block"]:
        if site in query:
            filters["SiteDetails"] = site.title()
            break

    # Now filter docs
    filtered = []
    for doc in docs:
        match = True
        for k, v in filters.items():
            if k == "LocationCode":
                # Remove LOC-IN- and compare
                loc = doc.get("LocationCode", "").replace("LOC-IN-", "").upper()
                if loc != v:
                    match = False
                    break
            elif k == "TimeSlot":
                # Remove spaces for comparison
                slot = doc.get("TimeSlot", "").replace(" ", "")
                if slot != v:
                    match = False
                    break
            else:
                if str(doc.get(k, "")).lower() != v.lower():
                    match = False
                    break
        if match:
            filtered.append(doc)
    return filtered

# Init
def init_system():
    if not os.path.exists(INDEX_PATH):
        raw_data = load_json_data()
        entries = json_to_text_entries(raw_data)
        model = SentenceTransformer(EMBEDDING_MODEL)
        build_index(entries, model, raw_data)  # Pass raw_data here

    index = faiss.read_index(INDEX_PATH)
    with open(DOC_STORE_PATH, "r") as f:
        docs = json.load(f)
    model = SentenceTransformer(EMBEDDING_MODEL)
    return index, docs, model

index, docs, embed_model = init_system()

def doc_to_entry(d):
    # Remove LOC-IN- from LocationCode
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

@app.post("/query")
def query(req: QueryRequest):
    norm_q = normalize_dates(req.question).lower()
    filtered_docs = filter_logs(docs, norm_q)

    # If no filter matches, fallback to top 10 semantic search
    if not filtered_docs:
        results = search(norm_q, embed_model, index, docs, top_k=10)
    else:
        results = [doc_to_entry(d) for d in filtered_docs]

    prompt = f"""You are an expert log analyst. Use the following context to answer the question.

Relevant entries:
{chr(10).join(results)}

Question: {norm_q}
Answer:"""

    answer = ask_ollama(prompt)
    critique = ask_ollama(f"Critique the following answer:\n{answer}")

    return {"answer": answer, "critique": critique, "rewritten_query": norm_q}
