"""Demo end-to-end. Uso: python examples/demo.py"""
import csv, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.signals import Customer
from src.retention import RetentionEngine

def load():
    if not Path("data/customers.csv").exists():
        subprocess.run([sys.executable, "scripts/generate_customers.py"], check=True)
    out = []
    with open("data/customers.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(Customer(r["customer_id"], r["name"], r["segment"],
                float(r["monthly_fee"]), int(r["months_tenure"]),
                float(r["usage_trend"]), int(r["support_tickets_90d"]),
                float(r["competitor_discount"]), int(r["payment_delays_6m"])))
    return out

if __name__ == "__main__":
    customers = load()
    engine = RetentionEngine()
    results = [(c, engine.process(c)) for c in customers]

    offers = [(c, r) for c, r in results if r["outcome"] == "OFFER"]
    vip = [(c, r) for c, r in results if r["outcome"] == "ESCALATE_VIP"]
    passive = [r for _, r in results if r["outcome"] == "PASSIVE"]

    print("=" * 64)
    print("📉 ChurnShield — Demo de campaña de retención")
    print("=" * 64)
    print()
    print("🎁 OFERTAS LANZADAS (muestra de 3):")
    for c, r in offers[:3]:
        o = r["offer"]
        print("   {:<22} churn {:.0%} → {}% dto. | EV +${:,.0f} vs costo ${:,.0f}".format(
            c.name, r["churn"], int(o["discount"]*100), o["gain"], o["cost"]))
    print()
    print("👔 ESCALADOS VIP (muestra de 2):")
    for c, r in vip[:2]:
        print("   {:<22} churn {:.0%} → {}".format(c.name, r["churn"], r["reason"]))
    print()
    n = len(results)
    print("📊 MÉTRICAS")
    print("-" * 64)
    print("   Clientes analizados:    {}".format(n))
    print("   En riesgo (churn≥25%):  {}".format(sum(1 for _, r in results if r["churn"] >= 0.25)))
    print("   Ofertas rentables:      {} ({:.0%})".format(len(offers), len(offers)/n))
    print("   Escalados VIP:          {}".format(len(vip)))
    print("   Pasivos (no rentable):  {}".format(len(passive)))
    print("   EV total de ofertas:    +${:,.0f}/año".format(sum(r["offer"]["gain"]-r["offer"]["cost"] for _, r in offers)))
