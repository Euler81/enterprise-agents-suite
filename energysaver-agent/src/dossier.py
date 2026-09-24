"""Dossier de negociación con la distribuidora."""
from __future__ import annotations

from .meter import ConsumptionSeries
from .anomaly import estimate_savings


def build_dossier(cs: ConsumptionSeries) -> dict:
    est = estimate_savings(cs)
    args = []
    if est["anomalies"]:
        args.append("RECLAMO: {} mes(es) con consumo anómalo (+{:.0f}% vs media). "
                    "Se solicita revisión de medición y devolución de ${:,.0f}.".format(
                        len(est["anomalies"]),
                        max(a["kwh"] for a in est["anomalies"]) / cs.avg * 100 - 100,
                        est["anomaly_saving"]))
    if est["over_contracted_kw"] > 0:
        args.append("RECLASIFICACIÓN: potencia contratada excede el pico medido en "
                    "{:.0f} kW. Solicitud de reducción: ahorro anual ${:,.0f}.".format(
                        est["over_contracted_kw"], est["power_saving"]))
    args.append("DEMANDA RESPONSE: el perfil de consumo permite participar de "
                "programas de reducción con incentivos.")
    return {"savings": est, "arguments": args,
            "annual_consumption_kwh": round(cs.avg * 12, 0),
            "annual_cost": round(cs.avg * 12 * 12.5, 0)}
