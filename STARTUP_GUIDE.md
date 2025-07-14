# Unified Chatbot System - Startup Guide

## System Overview
Your unified chatbot system now integrates all three AI services:
- **Graph Chatbot**: Neo4j-based chatbot on port 8001
- **CrewAI Multi-Agent**: Multi-agent system on port 8002
- **RAG Chatbot**: FAISS-based chatbot on port 8003
- **Next.js Frontend**: Unified interface on port 3000

## Manual Startup Instructions

### Step 1: Start Backend Services

Open **3 separate PowerShell/Command Prompt windows** and run:

**Window 1 - Graph Chatbot (Port 8001):**
```bash
python -m uvicorn graphchatbot:app --host 0.0.0.0 --port 8001 --reload
```

**Window 2 - CrewAI Multi-Agent (Port 8002):**
```bash
cd crewAI
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Window 3 - RAG Chatbot (Port 8003):**
```bash
python -m uvicorn rag_chatbot:app --host 0.0.0.0 --port 8003 --reload
```

### Step 2: Start Frontend

Open **4th PowerShell/Command Prompt window** and run:
```bash
npm run dev
```

### Step 3: Access the Application

Open your browser and go to:
- **http://localhost:3000** (or whatever port Next.js shows)

## Using the System

1. **Select AI Service**: Use the dropdown in the top-right to choose between:
   - RAG Chatbot
   - Graph Chatbot  
   - CrewAI Multi-Agent

2. **Select Model**: Choose your Ollama model (not needed for CrewAI)

3. **Start Chatting**: Type your questions and get responses from the selected AI service

## Troubleshooting

- **Port conflicts**: If any port is in use, kill the process or change the port
- **Service not responding**: Check if the backend service is running and accessible
- **Health checks**: The system automatically checks if services are healthy

## Current Status
✅ All backend services are running:
- Graph Chatbot on port 8001
- CrewAI Multi-Agent on port 8002
- RAG Chatbot on port 8003

Now you need to start the Next.js frontend to access the unified interface!
