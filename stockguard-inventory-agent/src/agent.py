"""Orquestador: PLANNER (forecast) → EXECUTE (reorder) → VERIFY (mandato)."""
from __future__ import annotations

from .product import Product
from .reorder import suggest_order, MAX_DAYS_COVER

MAX_AUTO_ORDER = 500_000   # mandato económico del agente


class StockGuard:
    def __init__(self, max_auto_order: float = MAX_AUTO_ORDER):
        self.max_auto_order = max_auto_order
        self.trace: list[dict] = []

    def review_product(self, p: Product) -> dict:
        d = suggest_order(p)
        trace = [{"phase": "planner", "result": "demanda/día {:.1f}".format(d["reorder_point"] / (p.lead_time_days * 1.25) if p.lead_time_days else 0)},
                 {"phase": "execute", "result": "ROP {:.0f} u. → sugerido {} u. (${:,.0f})".format(
                     d["reorder_point"], d["suggested_qty"], d["order_value"])}]

        if d["suggested_qty"] == 0:
            return {"outcome": "OK", **d, "trace": trace}
        if d["days_of_cover_after"] > MAX_DAYS_COVER:
            return {"outcome": "SKIP", "reason": "sobreinventario: {} días de cobertura".format(
                int(d["days_of_cover_after"])), **d, "trace": trace}
        if d["order_value"] > self.max_auto_order:
            return {"outcome": "ESCALATE", "reason": "orden ${:,.0f} supera mandato".format(
                d["order_value"]), **d, "trace": trace}
        return {"outcome": "ORDER", **d, "trace": trace}

    def run_catalog(self, products: list[Product]) -> list[dict]:
        return [self.review_product(p) for p in products]
