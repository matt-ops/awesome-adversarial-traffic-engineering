"""Evaluate deterministic classifier thresholds without relabeling unknown events."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

KNOWN_LABELS = {"legitimate", "abuse"}
REQUIRED_POPULATION_FIELDS = {
    "population",
    "count",
    "label",
    "baseline_score",
    "post_adaptation_score",
    "protected_actions_if_flagged",
    "protected_actions_if_allowed",
}
REQUIRED_COST_FIELDS = {
    "review_usd_per_flag",
    "challenge_operation_usd_per_flag",
    "legitimate_near_neighbor_cost_usd_per_challenge",
}
REQUIRED_BASE_RATE_FIELDS = {
    "legitimate_events",
    "abusive_events",
    "false_positive_rate",
    "recall",
}
SCORE_FIELDS = {"baseline_score", "post_adaptation_score"}
PROTECTED_ACTION_FIELDS = {
    "protected_actions_if_flagged",
    "protected_actions_if_allowed",
}


def _bounded_number(value: Any, label: str, *, lower: float = 0.0, upper: float = 1.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    number = float(value)
    if not math.isfinite(number) or not lower <= number <= upper:
        raise ValueError(f"{label} must be between {lower:g} and {upper:g}")
    return number


def _nonnegative_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label} must be nonnegative")
    return number


def load_fixture(path: Path) -> dict[str, Any]:
    """Load and validate the compact aggregate fixture."""
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("classifier fixture must be an object")
    thresholds = raw.get("thresholds")
    populations = raw.get("populations")
    costs = raw.get("costs")
    base_rate = raw.get("base_rate_example")
    if not isinstance(thresholds, list) or len(thresholds) < 2:
        raise ValueError("classifier fixture requires at least two thresholds")
    if not isinstance(populations, list) or not populations:
        raise ValueError("classifier fixture requires populations")
    if not isinstance(costs, dict):
        raise ValueError("classifier fixture requires costs")
    if not isinstance(base_rate, dict):
        raise ValueError("classifier fixture requires a base_rate_example")

    normalized_thresholds = [
        _bounded_number(value, f"threshold {number}")
        for number, value in enumerate(thresholds, start=1)
    ]
    if len(set(normalized_thresholds)) != len(normalized_thresholds):
        raise ValueError("classifier thresholds must be unique")

    missing_costs = REQUIRED_COST_FIELDS - costs.keys()
    if missing_costs:
        raise ValueError(f"classifier costs are missing {sorted(missing_costs)}")
    for name, value in costs.items():
        _nonnegative_number(value, f"cost {name}")

    missing_base_rate = REQUIRED_BASE_RATE_FIELDS - base_rate.keys()
    if missing_base_rate:
        raise ValueError(f"base_rate_example is missing {sorted(missing_base_rate)}")
    for name in ("legitimate_events", "abusive_events"):
        value = base_rate[name]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"base_rate_example {name} must be a nonnegative integer")
    for name in ("false_positive_rate", "recall"):
        _bounded_number(base_rate[name], f"base_rate_example {name}")

    population_names: set[str] = set()
    has_unknown_or_delayed_label = False
    for number, population in enumerate(populations, start=1):
        if not isinstance(population, dict):
            raise ValueError(f"population {number} must be an object")
        missing = REQUIRED_POPULATION_FIELDS - population.keys()
        if missing:
            raise ValueError(f"population {number} is missing {sorted(missing)}")
        if population["label"] not in KNOWN_LABELS | {None}:
            raise ValueError(f"population {number} has an unsupported label")
        has_unknown_or_delayed_label |= population["label"] is None
        name = population["population"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"population {number} name must be a non-empty string")
        if name in population_names:
            raise ValueError(f"population names must be unique: {name}")
        population_names.add(name)
        count = population["count"]
        if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            raise ValueError(f"population {number} count must be a positive integer")
        for field in SCORE_FIELDS:
            _bounded_number(population[field], f"population {number} {field}")
        for field in PROTECTED_ACTION_FIELDS:
            protected_count = population[field]
            if (
                isinstance(protected_count, bool)
                or not isinstance(protected_count, int)
                or not 0 <= protected_count <= count
            ):
                raise ValueError(
                    f"population {number} {field} must be an integer between 0 and count"
                )
    if not has_unknown_or_delayed_label:
        raise ValueError("classifier fixture requires at least one unknown or delayed-label population")
    return raw


def ratio(numerator: int | float, denominator: int | float) -> float | None:
    """Return a four-place ratio, preserving an undefined denominator."""
    if denominator == 0:
        return None
    return round(float(numerator) / float(denominator), 4)


def evaluate_threshold(
    populations: list[dict[str, Any]], costs: dict[str, Any], threshold: float, score_field: str
) -> dict[str, Any]:
    """Calculate one threshold window; unknown labels never enter the matrix."""
    matrix = {"true_positive": 0, "false_positive": 0, "true_negative": 0, "false_negative": 0}
    total_flagged = 0
    known_events = 0
    unknown_events = 0
    flagged_unknown = 0
    near_neighbor_challenges = 0
    completions = {"stock-abusive-client": 0, "adapted-abusive-client": 0}
    population_results: list[dict[str, Any]] = []

    for population in populations:
        name = str(population["population"])
        count = int(population["count"])
        label = population["label"]
        score = float(population[score_field])
        flagged = score >= threshold
        flagged_count = count if flagged else 0
        total_flagged += flagged_count

        if label is None:
            unknown_events += count
            flagged_unknown += flagged_count
            matrix_bucket = "excluded-unknown-label"
        else:
            known_events += count
            abusive = label == "abuse"
            if flagged and abusive:
                matrix_bucket = "true_positive"
            elif flagged:
                matrix_bucket = "false_positive"
            elif abusive:
                matrix_bucket = "false_negative"
            else:
                matrix_bucket = "true_negative"
            matrix[matrix_bucket] += count

        if name == "legitimate-automation-or-accessibility-like-near-neighbor":
            near_neighbor_challenges = flagged_count
        if name in completions:
            completions[name] = int(
                population["protected_actions_if_flagged"]
                if flagged
                else population["protected_actions_if_allowed"]
            )
        population_results.append(
            {
                "population": name,
                "label": label if label is not None else "unknown-or-delayed",
                "score": score,
                "flagged": flagged,
                "count": count,
                "matrix_bucket": matrix_bucket,
            }
        )

    tp = matrix["true_positive"]
    fp = matrix["false_positive"]
    tn = matrix["true_negative"]
    fn = matrix["false_negative"]
    review_cost = round(total_flagged * float(costs["review_usd_per_flag"]), 2)
    challenge_cost = round(total_flagged * float(costs["challenge_operation_usd_per_flag"]), 2)
    neighbor_cost = round(
        near_neighbor_challenges * float(costs["legitimate_near_neighbor_cost_usd_per_challenge"]), 2
    )
    return {
        "threshold": threshold,
        "score_field": score_field,
        "confusion_matrix": matrix,
        "precision": ratio(tp, tp + fp),
        "recall": ratio(tp, tp + fn),
        "false_positive_rate": ratio(fp, fp + tn),
        "false_negative_rate": ratio(fn, tp + fn),
        "known_label_events": known_events,
        "unknown_or_delayed_label_events": unknown_events,
        "unknown_label_coverage": ratio(flagged_unknown, unknown_events),
        "total_flagged_events": total_flagged,
        "legitimate_near_neighbor_challenges": near_neighbor_challenges,
        "estimated_review_cost_usd": review_cost,
        "estimated_challenge_operation_cost_usd": challenge_cost,
        "estimated_legitimate_near_neighbor_cost_usd": neighbor_cost,
        "estimated_total_operational_cost_usd": round(review_cost + challenge_cost + neighbor_cost, 2),
        "stock_attacker_protected_actions_completed": completions["stock-abusive-client"],
        "adapted_attacker_protected_actions_completed": completions["adapted-abusive-client"],
        "populations": population_results,
    }


def base_rate_workload(example: dict[str, Any]) -> dict[str, Any]:
    """Show why a small false-positive rate can dominate a rare positive class."""
    legitimate = int(example["legitimate_events"])
    abusive = int(example["abusive_events"])
    false_positives = round(legitimate * float(example["false_positive_rate"]))
    true_positives = round(abusive * float(example["recall"]))
    return {
        **example,
        "false_positive_alerts": false_positives,
        "true_positive_alerts": true_positives,
        "total_alerts": false_positives + true_positives,
        "alert_precision": ratio(true_positives, true_positives + false_positives),
        "interpretation": "A 0.1% false-positive rate creates more false alerts than true alerts in this window.",
    }


def calculate(fixture: dict[str, Any]) -> dict[str, Any]:
    """Evaluate baseline and post-adaptation scores at every candidate threshold."""
    populations = fixture["populations"]
    thresholds = sorted(float(value) for value in fixture["thresholds"])
    costs = fixture["costs"]
    windows = {
        window: [evaluate_threshold(populations, costs, threshold, score_field) for threshold in thresholds]
        for window, score_field in (
            ("baseline", "baseline_score"),
            ("post_adaptation", "post_adaptation_score"),
        )
    }
    return {
        "analysis_date": fixture["analysis_date"],
        "class_base_rate": ratio(
            sum(int(row["count"]) for row in populations if row["label"] == "abuse"),
            sum(int(row["count"]) for row in populations if row["label"] in KNOWN_LABELS),
        ),
        "windows": windows,
        "base_rate_example": base_rate_workload(fixture["base_rate_example"]),
        "interpretation": [
            "Raising the post-adaptation threshold improves precision but reduces recall.",
            "The adapted population crosses the former boundary and completes more protected actions at 0.75.",
            "Unknown or delayed labels remain coverage counts and are excluded from the confusion matrix.",
            (
                "A bypass is bounded evidence about this threshold and population, "
                "not proof that the classifier is useless."
            ),
            "A lower detector score is not offensive success; the protected action remains the success criterion.",
        ],
        "limitations": [
            "Synthetic aggregate counts and transparent scores",
            "No production prevalence, model internals, causal attribution, or live customer labels",
            "Cost inputs are exercise assumptions rather than commercial-control prices",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="?", type=Path, default=Path("lab/fixtures/classifier_tradeoffs.json"))
    args = parser.parse_args()
    print(json.dumps(calculate(load_fixture(args.fixture)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
