import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.product import Product
from src.forecast import daily_forecast
from src.reorder import reorder_point, suggest_order
from src.agent import StockGuard

def prod(**kw):
    base = dict(sku="SKU-1", name="Test", stock=100, avg_daily_demand=5.0,
                demand_trend=0.0, lead_time_days=10, unit_cost=1000, margin_pct=0.3)
    base.update(kw)
    return Product(**base)

class TestForecast(unittest.TestCase):
    def test_positive_demand_trend_raises_forecast(self):
        self.assertGreater(daily_forecast(prod(demand_trend=0.1)),
                           daily_forecast(prod(demand_trend=-0.1)))
    def test_forecast_floor(self):
        self.assertGreaterEqual(daily_forecast(prod(avg_daily_demand=0.0)), 0.1)

class TestReorder(unittest.TestCase):
    def test_rop_includes_safety_stock(self):
        p = prod()
        self.assertGreater(reorder_point(p), p.avg_daily_demand * p.lead_time_days)
    def test_no_order_when_stock_healthy(self):
        d = suggest_order(prod(stock=500))
        self.assertEqual(d["suggested_qty"], 0)

class TestAgent(unittest.TestCase):
    def test_low_stock_generates_order(self):
        r = StockGuard().review_product(prod(stock=5, avg_daily_demand=8.0, unit_cost=100))
        self.assertEqual(r["outcome"], "ORDER")
        self.assertGreater(r["suggested_qty"], 0)
    def test_big_order_escalates(self):
        r = StockGuard().review_product(prod(stock=0, avg_daily_demand=50,
                                             unit_cost=900_000, lead_time_days=5))
        self.assertEqual(r["outcome"], "ESCALATE")
    def test_healthy_product_ok(self):
        self.assertEqual(StockGuard().review_product(prod(stock=400))["outcome"], "OK")

if __name__ == "__main__":
    unittest.main()
