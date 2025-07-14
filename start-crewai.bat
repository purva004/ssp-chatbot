@echo off
echo Starting CrewAI Multi-Agent on port 8002...
cd /d "%~dp0\crewAI"
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
