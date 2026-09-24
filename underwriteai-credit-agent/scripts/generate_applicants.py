"""Genera 120 solicitudes PyME sintéticas. Uso: python scripts/generate_applicants.py"""
import csv, os, random

def main(n=120, seed=23):
    random.seed(seed)
    os.makedirs("data", exist_ok=True)
    NAMES = ["Metalúrgica Sur", "Logística Rápida", "Alimentos del Valle",
             "Textiles Andina", "Construcciones Sur", "Agroexport SA",
             "Software del Sur", "Distribuidora Córdoba", "Plásticos Patagonia",
             "Gráfica Rioplatense"]
    with open("data/applicants.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["applicant_id","company","annual_revenue","years_in_business",
                    "monthly_invoices","bank_debt_ratio","bounced_payments_12m","requested_amount"])
        for i in range(1, n+1):
            rev = round(random.lognormvariate(16, 0.8), 0)
            w.writerow([f"A-{i:04d}", random.choice(NAMES)+f" {i}",
                        rev, random.randint(1, 25),
                        random.randint(2, 40),
                        round(random.betavariate(3, 4), 2),
                        random.choices([0,1,2,4], weights=[70,18,8,4])[0],
                        round(rev * random.uniform(0.05, 0.30), 0)])
    print("✅ {} solicitudes generadas en data/applicants.csv".format(n))

if __name__ == "__main__":
    main()
