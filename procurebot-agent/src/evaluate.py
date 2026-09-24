"""Scoring multi-criterio: precio 50%, plazo 25%, calidad 25%."""
from __future__ import annotations

from .quotes import Quote

W_PRICE, W_LEAD, W_QUALITY = 0.50, 0.25, 0.25


def score_quotes(quotes: list[Quote]) -> list[tuple[Quote, float]]:
    best = min(q.price for q in quotes)
    max_lead = max(q.lead_days for q in quotes) or 1
    scored = []
    for q in quotes:
        p = best / q.price
        l = 1 - (q.lead_days - 1) / max_lead
        g = q.quality / 5.0
        scored.append((q, round(W_PRICE * p + W_LEAD * l + W_QUALITY * g, 4)))
    return sorted(scored, key=lambda x: -x[1])
