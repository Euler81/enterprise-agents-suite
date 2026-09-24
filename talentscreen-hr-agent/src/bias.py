"""Auditoría de impacto adverso (adverse impact ratio)."""
from __future__ import annotations

ADVERS_IMPACT_THRESHOLD = 0.80


def adverse_impact_audit(scores_by_group: dict[str, list[float]]) -> dict:
    """Ratio = media del grupo con menor media / media del de mayor media.
    Flag si < 0.80 (criterio legal US EEOC, referencia internacional)."""
    means = {g: (sum(s) / len(s) if s else 0.0) for g, s in scores_by_group.items()}
    if len(means) < 2 or max(means.values()) == 0:
        return {"flagged": False, "means": means, "ratio": 1.0}
    hi, lo = max(means.values()), min(means.values())
    ratio = lo / hi
    return {"flagged": ratio < ADVERS_IMPACT_THRESHOLD, "means": means,
            "ratio": round(ratio, 3)}
