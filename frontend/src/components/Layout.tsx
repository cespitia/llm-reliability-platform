import type { ReactNode } from "react";

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div style={{ fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial" }}>
      <div
        style={{
          display: "flex",
          gap: 12,
          padding: 12,
          borderBottom: "1px solid #e5e5e5",
          alignItems: "center",
        }}
      >
        <strong>LLM Reliability Platform</strong>
        <a href="#/" style={{ color: "#0366d6" }}>
          Prompts
        </a>
        <a href="#/evals" style={{ color: "#0366d6" }}>
          Evaluations
        </a>
      </div>
      <div style={{ padding: 16, maxWidth: 1100, margin: "0 auto" }}>{children}</div>
    </div>
  );
}
