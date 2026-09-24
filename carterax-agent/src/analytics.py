"""Métricas de campaña: qué tan bien le fue al agente."""
from __future__ import annotations

from collections import Counter


class CampaignAnalytics:
    def summarize(self, results: list[dict]) -> dict:
        c = Counter(r["outcome"] for r in results)
        total_debt = sum(r["debt"] for r in results)
        recovered = sum(r.get("recovered_pv", 0) for r in results)

        agreed = c.get("AGREED", 0)
        human_cost_per_call = 8.0       # USD costo gestor humano por contacto
        agent_cost = len(results) * 0.05  # costo marginal del agente

        savings = (c.get("ESCALATE", 0) * human_cost_per_call) - agent_cost

        return {
            "debtors": len(results),
            "agreed": agreed,
            "escalated": c.get("ESCALATE", 0),
            "passive": c.get("PASSIVE", 0),
            "agreement_rate": round(agreed / len(results), 3) if results else 0,
            "total_debt": round(total_debt, 0),
            "recovered_pv": round(recovered, 0),
            "recovery_rate": round(recovered / total_debt, 3) if total_debt else 0,
            "estimated_human_hours_saved": round(
                (len(results) - c.get("ESCALATE", 0)) * 12 / 60, 1),
            "estimated_savings_usd": round(savings, 0),
        }
