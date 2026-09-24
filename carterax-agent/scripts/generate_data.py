"""Genera una cartera sintética realista (300 deudores) en CSV.

Correr desde la raíz:  python scripts/generate_data.py
"""
import csv
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SEGMENTS = ["consumer"] * 70 + ["sme"] * 25 + ["enterprise"] * 5
FIRST = ["Martín", "Lucía", "Sofía", "Julián", "Camila", "Facundo", "Valeria",
         "Nicolás", "Antonella", "Sebastián", "Florencia", "Agustín", "Micaela",
         "Rodrigo", "Paula", "Ignacio", "Daniela", "Gonzalo", "Mercedes", "Tomás"]
LAST = ["Gómez", "Fernández", "Acosta", "Paredes", "Molina", "Sosa", "Ríos",
        "Navarro", "Delgado", "Vega", "Castro", "Ortiz", "Silva", "Núñez",
        "Ibáñez", "Morales", "Cabrera", "Ferreyra", "Ponce", "Villalba"]
DOMAINS = {"consumer": "", "sme": " (PyME)", "enterprise": " SA"}


def main(n: int = 300, seed: int = 42) -> None:
    random.seed(seed)
    os.makedirs("data", exist_ok=True)
    path = "data/cartera_sintetica.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["debtor_id", "name", "debt", "days_past_due", "segment",
                    "prior_promises", "avg_payment_delay_days",
                    "contactability", "hostility_signals"])
        for i in range(1, n + 1):
            seg = random.choice(SEGMENTS)
            debt = round(random.lognormvariate(9.5, 0.9), 0)
            debt = min(debt, 2_500_000)
            w.writerow([
                f"D-{i:04d}",
                f"{random.choice(FIRST)} {random.choice(LAST)}{DOMAINS[seg]}",
                debt,
                random.randint(5, 170),
                seg,
                random.choices([0, 1, 2, 3, 4], weights=[40, 25, 20, 10, 5])[0],
                random.randint(0, 80),
                round(random.betavariate(4, 3), 2),
                round(max(0, random.gauss(0.25, 0.25)), 2),
            ])
    print(f"✅ {n} deudores generados en {path}")


if __name__ == "__main__":
    main()
