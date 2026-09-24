"""Genera 150 candidatos sintéticos balanceados. Uso: python scripts/generate_candidates.py"""
import csv, os, random

SKILL_POOL = ["python", "sql", "aws", "docker", "ml", "comunicacion", "liderazgo", "agile"]

def main(n=150, seed=17):
    random.seed(seed)
    os.makedirs("data", exist_ok=True)
    FIRST = ["Martín","Lucía","Sofía","Julián","Camila","Facundo","Valeria","Nicolás","Renata","Bruno"]
    GROUPS = ["A", "B"]
    with open("data/candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["candidate_id","name","group","skills","years_experience",
                    "salary_expectation"])
        for i in range(1, n+1):
            skills = random.sample(SKILL_POOL, random.randint(3, 7))
            w.writerow([f"CV-{i:04d}", random.choice(FIRST)+" "+random.choice(FIRST),
                        random.choice(GROUPS), "|".join(skills),
                        random.randint(0, 12), random.randint(800, 2600) * 1000])
    print("✅ {} candidatos generados en data/candidates.csv".format(n))

if __name__ == "__main__":
    main()
