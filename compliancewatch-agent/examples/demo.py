"""Demo: escanea toda la base normativa. Uso: python examples/demo.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.agent import ComplianceAgent

if __name__ == "__main__":
    print("=" * 64)
    print("⚖️  ComplianceWatch — Escaneo regulatorio")
    print("=" * 64)
    results = ComplianceAgent().scan_all()
    print()
    for r in results:
        icon = {"ESCALATE": "🚨", "ACTION_PLAN": "📋", "NO_IMPACT": "✅"}[r["outcome"]]
        print("{} {} [{}] impacto {}".format(icon, r["norm_id"], r["outcome"], r["impact"]))
        print("   → {}".format(r["action"]))
    n_esc = sum(1 for r in results if r["outcome"] == "ESCALATE")
    print()
    print("📊 {} normas: {} planes de acción, {} escalados".format(
        len(results), sum(1 for r in results if r["outcome"] == "ACTION_PLAN"), n_esc))
