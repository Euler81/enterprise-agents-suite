"""Orquestador: PLANNER (perfil) → EXECUTE (anomalías) → VERIFY (viabilidad)."""
from __future__ import annotations

from .meter import ConsumptionSeries
from .dossier import build_dossier

MIN_MANAGEMENT_COST = 40_000   # costo mínimo de gestionar la negociación


class EnergySaver:
    def audit(self, cs: ConsumptionSeries) -> dict:
        trace = [{"phase": "planner", "result": "perfil: media {:.0f} kWh/mes, σ {:.0f}, pico {:.0f} kW".format(
            cs.avg, cs.std, cs.contracted_kw)}]
        dossier = build_dossier(cs)
        trace.append({"phase": "execute", "result": "ahorro estimado ${:,.0f}/año".format(
            dossier["savings"]["total"])})

        if dossier["savings"]["total"] < MIN_MANAGEMENT_COST:
            return {"outcome": "REPORT_ONLY", "reason": "ahorro insuficiente para gestionar",
                    "dossier": dossier, "trace": trace}
        return {"outcome": "NEGOTIATE", "dossier": dossier, "trace": trace}
