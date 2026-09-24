"""Demo end-to-end: genera cartera, corre campaña, muestra métricas.

Correr desde la raíz:  python examples/demo_campaign.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import CarteraXAgent
from src.scoring import Debtor


def load_portfolio() -> list[Debtor]:
    import csv, subprocess
    data = Path("data/cartera_sintetica.csv")
    if not data.exists():
        subprocess.run([sys.executable, "scripts/generate_data.py"], check=True)
    debtors = []
    with open(data, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            debtors.append(Debtor(
                debtor_id=row["debtor_id"], name=row["name"],
                debt=float(row["debt"]), days_past_due=int(row["days_past_due"]),
                segment=row["segment"], prior_promises=int(row["prior_promises"]),
                avg_payment_delay_days=int(row["avg_payment_delay_days"]),
                contactability=float(row["contactability"]),
                hostility_signals=float(row["hostility_signals"])))
    return debtors


if __name__ == "__main__":
    print("=" * 64)
    print("💼 CarteraX — Demo de campaña de recupero")
    print("=" * 64)

    portfolio = load_portfolio()
    print("\n📂 Cartera cargada: %d deudores\n" % len(portfolio))

    campaign = CarteraXAgent().run_campaign(portfolio)

    agreed = [r for r in campaign["results"] if r["outcome"] == "AGREED"]
    escalated = [r for r in campaign["results"] if r["outcome"] == "ESCALATE"]

    print("🤝 NEGOCIACIONES CERRADAS (muestra de 3):")
    for r in agreed[:3]:
        o = r["offer"]
        print("  • {:<26} deuda ${:>10,.0f} → {} cuota(s), {:.0%} dto., "
              "PV recuperado {:.0%} [{}]".format(
                  r["name"], r["debt"], o["installments"],
                  o["discount"], r["recovered_pv"] / r["debt"], r["verify"]))

    print("\n🙋 ESCALADOS A HUMANO (muestra de 3):")
    for r in escalated[:3]:
        reason = r.get("escalation", {}).get("reason", "")
        print("  • {:<26} deuda ${:>10,.0f} → {}".format(r["name"], r["debt"], reason))

    m = campaign["metrics"]
    print("\n📊 MÉTRICAS DE CAMPAÑA")
    print("-" * 64)
    print("  Acuerdos:                {} ({:.0%})".format(m["agreed"], m["agreement_rate"]))
    print("  Escalados:               %d" % m["escalated"])
    print("  Cartera gestionada:      $%,.0f" % m["total_debt"] if False else
          "  Cartera gestionada:      ${:,.0f}".format(m["total_debt"]))
    print("  Recuperado (PV):         ${:,.0f} ({:.0%} de la cartera)".format(
        m["recovered_pv"], m["recovery_rate"]))
    print("  Horas humanas ahorradas: ~{}".format(m["estimated_human_hours_saved"]))
    print("  Ahorro estimado:         ${:,.0f}".format(m["estimated_savings_usd"]))
    print("\n📄 Reporte completo: output/campaign_report.csv")
