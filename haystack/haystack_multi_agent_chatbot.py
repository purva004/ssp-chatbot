import csv
import threading
from typing import List, Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from neo4j import GraphDatabase
from haystack.pipelines import Pipeline
from haystack.nodes.base import BaseComponent
from haystack.schema import Document
import requests
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "purva@1234"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

CSV_PATH = "occupancy.csv"  # Your actual path

# -----------------------------
# UTILITIES
# -----------------------------
class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_csv_to_graph(self, records: List[Dict[str, str]]):
        def insert(tx, row):
            tx.run(
                """
                MERGE (l:Location {code: $LocationCode})
                MERGE (l)-[:HAS_SITE]->(s:Site {details: $SiteDetails})
                CREATE (r:Record {
                    date: $RecordDate,
                    timeslot: $TimeSlot,
                    floor: $Floor,
                    wifi: toInteger($WiFiCount)
                })
                CREATE (s)-[:HAS_RECORD]->(r)
                """,
                **row
            )

        with self.driver.session() as session:
            for row in records:
                session.write_transaction(insert, row)

# -----------------------------
# CSV LOADING
# -----------------------------
def parse_csv(path: str) -> List[Dict[str, str]]:
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# -----------------------------
# MULTI-AGENT: Custom Retriever + Generator
# -----------------------------
class OllamaGenerator(BaseComponent):
    outgoing_edges = 1

    def __init__(self, model=OLLAMA_MODEL):
        self.model = model

    def run(self, query, documents=None, **kwargs):
        context = "\n".join([doc.content for doc in documents]) if documents else ""
        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": self.model, "prompt": prompt, "stream": False}
            )
            result = response.json()
            return {"answers": [{"answer": result.get("response", "No answer found.")}]}, "output_1"
        except Exception as e:
            return {"answers": [{"answer": f"Ollama error: {e}"}]}, "output_1"

class Neo4jRetriever(BaseComponent):
    outgoing_edges = 1

    def __init__(self, client: Neo4jClient):
        self.client = client

    def run(self, query: str, **kwargs):
        with self.client.driver.session() as session:
            result = session.run(
                """
                MATCH (l:Location)-[:HAS_SITE]->(s:Site)-[:HAS_RECORD]->(r:Record)
                WHERE toLower(r.floor) CONTAINS toLower($q)
                   OR toLower(s.details) CONTAINS toLower($q)
                   OR toLower(l.code) CONTAINS toLower($q)
                RETURN r.date AS date, r.timeslot AS timeslot, r.floor AS floor, r.wifi AS wifi, s.details AS site
                LIMIT 5
                """,
                q=query
            )
            docs = []
            for record in result:
                content = f"Date: {record['date']}, TimeSlot: {record['timeslot']}, Floor: {record['floor']}, WiFi: {record['wifi']}, Site: {record['site']}"
                docs.append(Document(content=content))
            return {"documents": docs}, "output_1"

    def run_batch(self, queries, **kwargs):
        results = []
        for query in queries:
            docs, _ = self.run(query)
            results.append(docs)
        return results

# -----------------------------
# FASTAPI
# -----------------------------
class QueryModel(BaseModel):
    query: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

app = FastAPI()

# -----------------------------
# COMPONENT INITIALIZATION
# -----------------------------
neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
retriever = Neo4jRetriever(neo4j_client)
generator = OllamaGenerator()
pipeline = Pipeline()
pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
pipeline.add_node(component=generator, name="Generator", inputs=["Retriever"])

# -----------------------------
# ENDPOINTS
# -----------------------------
@app.post("/chat")
def chat(q: QueryModel):
    result = pipeline.run(query=q.query)
    return {"answer": result["answers"][0]["answer"]}

@app.post("/load-csv")
def load_csv():
    records = parse_csv(CSV_PATH)
    thread = threading.Thread(target=neo4j_client.load_csv_to_graph, args=(records,))
    thread.start()
    return {"status": "Data loading in background."}

@app.on_event("shutdown")
def shutdown():
    neo4j_client.close()
