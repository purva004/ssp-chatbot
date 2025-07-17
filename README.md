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

## License
MIT
