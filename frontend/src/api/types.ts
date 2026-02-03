export type Prompt = {
  id: number;
  name: string;
  description: string;
};

export type PromptVersion = {
  id: number;
  prompt_id: number;
  version: number;
  template: string;
  model: string;
  temperature: number;
};

export type EvalRun = {
  id: number;
  provider: string;
  dataset: string;
  total_cases: number;
  passed_cases: number;
  pass_rate: number;
  prompt_version_id?: number | null;
};

export type EvalCaseResult = {
  case_id: string;
  category: string;
  passed: boolean;
  error_type?: string | null;
  confidence?: string | null;
  violations: string[];
};
