"""Genera 200 siniestros sintéticos + pólizas. Uso: python scripts/generate_claims.py"""
import csv, os, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def main(n=200, seed=7):
    random.seed(seed)
    os.makedirs("data", exist_ok=True)
    with open("data/policies.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["policy_id", "coverage_limit", "deductible_pct",
                    "depreciation_per_year", "waiting_days", "max_auto_settle"])
        for i in range(1, 41):
            w.writerow([f"P-{i:03d}", random.choice([10e6, 20e6, 50e6]),
                        random.choice([0.10, 0.15, 0.20]),
                        random.choice([0.05, 0.08, 0.10]),
                        random.choice([0, 15, 30]),
                        random.choice([1.5e6, 3e6, 5e6])])
    with open("data/claims.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["claim_id", "policy_id", "amount", "days_after_start",
                    "prior_claims", "inconsistency_flags", "item_age_years"])
        for i in range(1, n + 1):
            w.writerow([f"S-{i:04d}", "P-{:03d}".format(random.randint(1, 40)),
                        round(random.lognormvariate(13, 0.8), 0),
                        random.randint(3, 900),
                        random.choices([0, 1, 2, 3, 5], weights=[55, 20, 12, 8, 5])[0],
                        random.choices([0, 1, 2, 3], weights=[70, 15, 10, 5])[0],
                        round(random.uniform(0, 8), 1)])
    print("✅ {} siniestros y 40 pólizas generados en data/".format(n))

if __name__ == "__main__":
    main()
