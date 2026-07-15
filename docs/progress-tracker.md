# Progress tracking

`curriculum/progress.yaml` is JSON-compatible YAML so the standard-library progress script can read it without an extra package.

## Recording a module

Set `level` only after the matching completion test passes. Add evidence paths under `artifacts`, for example:

```json
"safety": {
  "title": "Safety and red-team engagement discipline",
  "level": 1,
  "artifacts": ["artifacts/foundation/safe-engagement-checklist.md"]
}
```

Levels are cumulative. Level 3 means Foundation, Applied, and Integrated are complete.

## Recording a gate

Each gate has five booleans: `explain`, `build_or_run`, `measure`, `communicate`, and `operate_safely`. Set them from a real review session, not inferred from elapsed time.

## Report behavior

`python scripts/progress.py` prints:

- current checkpoint;
- completed modules at the current level;
- missing artifacts;
- recommended next three tasks;
- satisfaction state for all four gates.

`python scripts/progress.py --check` exits nonzero for an invalid schema. It does not require a gate to be complete.

