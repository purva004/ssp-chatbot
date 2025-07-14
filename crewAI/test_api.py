#!/usr/bin/env python3

import requests
import json

def test_api():
    """Test the API endpoint"""
    
    url = "http://localhost:8000/crewquery"
    payload = {
        "query": "What is the WiFi count on the First Floor of Kalwa location on date 6/14/2025?"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
        print("Start the server with: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
