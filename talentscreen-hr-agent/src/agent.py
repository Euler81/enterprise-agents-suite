"""Orquestador: PLANNER → EXECUTE (match) → VERIFY (umbrales) → AUDIT."""
from __future__ import annotations

from .jd import JobDescription
from .candidate import Candidate
from .match import match_score
from .bias import adverse_impact_audit

SHORTLIST = 0.70
REJECT = 0.40


class TalentScreen:
    def screen(self, jd: JobDescription, candidates: list[Candidate]) -> dict:
        decisions = []
        scores_by_group: dict[str, list[float]] = {}
        for c in candidates:
            score, detail = match_score(jd, c)
            scores_by_group.setdefault(c.group, []).append(score)
            if score >= SHORTLIST:
                outcome = "SHORTLIST"
            elif score < REJECT:
                outcome = "HOLD"     # nunca rechazo automático: hold revisable
            else:
                outcome = "HOLD"
            decisions.append({"candidate_id": c.candidate_id, "name": c.name,
                              "group": c.group, "score": score, "outcome": outcome,
                              **detail})

        audit = adverse_impact_audit(scores_by_group)
        return {"decisions": sorted(decisions, key=lambda d: -d["score"]),
                "audit": audit, "total": len(candidates),
                "shortlisted": sum(1 for d in decisions if d["outcome"] == "SHORTLIST")}
