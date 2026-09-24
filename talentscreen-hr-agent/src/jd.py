"""Job description con skills ponderadas."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class JobDescription:
    title: str
    required_skills: dict   # skill -> peso (suma 1.0 dentro de skills)
    min_years: int
    salary_min: float
    salary_max: float

    @property
    def total_skill_weight(self) -> float:
        return sum(self.required_skills.values()) or 1.0
