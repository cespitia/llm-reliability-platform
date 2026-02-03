import { Layout } from "./components/Layout";
import { EvalsPage } from "./pages/EvalsPage";
import { PromptsPage } from "./pages/PromptsPage";
import { PromptVersionsPage } from "./pages/PromptVersionsPage";

function route() {
  const hash = window.location.hash || "#/";
  if (hash.startsWith("#/evals")) return <EvalsPage />;
  if (hash.startsWith("#/prompts/")) return <PromptVersionsPage />;
  return <PromptsPage />;
}

export default function App() {
  return <Layout>{route()}</Layout>;
}

