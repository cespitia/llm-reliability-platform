import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { PromptVersion } from "../api/types";

function parsePromptId(): number | null {
  const m = window.location.hash.match(/#\/prompts\/(\d+)/);
  if (!m) return null;
  return Number(m[1]);
}

export function PromptVersionsPage() {
  const promptId = parsePromptId();
  const [versions, setVersions] = useState<PromptVersion[]>([]);
  const [template, setTemplate] = useState("Summarize this CI log and propose next steps:\n\n{{log}}");
  const [model, setModel] = useState("fake");
  const [temperature, setTemperature] = useState(0);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    if (!promptId) return;
    setError(null);
    try {
      const data = await api.listVersions(promptId);
      setVersions(data);
    } catch (e) {
      setError(String(e));
    }
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [window.location.hash]);

  async function onCreateVersion(e: React.FormEvent) {
    e.preventDefault();
    if (!promptId) return;
    setError(null);
    try {
      await api.createVersion(promptId, template, model, temperature);
      await refresh();
    } catch (e) {
      setError(String(e));
    }
  }

  if (!promptId) {
    return (
      <div>
        <h1 style={{ marginTop: 0 }}>Prompt Versions</h1>
        <p>Missing prompt id in URL.</p>
        <p>
          Go back to <a href="#/" style={{ color: "#0366d6" }}>Prompts</a>.
        </p>
      </div>
    );
  }

  return (
    <div>
      <h1 style={{ marginTop: 0 }}>Prompt {promptId} Versions</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ display: "grid", gridTemplateColumns: "420px 1fr", gap: 16 }}>
        <div style={{ border: "1px solid #e5e5e5", borderRadius: 10, padding: 12 }}>
          <h2 style={{ marginTop: 0, fontSize: 16 }}>Create Version</h2>
          <form onSubmit={onCreateVersion} style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <label style={{ fontSize: 12, color: "#555" }}>Template</label>
            <textarea
              value={template}
              onChange={(e) => setTemplate(e.target.value)}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc", minHeight: 140 }}
            />

            <label style={{ fontSize: 12, color: "#555" }}>Model</label>
            <input
              value={model}
              onChange={(e) => setModel(e.target.value)}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
            />

            <label style={{ fontSize: 12, color: "#555" }}>Temperature</label>
            <input
              type="number"
              step="0.1"
              min="0"
              max="2"
              value={temperature}
              onChange={(e) => setTemperature(Number(e.target.value))}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
            />

            <button style={{ padding: 10, borderRadius: 8, border: "1px solid #333", cursor: "pointer" }}>
              Create Version
            </button>
          </form>

          <p style={{ marginTop: 14 }}>
            Back to <a href="#/" style={{ color: "#0366d6" }}>Prompts</a>
          </p>
        </div>

        <div style={{ border: "1px solid #e5e5e5", borderRadius: 10, padding: 12 }}>
          <h2 style={{ marginTop: 0, fontSize: 16 }}>Versions</h2>
          {versions.length === 0 && <p>No versions yet.</p>}
          {versions.map((v) => (
            <div key={v.id} style={{ border: "1px solid #eee", borderRadius: 10, padding: 12, marginBottom: 10 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                <strong>v{v.version}</strong>
                <span style={{ fontSize: 12, color: "#555" }}>
                  model={v.model}, temp={v.temperature}
                </span>
              </div>
              <pre style={{ whiteSpace: "pre-wrap", marginTop: 8, fontSize: 12, background: "#fafafa", padding: 10, borderRadius: 8 }}>
                {v.template}
              </pre>
              <p style={{ marginTop: 10 }}>
                Run eval with this version:{" "}
                <a href={`#/evals?pv=${v.id}`} style={{ color: "#0366d6" }}>
                  Open eval page
                </a>
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
