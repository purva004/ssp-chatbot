@echo off
echo =========================================
echo Starting Unified Chatbot System
echo =========================================
echo Frontend: Next.js on port 3000
echo Backend Services:
echo   - Graph Chatbot on port 8001
echo   - CrewAI Multi-Agent on port 8002
echo   - RAG Chatbot on port 8003
echo =========================================

rem Start each service in a new window
start "Graph Chatbot" cmd /k "start-graph.bat"
timeout /t 2 /nobreak > nul

start "CrewAI Multi-Agent" cmd /k "start-crewai.bat"
timeout /t 2 /nobreak > nul

start "RAG Chatbot" cmd /k "start-rag.bat"
timeout /t 2 /nobreak > nul

echo All backend services started!
echo Now starting Next.js frontend...
timeout /t 5 /nobreak > nul

rem Start Next.js frontend
npm run dev
