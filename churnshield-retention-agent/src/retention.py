"""Motor de retención: PLANNER (score) → EXECUTE (oferta) → VERIFY (rentabilidad)."""
from __future__ import annotations

from .signals import Customer, churn_score
from .ltv import ltv, stay_probability, OFFERS, MAX_DISCOUNT

VIP_CHURN_THRESHOLD = 0.45


class RetentionEngine:
    def __init__(self, margin: float = 0.35):
        self.margin = margin

    def process(self, c: Customer) -> dict:
        trace = []
        churn, reasons = churn_score(c)
        trace.append({"phase": "planner", "result": "churn={:.2f} ({})".format(
            churn, ", ".join(reasons) or "sin señales")})

        if churn < 0.25:
            return {"outcome": "NO_ACTION", "churn": churn, "trace": trace}
        if c.segment == "enterprise" and churn > VIP_CHURN_THRESHOLD:
            return {"outcome": "ESCALATE_VIP", "churn": churn,
                    "reason": "cliente enterprise en riesgo crítico", "trace": trace}

        value = ltv(c.monthly_fee, c.months_tenure)
        annual_value = c.monthly_fee * 12 * self.margin

        # Elegir la oferta más barata que logra permanencia esperada rentable
        chosen = None
        for d in OFFERS:
            if d > MAX_DISCOUNT:
                continue
            p_stay = stay_probability(churn, d)
            gain = p_stay * annual_value
            cost = c.monthly_fee * 12 * d * p_stay
            trace.append({"phase": "execute", "offer": d,
                          "p_stay": round(p_stay, 2),
                          "gain": round(gain, 0), "cost": round(cost, 0)})
            if gain > cost and p_stay >= 0.85:
                chosen = {"discount": d, "p_stay": p_stay, "gain": gain, "cost": cost}
                break

        if not chosen:
            return {"outcome": "PASSIVE", "churn": churn,
                    "reason": "ninguna oferta rentable", "trace": trace}

        # VERIFY final
        if chosen["gain"] <= chosen["cost"]:
            return {"outcome": "PASSIVE", "churn": churn,
                    "reason": "oferta no rentable", "trace": trace}

        return {"outcome": "OFFER", "churn": churn, "ltv": value,
                "offer": chosen, "trace": trace}
