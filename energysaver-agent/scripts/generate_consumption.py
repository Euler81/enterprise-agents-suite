"""Genera 18 sitios con 24 meses de consumo. Uso: python scripts/generate_consumption.py"""
import csv, os, random

def main(n=18, seed=41):
    random.seed(seed)
    os.makedirs("data", exist_ok=True)
    with open("data/consumption.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["site", "contracted_kw"] + [f"m{i:02d}" for i in range(1, 25)])
        for i in range(1, n + 1):
            base = random.uniform(800, 9000)
            series = [round(base * random.uniform(0.85, 1.15), 0) for _ in range(24)]
            if random.random() < 0.6:   # 60% de los sitios tienen anomalías
                for _ in range(random.randint(1, 3)):
                    series[random.randint(0, 23)] = round(base * random.uniform(1.6, 2.4), 0)
            peak_kw = max(series) / 720
            contracted = round(peak_kw * random.uniform(0.9, 1.9), 0)  # a veces de más
            w.writerow([f"SITE-{i:02d}", contracted] + series)
    print("✅ {} sitios generados en data/consumption.csv".format(n))

if __name__ == "__main__":
    main()
