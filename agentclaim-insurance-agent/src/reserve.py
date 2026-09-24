"""Cálculo de reserva: deducible + depreciación, piso del 40%."""
from __future__ import annotations

from .policy import Claim, Policy


def calculate_reserve(policy: Policy, claim: Claim) -> float:
    depreciated = claim.amount * max(0.4, 1 - policy.depreciation_per_year * claim.item_age_years)
    reserve = depreciated * (1 - policy.deductible_pct)
    return round(max(0.0, reserve), 2)
