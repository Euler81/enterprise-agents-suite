"""Mapeo norma → procesos afectados, con score de impacto."""
from __future__ import annotations

from .norms import Norm
from .inventory import Process, PROCESSES

SEVERITY_WEIGHT = {"baja": 1, "media": 2, "alta": 3, "critica": 5}


def affected_processes(norm: Norm) -> list[Process]:
    return [p for p in PROCESSES if p.area == norm.area]


def impact_score(norm: Norm, processes: list[Process]) -> int:
    """Impacto = peso de severidad × sensibilidad acumulada de procesos."""
    base = SEVERITY_WEIGHT.get(norm.severity, 1)
    sens = sum(p.sensitivity for p in processes) or 1
    return base * sens
