from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any, ClassVar

from lab.analysis.classifier_tradeoffs import calculate, load_fixture


class ClassifierTradeoffTests(unittest.TestCase):
    summary: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        fixture = Path(__file__).resolve().parents[1] / "fixtures" / "classifier_tradeoffs.json"
        cls.summary = calculate(load_fixture(fixture))

    def test_baseline_threshold_tradeoff_and_unknown_labels(self) -> None:
        low, high = self.summary["windows"]["baseline"]
        self.assertEqual(low["confusion_matrix"], {
            "true_positive": 100,
            "false_positive": 700,
            "true_negative": 9300,
            "false_negative": 0,
        })
        self.assertEqual(low["precision"], 0.125)
        self.assertEqual(low["recall"], 1.0)
        self.assertEqual(low["unknown_label_coverage"], 1.0)
        self.assertEqual(high["precision"], 1.0)
        self.assertEqual(high["unknown_label_coverage"], 0.0)
        self.assertEqual(high["known_label_events"], 10100)

    def test_adaptation_changes_high_threshold_outcome(self) -> None:
        low, high = self.summary["windows"]["post_adaptation"]
        self.assertEqual(low["recall"], 1.0)
        self.assertEqual(high["recall"], 0.7)
        self.assertEqual(high["false_negative_rate"], 0.3)
        self.assertEqual(low["adapted_attacker_protected_actions_completed"], 3)
        self.assertEqual(high["adapted_attacker_protected_actions_completed"], 28)
        self.assertEqual(low["legitimate_near_neighbor_challenges"], 700)
        self.assertEqual(high["legitimate_near_neighbor_challenges"], 0)

    def test_costs_and_base_rate_are_deterministic(self) -> None:
        low = self.summary["windows"]["post_adaptation"][0]
        self.assertEqual(low["total_flagged_events"], 900)
        self.assertEqual(low["estimated_review_cost_usd"], 2250.0)
        self.assertEqual(low["estimated_total_operational_cost_usd"], 3162.0)
        base_rate = self.summary["base_rate_example"]
        self.assertEqual(base_rate["false_positive_alerts"], 1000)
        self.assertEqual(base_rate["true_positive_alerts"], 900)
        self.assertEqual(base_rate["alert_precision"], 0.4737)


if __name__ == "__main__":
    unittest.main()
