from __future__ import annotations

import re
from typing import List, Tuple

from app.llm.provider import LLMProvider
from app.llm.schemas import IncidentSummary


class FakeProvider(LLMProvider):
    """
    Deterministic provider for local development and CI.
    Uses simple pattern matching to produce a structured IncidentSummary.
    """

    def summarize_incident(self, log_text: str) -> IncidentSummary:
        error_type = self._classify_error_type(log_text)
        citations = self._extract_citations(log_text)

        summary = "CI run failed based on the provided log output."
        root_cause = self._derive_root_cause(log_text, error_type)

        next_steps = self._default_next_steps(error_type, log_text)

        confidence = "low"
        if error_type in {"test_failure", "build_failure", "lint_failure", "dependency_failure"}:
            confidence = "medium"

        return IncidentSummary(
            summary=summary,
            root_cause=root_cause,
            error_type=error_type,
            next_steps=next_steps,
            citations=citations,
            confidence=confidence,
        )

    def _classify_error_type(self, log_text: str) -> str:
        text = log_text.lower()

        if "ruff" in text and ("f401" in text or "lint" in text or "imported but unused" in text):
            return "lint_failure"

        if "eresolve" in text or "unable to resolve dependency tree" in text or "peer react@" in text:
            return "dependency_failure"

        if "ts2322" in text or "tsc" in text or "vite build" in text:
            return "build_failure"

        if "pytest" in text and ("failed" in text or "assertionerror" in text or "timeouterror" in text):
            return "test_failure"

        if "docker build" in text or "returned a non-zero code" in text or "requires a different python" in text:
            return "build_failure"

        return "unknown"

    def _extract_citations(self, log_text: str) -> List[str]:
        citations: List[str] = []

        patterns: List[Tuple[str, str]] = [
            ("pytest", r"\bpytest\b"),
            ("ruff", r"\bruff\b"),
            ("npm", r"\bnpm\b"),
            ("TS2322", r"\bTS2322\b"),
            ("ERESOLVE", r"\bERESOLVE\b"),
            ("AssertionError", r"\bAssertionError\b"),
            ("TimeoutError", r"\bTimeoutError\b"),
        ]

        for label, pat in patterns:
            if re.search(pat, log_text):
                citations.append(label)

        # Extract first file-like reference if present, e.g. tests/test_x.py or src/file.tsx
        file_match = re.search(r"([A-Za-z0-9_\-/]+\.(py|ts|tsx|js|jsx))", log_text)
        if file_match:
            citations.append(file_match.group(1))

        # Remove duplicates while preserving order
        seen = set()
        deduped: List[str] = []
        for c in citations:
            if c not in seen:
                seen.add(c)
                deduped.append(c)

        return deduped[:8]

    def _derive_root_cause(self, log_text: str, error_type: str) -> str:
        if error_type == "test_failure":
            if "AssertionError" in log_text:
                return "A test assertion failed, indicating the code produced an unexpected result."
            if "TimeoutError" in log_text:
                return "An end-to-end test exceeded the timeout threshold."
            return "One or more tests failed during the CI test phase."

        if error_type == "build_failure":
            if "TS2322" in log_text:
                return "TypeScript compilation failed due to a type mismatch."
            if "requires a different Python" in log_text:
                return "Build failed due to an incompatible Python version constraint."
            return "Build step failed due to a compilation or environment issue."

        if error_type == "lint_failure":
            return "Linting failed due to a code quality violation."

        if error_type == "dependency_failure":
            return "Dependency resolution failed due to incompatible package versions."

        return "Root cause could not be determined from the log with high confidence."

    def _default_next_steps(self, error_type: str, log_text: str) -> List[str]:
        if error_type == "test_failure":
            return [
                "Re-run the failing test locally to reproduce the issue.",
                "Inspect the failing assertion or timeout and review recent code changes affecting it.",
                "Add or refine test coverage around the failing behavior to prevent regressions.",
            ][:6]

        if error_type == "build_failure":
            return [
                "Re-run the build locally using the same command shown in the log.",
                "Fix the compilation or environment error (types, toolchain versions, or config).",
                "Pin tool versions in the build environment to reduce future drift.",
            ][:6]

        if error_type == "lint_failure":
            return [
                "Run the linter locally and apply the recommended fix.",
                "Enable auto-fix where safe and add pre-commit hooks to prevent recurrence.",
                "Update lint rules only if justified and documented.",
            ][:6]

        if error_type == "dependency_failure":
            return [
                "Identify the conflicting packages and align versions to satisfy peer dependencies.",
                "Consider using a lockfile update strategy and document supported dependency ranges.",
                "Avoid force flags unless you understand the downstream impact.",
            ][:6]

        return [
            "Scan the log for the first fatal error and reproduce locally.",
            "Add structured logging or more verbose output for better diagnostics.",
        ][:6]
