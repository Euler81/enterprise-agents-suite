"""Genera 250 clientes sintéticos. Uso: python scripts/generate_customers.py"""
import csv, os, random

def main(n=250, seed=11):
    random.seed(seed)
    os.makedirs("data", exist_ok=True)
    FIRST = ["Martín","Lucía","Sofía","Julián","Camila","Facundo","Valeria","Nicolás"]
    LAST = ["Gómez","Fernández","Acosta","Paredes","Molina","Sosa","Ríos","Navarro"]
    SEG = ["consumer"]*70 + ["sme"]*25 + ["enterprise"]*5
    with open("data/customers.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["customer_id","name","segment","monthly_fee","months_tenure",
                    "usage_trend","support_tickets_90d","competitor_discount","payment_delays_6m"])
        for i in range(1, n+1):
            w.writerow([f"C-{i:04d}", random.choice(FIRST)+" "+random.choice(LAST),
                        random.choice(SEG),
                        round(random.uniform(800, 9000) if random.random()<.9 else random.uniform(9000, 45000), 0),
                        random.randint(1, 60),
                        round(random.uniform(-1, 1), 2),
                        random.choices([0,1,2,3,5], weights=[50,25,12,8,5])[0],
                        random.choice([0,0,0,0.10,0.20,0.30]),
                        random.choices([0,1,2,3], weights=[60,22,12,6])[0]])
    print("✅ {} clientes generados en data/customers.csv".format(n))

if __name__ == "__main__":
    main()
