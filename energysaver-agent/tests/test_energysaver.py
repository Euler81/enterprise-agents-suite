import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.meter import ConsumptionSeries
from src.anomaly import detect_anomalies, estimate_savings
from src.dossier import build_dossier
from src.agent import EnergySaver

def series(base=1000, spike=None, contracted=3.0):
    m = [base] * 24
    if spike:
        m[10] = spike
    return ConsumptionSeries("T-1", m, contracted)

class TestAnomaly(unittest.TestCase):
    def test_calm_series_no_anomalies(self):
        self.assertEqual(detect_anomalies(series()), [])
    def test_spike_detected(self):
        a = detect_anomalies(series(spike=3000))
        self.assertEqual(len(a), 1)
        self.assertEqual(a[0]["month"], 11)
        self.assertGreater(a[0]["excess_cost"], 0)
    def test_over_contracted_power_found(self):
        est = estimate_savings(series(contracted=6.0))
        self.assertGreater(est["power_saving"], 0)

class TestDossier(unittest.TestCase):
    def test_dossier_has_arguments(self):
        d = build_dossier(series(spike=3000, contracted=6.0))
        self.assertGreaterEqual(len(d["arguments"]), 2)
        self.assertGreater(d["savings"]["total"], 0)

class TestAgent(unittest.TestCase):
    def test_worthwhile_site_negotiates(self):
        r = EnergySaver().audit(series(spike=3500, contracted=8.0))
        self.assertEqual(r["outcome"], "NEGOTIATE")
    def test_small_site_report_only(self):
        r = EnergySaver().audit(series(base=500, contracted=1.0))
        self.assertEqual(r["outcome"], "REPORT_ONLY")

if __name__ == "__main__":
    unittest.main()
