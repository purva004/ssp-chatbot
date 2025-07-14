import requests
from tool import neo4j_query_tool

def process_query(user_query: str) -> str:
    """Process user query using Ollama for NL to Cypher conversion and Neo4j for data retrieval."""
    
    # Create a prompt for Ollama to convert natural language to Cypher
    cypher_prompt = f"""
You are an expert in converting natural language queries to Cypher queries for a Neo4j database.

DATABASE SCHEMA:
The database contains Occupancy nodes with these properties:
- Floor: The floor name (e.g., "First Floor", "Second Floor")
- SiteDetails: Location details (e.g., "Kalwa_Switchboard_ShopFloor")
- RecordDate: Date in format 'YYYY-MM-DD'
- LocationCode: Location code (e.g., "LOC-IN-KALWA")
- WiFiCount: Number of WiFi connections (integer)
- TimeSlot: Time range (e.g., "01:45 - 02:00")

EXAMPLES:
Question: "What is the WiFi count on the First Floor of Kalwa location on date 6/14/2025?"
Cypher: MATCH (o:Occupancy) WHERE o.Floor = 'First Floor' AND o.LocationCode = 'LOC-IN-KALWA' AND o.RecordDate = '2025-06-14' RETURN sum(o.WiFiCount) as total_wifi_count

Question: "Show me occupancy data for Kalwa location"
Cypher: MATCH (o:Occupancy) WHERE o.LocationCode = 'LOC-IN-KALWA' RETURN o.Floor, o.RecordDate, o.WiFiCount, o.TimeSlot LIMIT 10

Convert this question to a Cypher query:
Question: {user_query}
Cypher:"""

    try:
        # Get Cypher query from Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": cypher_prompt,
                "stream": False
            }
        )
        
        if response.status_code != 200:
            return f"Error getting Cypher query: {response.status_code}"
        
        cypher_query = response.json().get("response", "").strip()
        
        # Clean up the Cypher query (remove any extra text)
        if "MATCH" in cypher_query:
            cypher_query = cypher_query[cypher_query.find("MATCH"):]
            # Take only the first line if there are multiple lines
            cypher_query = cypher_query.split('\n')[0]
        
        print(f"Generated Cypher: {cypher_query}")
        
        # Execute the Cypher query using our Neo4j tool
        result = neo4j_query_tool._run(cypher_query)
        
        # Format the response
        if "Error" in result:
            return f"Database query failed: {result}"
        
        # Create a natural language response
        response_prompt = f"""
Based on this database query result, provide a clear, natural language answer to the user's question.

User Question: {user_query}
Database Result: {result}

Provide a concise, helpful answer:"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": response_prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            natural_response = response.json().get("response", "").strip()
            return natural_response
        else:
            return f"Raw data: {result}"
            
    except Exception as e:
        return f"Error processing query: {str(e)}"

def run_simple_query(query: str) -> str:
    """Simple wrapper for the query processor."""
    return process_query(query)
