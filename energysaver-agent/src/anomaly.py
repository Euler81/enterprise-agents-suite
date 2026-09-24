"""Detección estadística de anomalías y estimación de ahorro."""
from __future__ import annotations

from .meter import ConsumptionSeries, TARIFF_KWH_PRICE

SIGMA = 2.0


def detect_anomalies(cs: ConsumptionSeries) -> list[dict]:
    """Meses con consumo > media + 2σ: posibles fugas, picos o errores."""
    threshold = cs.avg + SIGMA * cs.std
    out = []
    for i, kwh in enumerate(cs.monthly_kwh):
        if kwh > threshold:
            out.append({"month": i + 1, "kwh": kwh,
                        "excess_kwh": round(kwh - cs.avg, 0),
                        "excess_cost": round((kwh - cs.avg) * TARIFF_KWH_PRICE, 0)})
    return out


def estimate_savings(cs: ConsumptionSeries) -> dict:
    """Ahorro estimado: anomalías corregibles + potencia contratada de más."""
    anomalies = detect_anomalies(cs)
    anomaly_saving = sum(a["excess_cost"] for a in anomalies) * 0.6  # 60% corregible
    peak_kw = max(cs.monthly_kwh) / 720.0          # kWh/mes → kW aprox (720 h/mes)
    over_kw = max(0.0, cs.contracted_kw - peak_kw * 1.15)
    power_saving = over_kw * 850 * 12              # $/kW-mes contratado
    return {"anomaly_saving": round(anomaly_saving, 0),
            "power_saving": round(power_saving, 0),
            "total": round(anomaly_saving + power_saving, 0),
            "anomalies": anomalies,
            "over_contracted_kw": round(over_kw, 1)}
