"""Demo end-to-end. Uso: python examples/demo.py"""
import csv, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.meter import ConsumptionSeries
from src.agent import EnergySaver

def load():
    if not Path("data/consumption.csv").exists():
        subprocess.run([sys.executable, "scripts/generate_consumption.py"], check=True)
    out = []
    with open("data/consumption.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(ConsumptionSeries(r["site"],
                [float(r[f"m{i:02d}"]) for i in range(1, 25)], float(r["contracted_kw"])))
    return out

if __name__ == "__main__":
    sites = load()
    results = [(s, EnergySaver().audit(s)) for s in sites]
    neg = [(s, r) for s, r in results if r["outcome"] == "NEGOTIATE"]
    total_savings = sum(r["dossier"]["savings"]["total"] for _, r in neg)

    print("=" * 64)
    print("⚡ EnergySaver — Auditoría energética")
    print("=" * 64)
    print()
    print("📁 DOSSIERS DE NEGOCIACIÓN (muestra de 2):")
    for s, r in neg[:2]:
        d = r["dossier"]
        print("   {} → ahorro ${:,.0f}/año".format(s.site, d["savings"]["total"]))
        for arg in d["arguments"][:2]:
            print("      • {}".format(arg))
        print()
    print("📊 {} sitios auditados | {} con dossier | ahorro total identificado: ${:,.0f}/año".format(
        len(sites), len(neg), total_savings))
