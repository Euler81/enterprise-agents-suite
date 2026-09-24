"""Orquestador: PLANNER (RFQ) → EXECUTE (scoring) → NEGOTIATE → VERIFY."""
from __future__ import annotations

from .rfq import RFQ
from .quotes import collect_quotes
from .evaluate import score_quotes
from .negotiate import counter_offer

MIN_SAVINGS_PCT = 0.03
MIN_SCORE_GAP = 0.05


class ProcureBot:
    def procure(self, rfq: RFQ) -> dict:
        trace = [{"phase": "planner", "result": "RFQ {} x{} — presupuesto ${:,.0f}".format(
            rfq.item, rfq.quantity, rfq.budget)}]

        quotes = collect_quotes(rfq)
        ranked = score_quotes(quotes)
        best, best_score = ranked[0]
        second_score = ranked[1][1]
        trace.append({"phase": "execute",
                      "result": "5 cotizaciones; mejor: {} (score {:.3f})".format(
                          best.supplier, best_score)})

        # Negotiate
        final_price, negotiated = counter_offer(best)
        savings = rfq.budget - final_price
        savings_pct = savings / rfq.budget
        trace.append({"phase": "negotiate", "result": "{} → ${:,.0f} (ahorro {:.1%})".format(
            "contraoferta aceptada" if negotiated else "proveedor sin margen",
            final_price, savings_pct)})

        # Verify
        if savings_pct < MIN_SAVINGS_PCT:
            return {"outcome": "ESCALATE", "reason": "ahorro insuficiente ({:.1%} < 3%)".format(savings_pct),
                    "trace": trace}
        if best_score - second_score < MIN_SCORE_GAP:
            return {"outcome": "ESCALATE", "reason": "empate técnico entre finalistas",
                    "trace": trace}

        return {"outcome": "AWARDED", "supplier": best.supplier,
                "price": final_price, "savings_pct": round(savings_pct, 4),
                "score": best_score, "negotiated": negotiated, "trace": trace}
