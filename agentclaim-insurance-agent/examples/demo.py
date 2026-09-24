"""Demo end-to-end de liquidación. Uso: python examples/demo.py"""
import csv, os, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.policy import Policy, Claim
from src.liquidator import AgentClaim

def load():
    if not Path("data/claims.csv").exists():
        subprocess.run([sys.executable, "scripts/generate_claims.py"], check=True)
    policies = {}
    with open("data/policies.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            policies[r["policy_id"]] = Policy(
                r["policy_id"], float(r["coverage_limit"]), float(r["deductible_pct"]),
                float(r["depreciation_per_year"]), int(r["waiting_days"]),
                float(r["max_auto_settle"]))
    claims = []
    with open("data/claims.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            claims.append(Claim(r["claim_id"], r["policy_id"], float(r["amount"]),
                                int(r["days_after_start"]), int(r["prior_claims"]),
                                int(r["inconsistency_flags"]), float(r["item_age_years"])))
    return policies, claims

if __name__ == "__main__":
    policies, claims = load()
    results = [AgentClaim(policies[c.policy_id]).process(c) for c in claims]

    settled = [r for r in results if r["outcome"] == "SETTLED"]
    denied = [r for r in results if r["outcome"] == "DENIED"]
    esc_fraud = [r for r in results if r["outcome"] == "ESCALATE_FRAUD"]
    esc_amount = [r for r in results if r["outcome"] == "ESCALATE_AMOUNT"]

    print("=" * 64)
    print("🛡️  AgentClaim — Demo de liquidación de siniestros")
    print("=" * 64)
    print()
    print("💰 LIQUIDADOS (muestra de 2):")
    for r in settled[:2]:
        print("   " + r["document"])
    print()
    print("🕵️  ESCALADOS POR FRAUDE (muestra de 2):")
    for r in esc_fraud[:2]:
        print("   score {:.2f} → {}".format(r["fraud_score"], "; ".join(r["signals"])))
    print()
    total = sum(c.amount for c in claims)
    paid = sum(r["settlement"] for r in settled)
    print("📊 MÉTRICAS")
    print("-" * 64)
    print("   Siniestros procesados:   {}".format(len(results)))
    print("   Liquidados por agente:   {} ({:.0%})".format(len(settled), len(settled)/len(results)))
    print("   Denegados (póliza):      {}".format(len(denied)))
    print("   Escalados fraude:        {}".format(len(esc_fraud)))
    print("   Escalados por monto:     {}".format(len(esc_amount)))
    print("   Reclamado total:         ${:,.0f}".format(total))
    print("   Pagado (reservas):       ${:,.0f} ({:.0%} del reclamado)".format(paid, paid/max(total,1)))
    print("   Ahorro vs. pago directo: ${:,.0f}".format(total - paid))
