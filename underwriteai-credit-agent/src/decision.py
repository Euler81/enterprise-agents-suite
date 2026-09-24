"""Orquestador: PLANNER (features) → EXECUTE (score) → VERIFY (política)."""
from __future__ import annotations

from .applicant import Applicant
from .score import credit_score
from .policy import max_exposure, APPROVE_THRESHOLD, DECLINE_THRESHOLD


class CreditAgent:
    def evaluate(self, a: Applicant) -> dict:
        trace = [{"phase": "planner", "result": "solicitud ${:,.0f} — {}".format(
            a.requested_amount, a.company)}]

        score, pos, neg = credit_score(a)
        trace.append({"phase": "execute", "result": "score {} (+{} / -{})".format(
            score, ",".join(pos) or "-", ",".join(neg) or "-")})

        limit = max_exposure(a.annual_revenue)
        within_limit = a.requested_amount <= limit
        trace.append({"phase": "verify", "result": "exposición máx ${:,.0f} → {}".format(
            limit, "OK" if within_limit else "EXCEDE")})

        if score >= APPROVE_THRESHOLD and within_limit:
            rate = round(0.28 + (1000 - score) * 0.0004, 2)  # pricing por riesgo
            return {"outcome": "APPROVE", "score": score, "limit": limit,
                    "suggested_rate": rate, "positive_reasons": pos,
                    "negative_reasons": neg, "trace": trace}
        if score < DECLINE_THRESHOLD or not within_limit:
            reason = "score insuficiente" if score < DECLINE_THRESHOLD else "exposición excede política"
            return {"outcome": "DECLINE", "score": score, "motive": reason,
                    "negative_reasons": neg, "trace": trace}
        return {"outcome": "REFER", "score": score, "limit": limit,
                "negative_reasons": neg, "positive_reasons": pos,
                "motive": "zona gris: decisión de analista", "trace": trace}
