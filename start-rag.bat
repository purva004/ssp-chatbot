@echo off
echo Starting RAG Chatbot on port 8003...
cd /d "%~dp0"
python -m uvicorn rag_chatbot:app --host 0.0.0.0 --port 8003 --reload
