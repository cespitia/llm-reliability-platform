from __future__ import annotations

from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    name: str = Field(..., max_length=120)
    description: str = Field(default="", max_length=500)


class PromptRead(BaseModel):
    id: int
    name: str
    description: str


class PromptVersionCreate(BaseModel):
    template: str = Field(..., max_length=8000)
    model: str = Field(default="fake", max_length=60)
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)


class PromptVersionRead(BaseModel):
    id: int
    prompt_id: int
    version: int
    template: str
    model: str
    temperature: float
