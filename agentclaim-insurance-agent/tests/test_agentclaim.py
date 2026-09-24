import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.policy import Policy, Claim, check_coverage
from src.fraud import fraud_score
from src.reserve import calculate_reserve
from src.liquidator import AgentClaim

POL = Policy("P-1", 20_000_000, 0.15, 0.08, 30, 3_000_000)

def claim(**kw):
    base = dict(claim_id="S-1", policy_id="P-1", amount=1_000_000,
                days_after_start=200, prior_claims=0, inconsistency_flags=0,
                item_age_years=2)
    base.update(kw)
    return Claim(**base)

class TestCoverage(unittest.TestCase):
    def test_waiting_period_denies(self):
        ok, m = check_coverage(POL, claim(days_after_start=10))
        self.assertFalse(ok); self.assertIn("carencia", m)
    def test_over_limit_denies(self):
        ok, m = check_coverage(POL, claim(amount=25_000_000))
        self.assertFalse(ok)
    def test_normal_claim_covered(self):
        self.assertTrue(check_coverage(POL, claim())[0])

class TestFraud(unittest.TestCase):
    def test_clean_claim_low_score(self):
        s, _ = fraud_score(POL, claim())
        self.assertLess(s, 0.3)
    def test_many_signals_high_score(self):
        s, sig = fraud_score(POL, claim(amount=19_000_000, days_after_start=20,
                                        prior_claims=5, inconsistency_flags=3))
        self.assertGreaterEqual(s, 0.6)
        self.assertTrue(sig)

class TestReserve(unittest.TestCase):
    def test_deductible_and_depreciation_applied(self):
        r = calculate_reserve(POL, claim(amount=1_000_000, item_age_years=5))
        self.assertLess(r, 1_000_000 * 0.85 + 1)
    def test_depreciation_floor_40pct(self):
        r = calculate_reserve(POL, claim(amount=1_000_000, item_age_years=50))
        self.assertAlmostEqual(r, 1_000_000 * 0.4 * 0.85)

class TestLiquidator(unittest.TestCase):
    def test_settles_routine_claim(self):
        res = AgentClaim(POL).process(claim())
        self.assertEqual(res["outcome"], "SETTLED")
        self.assertGreater(res["settlement"], 0)
    def test_escalates_fraud(self):
        res = AgentClaim(POL).process(claim(amount=19e6, days_after_start=35,
                                            prior_claims=5, inconsistency_flags=3))
        self.assertEqual(res["outcome"], "ESCALATE_FRAUD")
    def test_escalates_over_mandate(self):
        res = AgentClaim(POL).process(claim(amount=4_000_000, item_age_years=0))
        self.assertEqual(res["outcome"], "ESCALATE_AMOUNT")
    def test_denies_waiting_period(self):
        res = AgentClaim(POL).process(claim(days_after_start=5))
        self.assertEqual(res["outcome"], "DENIED")

if __name__ == "__main__":
    unittest.main()
