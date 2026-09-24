"""Demo end-to-end. Uso: python examples/demo.py"""
import csv, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.jd import JobDescription
from src.candidate import Candidate
from src.agent import TalentScreen

if __name__ == "__main__":
    if not Path("data/candidates.csv").exists():
        subprocess.run([sys.executable, "scripts/generate_candidates.py"], check=True)
    candidates = []
    with open("data/candidates.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            candidates.append(Candidate(r["candidate_id"], r["name"], r["group"],
                r["skills"].split("|"), int(r["years_experience"]),
                float(r["salary_expectation"])))

    jd = JobDescription("Backend Developer SR",
                        {"python": 0.35, "sql": 0.20, "aws": 0.20,
                         "docker": 0.15, "ml": 0.10},
                        min_years=4, salary_min=1_200_000, salary_max=2_400_000)

    result = TalentScreen().screen(jd, candidates)

    print("=" * 64)
    print("🧑‍💼 TalentScreen — Screening:", jd.title)
    print("=" * 64)
    print()
    print("🏆 SHORTLIST (top 5):")
    for d in result["decisions"][:5]:
        print("   {:.0%} {} [{}] | falta: {}".format(
            d["score"], d["name"], d["group"], ", ".join(d["missing_skills"]) or "nada"))
    print()
    a = result["audit"]
    print("⚖️  AUDITORÍA DE SESGO")
    print("-" * 64)
    print("   Medias por grupo: " + ", ".join("{}: {:.1%}".format(g, m) for g, m in a["means"].items()))
    print("   Adverse impact ratio: {:.3f} → {}".format(
        a["ratio"], "🚩 INVESTIGAR" if a["flagged"] else "✅ dentro de umbral"))
    print()
    print("📊 {} CVs | {} en shortlist | {} en hold revisable".format(
        result["total"], result["shortlisted"], result["total"] - result["shortlisted"]))
