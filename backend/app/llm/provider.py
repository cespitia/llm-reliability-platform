from __future__ import annotations

from abc import ABC, abstractmethod

from app.llm.schemas import IncidentSummary


class LLMProvider(ABC):
    @abstractmethod
    def summarize_incident(self, log_text: str) -> IncidentSummary:
        raise NotImplementedError
