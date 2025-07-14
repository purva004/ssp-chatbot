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

# Neo4j Query Function (not a CrewAI tool)
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
        "You are a Cypher query generator. Convert natural language to Cypher queries ONLY.\n"
        "DATABASE SCHEMA: Occupancy nodes with properties: Floor, SiteDetails, RecordDate, LocationCode, WiFiCount, TimeSlot\n"
        "IMPORTANT: Return ONLY the Cypher query, no explanations or conversation.\n\n"
        "EXAMPLES:\n"
        "Q: What is the WiFi count on the First Floor of Kalwa location on date 6/14/2025?\n"
        "A: MATCH (o:Occupancy) WHERE o.Floor = 'First Floor' AND o.LocationCode = 'LOC-IN-KALWA' AND o.RecordDate = '2025-06-14' RETURN sum(o.WiFiCount) as total_wifi_count\n"
        "Q: Show me occupancy data for Kalwa location\n"
        "A: MATCH (o:Occupancy) WHERE o.LocationCode = 'LOC-IN-KALWA' RETURN o.Floor, o.RecordDate, o.WiFiCount, o.TimeSlot LIMIT 10\n"
        "Q: What is the wifi count of 1st floor of kalwa location of RnD building for the 14th june 2025\n"
        "A: MATCH (o:Occupancy) WHERE o.Floor = 'First Floor' AND o.LocationCode = 'LOC-IN-KALWA' AND o.SiteDetails CONTAINS 'RnD' AND o.RecordDate = '2025-06-14' RETURN sum(o.WiFiCount) as total_wifi_count\n\n"
        f"Q: {nl_query}\n"
        "A: "
    )
    cypher = call_llm(prompt)
    
    # Extract only the Cypher query part
    lines = cypher.split('\n')
    for line in lines:
        line = line.strip()
        if line.upper().startswith('MATCH') or line.upper().startswith('RETURN') or line.upper().startswith('CREATE'):
            return line
    
    # If no proper Cypher found, return the first non-empty line
    for line in lines:
        line = line.strip()
        if line and not line.lower().startswith(('i can', 'let me', 'sure', 'of course')):
            return line
    
    return cypher.strip()

# Step 2 & 3: Run Cypher, then LLM explains result
def run_crewai_query(user_query: str) -> str:
    print(f"[CrewAI Runner] Received query: {user_query}")
    
    # If user enters Cypher directly, skip LLM
    if user_query.strip().lower().startswith("match"):
        cypher_query = user_query
    else:
        cypher_query = nl_to_cypher(user_query)
    
    print(f"[CrewAI Runner] Cypher: {cypher_query}")
    
    # Validate that we have a proper Cypher query
    if not cypher_query or not any(keyword in cypher_query.upper() for keyword in ['MATCH', 'RETURN', 'CREATE']):
        print("[CrewAI Runner] Invalid Cypher query generated, using fallback")
        # Fallback to a simple pattern-based query generation
        cypher_query = generate_fallback_cypher(user_query)
        print(f"[CrewAI Runner] Fallback Cypher: {cypher_query}")
    
    try:
        result = neo4j_query_tool(cypher_query)
        print(f"[CrewAI Runner] Neo4j result: {result}")
    except Exception as e:
        print(f"[CrewAI Runner] Neo4j query failed: {e}")
        return f"Sorry, I couldn't execute the database query. Error: {str(e)}"

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

# Fallback Cypher generation using pattern matching
def generate_fallback_cypher(query: str) -> str:
    query_lower = query.lower()
    
    # Basic patterns for common queries
    if 'wifi count' in query_lower:
        conditions = []
        
        # Extract floor
        if '1st floor' in query_lower or 'first floor' in query_lower:
            conditions.append("o.Floor = 'First Floor'")
        elif '2nd floor' in query_lower or 'second floor' in query_lower:
            conditions.append("o.Floor = 'Second Floor'")
        
        # Extract location
        if 'kalwa' in query_lower:
            conditions.append("o.LocationCode = 'LOC-IN-KALWA'")
        elif 'mumbai' in query_lower:
            conditions.append("o.LocationCode = 'LOC-IN-MUMBAI'")
        elif 'pune' in query_lower:
            conditions.append("o.LocationCode = 'LOC-IN-PUNE'")
        
        # Extract site details
        if 'rnd' in query_lower or 'r&d' in query_lower:
            conditions.append("o.SiteDetails CONTAINS 'RnD'")
        elif 'innovation' in query_lower:
            conditions.append("o.SiteDetails CONTAINS 'Innovation'")
        
        # Extract date
        if '14th june 2025' in query_lower or '2025-06-14' in query_lower:
            conditions.append("o.RecordDate = '2025-06-14'")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        return f"MATCH (o:Occupancy) WHERE {where_clause} RETURN sum(o.WiFiCount) as total_wifi_count"
    
    # Default fallback
    return "MATCH (o:Occupancy) RETURN o.Floor, o.LocationCode, o.WiFiCount, o.RecordDate LIMIT 5"
