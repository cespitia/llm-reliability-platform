from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Prompt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=120)
    description: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=utc_now)


class PromptVersion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt_id: int = Field(index=True, foreign_key="prompt.id")

    version: int = Field(index=True)
    template: str = Field(max_length=8000)

    model: str = Field(default="fake", max_length=60)
    temperature: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=utc_now)


class EvalRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    prompt_version_id: Optional[int] = Field(default=None, index=True, foreign_key="promptversion.id")
    provider: str = Field(default="fake", max_length=40)
    dataset: str = Field(default="datasets/cicd/golden", max_length=200)

    total_cases: int = Field(default=0)
    passed_cases: int = Field(default=0)
    pass_rate: float = Field(default=0.0)

    created_at: datetime = Field(default_factory=utc_now)


class EvalCaseResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    eval_run_id: int = Field(index=True, foreign_key="evalrun.id")

    case_id: str = Field(index=True, max_length=40)
    category: str = Field(max_length=60)
    passed: bool = Field(default=False)

    error_type: Optional[str] = Field(default=None, max_length=40)
    confidence: Optional[str] = Field(default=None, max_length=20)
    violations_json: str = Field(default="[]", max_length=4000)
