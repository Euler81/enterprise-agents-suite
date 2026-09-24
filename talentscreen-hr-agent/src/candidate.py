"""Candidato."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Candidate:
    candidate_id: str
    name: str
    group: str               # demographic group (auditoría)
    skills: list
    years_experience: int
    salary_expectation: float
