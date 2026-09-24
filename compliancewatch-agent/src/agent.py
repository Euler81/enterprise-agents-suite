"""Orquestador: PLANNER (interpretar norma) → EXECUTE (mapear impacto)
→ VERIFY (reglas de escalado) → reporte/acción."""
from __future__ import annotations

from .norms import Norm, NORM_DB
from .impact import affected_processes, impact_score

CRITICAL_DAYS = 15


class ComplianceAgent:
    def __init__(self):
        self.trace: list[dict] = []

    def process_norm(self, norm: Norm) -> dict:
        trace = [{"phase": "planner", "result": "{} ({}) — severidad {}".format(
            norm.norm_id, norm.issuer, norm.severity)}]

        processes = affected_processes(norm)
        score = impact_score(norm, processes)
        trace.append({"phase": "execute", "result": "{} procesos afectados, impacto {}".format(
            len(processes), score)})

        # VERIFY
        if norm.severity == "critica" or norm.deadline_days < CRITICAL_DAYS:
            outcome = "ESCALATE"
            action = ("Escalar a compliance/legal: norma crítica o plazo <{} días. "
                      "Revisión humana inmediata requerida.").format(CRITICAL_DAYS)
        elif not processes:
            outcome = "NO_IMPACT"
            action = "Sin procesos internos en el área; registrar y seguir monitoreando."
        else:
            outcome = "ACTION_PLAN"
            owners = sorted({p.owner for p in processes})
            action = ("Notificar a {}: actualizar '{}' (plazo: {} días). "
                      "Impacto estimado: {}.").format(
                ", ".join(owners), norm.title, norm.deadline_days, score)

        result = {"norm_id": norm.norm_id, "outcome": outcome, "impact": score,
                  "affected": [p.name for p in processes], "action": action,
                  "trace": trace}
        self.trace.append(result)
        return result

    def scan_all(self) -> list[dict]:
        return [self.process_norm(n) for n in NORM_DB]
