"""Punto de reorden y dimensionamiento de la orden."""
from __future__ import annotations

from .product import Product
from .forecast import daily_forecast

SAFETY_FACTOR = 0.25      # stock de seguridad = 25% de la demanda del lead time
TARGET_DAYS = 30          # cobertura objetivo post-reposición
MAX_DAYS_COVER = 90       # tope de sobreinventario


def reorder_point(p: Product) -> float:
    lead = daily_forecast(p) * p.lead_time_days
    return lead * (1 + SAFETY_FACTOR)


def suggest_order(p: Product) -> dict:
    """Devuelve la decisión de reposición para el SKU."""
    rop = reorder_point(p)
    target = daily_forecast(p) * TARGET_DAYS + rop
    qty = max(0, int(target - p.stock))
    return {"sku": p.sku, "reorder_point": round(rop, 1), "suggested_qty": qty,
            "order_value": round(qty * p.unit_cost, 0),
            "days_of_cover_after": round((p.stock + qty) / max(daily_forecast(p), 0.1), 0)}
