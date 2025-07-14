#!/usr/bin/env python3

import sys
sys.path.append('.')

from crewai_agent import neo4j_query_tool

def test_neo4j_connection():
    """Test the Neo4j connection and query execution"""
    
    print("=== Testing Neo4j Connection ===")
    
    # Test a simple query first
    simple_query = "MATCH (o:Occupancy) RETURN count(o) as total_count LIMIT 1"
    print(f"Testing simple query: {simple_query}")
    
    try:
        result = neo4j_query_tool(simple_query)
        print(f"Result: {result}")
        print("✅ Neo4j connection successful!")
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        return
    
    print("\n=== Testing Specific Query ===")
    # Test the specific query from the user
    specific_query = "MATCH (o:Occupancy) WHERE o.Floor = 'First Floor' AND o.LocationCode = 'LOC-IN-KALWA' AND o.RecordDate = '2025-06-14' RETURN sum(o.WiFiCount) as total_wifi_count"
    print(f"Testing specific query: {specific_query}")
    
    try:
        result = neo4j_query_tool(specific_query)
        print(f"Result: {result}")
        print("✅ Specific query successful!")
    except Exception as e:
        print(f"❌ Specific query failed: {e}")

if __name__ == "__main__":
    test_neo4j_connection()
