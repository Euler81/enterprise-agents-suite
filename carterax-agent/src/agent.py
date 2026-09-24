"""Orquestador: corre la campaña completa sobre la cartera.

Ciclo por deudor: score → policy → plan → negociación → verify → outreach/escalate.
"""
from __future__ import annotations

import csv
import os
from .scoring import Debtor, risk_score, priority_tier
from .policies import PolicyEngine
from .negotiation import Negotiator
from .escalator import Escalator
from .outreach import OutreachGenerator
from .analytics import CampaignAnalytics


class CarteraXAgent:
    def __init__(self, policy: PolicyEngine | None = None):
        self.policy = policy or PolicyEngine()
        self.escalator = Escalator()
        self.outreach = OutreachGenerator()

    def process_debtor(self, d: Debtor) -> dict:
        score = risk_score(d)
        result: dict = {"debtor_id": d.debtor_id, "name": d.name,
                        "debt": d.debt, "score": score,
                        "tier": priority_tier(score), "outcome": None}

        if d.hostility_signals >= 0.8:  # política dura: no negociar con hostiles
            result["outcome"] = "ESCALATE"
            result["escalation"] = self.escalator.escalate(
                d, "hostilidad previa detectada", [])
        else:
            neg = Negotiator(self.policy, d)
            res = neg.negotiate()
            result["outcome"] = res["outcome"]
            result["trace"] = res["trace"]
            if res["outcome"] == "AGREED":
                offer = res["offer"]
                result["offer"] = offer
                result["recovered_pv"] = d.debt * self.policy.recovery_pv(offer)
                # Verify: doble chequeo del plan cerrado
                ok, motive = self.policy.check_offer(offer)
                result["verify"] = "PASS" if ok else f"FAIL: {motive}"
                if not ok:
                    result["outcome"] = "ESCALATE"
                    result["escalation"] = self.escalator.escalate(d, motive, res["trace"])
            elif res["outcome"] == "ESCALATE":
                result["escalation"] = self.escalator.escalate(
                    d, res["reason"], res["trace"])
            else:
                result["message"] = self.outreach.message(d, None)
                result["recovered_pv"] = 0.0

        if result["outcome"] == "ESCALATE":
            result["recovered_pv"] = 0.0
        return result

    def run_campaign(self, debtors: list[Debtor]) -> dict:
        results = [self.process_debtor(d) for d in debtors]
        metrics = CampaignAnalytics().summarize(results)
        _export_csv(results)
        return {"results": results, "metrics": metrics}


def _export_csv(results: list[dict], path: str = "output/campaign_report.csv") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["debtor_id", "name", "debt", "score", "tier",
                    "outcome", "discount", "installments", "recovered_pv", "verify"])
        for r in results:
            offer = r.get("offer", {})
            w.writerow([r["debtor_id"], r["name"], r["debt"], r["score"],
                        r["tier"], r["outcome"], offer.get("discount", ""),
                        offer.get("installments", ""), r.get("recovered_pv", 0),
                        r.get("verify", "")])
