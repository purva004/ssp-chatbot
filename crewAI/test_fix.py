#!/usr/bin/env python3

import sys
sys.path.append('.')

from crewai_agent import run_crewai_query, generate_fallback_cypher

def test_query_generation():
    """Test the query generation functions"""
    
    # Test the fallback function
    print("=== Testing Fallback Cypher Generation ===")
    test_query = "what is the wifi count of 1st floor of kalwa location of RnD building for the 14th june 2025"
    fallback_cypher = generate_fallback_cypher(test_query)
    print(f"Input: {test_query}")
    print(f"Fallback Cypher: {fallback_cypher}")
    print()
    
    # Test a few more queries
    test_queries = [
        "show me wifi count for second floor mumbai",
        "what is the occupancy data for pune innovation center",
        "total wifi count for kalwa location"
    ]
    
    for query in test_queries:
        cypher = generate_fallback_cypher(query)
        print(f"Query: {query}")
        print(f"Cypher: {cypher}")
        print()

if __name__ == "__main__":
    test_query_generation()
