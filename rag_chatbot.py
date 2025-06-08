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
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import ssl
from transformers import logging
from huggingface_hub import hf_hub_download

# -------- CONFIG --------
DATA_PATH = "data.json"
INDEX_PATH = "vector.index"
DOC_STORE_PATH = "data_store.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
load_dotenv(".env.local")
DEFAULT_OLLAMA_MODEL = os.getenv("NEXT_PUBLIC_DEFAULT_MODEL", "Gemma3:1b")

# Update to use a local model path
LOCAL_MODEL_PATH = "./all-MiniLM-L6-v2"

# Ensure the model is loaded from the local path
if not os.path.exists(LOCAL_MODEL_PATH):
    raise FileNotFoundError(f"Local model path '{LOCAL_MODEL_PATH}' does not exist. Please download the model manually.")

# Disable SSL verification globally for requests
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

# Disable SSL verification globally for Hugging Face Hub
hf_hub_download._create_default_https_context = ssl._create_unverified_context

# Disable SSL verification for SentenceTransformer
class NoSSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = ssl.create_default_context()
        kwargs["ssl_context"].check_hostname = False
        kwargs["ssl_context"].verify_mode = ssl.CERT_NONE
        return super().init_poolmanager(*args, **kwargs)

requests_session = requests.Session()
requests_session.mount("https://", NoSSLAdapter())
SentenceTransformer._http_client = requests_session

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    question: str
    model: str | None = None  # Optional model field

def normalize_dates(text):
    parsed = dateparser.parse(text)
    return parsed.strftime("%Y-%m-%d") if parsed else text

def ask_ollama(prompt: str, model: str) -> str:
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
    timeslot_match = re.search(r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})", query)
    if timeslot_match:
        filters["TimeSlot"] = f"{timeslot_match.group(1)}-{timeslot_match.group(2)}".replace(" ", "")

    # Extract location (city name)
    for city in ["pune", "mumbai", "bangalore", "kalwa"]:
        if city in query:
            filters["LocationCode"] = city.upper()
            break

    # Extract floor (e.g., "2nd Floor", "Ground Floor", etc.)
    floor_match = re.search(r"(\d+(?:st|nd|rd|th)\s+floor|ground floor)", query)
    if floor_match:
        filters["Floor"] = floor_match.group(1).title()

    # Extract SiteDetails
    for site in ["tech park", "innovation hub", "rnd building", "admin block"]:
        if site in query:
            filters["SiteDetails"] = site.title()
            break

    # Extract DayOfWeek
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        if day in query:
            filters["DayOfWeek"] = day.title()
            break

    # Extract DayType
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

# Init
def init_system():
    if not os.path.exists(INDEX_PATH):
        raw_data = load_json_data()
        entries = json_to_text_entries(raw_data)
        model = SentenceTransformer(LOCAL_MODEL_PATH)  # Update SentenceTransformer initialization to use local model
        build_index(entries, model, raw_data)  # Pass raw_data here

    index = faiss.read_index(INDEX_PATH)
    with open(DOC_STORE_PATH, "r") as f:
        docs = json.load(f)
    model = SentenceTransformer(LOCAL_MODEL_PATH)  # Update SentenceTransformer initialization to use local model
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

    if not filtered_docs:
        results = search(norm_q, embed_model, index, docs, top_k=10)
    else:
        results = [doc_to_entry(d) for d in filtered_docs]

    prompt = f"""You are an expert log analyst. Use the following context to answer the question.

Relevant entries:
{chr(10).join(results)}

Question: {norm_q}
Answer:"""

    # Use model from request, or fallback to default
    model_name = req.model or DEFAULT_OLLAMA_MODEL

    answer = ask_ollama(prompt, model_name)
    critique = ask_ollama(f"Critique the following answer:\n{answer}", model_name)

    return {"answer": answer, "critique": critique, "rewritten_query": norm_q}
