from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class EvalRunRead(BaseModel):
    id: int
    provider: str
    dataset: str
    total_cases: int
    passed_cases: int
    pass_rate: float
    prompt_version_id: Optional[int] = None


class EvalCaseResultRead(BaseModel):
    case_id: str
    category: str
    passed: bool
    error_type: Optional[str] = None
    confidence: Optional[str] = None
    violations: List[str]
