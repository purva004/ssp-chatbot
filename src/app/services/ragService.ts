export async function askRAG(question: string, model?: string): Promise<string> {
  const res = await fetch("http://localhost:8000/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, model }),
  });
  const data = await res.json();
  return data.answer;
}