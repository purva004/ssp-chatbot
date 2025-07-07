from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from neo4j import GraphDatabase
import os
import requests
import ast

# Set environment variables for CrewAI
os.environ["OPENAI_API_KEY"] = "not-needed"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# LLM setup (Ollama)
def call_llm(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3:8b", "prompt": prompt, "stream": False}
    )
    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        print("LLM Error:", response.text)
        return "Sorry, I couldn't process your request."

# Neo4j Tool
@tool
def neo4j_query_tool(query: str) -> str:
    """Execute Cypher queries against Neo4j database to retrieve occupancy data."""
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "purva@1234"
    driver = GraphDatabase.driver(uri, auth=(username, password))
    result_string = ""
    try:
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            if records:
                for record in records:
                    result_string += str(record.data()) + "\n"
            else:
                result_string = "No results found for this query."
    except Exception as e:
        result_string = f"Neo4j Error: {str(e)}"
    finally:
        driver.close()
    return result_string.strip()

# Step 1: LLM generates Cypher
def nl_to_cypher(nl_query: str) -> str:
    prompt = (
        "You are an expert in translating natural language to Cypher for a Neo4j occupancy database.\n"
        "DATABASE SCHEMA:\n"
        "- Floor, SiteDetails, RecordDate, LocationCode, WiFiCount, TimeSlot\n"
        "EXAMPLES:\n"
        "Q: What is the WiFi count on the First Floor of Kalwa location on date 6/14/2025?\n"
        "A: MATCH (o:Occupancy) WHERE o.Floor = 'First Floor' AND o.LocationCode = 'LOC-IN-KALWA' AND o.RecordDate = '2025-06-14' RETURN sum(o.WiFiCount) as total_wifi_count\n"
        "Q: Show me occupancy data for Kalwa location\n"
        "A: MATCH (o:Occupancy) WHERE o.LocationCode = 'LOC-IN-KALWA' RETURN o.Floor, o.RecordDate, o.WiFiCount, o.TimeSlot LIMIT 10\n"
        f"Q: {nl_query}\nA:"
    )
    cypher = call_llm(prompt)
    cypher_line = cypher.split("\n")[0]
    return cypher_line.strip()

# Step 2 & 3: Run Cypher, then LLM explains result
def run_crewai_query(user_query: str) -> str:
    print(f"[CrewAI Runner] Received query: {user_query}")
    # If user enters Cypher directly, skip LLM
    if user_query.strip().lower().startswith("match"):
        cypher_query = user_query
    else:
        cypher_query = nl_to_cypher(user_query)
    print(f"[CrewAI Runner] Cypher: {cypher_query}")
    result = neo4j_query_tool(cypher_query)
    print(f"[CrewAI Runner] Neo4j result: {result}")

    # Try to parse result for LLM
    try:
        result_dict = ast.literal_eval(result)
        result_str = ', '.join(f"{k}: {v}" for k, v in result_dict.items())
    except Exception:
        result_str = result

    # LLM explains result
    prompt = (
        f"User question: {user_query}\n"
        f"Cypher query: {cypher_query}\n"
        f"Database result: {result_str}\n"
        "Based on the user's question and the database result, provide a clear, concise answer in plain English. Do not show code or JSON."
    )
    answer = call_llm(prompt)
    print(f"[CrewAI Runner] LLM answer: {answer}")
    return answer