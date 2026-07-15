# Scripts

- `python scripts/progress.py` reports the current checkpoint, completed modules, missing artifacts, next three tasks, and all gate states.
- `python scripts/progress.py --check` validates the progress schema.
- `python scripts/validate_curriculum.py` enforces the authoritative one-path contract.
- `python scripts/validate_links.py` checks relative Markdown targets without network access.
- `python scripts/build_docs.py` stages canonical sources in ignored `.docs-build/` for MkDocs; it does not create alternate lesson sources.
- `python -m lab.analysis.analyze` evaluates deterministic detector fixtures.

No script creates a remote, pushes code, targets an external service, or disables safety controls.
