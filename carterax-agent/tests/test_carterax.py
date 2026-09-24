"""Suite de tests del agente de recupero."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.scoring import Debtor, risk_score, priority_tier
from src.policies import PolicyEngine, PolicyConfig
from src.negotiation import Negotiator
from src.agent import CarteraXAgent


def make_debtor(**kw) -> Debtor:
    base = dict(debtor_id="D-1", name="Test Usuario", debt=100_000,
                days_past_due=30, segment="consumer", prior_promises=0,
                avg_payment_delay_days=10, contactability=0.8,
                hostility_signals=0.1)
    base.update(kw)
    return Debtor(**base)


class TestScoring(unittest.TestCase):
    def test_score_range(self):
        for dpd in (5, 30, 90, 170):
            s = risk_score(make_debtor(days_past_due=dpd))
            self.assertTrue(0 <= s <= 100)

    def test_fresh_payer_scores_higher(self):
        good = make_debtor(days_past_due=10, contactability=0.9)
        bad = make_debtor(days_past_due=150, prior_promises=4, contactability=0.1)
        self.assertGreater(risk_score(good), risk_score(bad))

    def test_tiers(self):
        self.assertEqual(priority_tier(80), "P1")
        self.assertEqual(priority_tier(50), "P2")
        self.assertEqual(priority_tier(20), "P3")


class TestPolicies(unittest.TestCase):
    def test_rejects_excessive_discount(self):
        p = PolicyEngine()
        ok, motive = p.check_offer({"debt": 100_000, "discount": 0.50,
                                    "installments": 1, "first_payment_pct": 1.0})
        self.assertFalse(ok)
        self.assertIn("descuento", motive)

    def test_rejects_low_first_payment(self):
        p = PolicyEngine()
        ok, _ = p.check_offer({"debt": 100_000, "discount": 0.0,
                               "installments": 3, "first_payment_pct": 0.05})
        self.assertFalse(ok)

    def test_pv_discounts_future_installments(self):
        p = PolicyEngine()
        pv_cash = p.recovery_pv({"debt": 100_000, "discount": 0.0,
                                 "installments": 1, "first_payment_pct": 1.0})
        pv_plan = p.recovery_pv({"debt": 100_000, "discount": 0.0,
                                 "installments": 6, "first_payment_pct": 0.3})
        self.assertGreater(pv_cash, pv_plan)


class TestNegotiation(unittest.TestCase):
    def test_good_debtor_agrees_within_policy(self):
        d = make_debtor(days_past_due=15, contactability=0.95, debt=80_000)
        res = Negotiator(PolicyEngine(), d).negotiate()
        self.assertIn(res["outcome"], ("AGREED", "PASSIVE"))
        if res["outcome"] == "AGREED":
            ok, _ = PolicyEngine().check_offer(res["offer"])
            self.assertTrue(ok)

    def test_concessions_never_break_policy(self):
        d = make_debtor(days_past_due=60, debt=200_000)
        res = Negotiator(PolicyEngine(), d, max_rounds=6).negotiate()
        for t in res["trace"]:
            ok, _ = PolicyEngine().check_offer(t["offer"])
            self.assertTrue(ok, f"oferta fuera de política: {t['offer']}")

    def test_hostile_debtor_escalates(self):
        d = make_debtor(hostility_signals=0.95)
        res = Negotiator(PolicyEngine(), d).negotiate()
        self.assertEqual(res["outcome"], "ESCALATE")


class TestAgent(unittest.TestCase):
    def test_campaign_end_to_end(self):
        campaign = CarteraXAgent().run_campaign(
            [make_debtor(debtor_id=f"D-{i}", debt=50_000 * (i + 1))
             for i in range(10)])
        m = campaign["metrics"]
        self.assertEqual(m["debtors"], 10)
        self.assertTrue((Path("output/campaign_report.csv")).exists())

    def test_hostile_never_negotiates(self):
        r = CarteraXAgent().process_debtor(make_debtor(hostility_signals=0.9))
        self.assertEqual(r["outcome"], "ESCALATE")
        self.assertIn("recommendation", r["escalation"])


if __name__ == "__main__":
    unittest.main()
