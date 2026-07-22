from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any, ClassVar

from lab.analysis.traffic_intelligence import calculate, load_fixture


class TrafficIntelligenceTests(unittest.TestCase):
    summary: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        fixture = Path(__file__).resolve().parents[1] / "fixtures" / "traffic_intelligence_events.json"
        cls.summary = calculate(load_fixture(fixture))

    def test_two_clusters_and_ambiguous_event_are_preserved(self) -> None:
        clusters = self.summary["proposed_clusters"]
        self.assertEqual([cluster["cluster_id"] for cluster in clusters], [
            "checkout-sequence-with-challenge-replay",
            "multi-account-login-sequence",
        ])
        self.assertEqual(self.summary["ambiguous_events"][0]["event_id"], "obs-005")
        self.assertEqual(self.summary["ambiguous_events"][0]["candidate_clusters"], [
            "checkout-sequence-with-challenge-replay",
            "multi-account-login-sequence",
        ])

    def test_ratings_staleness_and_version_drift_are_explicit(self) -> None:
        first = self.summary["normalized_evidence"][0]
        self.assertEqual(first["source_rating"], {"code": "A", "meaning": "reliable"})
        self.assertEqual(first["information_rating"], {"code": "2", "meaning": "probably true"})
        lifecycle = {item["indicator_id"]: item for item in self.summary["indicator_lifecycle"]}
        self.assertEqual(lifecycle["chromium-132-automation-artifact"]["status"], "stale")
        self.assertIn("Chromium 140", self.summary["version_drift_explanation"])
        self.assertIn("insufficient for attribution", self.summary["shared_infrastructure_assessment"])

    def test_emulation_and_regression_are_bounded_and_exact(self) -> None:
        plan = self.summary["bounded_emulation_plan"]
        self.assertIn("loopback", plan["local_safe_approximation"])
        self.assertIn("Session B", plan["protected_action_or_service_effect"])
        regression = self.summary["regression_test_definition"]
        self.assertIn("Session B is rejected", regression["pass"])
        self.assertEqual(regression["evidence"][-1], "HTTP status")


if __name__ == "__main__":
    unittest.main()
