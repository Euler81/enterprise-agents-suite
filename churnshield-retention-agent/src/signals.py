"""Señales de churn → score 0-1 (explicable)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Customer:
    customer_id: str
    name: str
    segment: str              # consumer | sme | enterprise
    monthly_fee: float
    months_tenure: int
    usage_trend: float        # -1 (cae fuerte) .. +1 (crece)
    support_tickets_90d: int
    competitor_discount: float  # 0-0.4, oferta activa de competencia
    payment_delays_6m: int


def churn_score(c: Customer) -> tuple[float, list[str]]:
    score, reasons = 0.0, []
    u = max(0.0, -c.usage_trend) * 0.35
    if u > 0.1: reasons.append("caída de uso")
    score += u
    t = min(0.25, c.support_tickets_90d * 0.06)
    if t > 0.05: reasons.append("quejas frecuentes")
    score += t
    comp = c.competitor_discount * 0.6
    if comp > 0.1: reasons.append("oferta activa de competencia")
    score += comp
    d = min(0.15, c.payment_delays_6m * 0.05)
    if d > 0.04: reasons.append("retrasos de pago")
    score += d
    return min(1.0, round(score, 3)), reasons
