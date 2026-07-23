"""Derive behavior groups and confidence-bounded emulation inputs from synthetic evidence."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
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
DIRECT_EVIDENCE_STATES = {"observation", "confirmed-fact"}
HISTORICAL_EVIDENCE_STATE = "historical-reporting"
STRONG_SOURCE_RATINGS = {"A", "B"}
STRONG_INFORMATION_RATINGS = {"1", "2"}
PROHIBITED_ANSWER_FIELDS = {"cluster_key", "cluster_candidates"}
GROUPING_DIMENSIONS = (
    "protected_workflow",
    "request_sequence_family",
    "account_or_session_behavior",
    "challenge_behavior",
    "protected_action_result",
    "timing_pattern",
    "network_or_proxy_category",
    "browser_and_protocol_observation_availability",
)
REQUIRED_CONTINUITY_DIMENSIONS = (
    "protected_workflow",
    "request_sequence_family",
    "account_or_session_behavior",
    "challenge_behavior",
    "protected_action_result",
)
CONFIDENCE_RUBRIC = {
    "name": "AATE categorical confidence rubric v1",
    "high": (
        "At least two independently collected, current, directly observed records; all source ratings are A or B; "
        "all information ratings are 1 or 2; protected-workflow continuity is complete; and no material "
        "contradiction is unresolved."
    ),
    "moderate": (
        "At least two independent current records preserve workflow continuity and at least one is direct, but a "
        "direct-observation gap, weaker rating, missing supporting dimension, historical dependency, or bounded "
        "alternative explanation remains."
    ),
    "low": (
        "Support is single-source, entirely inferred or historical, materially contradictory, weakly rated, or "
        "missing the protected-workflow and protected-action continuity needed for the conclusion."
    ),
    "numeric_mapping": "none; FIRST ratings and course confidence are not probabilities",
}
REQUIRED_EVENT_FIELDS = {
    "event_id",
    "observed_at",
    "evidence_state",
    "collection_source",
    "source_reliability",
    "information_reliability",
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
    """Load the deterministic fixture and reject incomplete or answer-labeled records."""
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("events"), list):
        raise ValueError("traffic-intelligence fixture must contain an events list")
    if not isinstance(raw.get("indicators"), list):
        raise ValueError("traffic-intelligence fixture must contain an indicators list")
    for number, event in enumerate(raw["events"], start=1):
        if not isinstance(event, dict):
            raise ValueError(f"event {number} must be an object")
        prohibited = PROHIBITED_ANSWER_FIELDS & event.keys()
        if prohibited:
            raise ValueError(f"event {number} contains prohibited answer fields: {sorted(prohibited)}")
        missing = REQUIRED_EVENT_FIELDS - event.keys()
        if missing:
            raise ValueError(f"event {number} is missing {sorted(missing)}")
        if event["source_reliability"] not in SOURCE_RATINGS:
            raise ValueError(f"event {number} has an invalid source rating")
        if event["information_reliability"] not in INFORMATION_RATINGS:
            raise ValueError(f"event {number} has an invalid information rating")
        sequence = event["request_sequence"]
        if not isinstance(sequence, list) or not all(isinstance(item, str) for item in sequence):
            raise ValueError(f"event {number} request_sequence must be a string list")
    return raw


def _normalized_request(request: str) -> str:
    method, separator, raw_path = request.strip().partition(" ")
    if not separator:
        return request.strip().upper()
    path = raw_path.split("?", maxsplit=1)[0].rstrip("/") or "/"
    path = re.sub(r"/\d+(?=/|$)", "/:id", path)
    return f"{method.upper()} {path.casefold()}"


def _request_sequence_family(event: dict[str, Any]) -> str:
    return " -> ".join(_normalized_request(str(request)) for request in event["request_sequence"])


def _account_or_session_family(value: str) -> str:
    lowered = value.casefold()
    if "unavailable" in lowered:
        return "unavailable"
    if "proof" in lowered and ("session a to b" in lowered or "second session" in lowered):
        return "cross-session-proof-transfer"
    if "account names" in lowered and "one session" in lowered:
        return "multi-account-one-session"
    if "historical" in lowered:
        return "historical-only"
    return "other-recorded-session-behavior"


def _challenge_family(value: str) -> str:
    lowered = value.casefold()
    if "not observed" in lowered:
        return "unavailable"
    if "proof" in lowered and any(token in lowered for token in ("replay", "transferred", "accepted")):
        return "cross-session-proof-transfer"
    if "challenge" in lowered and any(token in lowered for token in ("issued", "encountered", "abandoned")):
        return "challenge-encountered"
    if "historical" in lowered:
        return "historical-only"
    return "other-recorded-challenge-behavior"


def _protected_action_family(value: str) -> str:
    lowered = value.casefold()
    if lowered == "unknown":
        return "unavailable"
    if "completed" in lowered or "returned 200" in lowered:
        return "completed"
    if "blocked" in lowered or "no account page" in lowered:
        return "blocked"
    return "other-recorded-result"


def _timing_family(value: str) -> str:
    lowered = value.casefold()
    if "historical" in lowered:
        return "historical-only"
    if any(token in lowered for token in ("700-", "900 ms", "within 1 second")):
        return "subsecond-to-one-second"
    if any(token in lowered for token in ("1100", "1200", "1300")):
        return "about-one-second"
    return "other-recorded-timing"


def _observation_availability(event: dict[str, Any]) -> str:
    browser = str(event["browser_javascript"]).casefold()
    protocol = str(event["http_tls"]).casefold()
    browser_available = not any(token in browser for token in ("unavailable", "no browser"))
    protocol_available = not any(token in protocol for token in ("missing", "partial", "historical"))
    if browser_available and protocol_available:
        return "browser-and-protocol"
    if browser_available:
        return "browser-only"
    if protocol_available:
        return "protocol-only"
    return "unavailable"


def evidence_dimensions(event: dict[str, Any]) -> dict[str, str]:
    """Normalize observable behavior into the dimensions used by the grouping algorithm."""
    workflow = str(event["protected_workflow"])
    if workflow.casefold().startswith("unknown"):
        workflow = "unavailable"
    return {
        "protected_workflow": workflow,
        "request_sequence_family": _request_sequence_family(event),
        "account_or_session_behavior": _account_or_session_family(str(event["account_or_session_behavior"])),
        "challenge_behavior": _challenge_family(str(event["challenge_behavior"])),
        "protected_action_result": _protected_action_family(str(event["protected_action_result"])),
        "timing_pattern": _timing_family(str(event["timing"])),
        "network_or_proxy_category": str(event["network_proxy_category"]),
        "browser_and_protocol_observation_availability": _observation_availability(event),
    }


def _has_required_continuity(event: dict[str, Any], dimensions: dict[str, str]) -> bool:
    return (
        event["evidence_state"] != HISTORICAL_EVIDENCE_STATE
        and len(event["request_sequence"]) >= 3
        and all(dimensions[name] not in {"unavailable", "historical-only"} for name in REQUIRED_CONTINUITY_DIMENSIONS)
    )


def _behavior_cluster_id(members: list[dict[str, Any]], dimensions: dict[str, str]) -> str:
    session_family = dimensions["account_or_session_behavior"]
    workflow = dimensions["protected_workflow"].removeprefix("synthetic-")
    member_dimensions = [evidence_dimensions(member) for member in members]
    if all(item["challenge_behavior"] == "cross-session-proof-transfer" for item in member_dimensions) and all(
        item["protected_action_result"] == "completed" for item in member_dimensions
    ):
        return f"{workflow}-sequence-with-challenge-replay"
    if session_family == "multi-account-one-session":
        return f"multi-account-{'login' if workflow.endswith('login') else workflow}-sequence"
    requests = "-".join(_normalized_request(str(item)).split(" ", maxsplit=1)[-1].strip("/").replace("/", "-")
                        for item in members[0]["request_sequence"])
    return f"{workflow}-{requests}-sequence"


def _confidence(events: list[dict[str, Any]], continuity_complete: bool) -> dict[str, Any]:
    current = [event for event in events if event["evidence_state"] != HISTORICAL_EVIDENCE_STATE]
    direct = [event for event in current if event["evidence_state"] in DIRECT_EVIDENCE_STATES]
    independent_sources = {str(event["collection_source"]) for event in current}
    material_contradictions = sorted(
        {
            str(item)
            for event in events
            for item in event.get("material_contradictions", [])
        }
    )
    strong_sources = bool(current) and all(
        str(event["source_reliability"]) in STRONG_SOURCE_RATINGS for event in current
    )
    strong_information = bool(current) and all(
        str(event["information_reliability"]) in STRONG_INFORMATION_RATINGS for event in current
    )
    historical_only = not current
    if (
        historical_only
        or len(independent_sources) < 2
        or not direct
        or material_contradictions
        or not continuity_complete
    ):
        level = "low"
    elif len(direct) >= 2 and strong_sources and strong_information:
        level = "high"
    else:
        level = "moderate"
    return {
        "level": level,
        "rubric": CONFIDENCE_RUBRIC["name"],
        "basis": {
            "independent_current_observations": len(independent_sources),
            "current_direct_observations": len(direct),
            "strong_source_ratings": strong_sources,
            "strong_information_ratings": strong_information,
            "protected_workflow_continuity": continuity_complete,
            "material_contradictions": material_contradictions,
            "historical_only_support": historical_only,
            "plausible_alternative_explanations": sorted(
                {str(item) for event in events for item in event["alternative_explanations"]}
            ),
        },
        "not_a_probability": True,
    }


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    """Create an explicit observation without upgrading inference to fact."""
    return {
        "event_id": event["event_id"],
        "observed_at": event["observed_at"],
        "evidence_state": event["evidence_state"],
        "collection_source": event["collection_source"],
        "source_rating": {
            "code": event["source_reliability"],
            "meaning": SOURCE_RATINGS[str(event["source_reliability"])],
        },
        "information_rating": {
            "code": event["information_reliability"],
            "meaning": INFORMATION_RATINGS[str(event["information_reliability"])],
        },
        "evidence_dimensions": evidence_dimensions(event),
        "raw_behavior": {
            name: event[name]
            for name in (
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
            )
        },
        "contradictions": event.get("contradictions", []),
        "alternative_explanations": event["alternative_explanations"],
    }


def _candidate_cluster_ids(
    event: dict[str, Any],
    dimensions: dict[str, str],
    profiles: list[dict[str, Any]],
) -> list[str]:
    event_requests = {_normalized_request(str(request)) for request in event["request_sequence"]}
    candidates: list[str] = []
    for profile in profiles:
        same_workflow = (
            dimensions["protected_workflow"] != "unavailable"
            and dimensions["protected_workflow"] == profile["protected_workflow"]
        )
        sequence_overlap = bool(event_requests & set(profile["normalized_requests"]))
        if same_workflow or sequence_overlap:
            candidates.append(str(profile["cluster_id"]))
    return sorted(candidates)


def cluster_events(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Derive groups from workflow and behavior dimensions, preserving ambiguity."""
    dimensions_by_id = {str(event["event_id"]): evidence_dimensions(event) for event in events}
    anchor_groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for event in events:
        dimensions = dimensions_by_id[str(event["event_id"])]
        if not _has_required_continuity(event, dimensions):
            continue
        key = (dimensions["protected_workflow"], dimensions["request_sequence_family"])
        anchor_groups.setdefault(key, []).append(event)

    profiles: list[dict[str, Any]] = []
    clusters: list[dict[str, Any]] = []
    assigned_ids: set[str] = set()
    for (workflow, _sequence), members in sorted(anchor_groups.items()):
        if len(members) < 2:
            continue
        members = sorted(members, key=lambda item: str(item["event_id"]))
        reference = dimensions_by_id[str(members[0]["event_id"])]
        cluster_id = _behavior_cluster_id(members, reference)
        member_dimensions = [dimensions_by_id[str(member["event_id"])] for member in members]
        matched_dimensions = [
            f"{name}={member_dimensions[0][name]}"
            for name in GROUPING_DIMENSIONS
            if member_dimensions[0][name] not in {"unavailable", "historical-only"}
            and all(item[name] == member_dimensions[0][name] for item in member_dimensions[1:])
        ]
        missing_dimensions = sorted(
            {
                name
                for name in GROUPING_DIMENSIONS
                if any(item[name] in {"unavailable", "historical-only"} for item in member_dimensions)
            }
        )
        differing_dimensions = sorted(
            name
            for name in GROUPING_DIMENSIONS
            if len({item[name] for item in member_dimensions}) > 1
        )
        contradictions = sorted(
            {
                str(value)
                for member in members
                for value in member.get("contradictions", [])
            }
            | {f"member observations differ on {name}" for name in differing_dimensions}
        )
        alternatives = sorted(
            {str(value) for member in members for value in member["alternative_explanations"]}
        )
        normalized_requests = [_normalized_request(str(item)) for item in members[0]["request_sequence"]]
        historical_support = sorted(
            str(event["event_id"])
            for event in events
            if event["evidence_state"] == HISTORICAL_EVIDENCE_STATE
            and str(event["protected_workflow"]) == workflow
            and bool({_normalized_request(str(item)) for item in event["request_sequence"]} & set(normalized_requests))
        )
        continuity_complete = all(
            all(item[name] not in {"unavailable", "historical-only"} for name in REQUIRED_CONTINUITY_DIMENSIONS)
            for item in member_dimensions
        )
        confidence = _confidence(members, continuity_complete)
        member_ids = [str(member["event_id"]) for member in members]
        assigned_ids.update(member_ids)
        profiles.append(
            {
                "cluster_id": cluster_id,
                "protected_workflow": workflow,
                "normalized_requests": normalized_requests,
            }
        )
        clusters.append(
            {
                "cluster_id": cluster_id,
                "member_event_ids": member_ids,
                "matched_dimensions": matched_dimensions,
                "missing_dimensions": missing_dimensions,
                "contradictions": contradictions,
                "alternative_explanations": alternatives,
                "current_supporting_observations": member_ids,
                "historical_only_observations": historical_support,
                "confidence": confidence,
                "attribution_limitation": "behavior grouping does not establish an actor",
            }
        )

    ambiguous: list[dict[str, Any]] = []
    for event in events:
        event_id = str(event["event_id"])
        if event_id in assigned_ids:
            continue
        dimensions = dimensions_by_id[event_id]
        missing_or_contradictory = sorted(
            {
                name
                for name in REQUIRED_CONTINUITY_DIMENSIONS
                if dimensions[name] in {"unavailable", "historical-only"}
            }
            | {str(value) for value in event.get("contradictions", [])}
        )
        if len(event["request_sequence"]) < 3:
            missing_or_contradictory.append("normalized request-sequence continuity is incomplete")
        ambiguous.append(
            {
                "event_id": event_id,
                "candidate_behavior_families": _candidate_cluster_ids(event, dimensions, profiles),
                "insufficient_or_contradictory_dimensions": sorted(set(missing_or_contradictory)),
                "alternative_explanations": event["alternative_explanations"],
            }
        )
    return sorted(clusters, key=lambda item: str(item["cluster_id"])), sorted(
        ambiguous, key=lambda item: str(item["event_id"])
    )


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


def _most_common_text(events: list[dict[str, Any]], field: str) -> str:
    return Counter(str(event[field]) for event in events).most_common(1)[0][0]


def emulation_plan(cluster: dict[str, Any], events_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Derive the bounded plan and exact regression from the selected cluster members."""
    members = [events_by_id[str(event_id)] for event_id in cluster["member_event_ids"]]
    sequence = list(members[0]["request_sequence"])
    challenge = _most_common_text(members, "challenge_behavior")
    protected_result = _most_common_text(members, "protected_action_result")
    confidence = {
        "level": cluster["confidence"]["level"],
        "rubric": cluster["confidence"]["rubric"],
        "not_a_probability": True,
    }
    regression = {
        "cluster_id": cluster["cluster_id"],
        "source_member_event_ids": cluster["member_event_ids"],
        "confidence": confidence,
        "setup": "reset the bundled loopback fixture",
        "action": f"reproduce {sequence!r} with the observed challenge behavior: {challenge}",
        "pass": "Session B is rejected; Session A succeeds once; Session A replay is rejected",
        "evidence": ["session", "action", "origin", "nonce", "expiry", "use-count", "HTTP status"],
    }
    return {
        "selected_cluster_id": cluster["cluster_id"],
        "behavior_being_emulated": {
            "normalized_request_sequence": sequence,
            "challenge_behavior": challenge,
            "observed_protected_action_result": protected_result,
        },
        "evidence_supporting_it": cluster["member_event_ids"],
        "confidence": confidence,
        "alternative_explanations": cluster["alternative_explanations"],
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
        "exact_regression_test": regression,
    }


def calculate(fixture: dict[str, Any]) -> dict[str, Any]:
    """Produce the complete deterministic intelligence-to-regression output."""
    events = sorted(fixture["events"], key=lambda item: str(item["event_id"]))
    clusters, ambiguous = cluster_events(events)
    indicators = indicator_lifecycle(fixture["indicators"], date.fromisoformat(fixture["analysis_date"]))
    focus_event = str(fixture["emulation_focus_event"])
    selected = next(
        (cluster for cluster in clusters if focus_event in cluster["member_event_ids"]),
        None,
    )
    plan = (
        emulation_plan(selected, {str(event["event_id"]): event for event in events})
        if selected is not None
        else {
            "status": "not generated",
            "reason": "the focus event lacks a corroborated evidence-derived group",
            "confidence": {
                "level": "low",
                "rubric": CONFIDENCE_RUBRIC["name"],
                "not_a_probability": True,
            },
            "exact_regression_test": {
                "status": "not generated",
                "confidence": {
                    "level": "low",
                    "rubric": CONFIDENCE_RUBRIC["name"],
                    "not_a_probability": True,
                },
            },
        }
    )
    return {
        "analysis_date": fixture["analysis_date"],
        "grouping_method": {
            "name": "deterministic protected-workflow and normalized-sequence grouping",
            "dimensions": list(GROUPING_DIMENSIONS),
            "required_continuity": list(REQUIRED_CONTINUITY_DIMENSIONS),
            "rule": (
                "A proposed group needs at least two current events with the same protected workflow and normalized "
                "request sequence plus recorded session, challenge, and protected-action continuity. Other dimensions "
                "are reported as support, missing evidence, or contradictions; infrastructure never assigns membership."
            ),
        },
        "confidence_rubric": CONFIDENCE_RUBRIC,
        "normalized_evidence": [normalize_event(event) for event in events],
        "proposed_clusters": clusters,
        "ambiguous_events": ambiguous,
        "indicator_lifecycle": indicators,
        "version_drift_explanation": (
            "obs-006 is historical fixture Chromium 132 reporting; fixture-current Playwright Chromium 149 evidence "
            "contradicts treating the implementation artifact as stable. The fixture labels are not universal browser "
            "version claims."
        ),
        "shared_infrastructure_assessment": (
            "shared-relay.example appears in multiple observations but is never a membership key; shared "
            "infrastructure alone is insufficient for grouping or attribution."
        ),
        "bounded_emulation_plan": plan,
        "regression_test_definition": plan["exact_regression_test"],
        "limitations": [
            "Synthetic identities and documentation-only infrastructure values",
            "Deterministic teaching groups, not an attribution or production prevalence system",
            "No network requests and no external enrichment",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "fixture",
        nargs="?",
        type=Path,
        default=Path("lab/fixtures/traffic_intelligence_events.json"),
    )
    args = parser.parse_args()
    print(json.dumps(calculate(load_fixture(args.fixture)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
