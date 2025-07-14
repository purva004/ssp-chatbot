#!/usr/bin/env python3

import sys
sys.path.append('.')

from crewai_agent import run_crewai_query

def test_full_query():
    """Test the full query process"""
    
    print("=== Testing Full CrewAI Query Process ===")
    
    # Test the exact query that was failing
    test_query = "What is the WiFi count on the First Floor of Kalwa location on date 6/14/2025?"
    print(f"Testing query: {test_query}")
    
    try:
        result = run_crewai_query(test_query)
        print(f"✅ Query successful!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Query failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_query()
