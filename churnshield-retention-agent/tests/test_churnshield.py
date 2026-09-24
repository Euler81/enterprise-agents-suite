import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.signals import Customer, churn_score
from src.ltv import ltv, stay_probability
from src.retention import RetentionEngine

def cust(**kw):
    base = dict(customer_id="C-1", name="Test", segment="consumer",
                monthly_fee=2000, months_tenure=24, usage_trend=0.0,
                support_tickets_90d=0, competitor_discount=0.0, payment_delays_6m=0)
    base.update(kw)
    return Customer(**base)

class TestSignals(unittest.TestCase):
    def test_loyal_customer_low_churn(self):
        s, _ = churn_score(cust(usage_trend=0.8))
        self.assertLess(s, 0.2)
    def test_competitor_offer_raises_churn(self):
        s1, _ = churn_score(cust(usage_trend=-0.5))
        s2, _ = churn_score(cust(usage_trend=-0.5, competitor_discount=0.3))
        self.assertGreater(s2, s1)
    def test_score_capped(self):
        s, _ = churn_score(cust(usage_trend=-1, support_tickets_90d=9,
                                 competitor_discount=0.4, payment_delays_6m=5))
        self.assertLessEqual(s, 1.0)

class TestLTV(unittest.TestCase):
    def test_ltv_positive_and_scales(self):
        self.assertGreater(ltv(5000, 48), ltv(1000, 6))
    def test_discount_raises_stay_probability(self):
        p0 = stay_probability(0.6, 0.0)
        p1 = stay_probability(0.6, 0.15)
        self.assertGreater(p1, p0)

class TestRetention(unittest.TestCase):
    def test_loyal_customer_no_action(self):
        self.assertEqual(RetentionEngine().process(cust(usage_trend=0.9))["outcome"], "NO_ACTION")
    def test_moderate_risk_gets_profitable_offer(self):
        r = RetentionEngine().process(cust(usage_trend=-0.8, monthly_fee=4000, months_tenure=36))
        self.assertIn(r["outcome"], ("OFFER", "PASSIVE"))
        if r["outcome"] == "OFFER":
            self.assertGreater(r["offer"]["gain"], r["offer"]["cost"])
    def test_vip_critical_escalates(self):
        r = RetentionEngine().process(cust(segment="enterprise", usage_trend=-0.9,
                                           competitor_discount=0.3))
        self.assertEqual(r["outcome"], "ESCALATE_VIP")
    def test_offer_never_exceeds_cap(self):
        r = RetentionEngine().process(cust(usage_trend=-0.6, monthly_fee=3000,
                                           competitor_discount=0.35, months_tenure=48))
        if r["outcome"] == "OFFER":
            self.assertLessEqual(r["offer"]["discount"], 0.20)

if __name__ == "__main__":
    unittest.main()
