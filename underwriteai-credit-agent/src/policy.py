"""Políticas de producto crediticio."""
from __future__ import annotations

EXPOSURE_PCT = 0.20          # máx. 20% de la facturación anual
APPROVE_THRESHOLD = 600
DECLINE_THRESHOLD = 400


def max_exposure(annual_revenue: float) -> float:
    return annual_revenue * EXPOSURE_PCT
