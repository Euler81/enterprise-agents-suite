"""Scoring explicable de fraude (reglas versionables)."""
from __future__ import annotations

from .policy import Claim, Policy


def fraud_score(policy: Policy, claim: Claim) -> tuple[float, list[str]]:
    """Devuelve (score 0-1, señales activadas). Toda señal es explicable."""
    score, signals = 0.0, []
    amount_ratio = claim.amount / max(policy.coverage_limit, 1)

    if amount_ratio > 0.75:
        score += 0.35
        signals.append("reclamo cercano al límite de suma asegurada")
    if claim.days_after_start < 60:
        score += 0.25
        signals.append("siniestro muy próximo al alta de póliza")
    if claim.prior_claims >= 2:
        score += min(0.25, claim.prior_claims * 0.08)
        signals.append("historial siniestral repetido")
    if claim.inconsistency_flags > 0:
        score += min(0.15, claim.inconsistency_flags * 0.05)
        signals.append("inconsistencias en la denuncia")

    return min(1.0, round(score, 3)), signals
