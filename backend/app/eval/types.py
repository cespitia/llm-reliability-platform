from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional

ViolationType = Literal["must_contain", "forbidden_contain", "min_next_steps", "schema"]


@dataclass(frozen=True)
class ExpectedConstraints:
    case_id: str
    category: str
    must_contain: List[str]
    forbidden_contain: List[str]
    min_next_steps: int


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    category: str
    passed: bool
    violations: List[str]
    confidence: Optional[str] = None
    error_type: Optional[str] = None
