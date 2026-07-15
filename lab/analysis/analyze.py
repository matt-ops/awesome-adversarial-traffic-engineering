"""Evaluate the educational detector on labeled JSONL fixtures."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from lab.detectors.rules import score_event


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: expected an object")
        records.append(record)
    return records


def evaluate(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    matrix = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    populations: dict[str, dict[str, int]] = defaultdict(lambda: {"events": 0, "positives": 0, "false_positives": 0})
    outputs = []
    for record in records:
        result = score_event(record)
        predicted = result["decision"] != "allow"
        actual = bool(record.get("is_abuse", False))
        matrix["tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"] += 1
        population = str(record.get("population", "unknown"))
        populations[population]["events"] += 1
        populations[population]["positives"] += int(predicted)
        populations[population]["false_positives"] += int(predicted and not actual)
        outputs.append({"event_id": record.get("event_id"), **result})

    tp, fp, tn, fn = (matrix[key] for key in ("tp", "fp", "tn", "fn"))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    false_positive_rate = fp / (fp + tn) if fp + tn else 0.0
    return {
        "confusion_matrix": matrix,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "false_positive_rate": round(false_positive_rate, 4),
        "populations": dict(populations),
        "outputs": outputs,
        "limitations": [
            "Small deterministic synthetic fixture",
            "Transparent educational rules, not a production detector",
            "No real population diversity, drift, privacy governance, or enforcement feedback",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="?", type=Path, default=Path("lab/fixtures/requests.jsonl"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    summary = evaluate(load_jsonl(args.fixture))
    rendered = json.dumps(summary, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

