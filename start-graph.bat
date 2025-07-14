@echo off
echo Starting Graph Chatbot on port 8001...
cd /d "%~dp0"
python -m uvicorn graphchatbot:app --host 0.0.0.0 --port 8001 --reload
