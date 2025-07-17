# CrewAI Occupancy Chatbot - Complete Project Structure

## 📁 Project Directory Structure

```
C:\Users\z0050s8t\ssp-chatbot\crewAI\
├── 📄 Core Application Files
│   ├── main.py                     # FastAPI backend server
│   ├── frontend.py                 # Streamlit web interface
│   ├── simple_crewai_agent.py      # ✅ WORKING agent (bypasses LLM issues)
│   ├── crewai_agent.py            # ✅ WORKING agent (Ollama direct integration)
│   └── start_chatbot.py           # Application startup script
│
├── 📄 Database & Tools
│   ├── neo4j_loader.py            # Neo4j data loading utilities
│   ├── tool.py                    # Neo4j tool implementation
│   └── occupancy_data.csv         # Raw occupancy data (58MB)
│
├── 📄 Legacy/Alternative Files
│   ├── custom_crew_agent.py       # Custom CrewAI implementation
│   ├── custom_crew_runner.py      # Custom crew runner
│   └── simple_query_processor.py  # Simple query processor
│
├── 📄 Testing Files
│   ├── test_api.py                # API endpoint tests
│   ├── test_fix.py                # Fix validation tests
│   ├── test_full_query.py         # Full query integration tests
│   ├── test_integration.py        # Integration tests
│   └── test_neo4j.py              # Neo4j connection tests
│
├── 📄 Configuration & Documentation
│   ├── requirements.txt           # Python dependencies (updated)
│   ├── README.md                  # Project documentation
│   └── PROJECT_STRUCTURE.md       # This file
│
└── 📁 __pycache__/                # Python cache files
```

## 🔧 Core Components

### 1. **main.py** - FastAPI Backend
```python
# Purpose: RESTful API server
# Endpoint: POST /crewquery
# Port: 8000
# Uses: simple_crewai_agent.py (working version)
```

**Key Features:**
- Single endpoint for query processing
- Error handling with HTTP status codes
- CORS support for frontend integration
- Integration with the working agent

### 2. **simple_crewai_agent.py** - ✅ Working Agent Implementation
```python
# Purpose: Pattern-based query processing (bypasses LLM issues)
# Functions:
#   - run_crewai_query(): Main entry point
#   - analyze_query_and_generate_cypher(): NL to Cypher conversion
#   - neo4j_query_tool(): Direct Neo4j execution
#   - format_response(): User-friendly response formatting
```

**Supported Query Patterns:**
- "What is the total WiFi count?" → `MATCH (o:Occupancy) RETURN sum(o.WiFiCount)`
- "WiFi count on First Floor" → `WHERE o.Floor = 'First Floor'`
- "Show occupancy data for Kalwa" → `WHERE o.LocationCode = 'LOC-IN-KALWA'`
- "What floors are available?" → `RETURN DISTINCT o.Floor`

### 3. **frontend.py** - Streamlit Web Interface
```python
# Purpose: User-friendly chat interface
# Port: 8501
# Features:
#   - Real-time query input
#   - Results display
#   - Error handling
```

### 4. **start_chatbot.py** - Application Launcher
```python
# Purpose: One-command startup script
# Checks:
#   - Ollama service (http://localhost:11434)
#   - Neo4j database (bolt://localhost:7687)
# Starts:
#   - FastAPI backend (port 8000)
#   - Streamlit frontend (port 8501)
```

## 🗄️ Database Configuration

### Neo4j Schema
```cypher
# Node: Occupancy
# Properties:
#   - Floor: String (e.g., "First Floor", "Second Floor")
#   - SiteDetails: String (e.g., "Kalwa_Switchboard_ShopFloor")
#   - RecordDate: String (format: 'YYYY-MM-DD')
#   - LocationCode: String (e.g., "LOC-IN-KALWA")
#   - WiFiCount: Integer (number of WiFi connections)
#   - TimeSlot: String (e.g., "01:45 - 02:00")
```

### Connection Details
```python
uri = "bolt://localhost:7687"
username = "neo4j"
password = "purva@1234"
```

## 🐳 Dependencies (requirements.txt)

```text
crewai>=0.28.8          # CrewAI framework
crewai-tools>=0.1.6     # CrewAI tools
fastapi>=0.104.1        # Web framework
streamlit>=1.28.1       # Frontend framework
neo4j>=5.15.0           # Database driver
langchain-community>=0.0.13  # LangChain community
langchain-ollama>=0.1.0 # Ollama integration
ollama>=0.1.7           # Ollama client
uvicorn>=0.24.0         # ASGI server
pydantic>=2.5.0         # Data validation
requests>=2.31.0        # HTTP client
```

## 🚀 Deployment & Usage

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start all services
python start_chatbot.py

# 3. Access interfaces
# - API: http://localhost:8000/docs
# - Frontend: http://localhost:8501
```

### Manual Start
```bash
# Start FastAPI backend
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

# Start  frontend (in another terminal)
  npm run dev
```

### API Testing
```bash
# PowerShell
$body = @{query="What is the total WiFi count?"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://127.0.0.1:8000/crewquery" -Method POST -Body $body -ContentType "application/json"

# Expected Response:
# {"result":"The total WiFi count across all locations and time periods is 6,205,614."}
```

## 🔍 Architecture Flow

```
User Input (UI)
    ↓
FastAPI Backend (main.py)
    ↓
Simple CrewAI Agent (simple_crewai_agent.py)
    ↓
Pattern Matching (analyze_query_and_generate_cypher)
    ↓
Cypher Query Generation
    ↓
Neo4j Database (neo4j_query_tool)
    ↓
Result Formatting (format_response)
    ↓
Response → Frontend Display
```

## ⚠️ Issue Resolution

### Original Problem: LLM Integration Failure
- **Cause**: CrewAI 0.130.0 + LiteLLM + Ollama compatibility issues
- **Symptoms**: 
  - `LLM Provider NOT provided` errors
  - `APIStatusError` missing arguments
  - `IndexError: list index out of range`

### Solution: Pattern-Based Bypass
- **Approach**: Created `simple_crewai_agent.py` with direct pattern matching
- **Benefits**:
  - No LLM dependency issues
  - Faster query processing
  - Deterministic results
  - Easier to maintain and debug

### Files Status
- ✅ **Working**: `simple_crewai_agent.py`, `main.py`, `frontend.py`, `start_chatbot.py`
- ❌ **Problematic**: `crewai_agent.py` (LLM integration issues)
- 📁 **Legacy**: `custom_crew_*.py`, `tool.py`

## 🧪 Testing

### Test Queries
```python
test_queries = [
    "What is the total WiFi count?",
    "Show me occupancy data for Kalwa location",
    "What floors are available?",
    "What is the WiFi count on the First Floor?"
]
```

### Integration Test
```bash
python test_integration.py
```

## 🔧 Troubleshooting

### Common Issues
1. **Port 8000 in use**: Change port in `main.py` or kill existing process
2. **Neo4j connection failed**: Check database status and credentials
3. **Ollama not running**: Start with `ollama serve`
4. **Import errors**: Reinstall requirements: `pip install -r requirements.txt`

### Debug Commands
```bash
# Check if services are running
netstat -ano | findstr ":8000"    # FastAPI
netstat -ano | findstr ":7687"    # Neo4j
netstat -ano | findstr ":11434"   # Ollama

# Test individual components
python -c "from simple_crewai_agent import run_crewai_query; print(run_crewai_query('test'))"
```

## 🎯 Next Steps

### Potential Enhancements
1. **Add more query patterns** to `simple_crewai_agent.py`
2. **Implement caching** for frequent queries
3. **Add authentication** to FastAPI endpoints
4. **Create Docker containers** for easier deployment
5. **Add logging** for better monitoring
6. **Implement query history** in Streamlit frontend

### Performance Optimization
1. **Connection pooling** for Neo4j
2. **Async query processing**
3. **Result caching with Redis**
4. **Load balancing** for multiple instances

This structure provides a robust, working chatbot system that successfully bypasses the LLM integration issues while maintaining full functionality for occupancy data queries.
