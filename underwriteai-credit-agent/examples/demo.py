"""Demo end-to-end. Uso: python examples/demo.py"""
import csv, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.applicant import Applicant
from src.decision import CreditAgent

def load():
    if not Path("data/applicants.csv").exists():
        subprocess.run([sys.executable, "scripts/generate_applicants.py"], check=True)
    out = []
    with open("data/applicants.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(Applicant(r["applicant_id"], r["company"],
                float(r["annual_revenue"]), int(r["years_in_business"]),
                int(r["monthly_invoices"]), float(r["bank_debt_ratio"]),
                int(r["bounced_payments_12m"]), float(r["requested_amount"])))
    return out

if __name__ == "__main__":
    apps = load()
    agent = CreditAgent()
    results = [agent.evaluate(a) for a in apps]
    ap = [r for r in results if r["outcome"] == "APPROVE"]
    rf = [r for r in results if r["outcome"] == "REFER"]
    dc = [r for r in results if r["outcome"] == "DECLINE"]

    print("=" * 64)
    print("🏦 UnderwriteAI — Evaluación crediticia PyME")
    print("=" * 64)
    print()
    print("✅ APROBADOS (muestra de 2):")
    for r in ap[:2]:
        print("   score {} → tasa sugerida {:.0%} | motivos: {}".format(
            r["score"], r["suggested_rate"], ", ".join(r["positive_reasons"])))
    print()
    print("🙋 DERIVADOS (muestra de 2):")
    for r in rf[:2]:
        print("   score {} → {}".format(r["score"], r["motive"]))
    print()
    print("❌ DECLINADOS (muestra de 2):")
    for r in dc[:2]:
        print("   score {} → {} | {}".format(r["score"], r["motive"],
                                             ", ".join(r["negative_reasons"])))
    n = len(results)
    print()
    print("📊 MÉTRICAS")
    print("-" * 64)
    print("   Solicitudes:     {}".format(n))
    print("   Aprobación auto: {} ({:.0%})".format(len(ap), len(ap)/n))
    print("   Derivados:       {} ({:.0%})".format(len(rf), len(rf)/n))
    print("   Declinados:      {} ({:.0%})".format(len(dc), len(dc)/n))
