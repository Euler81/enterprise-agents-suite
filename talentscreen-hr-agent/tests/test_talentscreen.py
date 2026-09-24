import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.jd import JobDescription
from src.candidate import Candidate
from src.match import match_score
from src.bias import adverse_impact_audit
from src.agent import TalentScreen

JD = JobDescription("Dev", {"python": 0.5, "aws": 0.3, "docker": 0.2},
                    min_years=4, salary_min=1_000_000, salary_max=2_000_000)

def cand(**kw):
    base = dict(candidate_id="CV-1", name="Test", group="A",
                skills=["python", "aws", "docker"], years_experience=8,
                salary_expectation=1_500_000)
    base.update(kw)
    return Candidate(**base)

class TestMatch(unittest.TestCase):
    def test_perfect_candidate(self):
        s, d = match_score(JD, cand())
        self.assertGreaterEqual(s, 0.9)
        self.assertEqual(d["missing_skills"], [])
    def test_missing_key_skill_hurts(self):
        s, d = match_score(JD, cand(skills=["python"]))
        self.assertLess(s, 0.8)
        self.assertIn("aws", d["missing_skills"])
    def test_salary_over_band_penalized(self):
        s1, _ = match_score(JD, cand())
        s2, _ = match_score(JD, cand(salary_expectation=4_000_000))
        self.assertGreater(s1, s2)

class TestBiasAudit(unittest.TestCase):
    def test_flagged_when_gap_large(self):
        r = adverse_impact_audit({"A": [0.9, 0.85, 0.8], "B": [0.45, 0.4, 0.5]})
        self.assertTrue(r["flagged"])
        self.assertLess(r["ratio"], 0.8)
    def test_not_flagged_when_similar(self):
        r = adverse_impact_audit({"A": [0.8, 0.7], "B": [0.75, 0.72]})
        self.assertFalse(r["flagged"])

class TestAgent(unittest.TestCase):
    def test_shortlist_and_hold(self):
        cands = [cand(candidate_id=f"CV-{i}", skills=["python", "aws", "docker"][:i % 3 + 1],
                      years_experience=i, salary_expectation=1_500_000, group="A" if i % 2 else "B")
                 for i in range(1, 9)]
        r = TalentScreen().screen(JD, cands)
        self.assertEqual(r["total"], 8)
        self.assertTrue(all(d["outcome"] in ("SHORTLIST", "HOLD") for d in r["decisions"]))
        self.assertIn("audit", r)

if __name__ == "__main__":
    unittest.main()
