"""Demo end-to-end. Uso: python examples/demo.py"""
import csv, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.product import Product
from src.agent import StockGuard

def load():
    if not Path("data/catalog.csv").exists():
        subprocess.run([sys.executable, "scripts/generate_catalog.py"], check=True)
    out = []
    with open("data/catalog.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(Product(r["sku"], r["name"], int(r["stock"]),
                float(r["avg_daily_demand"]), float(r["demand_trend"]),
                int(r["lead_time_days"]), float(r["unit_cost"]), float(r["margin_pct"])))
    return out

if __name__ == "__main__":
    products = load()
    results = StockGuard().run_catalog(products)
    orders = [r for r in results if r["outcome"] == "ORDER"]
    esc = [r for r in results if r["outcome"] == "ESCALATE"]

    print("=" * 64)
    print("📦 StockGuard — Revisión de catálogo")
    print("=" * 64)
    print()
    print("🛒 ÓRDENES AUTOMÁTICAS (muestra de 3):")
    for r in orders[:3]:
        print("   {} → {} u. (${:,.0f}) | cobertura post-orden: {} días".format(
            r["sku"], r["suggested_qty"], r["order_value"], int(r["days_of_cover_after"])))
    print()
    print("🙋 ESCALADAS (muestra de 2):")
    for r in esc[:2]:
        print("   {} → {}".format(r["sku"], r["reason"]))
    print()
    total = sum(r["order_value"] for r in orders)
    print("📊 {} SKU revisados | {} órdenes automáticas | valor total ${:,.0f} | {} escaladas".format(
        len(results), len(orders), total, len(esc)))
