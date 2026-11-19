import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from metrics import metrics

class MetricsTest(unittest.TestCase):
    def test_multi_positive_not_hit_rate(self):
        m = metrics(["x", "a"], {"a", "b"}, 2)
        self.assertEqual(m["recall"], .5)
        self.assertEqual(m["hit_rate"], 1)
        self.assertEqual(m["mrr"], .5)
    def test_duplicate_and_empty(self):
        self.assertEqual(metrics(["a", "a", "b"], {"a", "b"}, 2)["recall"], 1)
        self.assertIsNone(metrics([], set()))
        self.assertEqual(metrics([], {"a"})["ndcg"], 0)
    def test_perfect(self):
        self.assertAlmostEqual(metrics(["a","b"], {"a","b"})["ndcg"],1)
