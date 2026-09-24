"""Genera catálogo de 60 SKU. Uso: python scripts/generate_catalog.py"""
import csv, os, random

def main(n=60, seed=31):
    random.seed(seed)
    os.makedirs("data", exist_ok=True)
    ITEMS = [("Notebook 15"", 900_000), ("Mouse inalámbrico", 12_000),
             ("Teclado mecánico", 85_000), ("Monitor 27"", 380_000),
             ("Cable USB-C 2m", 6_500), ("Disco SSD 1TB", 210_000),
             ("Silla ergonómica", 450_000), ("Escritorio ajustable", 720_000),
             ("Auriculares headset", 95_000), ("Webcam HD", 55_000)]
    with open("data/catalog.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sku","name","stock","avg_daily_demand","demand_trend",
                    "lead_time_days","unit_cost","margin_pct"])
        for i in range(1, n+1):
            name, cost = random.choice(ITEMS)
            w.writerow([f"SKU-{i:03d}", f"{name} mod.{i}",
                        random.randint(5, 400),
                        round(random.uniform(0.5, 12), 1),
                        round(random.uniform(-0.08, 0.12), 2),
                        random.randint(3, 30),
                        round(cost * random.uniform(0.9, 1.1), 0),
                        round(random.uniform(0.15, 0.45), 2)])
    print("✅ {} SKU generados en data/catalog.csv".format(n))

if __name__ == "__main__":
    main()
