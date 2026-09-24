"""Scoring de riesgo: prioriza deudores por probabilidad de recuperación.

Modelo explicable basado en reglas ponderadas (versionable a ML real).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Debtor:
    debtor_id: str
    name: str
    debt: float
    days_past_due: int
    segment: str              # "consumer" | "sme" | "enterprise"
    prior_promises: int       # promesas de pago incumplidas previas
    avg_payment_delay_days: int
    contactability: float     # 0-1, historial de respuesta a contactos
    hostility_signals: float  # 0-1, quejas previas / tono en últimos contactos


# Pesos explicables (suman 1.0)
WEIGHTS = {
    "recency": 0.30,        # a más días de atraso, menor score
    "prior_promises": 0.25, # incumplimientos previos castigan
    "delay": 0.20,          # mora promedio histórica
    "contactability": 0.15, # respondió antes → más probable
    "segment": 0.10,        # enterprise paga más consistentemente
}

SEGMENT_BONUS = {"enterprise": 1.0, "sme": 0.7, "consumer": 0.4}


def risk_score(d: Debtor) -> float:
    """Devuelve score 0-100 (mayor = mejor candidato a recuperar hoy)."""
    recency = max(0.0, 1.0 - d.days_past_due / 180)
    promises = max(0.0, 1.0 - d.prior_promises / 5)
    delay = max(0.0, 1.0 - d.avg_payment_delay_days / 90)
    contact = d.contactability
    segment = SEGMENT_BONUS.get(d.segment, 0.4)

    score = (WEIGHTS["recency"] * recency
             + WEIGHTS["prior_promises"] * promises
             + WEIGHTS["delay"] * delay
             + WEIGHTS["contactability"] * contact
             + WEIGHTS["segment"] * segment)
    return round(score * 100, 1)


def priority_tier(score: float) -> str:
    if score >= 70: return "P1"   # contactar hoy
    if score >= 45: return "P2"   # esta semana
    return "P3"                   # campaña pasiva (email/SMS)
