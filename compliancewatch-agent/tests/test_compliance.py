import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.norms import Norm, NORM_DB
from src.impact import affected_processes, impact_score
from src.agent import ComplianceAgent

class TestMapping(unittest.TestCase):
    def test_data_privacy_hits_two_processes(self):
        n = next(n for n in NORM_DB if n.area == "data_privacy")
        self.assertGreaterEqual(len(affected_processes(n)), 2)
    def test_critical_scores_higher_than_low(self):
        crit = next(n for n in NORM_DB if n.severity == "critica")
        low = next(n for n in NORM_DB if n.severity == "baja")
        self.assertGreater(impact_score(crit, affected_processes(crit)),
                           impact_score(low, affected_processes(low)))

class TestAgent(unittest.TestCase):
    def test_critical_norm_escalates(self):
        crit = next(n for n in NORM_DB if n.severity == "critica")
        self.assertEqual(ComplianceAgent().process_norm(crit)["outcome"], "ESCALATE")
    def test_short_deadline_escalates(self):
        n = Norm("T-1", "TEST", "Test", "tax", "alta", 5, "test")
        self.assertEqual(ComplianceAgent().process_norm(n)["outcome"], "ESCALATE")
    def test_normal_norm_action_plan_with_owners(self):
        n = next(n for n in NORM_DB if n.severity == "alta" and n.deadline_days >= 15)
        r = ComplianceAgent().process_norm(n)
        self.assertEqual(r["outcome"], "ACTION_PLAN")
        self.assertTrue(r["affected"])
    def test_scan_covers_db(self):
        self.assertEqual(len(ComplianceAgent().scan_all()), len(NORM_DB))

if __name__ == "__main__":
    unittest.main()
