"""Report evidence-based progress through the single AATE path."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_MODULES = (
    "safety",
    "request_path",
    "automated_abuse",
    "browser_automation",
    "bot_detection",
    "edge_ddos",
    "python_code_review",
    "experiment_reporting",
    "interview",
)
GATES = (("foundation", 1), ("applied", 2), ("integrated", 3), ("deep", 4))
GATE_FIELDS = ("explain", "build_or_run", "measure", "communicate", "operate_safely")
LEVEL_NAMES = {0: "not started", 1: "Foundation", 2: "Applied", 3: "Integrated", 4: "Deep"}


def load_progress(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"progress file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}:{exc.lineno}: invalid JSON-compatible YAML: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError("progress root must be an object")
    return payload


def validate_progress(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    modules = data.get("modules")
    if not isinstance(modules, dict):
        return ["modules must be an object"]
    if tuple(modules) != EXPECTED_MODULES:
        errors.append(f"modules must appear in canonical order: {', '.join(EXPECTED_MODULES)}")
    for module_id in EXPECTED_MODULES:
        module = modules.get(module_id)
        if not isinstance(module, dict):
            errors.append(f"module {module_id!r} must be an object")
            continue
        level = module.get("level")
        if not isinstance(level, int) or isinstance(level, bool) or level not in range(5):
            errors.append(f"module {module_id!r} level must be an integer from 0 through 4")
        artifacts = module.get("artifacts")
        if not isinstance(artifacts, list) or any(not isinstance(item, str) or not item.strip() for item in artifacts):
            errors.append(f"module {module_id!r} artifacts must be a list of non-empty paths")
    gate_evidence = data.get("gate_evidence")
    if not isinstance(gate_evidence, dict):
        errors.append("gate_evidence must be an object")
        return errors
    for gate, _ in GATES:
        evidence = gate_evidence.get(gate)
        if not isinstance(evidence, dict):
            errors.append(f"gate {gate!r} evidence must be an object")
            continue
        if tuple(evidence) != GATE_FIELDS:
            errors.append(f"gate {gate!r} must contain: {', '.join(GATE_FIELDS)}")
        elif any(not isinstance(evidence[field], bool) for field in GATE_FIELDS):
            errors.append(f"gate {gate!r} evidence values must be booleans")
    return errors


def gate_status(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    modules = data["modules"]
    statuses: dict[str, dict[str, Any]] = {}
    for gate, target_level in GATES:
        below = [module_id for module_id in EXPECTED_MODULES if modules[module_id]["level"] < target_level]
        missing_artifacts = [
            module_id
            for module_id in EXPECTED_MODULES
            if modules[module_id]["level"] >= target_level and not modules[module_id]["artifacts"]
        ]
        missing_evidence = [field for field in GATE_FIELDS if not data["gate_evidence"][gate][field]]
        statuses[gate] = {
            "target_level": target_level,
            "below_level": below,
            "missing_artifacts": missing_artifacts,
            "missing_evidence": missing_evidence,
            "satisfied": not below and not missing_artifacts and not missing_evidence,
        }
    return statuses


def recommended_tasks(data: dict[str, Any], statuses: dict[str, dict[str, Any]]) -> list[str]:
    modules = data["modules"]
    current_gate = next((gate for gate, _ in GATES if not statuses[gate]["satisfied"]), None)
    if current_gate is None:
        return ["Keep artifacts reproducible and revisit them when dependencies or browser versions change"]
    status = statuses[current_gate]
    target_level = status["target_level"]
    tasks: list[str] = []
    for module_id in status["below_level"]:
        tasks.append(f"Complete {modules[module_id]['title']} — {LEVEL_NAMES[target_level]}")
    for module_id in status["missing_artifacts"]:
        tasks.append(f"Record the required {LEVEL_NAMES[target_level]} artifact for {modules[module_id]['title']}")
    for field in status["missing_evidence"]:
        tasks.append(f"Review and record {current_gate} gate evidence: {field.replace('_', ' ')}")
    return tasks[:3]


def render_report(data: dict[str, Any]) -> str:
    statuses = gate_status(data)
    current_gate = next((gate for gate, _ in GATES if not statuses[gate]["satisfied"]), None)
    checkpoint = "All four checkpoints complete" if current_gate is None else f"{current_gate.title()} in progress"
    target_level = 4 if current_gate is None else statuses[current_gate]["target_level"]
    completed = [
        module["title"] for module in data["modules"].values() if module["level"] >= target_level
    ]
    missing_artifacts = [
        module["title"]
        for module in data["modules"].values()
        if module["level"] > 0 and not module["artifacts"]
    ]

    lines = [
        f"Current checkpoint: {checkpoint}",
        f"Completed modules at current level: {len(completed)}/9",
    ]
    if completed:
        lines.extend(f"  - {title}" for title in completed)
    lines.append("Missing artifacts:")
    lines.extend(f"  - {title}" for title in missing_artifacts)
    if not missing_artifacts:
        lines.append("  - None missing for completed modules")
    lines.append("Recommended next three tasks:")
    for index, task in enumerate(recommended_tasks(data, statuses), start=1):
        lines.append(f"  {index}. {task}")
    lines.append("Gate status:")
    for gate, _ in GATES:
        label = "satisfied" if statuses[gate]["satisfied"] else "not satisfied"
        lines.append(f"  - {gate.title()}: {label}")
    lines.append("This report describes curriculum evidence; it is not a hiring prediction.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path("curriculum/progress.yaml"))
    parser.add_argument("--check", action="store_true", help="validate the schema and exit")
    args = parser.parse_args()
    try:
        data = load_progress(args.file)
        errors = validate_progress(data)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2
    if args.check:
        print("Progress schema: PASS")
        return 0
    print(render_report(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
