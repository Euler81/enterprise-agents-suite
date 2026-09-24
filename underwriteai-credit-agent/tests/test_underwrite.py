import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.applicant import Applicant
from src.score import credit_score
from src.policy import max_exposure
from src.decision import CreditAgent

def app(**kw):
    base = dict(applicant_id="A-1", company="Test SA", annual_revenue=1_500_000,
                years_in_business=5, monthly_invoices=10, bank_debt_ratio=0.3,
                bounced_payments_12m=0, requested_amount=100_000)
    base.update(kw)
    return Applicant(**base)

class TestScore(unittest.TestCase):
    def test_strong_company_high_score(self):
        s, pos, _ = credit_score(app(annual_revenue=2_000_000))
        self.assertGreaterEqual(s, 600)
        self.assertIn("REVENUE_STRONG", pos)
    def test_incidents_crush_score(self):
        s, _, neg = credit_score(app(bounced_payments_12m=4, bank_debt_ratio=0.8))
        self.assertLess(s, 400)
        self.assertIn("PAYMENT_INCIDENTS", neg)
    def test_score_bounded(self):
        self.assertLessEqual(credit_score(app(annual_revenue=99e6))[0], 1000)

class TestPolicy(unittest.TestCase):
    def test_exposure_is_20pct(self):
        self.assertEqual(max_exposure(1_000_000), 200_000)

class TestDecision(unittest.TestCase):
    def test_good_applicant_approved(self):
        r = CreditAgent().evaluate(app())
        self.assertEqual(r["outcome"], "APPROVE")
        self.assertLessEqual(r["suggested_rate"], 0.60)
    def test_over_exposure_declined(self):
        r = CreditAgent().evaluate(app(requested_amount=900_000))
        self.assertEqual(r["outcome"], "DECLINE")
    def test_gray_zone_referred(self):
        r = CreditAgent().evaluate(app(annual_revenue=400_000, years_in_business=2,
                                       monthly_invoices=3, requested_amount=60_000))
        self.assertEqual(r["outcome"], "REFER")

if __name__ == "__main__":
    unittest.main()
