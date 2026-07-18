# Publish checklist

This checklist records the local release-candidate gate. The release remains
local until a human reviews the screenshots and explicitly authorizes a push.

## Release identity and cleanliness

- [x] **Clean Git status:** required and verified at handoff with
  `git status --short` producing no output.
- [x] **Release commit:** the commit containing this checklist has subject
  `chore: prepare source-first course release candidate`; its exact SHA is
  recorded in the local `fix-evidence/phase-4/release-commit.txt` and
  `FIX_STATUS.md` review records.
- [x] **Clean-worktree validation:** the complete gate is run from a temporary
  worktree created from that release commit, not from the development tree.
- [x] **No push or deployment:** Phase 4 performs neither operation.

## Automated acceptance

- [x] **Source validation:** schema, source IDs, lesson citations, synthesis
  labels, and source-review metadata pass.
- [x] **Curriculum validation:** depth, prerequisites, checkpoint budgets,
  links, closure, and artifacts pass.
- [x] **Lesson validation:** all 50 canonical lessons and 11 module indexes pass.
- [x] **Lab validation:** all 11 lab contracts, 29 command mappings, and the
  validated sample report pass.
- [x] **Safety tests:** local-target, redirect, timeout, wall-clock, rate, total,
  retry, and fixed-origin tests pass.
- [x] **Python tests:** the complete `lab/tests` pytest suite passes.
- [x] **JavaScript tests:** the five fast pure-helper tests pass without
  launching a browser.
- [x] **Lint:** Ruff, ESLint, Markdown lint, and Prettier check pass.
- [x] **Type checking:** strict MyPy and TypeScript checks pass.
- [x] **Strict docs build:** `mkdocs build --strict` passes.
- [x] **Compose configuration:** `docker compose ... config --quiet` passes; no
  containers or meaningful load run during the release check.
- [x] **Fixture analysis:** deterministic fixture analysis passes.

## Release-content review

- [x] **External-link review:** 46 external ledger URLs were checked on
  2026-07-17: 39 successful responses, 6 recorded redirects, 1 transient HTTP
  429, and no malformed or permanent-not-found URLs. Transient failures do not
  block local builds.
- [x] **Secret review:** the Git release tree contains no high-confidence
  private keys, service tokens, local user paths, or prohibited private
  development paths.
- [x] **Employer-confidentiality review:** the release-tree scan finds no
  employer-specific URLs or email markers; course examples remain synthetic.
- [x] **Checkpoint-hours review:** 23.75, 39.75, 71.75, and 101.75 cumulative
  lesson hours remain within their declared checkpoint ranges.
- [x] **Scenario-name review:** the executable observation cases remain
  `endpoint-cost-observation` and `workflow-sequence-observation`; they do not
  claim unimplemented mitigations.
- [x] **Protocol-claim review:** executable claims remain limited to protocol
  identity foundations using Python/OpenSSL ClientHello material and loopback
  plain HTTP.
- [x] **Exercise-claim review:** the counted portfolio work remains labeled as
  drills, not independently packaged exercises.
- [x] **Report-capability review:** the repository provides a validated sample
  and learner-written template, not a report generator.

## Public-tree exclusions

The release intentionally excludes local prompt/specification inputs, repair
playbooks, raw Phase 1-4 transcripts, audit bundles, old course archives,
redundant ZIP files, remediation screenshots, caches, generated sites, and
scratch outputs. `.gitignore` keeps the preserved local copies outside the Git
release tree.

## Human review gate

- [ ] **Human screenshot review:** inspect the 11 images under the local
  `artifacts/release-review/screenshots/` directory in this order:
  Start Here, Methodology Provenance, First HTTP Lesson, Browser Process Model,
  JavaScript Core, First Browser, Control Reconnaissance, One-Variable Evasion,
  DDoS Resource Model, Checkpoints, and Safety.
- [ ] **Explicit approval before push:** a human must approve the content and
  screenshots in a new instruction. This checklist does not authorize push or
  deployment.
