"""LTV del cliente y verificación de rentabilidad de ofertas."""
from __future__ import annotations

MARGIN = 0.35          # margen bruto sobre la facturación
MAX_DISCOUNT = 0.20    # tope duro de descuento
OFFERS = [0.0, 0.05, 0.10, 0.15, 0.20]


def ltv(monthly_fee: float, months_tenure: int) -> float:
    """Valor de vida: facturación × margen × meses esperados restantes."""
    expected_months = min(36, 12 + months_tenure * 0.5)
    return monthly_fee * MARGIN * expected_months


def stay_probability(churn: float, discount: float) -> float:
    """Probabilidad de permanencia tras la oferta (el descuento reduce churn)."""
    return min(0.97, max(0.05, 1 - churn * (1 - 2.5 * discount)))
