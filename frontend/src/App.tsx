import { useEffect, useState } from "react";

type Health = { status: string };

export default function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/health")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setHealth)
      .catch((e) => setError(String(e)));
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial" }}>
      <h1 style={{ marginTop: 0 }}>LLM Reliability Platform</h1>
      <p style={{ color: "#555" }}>
        Frontend scaffold is live. This page calls <code>/api/health</code>.
      </p>

      <div style={{ marginTop: 16, padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
        <h2 style={{ marginTop: 0, fontSize: 16 }}>Backend health</h2>
        {!health && !error && <p>Loading...</p>}
        {error && <p style={{ color: "crimson" }}>Error: {error}</p>}
        {health && <p>Status: <strong>{health.status}</strong></p>}
      </div>
    </div>
  );
}
