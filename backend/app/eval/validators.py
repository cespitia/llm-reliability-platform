from __future__ import annotations

from typing import List

from app.eval.types import ExpectedConstraints
from app.llm.schemas import IncidentSummary


def validate_summary(summary: IncidentSummary, expected: ExpectedConstraints) -> List[str]:
    """
    Returns a list of violation strings. Empty list means pass.
    """
    violations: List[str] = []

    # Combine searchable text from model output
    haystack = " ".join(
        [
            summary.summary,
            summary.root_cause,
            summary.error_type,
            " ".join(summary.next_steps),
            " ".join(summary.citations),
            summary.confidence,
        ]
    )

    for token in expected.must_contain:
        if token not in haystack:
            violations.append(f"must_contain_missing:{token}")

    for token in expected.forbidden_contain:
        if token in haystack:
            violations.append(f"forbidden_contain_present:{token}")

    if len(summary.next_steps) < expected.min_next_steps:
        violations.append(
            f"min_next_steps_failed:expected>={expected.min_next_steps},got={len(summary.next_steps)}"
        )

    return violations
