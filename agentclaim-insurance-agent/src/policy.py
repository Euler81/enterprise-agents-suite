"""Pólizas y verificación de cobertura."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Policy:
    policy_id: str
    coverage_limit: float          # suma asegurada máxima
    deductible_pct: float          # deducible sobre el monto asegurado
    depreciation_per_year: float   # depreciación lineal del bien
    waiting_days: int              # período de carencia en días
    max_auto_settle: float         # mandato económico del agente


@dataclass
class Claim:
    claim_id: str
    policy_id: str
    amount: float                  # monto reclamado
    days_after_start: int          # antigüedad de la póliza al siniestro
    prior_claims: int              # siniestros previos del asegurado
    inconsistency_flags: int       # inconsistencias en la denuncia
    item_age_years: float          # antigüedad del bien dañado


def check_coverage(policy: Policy, claim: Claim) -> tuple[bool, str]:
    """Planner paso 1: ¿la póliza cubre este siniestro?"""
    if claim.days_after_start < policy.waiting_days:
        return False, "período de carencia vigente"
    if claim.amount > policy.coverage_limit:
        return False, "monto reclamado supera la suma asegurada"
    return True, "cobertura vigente"
