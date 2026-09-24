"""Scoring explicable 0-1000 con reason codes (reglas versionables)."""
from __future__ import annotations

from .applicant import Applicant


def credit_score(a: Applicant) -> tuple[int, list[str], list[str]]:
    """Devuelve (score, reason codes positivos, reason codes negativos)."""
    pos, neg = [], []
    score = 250.0  # base

    rev = min(250.0, a.annual_revenue * 250 / 2_000_000)
    score += rev
    if rev >= 200: pos.append("REVENUE_STRONG")
    elif rev < 60: neg.append("REVENUE_LOW")

    yrs = min(150.0, a.years_in_business * 30)
    score += yrs
    if yrs >= 120: pos.append("TRACK_RECORD_LONG")
    elif yrs < 30: neg.append("COMPANY_YOUNG")

    inv = min(150.0, a.monthly_invoices * 15)
    score += inv
    if inv >= 105: pos.append("INVOICE_FLOW_HEALTHY")

    if a.bank_debt_ratio > 0.6:
        score -= 150
        neg.append("HIGH_LEVERAGE")
    elif a.bank_debt_ratio < 0.3:
        score += 50
        pos.append("LOW_LEVERAGE")

    if a.bounced_payments_12m > 0:
        penalty = min(200.0, a.bounced_payments_12m * 100)
        score -= penalty
        neg.append("PAYMENT_INCIDENTS")

    return int(max(0, min(1000, round(score)))), pos, neg
