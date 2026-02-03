import type { EvalCaseResult, EvalRun, Prompt, PromptVersion } from "./types";

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  // Prompts
  listPrompts: async (): Promise<Prompt[]> => json(await fetch("/api/prompts")),
  createPrompt: async (name: string, description: string): Promise<Prompt> =>
    json(
      await fetch("/api/prompts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description }),
      })
    ),

  // Versions
  listVersions: async (promptId: number): Promise<PromptVersion[]> =>
    json(await fetch(`/api/prompts/${promptId}/versions`)),
  createVersion: async (
    promptId: number,
    template: string,
    model: string,
    temperature: number
  ): Promise<PromptVersion> =>
    json(
      await fetch(`/api/prompts/${promptId}/versions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ template, model, temperature }),
      })
    ),

  // Evals
  runEval: async (promptVersionId?: number): Promise<EvalRun> => {
    const qs = promptVersionId ? `?prompt_version_id=${promptVersionId}` : "";
    return json(await fetch(`/api/evals/run${qs}`, { method: "POST" }));
  },
  listRuns: async (): Promise<EvalRun[]> => json(await fetch("/api/evals/runs")),
  getRunDetails: async (runId: number): Promise<EvalCaseResult[]> =>
    json(await fetch(`/api/evals/runs/${runId}`)),
};
