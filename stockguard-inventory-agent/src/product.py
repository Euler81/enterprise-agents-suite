"""SKU del catálogo."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    name: str
    stock: int              # unidades actuales
    avg_daily_demand: float # demanda diaria promedio (histórica)
    demand_trend: float     # -0.1 .. +0.1 variación mensual
    lead_time_days: int     # lead time del proveedor
    unit_cost: float
    margin_pct: float       # margen bruto sobre venta
