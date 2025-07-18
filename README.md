# SSP Chatbot - Unified Multi-Agent Intelligence System



A unified multi-agent chatbot system that intelligently analyzes occupancy data through natural language queries. This project integrates three powerful AI architectures (RAG, Graph, and CrewAI) into a single seamless interface with Neo4j graph database and vector search capabilities.

## 🚀 Features

- **Unified Backend**: Single FastAPI server with multiple AI service endpoints
- **Three AI Architectures**: RAG (FAISS), Graph (Neo4j), and CrewAI Multi-Agent
- **Seamless Service Switching**: Toggle between AI services from the same interface
- **Real-time Chat Interface**: Modern Next.js frontend with TypeScript
- **Multiple LLM Support**: Ollama integration with various models
- **Smart Query Processing**: Intelligent date/time/location parsing
- **Responsive Design**: Mobile-first UI with dark/light theme support
- **Single Port Architecture**: All services unified on port 8000 with different endpoints

## 🏗️ Unified System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                Unified Chatbot System                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Frontend Layer                                                                          │
│  ┌─────────────────┐                                                                    │
│  │   Next.js UI    │                                                                    │
│  │   (React/TS)    │                                                                    │
│  └─────────────────┘                                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Backend Layer                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │  FastAPI (Unified API Server)                                                    │   │
│  │                                                                                  │   │
│  │  ┌────────────────────────┐┌─────────────────────┐┌───────────────────────────┐ │   │
│  │  │   /rag/query           ││ /graph/query       ││ /crewai/query             │ │   │
│  │  │   (FAISS + Ollama)     ││ (Neo4j + Language) ││ (Multi-Agent)             │ │   │
│  │  └────────────────────────┘└─────────────────────┘└───────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  LLM Layer                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          Ollama (Local LLM)                                     │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │   │
│  │  │  Llama3:8b  │ │  Gemma3:1b  │ │  Mistral:7b │ │   Llama2    │ │   Custom    │ │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
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


## 🔗 Neo4j Graph Database Integration

This project uses **Neo4j** as a **vector-enabled graph database** to store and semantically search vector embeddings using **LangChain + Neo4j**.

---

### ✅ Step 1: Install Neo4j Desktop

- Download Neo4j Desktop: [https://neo4j.com/download](https://neo4j.com/download)
- Run the installer and complete installation.
- Launch Neo4j Desktop and sign in using GitHub, Google, or email.

---

### ✅ Step 2: Create a New Project and Database

1. Open Neo4j Desktop → Click **"New Project"** → Name it (e.g., `VectorBotProject`).
2. Inside the project, click **"Add" → "Local DBMS"**.
3. Set:
   - **Name**: e.g., `vectorbot`
   - **Password**: (choose your own)
4. Click **Create**, then **Start** the database.

---

### ✅ Step 3: Enable Vector Search

#### 🧩 Option A: Enable via GUI

- Go to your running database → Click the **"Plugins"** tab.
- Search for and install plugins like:
  - **Vector**
  - **Vector Indexes**
  - **genAI**

#### ⚠️ Option B: Manual Configuration (if plugin not available via GUI)

1. Click **⋮ (three dots)** next to the database → **Manage** → **Settings**.
2. Scroll to `neo4j.conf` and add the following:

   ```ini
   dbms.security.procedures.unrestricted=apoc.*,gds.*,vector.*
   dbms.security.procedures.allowlist=apoc.*,gds.*,vector.*,genai.*
   dbms.memory.heap.initial_size=2G
   dbms.memory.heap.max_size=4G
   ```

3. Save the changes and **restart the database**.

---

### ✅ Step 4: Get Connection Details

- **URI**: `bolt://localhost:7687`
- **Username**: `neo4j` (default)
- **Password**: The one you set during database creation

---

### ✅ Step 5: Test the Setup

Open the Neo4j Browser (from Neo4j Desktop) and run:

```cypher
RETURN "Neo4j is ready!" AS message;
```

If the vector plugin is enabled, test a vector index creation:

```cypher
CALL db.index.vector.createNodeIndex('myVectorIndex', 'MyLabel', 'myVectorProperty', 384);
```

---

### ✅ Step 6: Connect from Python

Use the official Neo4j Python driver:

```python
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "your_password"

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("RETURN 'Neo4j connected!' AS msg")
    print(result.single()["msg"])
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
NEO4J_PASSWORD=The one you set during database creation
OLLAMA_URL=http://localhost:11434
```

## 🚀 Usage

### Unified System (Recommended)

```powershell
# Terminal 1: Start unified backend
python -m uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Next.js frontend
npm run dev
```

**Access**: http://localhost:3000

### Service Switching

1. **Select AI Service**: Use the dropdown in the header to choose between:
   - **RAG Chatbot** - FAISS vector search with Ollama
   - **Graph Chatbot** - Neo4j graph database with LangChain
   - **CrewAI Multi-Agent** - Multi-agent system with specialized tools

2. **Select Model**: Choose your Ollama model (RAG and Graph only)

3. **Start Chatting**: All services share the same conversation interface

### API Endpoints

- **RAG Service**: `POST /rag/query`
- **Graph Service**: `POST /graph/query`
- **CrewAI Service**: `POST /crewai/query`
- **Health Check**: `GET /health`

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

#### RAG Service
```bash
POST /rag/query
Content-Type: application/json

{
  "question": "What is the WiFi count for Kalwa?",
  "model": "llama3:8b"
}
```

#### Graph Service
```bash
POST /graph/query
Content-Type: application/json

{
  "question": "Show occupancy trends for last month",
  "model": "llama3:8b"
}
```

#### CrewAI Service
```bash
POST /crewai/query
Content-Type: application/json

{
  "query": "What is the highest occupancy floor?"
}
```

#### Health Check
```bash
GET /health

Response: {"status": "healthy", "service": "Unified Backend"}
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
NEO4J_PASSWORD = "put your password here"  
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

Developed by Purva Patil


## Acknowledgments

- **CrewAI**: For the multi-agent framework
- **Haystack**: For the NLP pipeline architecture
- **Ollama**: For local LLM inference
- **Neo4j**: For graph database capabilities
- **Next.js**: For the modern frontend framework
- **FastAPI**: For the high-performance API framework

---


