"""Demo: 3 compras simuladas. Uso: python examples/demo.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.rfq import RFQ
from src.agent import ProcureBot

if __name__ == "__main__":
    print("=" * 64)
    print("🛒 ProcureBot — Agente de compras y negociación")
    print("=" * 64)
    bot = ProcureBot()
    rfqs = [RFQ("Notebooks desarrollo", 20, 18_000_000, 20),
            RFQ("Servidores cloud anuales", 8, 45_000_000, 10),
            RFQ("Mobiliario oficina", 60, 9_000_000, 45)]
    total_saved = 0
    for rfq in rfqs:
        r = bot.procure(rfq)
        print()
        print("📦 {} x{} — presupuesto ${:,.0f}".format(rfq.item, rfq.quantity, rfq.budget))
        if r["outcome"] == "AWARDED":
            total_saved += rfq.budget - r["price"]
            print("   ✅ Adjudicado: {} — ${:,.0f} (ahorro {:.1%}, score {:.3f})".format(
                r["supplier"], r["price"], r["savings_pct"], r["score"]))
        else:
            print("   🙋 Escalado a compras: {}".format(r["reason"]))
    print()
    print("💰 Ahorro total capturado: ${:,.0f}".format(total_saved))
