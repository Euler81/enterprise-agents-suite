"""Pronóstico determinístico: demanda base ajustada por tendencia."""
from __future__ import annotations

from .product import Product


def daily_forecast(p: Product) -> float:
    """Demanda diaria esperada (trend mensual prorrateado a días)."""
    adjusted = p.avg_daily_demand * (1 + p.demand_trend)
    return max(0.1, adjusted)


def forecast_period(p: Product, days: int) -> float:
    return daily_forecast(p) * days
