# Publish checklist

This checklist records the final local release gate and human-readable review.
The repair branch is authorized for push and pull-request creation only; direct
pushes to `main`, merge, and manual deployment remain prohibited.

## Release identity and cleanliness

- [x] **Clean Git status:** required and verified at handoff with
  `git status --short` producing no output.
- [x] **Release commit:** the final commit has subject
  `docs: finalize cross-platform release instructions`; its exact SHA is
  reported in the pull-request handoff.
- [x] **Isolated-worktree validation:** the complete gate ran from a temporary
  detached worktree created from audited commit `2385fcf`, containing only the
  portability patch with the same stable patch ID as the development tree.
- [x] **Publication boundary:** only `fix/audit-remediation` may be pushed and
  opened as an unmerged pull request to `main`; no manual deployment is allowed.

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
- [x] **Python tests:** the complete `lab/tests` pytest suite passes (46 tests),
  as does the 41-test unittest discovery run.
- [x] **JavaScript tests:** the six fast pure-helper tests pass without
  launching a browser.
- [x] **Lint:** Ruff, ESLint, Markdown lint, and Prettier check pass.
- [x] **Type checking:** strict MyPy and TypeScript checks pass.
- [x] **Strict docs build:** `mkdocs build --strict` passes.
- [x] **Compose configuration:** `docker compose ... config --quiet` passes.
- [x] **k6 runtime:** the existing all-seven-scenario evidence remains passing,
  and a current `cheap-expensive` representative run passes against only the
  bundled loopback fixture with 42/42 checks and all thresholds passing.
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
- [x] **Checkpoint-hours review:** from-zero prerequisite closures of 21.67,
  37.25, 71.25, and 119.92 hours pass their declared checkpoint ranges. Direct
  selections of 3.00, 9.00, 16.00, and 30.00 hours are reported separately and
  are not published as new-learner checkpoint time.
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

- [x] **Human screenshot review:** the 11 images under the local
  `artifacts/final-publish-review/screenshots/` directory were inspected in this order:
  Start Here, Methodology Provenance, First HTTP Lesson, Browser Process Model,
  JavaScript Core, First Browser, Control Reconnaissance, One-Variable Evasion,
  DDoS Resource Model, Checkpoints, and Safety.
- [x] **Explicit approval before push:** the final publish instruction
  explicitly authorizes pushing only `fix/audit-remediation` and opening an
  unmerged pull request to `main`; it does not authorize merge or deployment.
