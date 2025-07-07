#!/usr/bin/env python3
"""
Startup script for CrewAI Occupancy Chatbot
This script helps you start all components of the chatbot system
"""

import subprocess
import sys
import time
import threading
import os

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_neo4j():
    """Check if Neo4j is running"""
    try:
        from neo4j import GraphDatabase
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "purva@1234"
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            session.run("RETURN 1")
        driver.close()
        return True
    except:
        return False

def start_fastapi():
    """Start FastAPI backend"""
    print("Starting FastAPI backend...")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def start_streamlit():
    """Start Streamlit frontend"""
    print("Starting Streamlit frontend...")
    time.sleep(2)  # Wait for FastAPI to start
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py", "--server.port", "8501"])

def main():
    print("🚀 CrewAI Occupancy Chatbot Startup")
    print("=" * 50)
    
    # Check dependencies
    print("Checking dependencies...")
    
    if not check_ollama():
        print("❌ Ollama is not running. Please start Ollama first:")
        print("   - Windows: Start Ollama from Start Menu or run 'ollama serve'")
        print("   - Make sure you have the llama3:8b model: 'ollama pull llama3:8b'")
        sys.exit(1)
    else:
        print("✅ Ollama is running")
    
    if not check_neo4j():
        print("❌ Neo4j is not running or not accessible.")
        print("   - Make sure Neo4j is running on bolt://localhost:7687")
        print("   - Username: neo4j, Password: purva@1234")
        sys.exit(1)
    else:
        print("✅ Neo4j is running")
    
    print("\n🎯 Starting application components...")
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Give FastAPI time to start
    time.sleep(3)
    
    print("✅ FastAPI backend started on http://localhost:8000")
    print("🌐 Starting Streamlit frontend...")
    print("📱 Streamlit will be available at http://localhost:8501")
    print("\n" + "=" * 50)
    print("🎉 CrewAI Occupancy Chatbot is ready!")
    print("=" * 50)
    
    # Start Streamlit (this will block)
    start_streamlit()

if __name__ == "__main__":
    main()
