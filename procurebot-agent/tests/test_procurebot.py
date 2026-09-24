import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.rfq import RFQ
from src.quotes import collect_quotes, Quote
from src.evaluate import score_quotes
from src.negotiate import counter_offer
from src.agent import ProcureBot

class TestEvaluate(unittest.TestCase):
    def test_cheapest_fastest_best_quality_wins(self):
        qs = [Quote("A", 1000, 5, 5.0, 0.95), Quote("B", 2000, 20, 2.5, 0.95),
              Quote("C", 1500, 10, 4.0, 0.95)]
        ranked = score_quotes(qs)
        self.assertEqual(ranked[0][0].supplier, "A")
    def test_scores_bounded(self):
        qs = collect_quotes(RFQ("Test", 1, 1000, 10))
        for _, s in score_quotes(qs):
            self.assertLessEqual(s, 1.0)

class TestNegotiate(unittest.TestCase):
    def test_counter_never_below_floor(self):
        q = Quote("X", 1000, 5, 4.0, 0.96)   # piso 960 > pedido 950
        price, neg = counter_offer(q)
        self.assertEqual(price, 1000)
        self.assertFalse(neg)
    def test_flexible_supplier_negotiates(self):
        q = Quote("Y", 1000, 5, 4.0, 0.94)   # piso 940 < pedido 950
        price, neg = counter_offer(q)
        self.assertEqual(price, 950)
        self.assertTrue(neg)

class TestAgent(unittest.TestCase):
    def test_award_is_audited_and_cheaper(self):
        r = ProcureBot().procure(RFQ("Monitores", 30, 12_000_000, 15))
        self.assertIn(r["outcome"], ("AWARDED", "ESCALATE"))
        if r["outcome"] == "AWARDED":
            self.assertLess(r["price"], 12_000_000)
            self.assertGreaterEqual(r["savings_pct"], 0.03)

if __name__ == "__main__":
    unittest.main()
