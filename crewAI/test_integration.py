#!/usr/bin/env python3
"""
Test script to verify CrewAI integration is working properly
"""

import sys
import os

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    
    try:
        from crewai import Agent, Task, Crew, Process
        print("✅ CrewAI core imports successful")
    except ImportError as e:
        print(f"❌ CrewAI core import failed: {e}")
        return False
    
    try:
        from crewai.tools import tool
        print("✅ CrewAI tools import successful")
    except ImportError as e:
        print(f"❌ CrewAI tools import failed: {e}")
        return False
    
    try:
        from langchain_ollama import OllamaLLM
        print("✅ LangChain Ollama import successful")
    except ImportError:
        try:
            from langchain_community.llms import Ollama
            print("✅ LangChain Community Ollama import successful (fallback)")
        except ImportError as e:
            print(f"❌ Ollama import failed: {e}")
            return False
    
    try:
        from neo4j import GraphDatabase
        print("✅ Neo4j import successful")
    except ImportError as e:
        print(f"❌ Neo4j import failed: {e}")
        return False
    
    try:
        from crewai_agent import run_crewai_query
        print("✅ CrewAI agent import successful")
    except ImportError as e:
        print(f"❌ CrewAI agent import failed: {e}")
        return False
    
    try:
        import main
        print("✅ Main FastAPI app import successful")
    except ImportError as e:
        print(f"❌ Main FastAPI app import failed: {e}")
        return False
    
    return True

def test_ollama_connection():
    """Test Ollama connection"""
    print("\n🔌 Testing Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
        else:
            print(f"❌ Ollama responded with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("   Make sure Ollama is running: 'ollama serve'")
        return False

def test_neo4j_connection():
    """Test Neo4j connection"""
    print("\n🗃️ Testing Neo4j connection...")
    
    try:
        from neo4j import GraphDatabase
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "purva@1234"
        
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            if record and record["test"] == 1:
                print("✅ Neo4j is running and accessible")
                driver.close()
                return True
        driver.close()
        return False
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        print("   Make sure Neo4j is running on bolt://localhost:7687")
        print("   Username: neo4j, Password: purva@1234")
        return False

def test_crewai_agent():
    """Test CrewAI agent initialization"""
    print("\n🤖 Testing CrewAI agent initialization...")
    
    try:
        from crewai_agent import occupancy_analyst, occupancy_task, occupancy_crew
        print("✅ CrewAI agent, task, and crew initialized successfully")
        print(f"   Agent role: {occupancy_analyst.role}")
        print(f"   Task description length: {len(occupancy_task.description)} characters")
        print(f"   Crew has {len(occupancy_crew.agents)} agent(s)")
        return True
    except Exception as e:
        print(f"❌ CrewAI agent initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 CrewAI Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_ollama_connection,
        test_neo4j_connection,
        test_crewai_agent
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your CrewAI integration is ready!")
        print("\n🚀 You can now start the application:")
        print("   python start_chatbot.py")
        print("   OR manually:")
        print("   uvicorn main:app --reload --port 8000")
    else:
        print("❌ Some tests failed. Please fix the issues before proceeding.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
