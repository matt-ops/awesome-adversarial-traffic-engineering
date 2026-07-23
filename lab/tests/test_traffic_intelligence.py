from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, ClassVar

from lab.analysis.traffic_intelligence import _confidence, calculate, load_fixture


class TrafficIntelligenceTests(unittest.TestCase):
    fixture: ClassVar[dict[str, Any]]
    summary: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        fixture_path = Path(__file__).resolve().parents[1] / "fixtures" / "traffic_intelligence_events.json"
        cls.fixture = load_fixture(fixture_path)
        cls.summary = calculate(cls.fixture)

    @staticmethod
    def _cluster(summary: dict[str, Any], cluster_id: str) -> dict[str, Any]:
        return next(cluster for cluster in summary["proposed_clusters"] if cluster["cluster_id"] == cluster_id)

    def test_fixture_has_no_answer_labels(self) -> None:
        for event in self.fixture["events"]:
            self.assertNotIn("cluster_key", event)
            self.assertNotIn("cluster_candidates", event)

    def test_two_behavior_families_are_derived_and_cross_workflow_event_is_ambiguous(self) -> None:
        clusters = self.summary["proposed_clusters"]
        self.assertEqual(
            [cluster["cluster_id"] for cluster in clusters],
            ["multi-account-login-sequence", "protected-report-sequence-with-challenge-replay"],
        )
        protected_report = self._cluster(
            self.summary, "protected-report-sequence-with-challenge-replay"
        )
        login = self._cluster(self.summary, "multi-account-login-sequence")
        self.assertEqual(protected_report["member_event_ids"], ["obs-001", "obs-002"])
        self.assertEqual(login["member_event_ids"], ["obs-003", "obs-004"])
        ambiguous = {item["event_id"]: item for item in self.summary["ambiguous_events"]}
        self.assertEqual(
            ambiguous["obs-005"]["candidate_behavior_families"],
            ["multi-account-login-sequence", "protected-report-sequence-with-challenge-replay"],
        )
        self.assertEqual(protected_report["historical_only_observations"], ["obs-006"])

    def test_changing_protected_workflow_changes_grouping(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["events"][0]["protected_workflow"] = "synthetic-account-login"
        summary = calculate(fixture)
        ambiguous_ids = {item["event_id"] for item in summary["ambiguous_events"]}
        self.assertIn("obs-001", ambiguous_ids)
        self.assertNotIn(
            "protected-report-sequence-with-challenge-replay",
            {cluster["cluster_id"] for cluster in summary["proposed_clusters"]},
        )

    def test_changing_stable_challenge_behavior_changes_group_eligibility(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["events"][0]["challenge_behavior"] = "challenge encountered and abandoned"
        summary = calculate(fixture)
        ambiguous_ids = {item["event_id"] for item in summary["ambiguous_events"]}
        self.assertIn("obs-001", ambiguous_ids)
        self.assertNotIn(
            "protected-report-sequence-with-challenge-replay",
            {cluster["cluster_id"] for cluster in summary["proposed_clusters"]},
        )

    def test_removing_required_continuity_makes_event_ambiguous(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["events"][0]["request_sequence"] = ["GET /api/reports/protected"]
        summary = calculate(fixture)
        ambiguous_ids = {item["event_id"] for item in summary["ambiguous_events"]}
        self.assertIn("obs-001", ambiguous_ids)

    def test_shared_infrastructure_alone_never_groups_or_attributes(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        ambiguous = fixture["events"][4]
        ambiguous["request_sequence"] = ["GET /unrelated"]
        summary = calculate(fixture)
        event = next(item for item in summary["ambiguous_events"] if item["event_id"] == "obs-005")
        self.assertEqual(event["candidate_behavior_families"], [])
        self.assertIn("never a membership key", summary["shared_infrastructure_assessment"])
        for cluster in summary["proposed_clusters"]:
            self.assertIn("does not establish an actor", cluster["attribution_limitation"])

    def test_confidence_rubric_changes_with_evidence_quality(self) -> None:
        protected_report_id = "protected-report-sequence-with-challenge-replay"
        baseline = self._cluster(self.summary, protected_report_id)["confidence"]["level"]
        self.assertEqual(baseline, "high")

        no_corroboration = copy.deepcopy(self.fixture)
        no_corroboration["events"][1]["request_sequence"] = ["GET /api/reports/protected"]
        summary = calculate(no_corroboration)
        self.assertNotIn(
            protected_report_id,
            {cluster["cluster_id"] for cluster in summary["proposed_clusters"]},
        )
        self.assertEqual(_confidence([no_corroboration["events"][0]], True)["level"], "low")

        contradiction = copy.deepcopy(self.fixture)
        contradiction["events"][0]["material_contradictions"] = ["protected result conflicts with server record"]
        level = self._cluster(calculate(contradiction), protected_report_id)["confidence"]["level"]
        self.assertEqual(level, "low")

        inferred = copy.deepcopy(self.fixture)
        inferred["events"][0]["evidence_state"] = "inference"
        level = self._cluster(calculate(inferred), protected_report_id)["confidence"]["level"]
        self.assertEqual(level, "moderate")

        historical = copy.deepcopy(self.fixture)
        historical["events"][0]["evidence_state"] = "historical-reporting"
        historical["events"][1]["evidence_state"] = "historical-reporting"
        clusters = calculate(historical)["proposed_clusters"]
        self.assertNotIn(protected_report_id, {cluster["cluster_id"] for cluster in clusters})
        self.assertEqual(_confidence(historical["events"][:2], True)["level"], "low")

    def test_ratings_version_language_plan_and_regression_are_consistent(self) -> None:
        first = self.summary["normalized_evidence"][0]
        self.assertEqual(first["source_rating"], {"code": "A", "meaning": "reliable"})
        self.assertEqual(first["information_rating"], {"code": "2", "meaning": "probably true"})
        self.assertIn("fixture-current Playwright Chromium 149", self.summary["version_drift_explanation"])
        plan = self.summary["bounded_emulation_plan"]
        regression = self.summary["regression_test_definition"]
        protected_report = self._cluster(
            self.summary, "protected-report-sequence-with-challenge-replay"
        )
        self.assertEqual(plan["supporting_evidence"], protected_report["supporting_evidence"])
        self.assertEqual(plan["current_evidence"], protected_report["current_evidence"])
        self.assertEqual(plan["contradictions"], protected_report["contradictions"])
        self.assertEqual(plan["confidence"], regression["confidence"])
        self.assertEqual(plan["confidence"], protected_report["confidence"])
        self.assertEqual(plan["workflow"], "synthetic-protected-report")
        self.assertEqual(
            plan["behavior_sequence"],
            ["POST /api/challenge", "GET /api/reports/protected"],
        )
        self.assertEqual(plan["protected_action"], "GET /api/reports/protected")
        self.assertIn("loopback", plan["local_safe_approximation"])
        self.assertIn("transferred or replayed proof is rejected", regression["pass"])

    def test_selected_group_drives_every_plan_field(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["emulation_focus_cluster"] = "multi-account-login-sequence"
        summary = calculate(fixture)
        selected = self._cluster(summary, "multi-account-login-sequence")
        plan = summary["bounded_emulation_plan"]
        self.assertEqual(plan["selected_cluster_id"], selected["cluster_id"])
        self.assertEqual(plan["supporting_evidence"], selected["supporting_evidence"])
        self.assertEqual(plan["current_evidence"], selected["current_evidence"])
        self.assertEqual(plan["confidence"], selected["confidence"])
        self.assertEqual(plan["contradictions"], selected["contradictions"])
        self.assertEqual(plan["alternative_explanations"], selected["alternative_explanations"])
        self.assertEqual(plan["workflow"], selected["workflow"])
        self.assertEqual(plan["behavior_sequence"], selected["behavior_sequence"])
        self.assertEqual(plan["challenge_behavior"], selected["challenge_behavior"])
        self.assertEqual(plan["protected_action"], selected["protected_action"])
        self.assertEqual(
            plan["observed_protected_action_result"],
            selected["protected_action_result"],
        )
        self.assertNotEqual(plan, self.summary["bounded_emulation_plan"])

    def test_stale_implementation_artifact_is_lifecycle_evidence_not_identity(self) -> None:
        protected_report = self._cluster(
            self.summary, "protected-report-sequence-with-challenge-replay"
        )
        self.assertNotIn("obs-006", protected_report["member_event_ids"])
        self.assertEqual(protected_report["historical_lifecycle_evidence"], ["obs-006"])
        indicator = next(
            item
            for item in self.summary["indicator_lifecycle"]
            if item["indicator_id"] == "chromium-132-automation-artifact"
        )
        self.assertEqual(indicator["status"], "stale")

    def test_output_is_deterministic(self) -> None:
        self.assertEqual(calculate(copy.deepcopy(self.fixture)), self.summary)

    def test_answer_labeled_fixture_is_rejected(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["events"][0]["cluster_key"] = "answer"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "prohibited answer fields"):
                load_fixture(path)


if __name__ == "__main__":
    unittest.main()
