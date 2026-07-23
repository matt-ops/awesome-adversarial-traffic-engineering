from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, ClassVar

from lab.analysis.classifier_tradeoffs import calculate, load_fixture


class ClassifierTradeoffTests(unittest.TestCase):
    fixture: ClassVar[dict[str, Any]]
    summary: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        fixture = Path(__file__).resolve().parents[1] / "fixtures" / "classifier_tradeoffs.json"
        cls.fixture = load_fixture(fixture)
        cls.summary = calculate(cls.fixture)

    def assert_fixture_rejected(self, fixture: dict[str, Any], message: str) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "classifier.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                load_fixture(path)

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

    def test_thresholds_must_be_numeric_bounded_and_unique(self) -> None:
        for value, message in (
            ("0.5", "must be numeric"),
            (-0.1, "between 0 and 1"),
            (1.1, "between 0 and 1"),
        ):
            with self.subTest(value=value):
                fixture = copy.deepcopy(self.fixture)
                fixture["thresholds"][0] = value
                self.assert_fixture_rejected(fixture, message)
        duplicate = copy.deepcopy(self.fixture)
        duplicate["thresholds"][1] = duplicate["thresholds"][0]
        self.assert_fixture_rejected(duplicate, "thresholds must be unique")

    def test_scores_population_names_and_counts_are_validated(self) -> None:
        malformed = (
            ("baseline_score", "high", "must be numeric"),
            ("post_adaptation_score", 1.01, "between 0 and 1"),
            ("count", 0, "positive integer"),
            ("count", 1.5, "positive integer"),
        )
        for field, value, message in malformed:
            with self.subTest(field=field, value=value):
                fixture = copy.deepcopy(self.fixture)
                fixture["populations"][0][field] = value
                self.assert_fixture_rejected(fixture, message)
        duplicate_name = copy.deepcopy(self.fixture)
        duplicate_name["populations"][1]["population"] = duplicate_name["populations"][0]["population"]
        self.assert_fixture_rejected(duplicate_name, "population names must be unique")

    def test_costs_and_protected_action_counts_are_validated(self) -> None:
        negative_cost = copy.deepcopy(self.fixture)
        negative_cost["costs"]["review_usd_per_flag"] = -1
        self.assert_fixture_rejected(negative_cost, "must be nonnegative")

        for value in (-1, self.fixture["populations"][0]["count"] + 1, 1.5):
            with self.subTest(value=value):
                fixture = copy.deepcopy(self.fixture)
                fixture["populations"][0]["protected_actions_if_flagged"] = value
                self.assert_fixture_rejected(fixture, "integer between 0 and count")

    def test_base_rate_fields_and_unknown_label_population_are_required(self) -> None:
        missing = copy.deepcopy(self.fixture)
        del missing["base_rate_example"]["recall"]
        self.assert_fixture_rejected(missing, "base_rate_example is missing")

        negative = copy.deepcopy(self.fixture)
        negative["base_rate_example"]["abusive_events"] = -1
        self.assert_fixture_rejected(negative, "nonnegative integer")

        rate = copy.deepcopy(self.fixture)
        rate["base_rate_example"]["false_positive_rate"] = 1.1
        self.assert_fixture_rejected(rate, "between 0 and 1")

        no_unknown = copy.deepcopy(self.fixture)
        for population in no_unknown["populations"]:
            if population["label"] is None:
                population["label"] = "legitimate"
        self.assert_fixture_rejected(no_unknown, "at least one unknown or delayed-label population")


if __name__ == "__main__":
    unittest.main()
