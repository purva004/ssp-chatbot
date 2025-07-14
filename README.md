# SSP Chatbot - Multi-Agent Occupancy Data Intelligence System

![SSP Chatbot](logobeautify.png)

A sophisticated multi-agent chatbot system built to intelligently analyze occupancy data through natural language queries. This project demonstrates multiple AI architectures including CrewAI, Haystack, and LangChain integrations with Neo4j graph database and vector search capabilities.

## 🚀 Features

- **Multi-Agent Architecture**: Supports CrewAI, Haystack, and custom agents
- **Vector Database Integration**: Neo4j with semantic search capabilities
- **RAG (Retrieval-Augmented Generation)**: Intelligent document retrieval and generation
- **Real-time Chat Interface**: Modern Next.js frontend with TypeScript
- **Multiple LLM Support**: Ollama integration with various models
- **Time-based Filtering**: Smart filtering by dates, times, and locations
- **Responsive Design**: Mobile-first UI with theme support
- **Multiple Deployment Options**: FastAPI, Streamlit, and hybrid architectures

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              SSP Chatbot System Architecture                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Frontend Layer                                                                          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                    │
│  │   Next.js UI    │    │  Streamlit UI   │    │  Direct API     │                    │
│  │   (React/TS)    │    │   (Python)      │    │   Integration   │                    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  API Gateway Layer                                                                       │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                    │
│  │   FastAPI       │    │   FastAPI       │    │   FastAPI       │                    │
│  │   (Main)        │    │   (CrewAI)      │    │   (Haystack)    │                    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Agent Layer                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                    │
│  │  RAG Agent      │    │  CrewAI Agent   │    │  Haystack       │                    │
│  │  (FAISS+LLM)    │    │  (Multi-Agent)  │    │  Pipeline       │                    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  LLM Layer                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │                          Ollama (Local LLM)                                     │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │  │
│  │  │  Llama3:8b  │ │  Gemma3:1b  │ │  Mistral:7b │ │   Llama2    │ │   Custom    │ │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Data Layer                                                                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                    │
│  │     Neo4j       │    │     FAISS       │    │   JSON/CSV      │                    │
│  │  (Graph + Vec)  │    │  (Vector Store) │    │  (Raw Data)     │                    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 15.3.3 with React 19
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.0
- **UI Components**: Radix UI, Lucide Icons
- **Animations**: Framer Motion
- **State Management**: React Hooks
- **Theme**: Next-themes with dark/light mode

### Backend
- **API Framework**: FastAPI with Uvicorn
- **AI Frameworks**: CrewAI, Haystack, LangChain
- **Vector Database**: Neo4j with vector search
- **Vector Store**: FAISS for similarity search
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: Ollama (Local inference)

### Database & Storage
- **Graph Database**: Neo4j (Primary)
- **Vector Search**: FAISS (Secondary)
- **Data Format**: JSON, CSV
- **Schema**: Occupancy data with temporal and spatial dimensions

### DevOps & Tools
- **Package Manager**: npm/pnpm, pip
- **Environment**: Windows PowerShell, Virtual Environment
- **Version Control**: Git
- **API Testing**: FastAPI automatic docs

## 📦 Installation & Setup

### System Requirements
- **Python**: 3.9+ (recommended: 3.10+)
- **Node.js**: 18.x+ (LTS recommended)
- **Ollama**: Latest version
- **Neo4j**: Desktop or Server edition
- **Memory**: 8GB+ RAM recommended
- **Storage**: 5GB+ free space

### 1. Clone and Setup Environment

```powershell
# Clone the repository
cd C:\Users\z0050s8t\ssp-chatbot

# Create Python virtual environment
python -m venv chatbot
.\chatbot\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install and Setup Ollama

```powershell
# Download and install Ollama from https://ollama.com/download
# Pull required models
ollama pull llama3:8b
ollama pull gemma3:1b
ollama pull mistral:7b

# Start Ollama service
ollama serve
```

### 3. Setup Neo4j Database

1. **Download Neo4j Desktop**: https://neo4j.com/download/
2. **Create Database**:
   - Project name: SSP-Chatbot
   - Database name: occupancy-db
   - Password: purva@1234 (or update in configs)
3. **Enable Vector Search**:
   ```cypher
   // Test connection
   RETURN "Neo4j is ready!" AS message;
   
   // Create vector index (if needed)
   CALL db.index.vector.createNodeIndex('embedding_index', 'LogEntry', 'embedding', 384);
   ```

### 4. Frontend Setup

```powershell
# Install Node.js dependencies
npm install
# OR
pnpm install

# Start development server
npm run dev
```

### 5. Configure Environment Variables

Create `.env.local` file:
```env
NEXT_PUBLIC_DEFAULT_MODEL=llama3:8b
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=purva@1234
OLLAMA_URL=http://localhost:11434
```

## 🚀 Usage

### Option 1: Main RAG Chatbot (Recommended)

```powershell
# Terminal 1: Start backend
uvicorn rag_chatbot:app --reload

# Terminal 2: Start frontend
npm run dev
```

**Access**: http://localhost:3000

### Option 2: CrewAI Multi-Agent System

```powershell
cd crewAI
python start_chatbot.py
```

**Access**: 
- API: http://localhost:8000
- Streamlit UI: http://localhost:8501

### Option 3: Haystack Pipeline

```powershell
cd haystack
uvicorn haystack_multi_agent_chatbot:app --reload
```

**Access**: http://localhost:8000

### Option 4: Graph-based Chatbot

```powershell
uvicorn graphchatbot:app --reload
```

**Access**: http://localhost:8000

## 💡 Usage Examples

### Natural Language Queries

```
# Location-based queries
"What is the WiFi count on the First Floor of Kalwa location?"
"Show me occupancy data for Mumbai site"

# Time-based queries
"What was the occupancy on 2025-06-14 at 10:00 AM?"
"Show me weekend occupancy trends"

# Analytical queries
"Which floor has the highest occupancy?"
"Compare WiFi usage between weekdays and weekends"

# Complex queries
"What is the total access count for all Pune locations during morning hours?"
"Show me the occupancy pattern for the last week"
```

### API Endpoints

#### Main RAG API
```bash
POST /query
Content-Type: application/json

{
  "question": "What is the WiFi count for Kalwa?",
  "model": "llama3:8b"
}
```

#### CrewAI API
```bash
POST /crewquery
Content-Type: application/json

{
  "query": "Show occupancy trends for last month"
}
```

#### Haystack API
```bash
POST /chat
Content-Type: application/json

{
  "query": "What is the highest occupancy floor?"
}
```

## 📊 Data Schema

### Occupancy Data Structure
```json
{
  "RecordDate": "2025-06-14",
  "Time": "10:30:00",
  "DayOfWeek": "Monday",
  "TimeSlot": "10:30 - 10:45",
  "Floor": "First Floor",
  "SiteDetails": "Kalwa_Innovation_Hub",
  "DayType": "Weekday",
  "LocationCode": "LOC-IN-KALWA",
  "WiFiCount": 45,
  "AccessControlCount": 28
}
```

### Neo4j Graph Schema
```cypher
// Nodes
(l:Location {code: "LOC-IN-KALWA"})
(s:Site {details: "Kalwa_Innovation_Hub"})
(r:Record {date: "2025-06-14", wifi: 45, access: 28})

// Relationships
(l)-[:HAS_SITE]->(s)
(s)-[:HAS_RECORD]->(r)
```

## 🔄 How It Works

### RAG Pipeline
1. **Query Processing**: Natural language input is normalized and parsed
2. **Document Retrieval**: FAISS similarity search finds relevant occupancy records
3. **Context Filtering**: Smart filtering by location, time, and other parameters
4. **LLM Generation**: Ollama generates human-readable responses
5. **Response Enhancement**: Critique and refinement of answers

### CrewAI Multi-Agent Flow
1. **Agent Initialization**: Occupancy Data Analyst agent with Neo4j tools
2. **Query Translation**: Natural language to Cypher query conversion
3. **Database Execution**: Cypher queries executed against Neo4j
4. **Result Processing**: Raw data transformed into insights
5. **Human Response**: LLM generates conversational explanations

### Haystack Pipeline
1. **Multi-Agent Architecture**: Retriever and Generator components
2. **Neo4j Integration**: Custom retriever for graph database queries
3. **Ollama Integration**: Local LLM generation with context
4. **Pipeline Orchestration**: Coordinated data flow through components

## 🎯 Key Features

### ✅ Pros
- **Multi-Architecture Support**: Choose between RAG, CrewAI, or Haystack
- **Local LLM Inference**: Privacy-focused with Ollama
- **Real-time Processing**: Fast response times with caching
- **Smart Filtering**: Intelligent date/time/location parsing
- **Scalable Design**: Microservices architecture
- **Graph Database**: Rich relationship modeling with Neo4j
- **Modern UI**: Responsive design with theme support
- **Model Flexibility**: Easy switching between LLM models
- **Conversation History**: Persistent chat sessions
- **API Documentation**: Auto-generated FastAPI docs

## 📁 Project Structure

```
ssp-chatbot/
├── 📂 src/                          # Next.js Frontend
│   ├── 📂 app/
│   │   ├── 📂 services/              # API service layers
│   │   ├── globals.css              # Global styles
│   │   ├── layout.tsx               # App layout
│   │   └── page.tsx                 # Main page
│   ├── 📂 components/               # React components
│   │   ├── 📂 ui/                   # UI components
│   │   ├── 📂 magicui/              # Magic UI components
│   │   ├── Chat.tsx                 # Main chat component
│   │   └── MarkdownRenderer.tsx     # Markdown support
│   └── 📂 lib/                      # Utility functions
├── 📂 crewAI/                       # CrewAI Implementation
│   ├── crewai_agent.py              # Main CrewAI agent
│   ├── main.py                      # FastAPI server
│   ├── frontend.py                  # Streamlit UI
│   ├── start_chatbot.py             # Startup script
│   ├── requirements.txt             # CrewAI dependencies
│   └── README.md                    # CrewAI documentation
├── 📂 haystack/                     # Haystack Implementation
│   ├── haystack_multi_agent_chatbot.py  # Haystack pipeline
│   ├── requirements.txt             # Haystack dependencies
│   └── occupancy.csv               # Sample data
├── 📂 dummy/                        # Test data
│   ├── wifi_data.csv               # WiFi sample data
│   └── wifi_data.py                # Data generator
├── 📂 chatbot/                      # Python virtual environment
├── 📂 all-MiniLM-L6-v2/            # Local embedding model
├── rag_chatbot.py                   # Main RAG implementation
├── graphchatbot.py                  # Graph-based chatbot
├── data.json                        # Main occupancy dataset
├── requirements.txt                 # Python dependencies
├── package.json                     # Node.js dependencies
├── next.config.ts                   # Next.js configuration
├── tailwind.config.js               # Tailwind CSS config
├── tsconfig.json                    # TypeScript config
└── README.md                        # This file
```

## 🔧 Configuration

### Model Configuration
```python
# rag_chatbot.py
DEFAULT_OLLAMA_MODEL = "llama3:8b"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LOCAL_MODEL_PATH = "./all-MiniLM-L6-v2"
```

### Database Configuration
```python
# Neo4j settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "purva@1234"
```

### Frontend Configuration
```typescript
// next.config.ts
export default {
  experimental: {
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
};
```

## 🚦 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```powershell
   # Check if Ollama is running
   ollama serve
   
   # Test model availability
   ollama list
   ollama pull llama3:8b
   ```

2. **Neo4j Connection Failed**
   ```powershell
   # Check Neo4j status
   # Verify credentials in config files
   # Ensure port 7687 is open
   ```

3. **Model Loading Issues**
   ```powershell
   # Download embedding model manually
   # Check LOCAL_MODEL_PATH in config
   ```

4. **Frontend Build Errors**
   ```powershell
   # Clear cache and reinstall
   rm -rf node_modules
   rm package-lock.json
   npm install
   ```

### Performance Optimization

1. **Memory Management**
   - Allocate sufficient RAM for LLM models
   - Configure Neo4j heap size appropriately
   - Use model quantization for resource constraints

2. **Response Time**
   - Implement caching for frequent queries
   - Use smaller models for faster inference
   - Optimize vector search parameters

## 🧪 Testing

### Unit Tests
```powershell
# Test individual components
python -m pytest tests/

# Test API endpoints
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question": "test"}'
```

### Integration Tests
```powershell
# Test full pipeline
cd crewAI
python test_integration.py
```

## 📈 Future Enhancements

- [ ] **Multi-Modal Support**: Image and voice input capabilities
- [ ] **Advanced Analytics**: Trend analysis and predictive modeling
- [ ] **Cloud Deployment**: Docker containerization and cloud support
- [ ] **Real-time Data**: Live data streaming and updates
- [ ] **User Management**: Authentication and personalization
- [ ] **Mobile App**: React Native or Flutter implementation
- [ ] **API Rate Limiting**: Production-ready API management
- [ ] **Data Visualization**: Interactive charts and dashboards

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Developed by [Your Name]
- GitHub: [Your GitHub Profile]
- Email: [Your Email]

## 🙏 Acknowledgments

- **CrewAI**: For the multi-agent framework
- **Haystack**: For the NLP pipeline architecture
- **Ollama**: For local LLM inference
- **Neo4j**: For graph database capabilities
- **Next.js**: For the modern frontend framework
- **FastAPI**: For the high-performance API framework

---

## 📞 Support

For support and questions:
- Check the troubleshooting section above
- Review the individual README files in subdirectories
- Open an issue on GitHub
- Check the FastAPI automatic documentation at `/docs`

---

*Built with ❤️ using modern AI technologies*

