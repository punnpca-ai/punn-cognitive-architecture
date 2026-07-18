import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Cannot connect to PCA API");
    }

    setLoading(false);
  }

  return (
    <div className="container">
      <h1>PCA Cognitive DNA</h1>

      <textarea
        rows={5}
        placeholder="Ask anything..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={analyze} disabled={loading}>
        {loading ? "Thinking..." : "Analyze"}
      </button>

      {result && (
        <>
          <h2>Response</h2>

          <pre>{result.response}</pre>

          <h2>Trace</h2>

          <ul>
            {result.trace.map((t: any, index: number) => (
              <li key={index}>
                <strong>{t.stage}</strong>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;