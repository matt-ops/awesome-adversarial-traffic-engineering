from __future__ import annotations

import unittest
from pathlib import Path

from lab.analysis.analyze import evaluate, load_jsonl
from lab.detectors.rules import score_event


class DetectorTests(unittest.TestCase):
    def test_reasons_are_explainable(self) -> None:
        result = score_event(
            {"webdriver": True, "user_agent": "Chrome Windows", "platform": "Linux", "inter_arrival_ms": 50}
        )
        self.assertEqual(result["decision"], "observe")
        self.assertIn("automation_property", result["reasons"])
        self.assertIn("ua_platform_mismatch", result["reasons"])

    def test_fixture_metrics_are_deterministic(self) -> None:
        fixture = Path(__file__).parents[1] / "fixtures" / "requests.jsonl"
        summary = evaluate(load_jsonl(fixture))
        self.assertEqual(summary["confusion_matrix"], {"tp": 4, "fp": 0, "tn": 6, "fn": 0})
        self.assertEqual(summary["precision"], 1.0)
        self.assertEqual(summary["recall"], 1.0)
        self.assertIn("limitations", summary)


if __name__ == "__main__":
    unittest.main()
