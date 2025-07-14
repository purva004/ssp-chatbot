export async function askRAG(question: string, model?: string): Promise<string> {
  try {
    const response = await fetch("http://localhost:8000/rag/query", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question, model }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.answer || "No response from RAG chatbot";
  } catch (error) {
    console.error("RAG Service Error:", error);
    throw new Error(`Failed to get response from RAG chatbot: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export async function checkRAGHealth(): Promise<boolean> {
  try {
    const response = await fetch("http://localhost:8000/health", {
      method: "GET",
      headers: { 
        "Content-Type": "application/json",
      },
    });
    return response.ok;
  } catch (error) {
    console.error("RAG Health Check Error:", error);
    return false;
  }
}
