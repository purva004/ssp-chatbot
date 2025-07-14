export async function askCrewAI(query: string): Promise<string> {
  try {
    const response = await fetch("http://localhost:8000/crewai/query", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.result || "No response from CrewAI";
  } catch (error) {
    console.error("CrewAI Service Error:", error);
    throw new Error(`Failed to get response from CrewAI: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export async function checkCrewAIHealth(): Promise<boolean> {
  try {
    const response = await fetch("http://localhost:8000/health", {
      method: "GET",
      headers: { 
        "Content-Type": "application/json",
      },
    });
    return response.ok;
  } catch (error) {
    console.error("CrewAI Health Check Error:", error);
    return false;
  }
}
