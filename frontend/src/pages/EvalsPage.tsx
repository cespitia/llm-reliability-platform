import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import type { EvalCaseResult, EvalRun } from "../api/types";

function parseQueryParam(name: string): string | null {
  const hash = window.location.hash;
  const idx = hash.indexOf("?");
  if (idx === -1) return null;
  const qs = new URLSearchParams(hash.slice(idx + 1));
  return qs.get(name);
}

export function EvalsPage() {
  const presetPv = parseQueryParam("pv");
  const [runs, setRuns] = useState<EvalRun[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<number | null>(null);
  const [details, setDetails] = useState<EvalCaseResult[]>([]);
  const [pvInput, setPvInput] = useState<string>(presetPv ?? "");
  const [error, setError] = useState<string | null>(null);
  const selectedRun = useMemo(() => runs.find((r) => r.id === selectedRunId) ?? null, [runs, selectedRunId]);

  async function refreshRuns() {
    setError(null);
    try {
      const data = await api.listRuns();
      setRuns(data);
      if (!selectedRunId && data.length) setSelectedRunId(data[0].id);
    } catch (e) {
      setError(String(e));
    }
  }

  async function refreshDetails(runId: number) {
    setError(null);
    try {
      const data = await api.getRunDetails(runId);
      setDetails(data);
    } catch (e) {
      setError(String(e));
    }
  }

  useEffect(() => {
    refreshRuns();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selectedRunId != null) refreshDetails(selectedRunId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedRunId]);

  async function onRunEval() {
    setError(null);
    try {
      const pv = pvInput.trim() ? Number(pvInput.trim()) : undefined;
      const run = await api.runEval(Number.isFinite(pv as number) ? (pv as number) : undefined);
      await refreshRuns();
      setSelectedRunId(run.id);
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <div>
      <h1 style={{ marginTop: 0 }}>Evaluations</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ display: "grid", gridTemplateColumns: "380px 1fr", gap: 16 }}>
        <div style={{ border: "1px solid #e5e5e5", borderRadius: 10, padding: 12 }}>
          <h2 style={{ marginTop: 0, fontSize: 16 }}>Run evaluation</h2>
          <p style={{ marginTop: 0, color: "#555", fontSize: 13 }}>
            Runs the golden CI/CD dataset using the FakeProvider and persists results.
          </p>

          <label style={{ fontSize: 12, color: "#555" }}>Optional Prompt Version ID</label>
          <input
            value={pvInput}
            onChange={(e) => setPvInput(e.target.value)}
            placeholder="e.g. 1"
            style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #ccc", marginTop: 6 }}
          />
          <button
            onClick={onRunEval}
            style={{ marginTop: 10, padding: 10, borderRadius: 8, border: "1px solid #333", cursor: "pointer" }}
          >
            Run eval
          </button>

          <hr style={{ margin: "16px 0" }} />

          <h2 style={{ marginTop: 0, fontSize: 16 }}>Runs</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {runs.map((r) => (
              <button
                key={r.id}
                onClick={() => setSelectedRunId(r.id)}
                style={{
                  textAlign: "left",
                  padding: 10,
                  borderRadius: 8,
                  border: r.id === selectedRunId ? "2px solid #0366d6" : "1px solid #ccc",
                  background: "white",
                  cursor: "pointer",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
                  <strong>Run #{r.id}</strong>
                  <span style={{ fontSize: 12, color: "#555" }}>{Math.round(r.pass_rate * 100)}%</span>
                </div>
                <div style={{ fontSize: 12, color: "#555" }}>
                  {r.passed_cases}/{r.total_cases} passed, provider={r.provider}
                </div>
              </button>
            ))}
          </div>
        </div>

        <div style={{ border: "1px solid #e5e5e5", borderRadius: 10, padding: 12 }}>
          <h2 style={{ marginTop: 0, fontSize: 16 }}>Run details</h2>
          {!selectedRun && <p>Select a run.</p>}
          {selectedRun && (
            <div style={{ marginBottom: 10, color: "#555" }}>
              <div>
                <strong>Run:</strong> #{selectedRun.id} ({Math.round(selectedRun.pass_rate * 100)}% pass)
              </div>
              <div>
                <strong>Dataset:</strong> {selectedRun.dataset}
              </div>
              <div>
                <strong>Provider:</strong> {selectedRun.provider}
              </div>
              <div>
                <strong>Prompt version:</strong> {selectedRun.prompt_version_id ?? "(none)"}
              </div>
            </div>
          )}

          {details.length > 0 && (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid #eee" }}>
                  <th style={{ padding: "8px 6px" }}>Case</th>
                  <th style={{ padding: "8px 6px" }}>Category</th>
                  <th style={{ padding: "8px 6px" }}>Result</th>
                  <th style={{ padding: "8px 6px" }}>Violations</th>
                </tr>
              </thead>
              <tbody>
                {details.map((d) => (
                  <tr key={d.case_id} style={{ borderBottom: "1px solid #f2f2f2" }}>
                    <td style={{ padding: "8px 6px" }}>{d.case_id}</td>
                    <td style={{ padding: "8px 6px" }}>{d.category}</td>
                    <td style={{ padding: "8px 6px" }}>
                      {d.passed ? "PASS" : "FAIL"}{" "}
                      <span style={{ fontSize: 12, color: "#777" }}>
                        ({d.error_type ?? "n/a"}, {d.confidence ?? "n/a"})
                      </span>
                    </td>
                    <td style={{ padding: "8px 6px", fontSize: 12, color: d.passed ? "#555" : "crimson" }}>
                      {d.violations.length ? d.violations.join(", ") : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {details.length === 0 && selectedRun && <p>No case results loaded.</p>}
        </div>
      </div>
    </div>
  );
}
