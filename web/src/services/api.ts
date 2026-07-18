const API_BASE = "http://127.0.0.1:8000";

export async function analyze(question: string) {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("API request failed");
  }

  return response.json();
}