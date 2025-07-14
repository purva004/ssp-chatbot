export async function askGraph(question: string, model?: string): Promise<string> {
  try {
    const response = await fetch("http://localhost:8000/graph/query", {
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
    return data.answer || "No response from Graph chatbot";
  } catch (error) {
    console.error("Graph Service Error:", error);
    throw new Error(`Failed to get response from Graph chatbot: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export async function checkGraphHealth(): Promise<boolean> {
  try {
    const response = await fetch("http://localhost:8000/health", {
      method: "GET",
      headers: { 
        "Content-Type": "application/json",
      },
    });
    return response.ok;
  } catch (error) {
    console.error("Graph Health Check Error:", error);
    return false;
  }
}
