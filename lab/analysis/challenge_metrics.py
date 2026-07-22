"""Calculate deterministic challenge-control and customer-impact metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "population",
    "category",
    "attempts",
    "challenges_issued",
    "challenge_solves",
    "challenge_bypasses",
    "protected_actions_completed",
    "challenge_abandonments",
    "repeated_challenges",
    "added_latency_ms",
    "false_positive_challenges",
    "attacker_time_seconds",
    "attacker_cost_usd",
    "alternate_workflow_successes",
}


def load_fixture(path: Path) -> list[dict[str, Any]]:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("rows"), list):
        raise ValueError("challenge metric fixture must contain a rows list")
    rows: list[dict[str, Any]] = []
    for number, raw_row in enumerate(raw["rows"], start=1):
        if not isinstance(raw_row, dict):
            raise ValueError(f"challenge metric row {number} must be an object")
        missing = REQUIRED_FIELDS - raw_row.keys()
        if missing:
            raise ValueError(f"challenge metric row {number} is missing {sorted(missing)}")
        rows.append(raw_row)
    return rows


def ratio(numerator: int | float, denominator: int | float) -> float:
    return round(float(numerator) / float(denominator), 4) if denominator else 0.0


def calculate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    populations: dict[str, dict[str, Any]] = {}
    for row in rows:
        population = str(row["population"])
        attempts = int(row["attempts"])
        issued = int(row["challenges_issued"])
        completed = int(row["protected_actions_completed"])
        attacker_successes = completed + int(row["alternate_workflow_successes"])
        populations[population] = {
            "category": str(row["category"]),
            "challenge_issuance_rate": ratio(issued, attempts),
            "solve_or_bypass_rate": ratio(int(row["challenge_solves"]) + int(row["challenge_bypasses"]), attempts),
            "protected_action_completion_rate": ratio(completed, attempts),
            "challenge_abandonment_rate": ratio(int(row["challenge_abandonments"]), attempts),
            "average_added_latency_ms_per_attempt": ratio(int(row["added_latency_ms"]), attempts),
            "repeated_challenge_rate": ratio(int(row["repeated_challenges"]), issued),
            "legitimate_false_positive_rate": ratio(int(row["false_positive_challenges"]), attempts),
            "attacker_time_seconds_per_successful_protected_action": ratio(
                int(row["attacker_time_seconds"]), completed
            ),
            "attacker_cost_usd_per_successful_protected_action": ratio(float(row["attacker_cost_usd"]), completed),
            "alternate_workflow_success_rate": ratio(int(row["alternate_workflow_successes"]), attempts),
            "abuse_outcome": (
                "not-applicable"
                if not str(row["category"]).startswith("attacker")
                else "displaced"
                if int(row["alternate_workflow_successes"]) > 0
                else "mostly-stopped"
                if attacker_successes < attempts / 2
                else "not-stopped"
            ),
        }

    manual = populations["manual-legitimate-user"]
    near_neighbor = populations["legitimate-automation-or-accessibility-like-client"]
    customer_impact = {
        "accessibility_privacy_tool_and_test_automation_proxy": {
            "challenge_issuance_delta": round(
                near_neighbor["challenge_issuance_rate"] - manual["challenge_issuance_rate"], 4
            ),
            "protected_action_completion_delta": round(
                near_neighbor["protected_action_completion_rate"] - manual["protected_action_completion_rate"], 4
            ),
            "abandonment_delta": round(
                near_neighbor["challenge_abandonment_rate"] - manual["challenge_abandonment_rate"], 4
            ),
            "added_latency_ms_per_attempt_delta": round(
                near_neighbor["average_added_latency_ms_per_attempt"]
                - manual["average_added_latency_ms_per_attempt"],
                4,
            ),
            "limitation": (
                "One synthetic composite is a test proxy, not evidence about real disabled users or privacy tools."
            ),
        }
    }
    return {
        "populations": populations,
        "customer_impact": customer_impact,
        "interpretation": (
            "The stock attacker is mostly stopped, while the adapted/replaying attacker succeeds and displaces abuse "
            "to an alternate workflow; the near-neighbor population bears substantial false-positive and "
            "abandonment cost."
        ),
        "limitations": [
            "Small deterministic synthetic dataset",
            "Rates teach calculation and comparison, not production prevalence or causal effect",
            "Attacker cost excludes tool development, infrastructure, and external solver markets",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="?", type=Path, default=Path("lab/fixtures/challenge_metrics.json"))
    args = parser.parse_args()
    print(json.dumps(calculate(load_fixture(args.fixture)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
