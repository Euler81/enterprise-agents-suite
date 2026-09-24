"""Escalado a humano: prioriza los casos que un gestor debe atender."""
from __future__ import annotations

from .scoring import Debtor, priority_tier, risk_score


class Escalator:
    """Genera la ficha de escalado para el equipo de cobranza humana."""

    def escalate(self, debtor: Debtor, reason: str, trace: list) -> dict:
        return {
            "debtor_id": debtor.debtor_id,
            "name": debtor.name,
            "debt": debtor.debt,
            "priority": priority_tier(risk_score(debtor)),
            "reason": reason,
            "recommendation": (
                "Llamada humana con capacidad de ofrecer descuento mayor "
                "al permitido por política (fuera de mandato del agente)."
            ),
            "history": [t["reason"] for t in trace],
        }
