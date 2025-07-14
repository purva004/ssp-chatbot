#!/usr/bin/env python3
"""
Simplified CrewAI agent that works around LLM configuration issues
"""

from neo4j import GraphDatabase
import json
import re

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

def analyze_query_and_generate_cypher(user_query: str) -> str:
    """Convert natural language query to Cypher based on common patterns."""
    
    query_lower = user_query.lower()
    
    # Common query patterns
    if "total wifi count" in query_lower or "total wifi" in query_lower:
        return "MATCH (o:Occupancy) RETURN sum(o.WiFiCount) as total_wifi_count"
    
    elif "wifi count" in query_lower and ("first floor" in query_lower or "1st floor" in query_lower):
        return "MATCH (o:Occupancy) WHERE o.Floor = 'First Floor' RETURN sum(o.WiFiCount) as total_wifi_count"
    
    elif "wifi count" in query_lower and ("second floor" in query_lower or "2nd floor" in query_lower):
        return "MATCH (o:Occupancy) WHERE o.Floor = 'Second Floor' RETURN sum(o.WiFiCount) as total_wifi_count"
    
    elif "kalwa" in query_lower and "wifi" in query_lower:
        return "MATCH (o:Occupancy) WHERE o.LocationCode = 'LOC-IN-KALWA' RETURN sum(o.WiFiCount) as total_wifi_count"
    
    elif "occupancy data" in query_lower and "kalwa" in query_lower:
        return "MATCH (o:Occupancy) WHERE o.LocationCode = 'LOC-IN-KALWA' RETURN o.Floor, o.RecordDate, o.WiFiCount, o.TimeSlot LIMIT 10"
    
    elif "show" in query_lower and "data" in query_lower:
        return "MATCH (o:Occupancy) RETURN o.Floor, o.RecordDate, o.WiFiCount, o.TimeSlot LIMIT 10"
    
    elif "floors" in query_lower or "floor" in query_lower:
        return "MATCH (o:Occupancy) RETURN DISTINCT o.Floor"
    
    elif "locations" in query_lower or "location" in query_lower:
        return "MATCH (o:Occupancy) RETURN DISTINCT o.LocationCode, o.SiteDetails"
    
    elif "dates" in query_lower or "date" in query_lower:
        return "MATCH (o:Occupancy) RETURN DISTINCT o.RecordDate ORDER BY o.RecordDate LIMIT 10"
    
    else:
        # Default query - show some sample data
        return "MATCH (o:Occupancy) RETURN o.Floor, o.RecordDate, o.WiFiCount, o.TimeSlot LIMIT 5"

def format_response(cypher_query: str, query_result: str, user_query: str) -> str:
    """Format the response in a user-friendly way."""
    
    try:
        # Try to parse the result if it looks like a dictionary
        if query_result.startswith("{'") and query_result.endswith("'}"):
            # Parse the result
            result_dict = eval(query_result)
            
            if 'total_wifi_count' in result_dict:
                count = result_dict['total_wifi_count']
                return f"The total WiFi count across all locations and time periods is {count:,}."
            
        # Handle multiple records
        elif "\n" in query_result and "{" in query_result:
            lines = query_result.strip().split('\n')
            if len(lines) <= 10:  # Small result set
                formatted_lines = []
                for line in lines:
                    if line.strip():
                        try:
                            data = eval(line)
                            if isinstance(data, dict):
                                formatted_lines.append(str(data))
                        except:
                            formatted_lines.append(line)
                
                return f"Here are the results:\n" + "\n".join(formatted_lines)
            else:
                return f"Found {len(lines)} records. Here are the first few:\n" + "\n".join(lines[:5])
        
        # Default formatting
        return f"Query result: {query_result}"
        
    except Exception as e:
        return f"Result: {query_result}"

def run_crewai_query(user_query: str) -> str:
    """Process user query without the problematic CrewAI LLM integration."""
    
    print(f"[Simple CrewAI Runner] Received query: {user_query}")
    
    try:
        # Step 1: Convert natural language to Cypher
        cypher_query = analyze_query_and_generate_cypher(user_query)
        print(f"[Simple CrewAI Runner] Generated Cypher: {cypher_query}")
        
        # Step 2: Execute the query
        query_result = neo4j_query_tool(cypher_query)
        print(f"[Simple CrewAI Runner] Query result: {query_result}")
        
        # Step 3: Format the response
        formatted_response = format_response(cypher_query, query_result, user_query)
        print(f"[Simple CrewAI Runner] Formatted response: {formatted_response}")
        
        return formatted_response
        
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(f"[Simple CrewAI Runner] Exception: {error_msg}")
        return error_msg

if __name__ == "__main__":
    # Test the simplified version
    test_queries = [
        "What is the total WiFi count?",
        "Show me occupancy data for Kalwa location",
        "What floors are available?",
        "What is the WiFi count on the First Floor?"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing: {query} ---")
        result = run_crewai_query(query)
        print(f"Result: {result}")
