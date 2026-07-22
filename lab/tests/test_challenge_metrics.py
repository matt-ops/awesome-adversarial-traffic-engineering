from __future__ import annotations

import unittest
from pathlib import Path

from lab.analysis.challenge_metrics import calculate, load_fixture


class ChallengeMetricTests(unittest.TestCase):
    def test_deterministic_population_and_customer_impact_metrics(self) -> None:
        fixture = Path(__file__).resolve().parents[1] / "fixtures" / "challenge_metrics.json"
        summary = calculate(load_fixture(fixture))
        populations = summary["populations"]

        manual = populations["manual-legitimate-user"]
        self.assertEqual(manual["challenge_issuance_rate"], 0.2)
        self.assertEqual(manual["protected_action_completion_rate"], 0.9)

        near_neighbor = populations["legitimate-automation-or-accessibility-like-client"]
        self.assertEqual(near_neighbor["legitimate_false_positive_rate"], 0.8)
        self.assertEqual(near_neighbor["challenge_abandonment_rate"], 0.4)

        stock = populations["stock-automated-attacker"]
        replaying = populations["adapted-or-replaying-attacker"]
        self.assertEqual(stock["abuse_outcome"], "mostly-stopped")
        self.assertEqual(replaying["abuse_outcome"], "displaced")
        self.assertEqual(replaying["attacker_cost_usd_per_successful_protected_action"], 0.1)

        impact = summary["customer_impact"]["accessibility_privacy_tool_and_test_automation_proxy"]
        self.assertEqual(impact["challenge_issuance_delta"], 0.6)
        self.assertEqual(impact["protected_action_completion_delta"], -0.4)


if __name__ == "__main__":
    unittest.main()
