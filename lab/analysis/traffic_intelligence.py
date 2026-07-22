"""Turn synthetic traffic observations into confidence-rated local emulation inputs."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

SOURCE_RATINGS = {
    "A": "reliable",
    "B": "usually reliable",
    "C": "fairly reliable",
    "D": "not usually reliable",
    "E": "unreliable",
    "F": "cannot be judged",
}
INFORMATION_RATINGS = {
    "1": "confirmed",
    "2": "probably true",
    "3": "possibly true",
    "4": "doubtfully true",
    "5": "improbable",
    "6": "cannot be judged",
}
REQUIRED_EVENT_FIELDS = {
    "event_id",
    "observed_at",
    "evidence_state",
    "source_reliability",
    "information_credibility",
    "protected_workflow",
    "request_sequence",
    "account_or_session_behavior",
    "browser_javascript",
    "http_tls",
    "network_proxy_category",
    "timing",
    "target_selection",
    "infrastructure",
    "challenge_behavior",
    "protected_action_result",
    "alternative_explanations",
}


def load_fixture(path: Path) -> dict[str, Any]:
    """Load the deterministic fixture and reject incomplete ratings or observations."""
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("events"), list):
        raise ValueError("traffic-intelligence fixture must contain an events list")
    if not isinstance(raw.get("indicators"), list):
        raise ValueError("traffic-intelligence fixture must contain an indicators list")
    for number, event in enumerate(raw["events"], start=1):
        if not isinstance(event, dict):
            raise ValueError(f"event {number} must be an object")
        missing = REQUIRED_EVENT_FIELDS - event.keys()
        if missing:
            raise ValueError(f"event {number} is missing {sorted(missing)}")
        if event["source_reliability"] not in SOURCE_RATINGS:
            raise ValueError(f"event {number} has an invalid source rating")
        if event["information_credibility"] not in INFORMATION_RATINGS:
            raise ValueError(f"event {number} has an invalid information rating")
        has_cluster = isinstance(event.get("cluster_key"), str)
        has_candidates = isinstance(event.get("cluster_candidates"), list)
        if has_cluster == has_candidates:
            raise ValueError(f"event {number} needs one cluster key or an ambiguous candidate list")
    return raw


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    """Create an ordered, explicit observation without upgrading inference to fact."""
    return {
        "event_id": event["event_id"],
        "observed_at": event["observed_at"],
        "evidence_state": event["evidence_state"],
        "source_rating": {
            "code": event["source_reliability"],
            "meaning": SOURCE_RATINGS[str(event["source_reliability"])],
        },
        "information_rating": {
            "code": event["information_credibility"],
            "meaning": INFORMATION_RATINGS[str(event["information_credibility"])],
        },
        "behavior": {
            "protected_workflow": event["protected_workflow"],
            "request_sequence": event["request_sequence"],
            "account_or_session_behavior": event["account_or_session_behavior"],
            "browser_javascript": event["browser_javascript"],
            "http_tls": event["http_tls"],
            "network_proxy_category": event["network_proxy_category"],
            "timing": event["timing"],
            "target_selection": event["target_selection"],
            "infrastructure": event["infrastructure"],
            "challenge_behavior": event["challenge_behavior"],
            "protected_action_result": event["protected_action_result"],
        },
        "cluster": event.get("cluster_key", "ambiguous"),
        "cluster_candidates": event.get("cluster_candidates", []),
        "contradicting_evidence": event.get("contradicts", []),
        "alternative_explanations": event["alternative_explanations"],
    }


def cluster_events(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Group declared behavior keys and preserve ambiguous observations separately."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    ambiguous: list[dict[str, Any]] = []
    for event in events:
        if "cluster_key" in event:
            grouped[str(event["cluster_key"])].append(event)
        else:
            ambiguous.append(
                {
                    "event_id": event["event_id"],
                    "candidate_clusters": sorted(str(value) for value in event["cluster_candidates"]),
                    "reason": "insufficient workflow, session, challenge, and protected-action continuity",
                    "contradicting_evidence": event.get("contradicts", []),
                    "alternative_explanations": event["alternative_explanations"],
                }
            )

    clusters: list[dict[str, Any]] = []
    for key in sorted(grouped):
        members = sorted(grouped[key], key=lambda item: str(item["event_id"]))
        contradictions = sorted(
            {str(value) for member in members for value in member.get("contradicts", [])}
        )
        alternatives = sorted(
            {str(value) for member in members for value in member["alternative_explanations"]}
        )
        current_members = [
            str(member["event_id"])
            for member in members
            if member["evidence_state"] != "historical-reporting"
        ]
        confidence = min(90, 45 + len(current_members) * 15 - len(contradictions) * 5)
        clusters.append(
            {
                "cluster_id": key,
                "confidence": confidence,
                "supporting_evidence": [str(member["event_id"]) for member in members],
                "current_evidence": current_members,
                "historical_reporting": [
                    str(member["event_id"])
                    for member in members
                    if member["evidence_state"] == "historical-reporting"
                ],
                "protected_workflows": sorted({str(member["protected_workflow"]) for member in members}),
                "challenge_behaviors": sorted({str(member["challenge_behavior"]) for member in members}),
                "protected_action_results": sorted(
                    {str(member["protected_action_result"]) for member in members}
                ),
                "contradicting_evidence": contradictions,
                "alternative_explanations": alternatives,
                "attribution": "not assessed; behavior grouping does not establish an actor",
            }
        )
    return clusters, sorted(ambiguous, key=lambda item: str(item["event_id"]))


def indicator_lifecycle(indicators: list[dict[str, Any]], analysis_date: date) -> list[dict[str, Any]]:
    """Add deterministic current/stale state without treating a warning as a verdict."""
    results: list[dict[str, Any]] = []
    for indicator in sorted(indicators, key=lambda item: str(item["indicator_id"])):
        expiry = date.fromisoformat(str(indicator["expires_on"]))
        result = dict(indicator)
        result["status"] = "stale" if expiry < analysis_date else "current-review-required"
        result["sharing_decision"] = (
            "retain only with version and limitation"
            if indicator["kind"] == "implementation-artifact"
            else "share with warning and review date"
        )
        results.append(result)
    return results


def emulation_plan(cluster_id: str) -> dict[str, Any]:
    """Define the fixed local approximation and exact defensive regression."""
    return {
        "behavior_being_emulated": "move a synthetic challenge proof between two local sessions before checkout",
        "evidence_supporting_it": ["obs-001", "obs-002"],
        "confidence_and_alternatives": {
            "confidence": 75,
            "alternatives": ["fixture reset failure", "bearer-proof defect independent of browser identity"],
        },
        "local_safe_approximation": (
            "Use the bundled loopback challenge flow with synthetic sessions A and B, "
            "one proof, and fixed request caps."
        ),
        "protected_action_or_service_effect": (
            "Session B must not complete the synthetic checkout with Session A proof."
        ),
        "expected_defensive_observations": [
            "proof issuance for Session A",
            "Session B verification rejection",
            "no Session B protected-action completion",
            "one allowed Session A use and rejected replay",
        ],
        "limitations": [
            "No malware, public infrastructure, real account, attribution, or harmful scale",
            "The behavior cluster is synthetic and does not establish campaign prevalence",
        ],
        "exact_regression_test": {
            "cluster_id": cluster_id,
            "setup": "reset the bundled loopback fixture",
            "action": "issue proof in Session A; present it once in Session B and twice in Session A",
            "pass": "Session B is rejected; Session A succeeds once; Session A replay is rejected",
            "evidence": ["session", "action", "origin", "nonce", "expiry", "use-count", "HTTP status"],
        },
    }


def calculate(fixture: dict[str, Any]) -> dict[str, Any]:
    """Produce the complete deterministic intelligence-to-regression output."""
    events = sorted(fixture["events"], key=lambda item: str(item["event_id"]))
    clusters, ambiguous = cluster_events(events)
    indicators = indicator_lifecycle(fixture["indicators"], date.fromisoformat(fixture["analysis_date"]))
    return {
        "analysis_date": fixture["analysis_date"],
        "normalized_evidence": [normalize_event(event) for event in events],
        "proposed_clusters": clusters,
        "ambiguous_events": ambiguous,
        "indicator_lifecycle": indicators,
        "version_drift_explanation": (
            "obs-006 is historical Chromium 132 reporting; current Chromium 140 evidence contradicts treating the "
            "implementation artifact as stable. Review or expire it rather than merging versions silently."
        ),
        "shared_infrastructure_assessment": (
            "shared-relay.example occurs across behaviors and is a grouping pivot only; "
            "it is insufficient for attribution."
        ),
        "bounded_emulation_plan": emulation_plan(str(fixture["emulation_focus_cluster"])),
        "regression_test_definition": emulation_plan(str(fixture["emulation_focus_cluster"]))[
            "exact_regression_test"
        ],
        "limitations": [
            "Synthetic identities and documentation-only infrastructure values",
            "Deterministic teaching clusters, not an attribution or production prevalence system",
            "No network requests and no external enrichment",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "fixture", nargs="?", type=Path, default=Path("lab/fixtures/traffic_intelligence_events.json")
    )
    args = parser.parse_args()
    print(json.dumps(calculate(load_fixture(args.fixture)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
