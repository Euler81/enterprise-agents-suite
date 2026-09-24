"""Orquestador del ciclo PLANNER → EXECUTE → VERIFY con escalado."""
from __future__ import annotations

from .policy import Claim, Policy, check_coverage
from .fraud import fraud_score
from .reserve import calculate_reserve

FRAUD_THRESHOLD = 0.60


class AgentClaim:
    def __init__(self, policy: Policy):
        self.policy = policy

    def process(self, claim: Claim) -> dict:
        trace = []

        # PLANNER: cobertura
        covered, motive = check_coverage(self.policy, claim)
        trace.append({"phase": "planner", "check": "coverage", "result": motive})
        if not covered:
            return {"outcome": "DENIED", "motive": motive, "trace": trace,
                    "settlement": 0.0}

        # EXECUTE: fraude + reserva
        fscore, signals = fraud_score(self.policy, claim)
        reserve = calculate_reserve(self.policy, claim)
        trace.append({"phase": "execute", "check": "fraud_score",
                      "result": "{:.2f} ({})".format(fscore, ", ".join(signals) or "sin señales")})
        trace.append({"phase": "execute", "check": "reserve", "result": "${:,.2f}".format(reserve)})

        # VERIFY: dentro de mandato y sin fraude
        if fscore >= FRAUD_THRESHOLD:
            return {"outcome": "ESCALATE_FRAUD", "fraud_score": fscore,
                    "signals": signals, "trace": trace, "settlement": 0.0}
        if reserve > self.policy.max_auto_settle:
            return {"outcome": "ESCALATE_AMOUNT", "reserve": reserve,
                    "limit": self.policy.max_auto_settle, "trace": trace,
                    "settlement": 0.0}

        doc = ("Liquidación N° {}: se aprueba el pago de ${:,.2f} por el "
               "siniestro {}. Deducible {:.0%} aplicado; depreciación por "
               "antigüedad considerada.").format(
            claim.claim_id, reserve, claim.claim_id, self.policy.deductible_pct)
        return {"outcome": "SETTLED", "settlement": reserve, "fraud_score": fscore,
                "document": doc, "trace": trace}
