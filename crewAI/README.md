# CrewAI Occupancy Chatbot

A sophisticated chatbot system built with CrewAI framework that analyzes occupancy data stored in Neo4j database using natural language queries.

## Features

- **CrewAI Framework**: Uses actual CrewAI agents and tasks for intelligent query processing
- **Neo4j Integration**: Queries occupancy data from Neo4j graph database
- **Ollama LLM**: Utilizes local Llama3:8b model via Ollama for natural language processing
- **FastAPI Backend**: RESTful API for handling queries
- **Streamlit Frontend**: User-friendly web interface
- **Automated Cypher Generation**: Converts natural language to Cypher queries

## Architecture

```
User Query → Streamlit → FastAPI → CrewAI Agent → Neo4j Tool → Neo4j Database
                                     ↓
                                  Ollama LLM
```

## Prerequisites

1. **Python 3.8+**
2. **Ollama**: Install from [ollama.ai](https://ollama.ai)
3. **Neo4j**: Running instance with occupancy data
4. **Llama3:8b model**: `ollama pull llama3:8b`

## Database Schema

The Neo4j database contains `Occupancy` nodes with these properties:
- `Floor`: Floor name (e.g., "First Floor", "Second Floor")
- `SiteDetails`: Location details (e.g., "Kalwa_Switchboard_ShopFloor")
- `RecordDate`: Date in format 'YYYY-MM-DD'
- `LocationCode`: Location code (e.g., "LOC-IN-KALWA")
- `WiFiCount`: Number of WiFi connections (integer)
- `TimeSlot`: Time range (e.g., "01:45 - 02:00")

## Installation

1. **Clone and navigate to the project**:
   ```bash
   cd C:\Users\z0050s8t\ssp-chatbot\crewAI
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure services are running**:
   - Start Ollama: `ollama serve`
   - Start Neo4j database
   - Pull Llama3 model: `ollama pull llama3:8b`

4. **Configure database connection** (if needed):
   Edit the connection details in `crewai_agent.py`:
   ```python
   uri = "bolt://localhost:7687"
   username = "neo4j"
   password = "purva@1234"
   ```
### To check it on postman
     


### Manual Start
    


1. **Start FastAPI backend**:
   ```bash
     uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

   ```

2. **Start Streamlit frontend**:
   ```bash
     npm run dev
   ```

### API Usage

 ### Solution:
 - You need to use the Postman Desktop App to test APIs running on your local machine.

### What to do:

 - Click the "Download Desktop Agent" or "Download Postman App" button shown in the error message.
 - Install and open the Postman Desktop App.
 - Run your Flask server as before (python crewai_agent.py).
 - In the Desktop App, create the same POST request to http://localhost:5000/occupancy with your JSON body.
 - Click Send—it will work!

## Example Queries

- "What is the WiFi count on the First Floor of Kalwa location on date 6/14/2025?"
- "Show me occupancy data for Kalwa location"
- "What is the total WiFi count for all locations?"
- "Which floor has the highest occupancy?"
- "Show me the occupancy trends for the last week"

## Project Structure

```
crewAI/
├── crewai_agent.py          # CrewAI agent implementation
├── main.py                  # FastAPI backend
├── frontend.py              # Streamlit frontend
├── tool.py                  # Neo4j tool (legacy)
├── start_chatbot.py         # Startup script
├── requirements.txt         # Dependencies
├── README.md               # This file
├── custom_crew_agent.py    # Legacy custom implementation
└── custom_crew_runner.py   # Legacy custom runner
```

## Key Components

### CrewAI Agent (`crewai_agent.py`)
- **Role**: Occupancy Data Analyst
- **Goal**: Answer occupancy queries using Neo4j
- **Tools**: Neo4j query tool
- **LLM**: Ollama Llama3:8b

### Neo4j Tool
- Executes Cypher queries against the database
- Handles connection management and error handling
- Returns formatted results

### FastAPI Backend (`main.py`)
- Provides `/crewquery` endpoint
- Handles CORS and error management
- Integrates with CrewAI crew

### Streamlit Frontend (`frontend.py`)
- Simple chat interface
- Real-time query processing
- Results display

## Troubleshooting

### Common Issues

1. **Ollama not accessible**:
   ```bash
   ollama serve
   ollama pull llama3:8b
   ```

2. **Neo4j connection failed**:
   - Check if Neo4j is running on port 7687
   - Verify credentials in `crewai_agent.py`

3. **Import errors**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Port conflicts**:
   - FastAPI: Change port in `start_chatbot.py` or `main.py`
   - Streamlit: Change port in `start_chatbot.py`

### Debug Mode

To enable verbose logging, the CrewAI agent is configured with `verbose=True`. Check console output for detailed execution traces.

## Advanced Usage

### Custom Agents

You can extend the system by adding more specialized agents:

```python
from crewai import Agent

data_validator = Agent(
    role="Data Validator",
    goal="Validate and clean occupancy data",
    backstory="Expert in data quality and validation",
    tools=[validation_tool],
    llm=llm
)
```

### Additional Tools

Add more tools for enhanced functionality:

```python
@tool
def export_data_tool(query: str, format: str) -> str:
    """Export query results to different formats"""
    # Implementation here
    pass
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review CrewAI documentation: [docs.crewai.com](https://docs.crewai.com)
- Check Ollama documentation: [ollama.ai](https://ollama.ai)
