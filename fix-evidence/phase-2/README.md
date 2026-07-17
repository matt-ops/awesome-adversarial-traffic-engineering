# Phase 2 evidence

Phase 2 is limited to canonical lesson metadata, prerequisite/depth validation,
honest checkpoint calculations, and repair of the four checkpoint definitions.

The authoritative metadata is `curriculum/manifest.yaml`. The acceptance gate
was run after all Phase 2 curriculum and documentation changes. Each required
command has its own timestamped transcript, and `acceptance-summary.txt` records
the final exit-code matrix.

## Acceptance commands

```text
python scripts/validate_curriculum.py
python scripts/validate_sources.py
python scripts/validate_lessons.py
python scripts/check_internal_links.py
mkdocs build --strict
python -m pytest lab/tests -q
```

All six commands exited 0.

## Scope

No safety code, DDoS implementation, protocol implementation, instructional
teaching section, deployment setting, or Phase 3 quality system was changed.
The only lesson-page edits are depth or prerequisite fields in visible Progress
metadata. Module-index edits repair depth/checkpoint summaries.

The repository already contained substantial unrelated uncommitted work before
Phase 2. That work remains outside the Phase 2 commit.

Acceptance therefore describes the preserved source-first working tree plus the
scoped Phase 1 and Phase 2 commits. Producing a standalone clean-checkout release
commit is explicitly deferred to the audit's release-hygiene phase.
