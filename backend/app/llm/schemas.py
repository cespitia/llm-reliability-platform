from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

ErrorType = Literal[
    "test_failure",
    "build_failure",
    "lint_failure",
    "dependency_failure",
    "unknown",
]
Confidence = Literal["low", "medium", "high"]


class IncidentSummary(BaseModel):
    summary: str = Field(..., max_length=600)
    root_cause: str = Field(..., max_length=600)
    error_type: ErrorType
    next_steps: List[str] = Field(default_factory=list, max_length=6)
    citations: List[str] = Field(default_factory=list, max_length=8)

    confidence: Confidence
