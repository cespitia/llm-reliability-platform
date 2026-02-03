import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import type { Prompt } from "../api/types";

export function PromptsPage() {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  const selected = useMemo(() => prompts.find((p) => p.id === selectedId) ?? null, [prompts, selectedId]);

  async function refresh() {
    setError(null);
    try {
      const data = await api.listPrompts();
      setPrompts(data);
      if (!selectedId && data.length) setSelectedId(data[0].id);
    } catch (e) {
      setError(String(e));
    }
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function onCreatePrompt(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const p = await api.createPrompt(name.trim(), description.trim());
      setName("");
      setDescription("");
      await refresh();
      setSelectedId(p.id);
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <div>
      <h1 style={{ marginTop: 0 }}>Prompts</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ display: "grid", gridTemplateColumns: "360px 1fr", gap: 16 }}>
        <div style={{ border: "1px solid #e5e5e5", borderRadius: 10, padding: 12 }}>
          <h2 style={{ marginTop: 0, fontSize: 16 }}>Create Prompt</h2>
          <form onSubmit={onCreatePrompt} style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <input
              placeholder="Prompt name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
              required
            />
            <textarea
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc", minHeight: 80 }}
            />
            <button style={{ padding: 10, borderRadius: 8, border: "1px solid #333", cursor: "pointer" }}>
              Create
            </button>
          </form>

          <hr style={{ margin: "16px 0" }} />

          <h2 style={{ marginTop: 0, fontSize: 16 }}>Existing</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {prompts.map((p) => (
              <button
                key={p.id}
                onClick={() => setSelectedId(p.id)}
                style={{
                  textAlign: "left",
                  padding: 10,
                  borderRadius: 8,
                  border: p.id === selectedId ? "2px solid #0366d6" : "1px solid #ccc",
                  background: "white",
                  cursor: "pointer",
                }}
              >
                <div style={{ fontWeight: 600 }}>{p.name}</div>
                <div style={{ fontSize: 12, color: "#555" }}>{p.description}</div>
              </button>
            ))}
          </div>
        </div>

        <div style={{ border: "1px solid #e5e5e5", borderRadius: 10, padding: 12 }}>
          <h2 style={{ marginTop: 0, fontSize: 16 }}>Selected Prompt</h2>
          {!selected && <p>Select a prompt to manage versions.</p>}
          {selected && (
            <div>
              <p style={{ margin: "6px 0" }}>
                <strong>ID:</strong> {selected.id}
              </p>
              <p style={{ margin: "6px 0" }}>
                <strong>Name:</strong> {selected.name}
              </p>
              <p style={{ margin: "6px 0" }}>
                <strong>Description:</strong> {selected.description || "(none)"}
              </p>
              <p style={{ marginTop: 14 }}>
                Manage versions:{" "}
                <a href={`#/prompts/${selected.id}`} style={{ color: "#0366d6" }}>
                  Open versions page
                </a>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
