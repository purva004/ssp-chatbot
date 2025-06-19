# SSP Chatbot

A full-stack chatbot application using RAG (Retrieval-Augmented Generation) with a FastAPI backend and a Next.js frontend. The backend uses Ollama for LLM inference and supports custom model selection.

---

## System Requirements

- **Python**: 3.9 or higher (recommended: 3.10+)
- **Node.js**: 18.x or higher (LTS recommended)
- **Ollama**: Latest version ([https://ollama.com/download](https://ollama.com/download))
- **Ollama Models**: Download and run a supported model (e.g., `llama3:8b`, `llama2:7b`, `mistral:7b`, etc.)
- **pip**: For Python package management
- **npm** or **pnpm**: For Node.js package management

---

## Backend Setup (FastAPI)

1. **Install Python dependencies:**
   ```pwsh
   pip install -r requirements.txt
   ```

2. **Set the Ollama model name:**
   - Open `rag_chatbot.py`.
   - Find the line:
     ```python
     OLLAMA_MODEL = "llama3:8b"
     ```
   - Change the value to your desired Ollama model name (e.g., `llama2:7b`, `mistral:7b`, etc).
   - Open `.env.loval` (if present).
   - Find the line:
     ```env
     NEXT_PUBLIC_DEFAULT_MODEL=llama3.2
     ```
   - Change the value to your desired Ollama model name (e.g., `llama2:7b`, `mistral:7b`, etc).

3. **Start the backend server:**
   ```pwsh
   uvicorn rag_chatbot:app --reload
   ```
   The backend will be available at `http://127.0.0.1:8000`.

---

## Frontend Setup (Next.js)

1. **Install Node.js dependencies:**
   ```pwsh
   npm install
   ```
   *(Or use `pnpm install` if you prefer.)*

2. **Start the frontend development server:**
   ```pwsh
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`.

---

## Notes
- Make sure the backend is running before using the frontend chat interface.
- The frontend communicates with the backend via API endpoints (see `src/app/services/ragService.ts`).
- You can change the Ollama model name in `rag_chatbot.py` at the `OLLAMA_MODEL` variable and in `.env.loval`.

---

## Project Structure
- `rag_chatbot.py` — FastAPI backend (Python)
- `src/` — Next.js frontend (TypeScript/React)
- `data.json` — Data source for RAG
- `requirements.txt` — Python dependencies
- `package.json` — Node.js dependencies

---

## Neo4j Graph Database Integration
This project uses Neo4j as a vector-enabled graph database to store and semantically search vector embeddings using LangChain + Neo4j.

- Step 1: Install Neo4j Desktop
   - Download Neo4j Desktop: https://neo4j.com/download/

   - Run the installer and complete installation.

   - Launch Neo4j Desktop and sign in (GitHub/Google/Email).

- Step 2: Create a New Project and Database
   - In Neo4j Desktop, click "New Project" → name it (e.g., VectorBotProject).

   - Inside the project, click "Add" → "Local DBMS".

   - Name your database (e.g., vectorbot), set a password, and click Create.

   - Click Start to launch the database.

- Step 3: Enable Vector Search
   - Option A: Enable via GUI
     Go to the database → click "Plugins".

     - Look for plugins like "Vector", "Vector Indexes", or "genAI".

     - Install them if listed.

   - Option B: Manual Configuration (if plugin not available)
     Go to database settings: ⋮ → Manage → Settings.

     - Edit the neo4j.conf file and add:

       dbms.security.procedures.unrestricted=apoc.*,gds.*,vector.*
       dbms.security.procedures.allowlist=apoc.*,gds.*,vector.*,genai.*
       dbms.memory.heap.initial_size=2G
       dbms.memory.heap.max_size=4G
       Save the file and restart the database.

- Step 4: Get Connection Details
   - URI: bolt://localhost:7687

   - Username: neo4j (default)

   - Password: the one you set during creation

- Step 5: Test the Setup
   - Open the Neo4j browser and run:
      - RETURN "Neo4j is ready!" AS message;
        - If the vector plugin is enabled, try:
          CALL db.index.vector.createNodeIndex('myVectorIndex', 'MyLabel', 'myVectorProperty', 384)
- Step 6: Connect from Python
   - Use the official Neo4j Python driver:
       - from neo4j import GraphDatabase
       - uri = "bolt://localhost:7687"
       - username = "neo4j"
       - password = "your_password"
       - driver = GraphDatabase.driver(uri, auth=       (username,   password))
       - with driver.session() as session:
           - result = session.run("RETURN 'Neo4j connected!' AS msg")
           - print(result.single()["msg"])


## License
MIT

