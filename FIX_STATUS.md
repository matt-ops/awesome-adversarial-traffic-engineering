# Targeted repair status

## Phase 1: safety boundaries and time enforcement

Status: **Phase 1 complete; acceptance passed; local commit prepared**

- Starting branch: `fix/audit-remediation`
- Starting commit: `e33b9751f67030b2a1da9e4ffd7b4f83bbda0b3d`
- Starting working tree: already dirty with the source-first remediation work;
  the complete pre-change status and diff summary are preserved in
  `fix-evidence/phase-1/starting-state.txt`.
- Phase scope: redirect-safe local targets, real wall-clock duration
  enforcement, associated tests, and matching boundary documentation only.
- Explicitly excluded: lesson rewrites, checkpoint changes, DDoS changes,
  Phase 2 work, push, deployment, and GitHub Pages changes.

### Files changed

- `lab/clients/safe_client.py`: reject every redirect, disable proxy routing,
  validate direct timeouts, enforce a monotonic deadline, and emit the distinct
  `duration_budget_exceeded` result.
- `lab/safety.py`: add the exact fixed-origin policy used by the bundled client
  while retaining the separate arbitrary-port local-development validator.
- `lab/tests/test_safe_client.py`: add the in-process HTTP redirect and duration
  test system.
- `lab/tests/test_safety.py`: test the exact fixed course origins.
- `SAFETY.md`, `docs/safety/local-target-policy.md`, and
  `docs/safety/traffic-guardrails.md`: document the implemented redirect,
  origin, deadline, timeout, rate, total, and retry behavior.
- `FIX_STATUS.md` and `fix-evidence/phase-1/`: record status and complete command
  evidence.

No lesson, checkpoint, navigation, DDoS scenario, or Phase 2 file was changed
by this phase. The scope comparison is in `fix-evidence/phase-1/scope-review.txt`.

### Tests added

Sixteen tests were added: fifteen safe-client tests plus one fixed-origin
validator test. They cover:

- local success without a redirect;
- external hostname, public IP, private-network IP, scheme, port, loop, and
  local-to-local redirect rejection;
- slow-response wall-clock enforcement;
- refusal to start after the deadline;
- remaining-budget timeout calculation;
- preservation of total and request-rate ceilings;
- a normal run and invalid direct timeouts;
- the fixed course-origin allowlist.

The existing retry-ceiling test remains in the full suite and passed.

### Implementation completed

- Fixed course-client origins have been separated from the general local
  development validator.
- The course client rejects all redirects, including unsupported-scheme and
  approved-local redirects.
- Direct request timeouts are validated and capped at two seconds.
- `run()` uses a monotonic deadline, bounds each timeout by remaining time,
  records `duration_budget_exceeded`, and does not start after the deadline.
- Deterministic in-process server and timing tests have been added.
- Safety and execution-boundary pages have been updated; lessons and
  checkpoints have not been edited in this phase.

### Acceptance results

- `python -m pytest lab/tests -q`: exit 0, 38 tests.
- `python -m unittest discover -s lab/tests -v`: exit 0, 38 tests.
- `ruff check .`: exit 0.
- repository MyPy equivalent, `mypy lab scripts`: exit 0, 30 source files.
- source, lesson, lab, bounded-load-script, and internal-link validators: exit
  0.
- `mkdocs build --strict`: exit 0.
- scoped `git diff --check` for Phase 1 tracked paths: exit 0.
- No safe-client or lab request contacted an external target. Redirect tests
  sent their first request only to an in-process loopback server and rejected
  the returned `Location` before another hop.

Complete stdout, stderr, timestamps, and exit codes are under
`fix-evidence/phase-1/`. The final matrix is in `acceptance-summary.txt`.

### Failing and corrected results

- The first focused preflight returned exit 1 because urllib surfaced a
  `file:` redirect as an HTTP 302 instead of calling its HTTP redirect handler.
  Explicit 3xx rejection fixed it; the post-fix preflight passed.
- The first executable MyPy preflight returned exit 1 for undeclared test class
  attributes. Adding `ClassVar` declarations fixed it.
- The first full acceptance attempt returned exit 1 only for source validation
  because the temporary Python tool directory lacked pinned PyYAML. After
  installing `PyYAML==6.0.2`, the complete gate was rerun and passed.
- Direct `python -m ruff` and `python -m mypy` preflights returned exit 1 because
  that target-style installation exposes executable entry points but no
  runnable `__main__`. The acceptance gate used the repository-equivalent
  executables and both passed.
- Whole-working-tree `git diff --check` remains exit 2 because the pre-existing
  dirty lesson rewrite uses Markdown hard-break trailing spaces and has one
  pre-existing blank EOF. Phase 1's scoped diff check passes, and prohibited
  lesson cleanup was deliberately not performed.
- The all-files staged diff check also returns exit 2 because the required
  verbatim stdout/stderr transcripts preserve trailing spaces emitted by Git,
  PowerShell, and unittest. The implementation/documentation-only Phase 1 diff
  check remains exit 0; evidence output was not rewritten or falsely cleaned.

### Known limitations

- The Foundation policy rejects every redirect, even to another approved local
  origin. It does not implement a validated redirect-following mode.
- Socket scheduling can finish a timeout a small amount after the mathematical
  deadline. The timeout supplied to the network call never exceeds remaining
  time, the overrun is recorded distinctly, and no later request starts.
- Ephemeral ports are available only through the separate general-development
  validator. Tests temporarily patch the fixed-origin constant for their
  in-process loopback server; the CLI exposes no equivalent bypass.
- Pinned pytest and PyYAML packages were downloaded into `C:\tmp\aate-dev` for
  validation. That setup traffic was not a lab target request and is recorded
  in `tool-setup.txt`.
- The repository retains substantial pre-existing, unrelated uncommitted work.
  Only the Phase 1 paths listed above are included in the local Phase 1 commit.

### Exact next phase

Phase 2 is curriculum integrity: machine-readable lesson depth,
prerequisites/estimates, checkpoint dependency validation, and checkpoint
budget repair. It has **not** been started and requires a separate instruction.

Phase 1 local commit message:

```text
fix: enforce redirect-safe targets and wall-clock load budgets
```

---

## Phase 2: curriculum integrity

Status: **Phase 2 complete; acceptance passed; local commit prepared**

- Starting branch: `fix/audit-remediation`
- Starting commit: `8baff6ba6a5b1536851a604e0f9b4e83e3ea16c6`
- Phase 1 confirmation: Phase 1 is the current starting commit, its recorded
  ten-command acceptance matrix is all exit 0, and a fresh 38-test lab run passed
  before Phase 2 edits.
- Phase scope: canonical lesson metadata, prerequisite/depth validation, honest
  checkpoint time calculations, four checkpoint repairs, and matching
  navigation/progress language only.
- Explicitly excluded: instructional rewrites, safety code, DDoS implementation,
  protocol implementation, Phase 3 work, push, and deployment.

### Canonical metadata and dependency repairs

- `curriculum/manifest.yaml` is the one authoritative manifest for 50 canonical
  lessons, 11 module indexes, and four cumulative checkpoints.
- Lesson counts are 24 Foundation, 12 Applied, 10 Integrated, and 4 Deep.
- Every lesson has an ID, path, module, title, depth, `estimated_minutes`, exact
  prerequisite IDs, required artifacts, and source IDs.
- The 50-node prerequisite graph has no missing IDs, cycles, or forward-depth
  dependencies.
- Browser-evasion hypothesis, one-variable, and identity-coherence lessons were
  moved to Integrated because their blocked-baseline dependency is Integrated.
- Bounded application-layer load testing was moved to Applied so the Applied
  checkpoint can honestly require one bounded Layer 7 experiment.
- TLS ClientHello now depends on Foundation network-evidence and signal-family
  lessons instead of the later browser-evasion module.
- Foundation finding and role-narrative lessons now depend on Foundation
  evidence work rather than Integrated secure-review or briefing work.
- Automated Abuse, Browser Evasion, and DDoS module indexes now agree with the
  canonical lesson depths.

### Checkpoint hours before and after

The old pages had no machine-readable membership. Expanding their linked module
sections and direct lesson links, deduplicating lessons, and excluding
unestimated lab/portfolio pages produces these exact lower bounds:

| Checkpoint | Before | After |
|---|---:|---:|
| 24 focused hours | 3,895 minutes / 64h55m | 1,425 minutes / 23h45m |
| 7 days cumulative | 5,575 minutes / 92h55m | 2,385 minutes / 39h45m |
| 21 days cumulative | 6,835 minutes / 113h55m | 4,305 minutes / 71h45m |
| 6 weeks cumulative | 7,435 minutes / 123h55m | 6,105 minutes / 101h45m |

The repaired checkpoint pages contain required canonical lesson links,
calculated time, required artifacts, a capability claim, explicit non-claims,
and an exit gate. The 24-hour claim is exactly:

> Foundation and informational readiness, not browser-evasion competence.

### Validator coverage

`scripts/validate_curriculum.py` rejects:

- missing metadata and duplicate lesson IDs or paths;
- missing prerequisite IDs, cycles, and forward-depth dependencies;
- checkpoint lessons or prerequisite closure above the depth ceiling;
- checkpoint totals outside the declared range;
- module-index links that overstate lesson depth;
- visible lesson depth, estimate, artifact, or source-ID disagreement;
- checkpoint links to non-canonical lessons; and
- checkpoint artifacts that are undefined, unowned, or absent from the page.

It prints lesson counts by depth, checkpoint lesson counts, exact minutes and
hours, prerequisite-closure sizes, and all validation errors.

### Files changed

- `curriculum/manifest.yaml` and `scripts/validate_curriculum.py`: canonical
  metadata and the complete Phase 2 validator.
- `docs/checkpoints/*.md`: manifest-backed 24-hour, 7-day, 21-day, and 6-week
  definitions.
- `docs/path.md`, `docs/progress.md`, `docs/start-here.md`, `mkdocs.yml`, and
  `Makefile`: calculated checkpoint navigation/progress and gate integration.
- Seven lesson Progress boxes and three module indexes: depth/prerequisite
  consistency repairs only.
- `fix-evidence/phase-2/`: starting state, before/after budget method, command
  transcripts, scope review, and acceptance summary.

No instructional teaching section, safety file, lab implementation, DDoS
implementation, or protocol implementation was changed.

### Phase 2 acceptance results

- `python scripts/validate_curriculum.py`: exit 0; 50 lessons, 11 indexes, four
  depth-safe and time-valid checkpoints.
- `python scripts/validate_sources.py`: exit 0.
- `python scripts/validate_lessons.py`: exit 0.
- `python scripts/check_internal_links.py`: exit 0; 103 Markdown files.
- `mkdocs build --strict`: exit 0.
- `python -m pytest lab/tests -q`: exit 0; 38 tests.
- Focused `ruff check scripts/validate_curriculum.py`: exit 0.
- Focused strict `mypy scripts/validate_curriculum.py`: exit 0.

Complete required-gate output and timestamps are under
`fix-evidence/phase-2/`. The final matrix is in `acceptance-summary.txt`.

### Remaining limitations

- Checkpoint totals sum the explicitly required canonical lesson selections.
  Learners who have not completed a prerequisite must add its full estimate;
  every checkpoint page states this boundary.
- The old checkpoint totals are exact lower bounds for lesson time only because
  the old lab and portfolio pages did not carry estimates.
- Checkpoints are curated cumulative capability selections, not every lesson at
  or below their depth ceiling.
- Substantial unrelated pre-existing work remains uncommitted and outside the
  scoped Phase 2 commit.
- Acceptance was run against that preserved source-first working tree. The
  scoped Phase 2 commit intentionally does not absorb the pre-existing lesson,
  source-ledger, lab, or navigation rewrite and is therefore not a standalone
  clean-checkout release commit; clean release integration remains Phase 4 work.
- Phase 3 has not begun.

Phase 2 local commit message:

```text
fix: validate curriculum depth dependencies and checkpoint budgets
```

---

## Phase 3: lab and claim fidelity

Status: **Phase 3 complete; acceptance passed; local commit prepared**

- Starting branch: `fix/audit-remediation`
- Starting commit: `2c6da2d` (`fix: validate curriculum depth dependencies and checkpoint budgets`)
- Phase 1 confirmation: committed as `8baff6b`; the fresh pre-Phase 3 lab suite passed.
- Phase 2 confirmation: committed as `2c6da2d`; fresh curriculum, source,
  lesson, link, Ruff, strict MyPy, pytest, and strict MkDocs checks passed.
- Phase scope: DDoS scenario truthfulness/assertions, protocol-lab claim
  alignment, exercise-packaging language, report-generation claim alignment,
  and directly required maps/metadata/navigation/evidence only.
- Explicitly excluded: foundational lesson rewrites, checkpoint scope/time/depth
  changes, fake endpoint/workflow controls, Phase 4, push, and deployment.

### Scenario names before and after

| Before | After | Reason |
|---|---|---|
| `endpoint-specific` | `endpoint-cost-observation` | Same-endpoint low/high work is observed; no endpoint-specific quota or admission control exists. |
| `workflow-aware` | `workflow-sequence-observation` | Search/product continuity is observed; no workflow-aware identity, quota, reservation, or admission control exists. |

The other five names remain `cheap-expensive`, `cache-bypass`, `identity-key`,
`retry-amplification`, and `recovery`.

### Controls implemented or intentionally not implemented

- Retained the real application cache and per-session quota fixtures.
- Retained the deterministic fail-once retry fixture and the global Nginx
  per-IP rate limit.
- Added cache priming and two fixed-key setup calls so cache/identity outcomes
  have deterministic baselines. Worst-case lifecycle accounting increased from
  two to four requests inside the unchanged 100-request ceiling.
- Intentionally did not add endpoint-specific or workflow-aware controls. The
  two scenarios are observations and all current claims say so.
- Did not claim the unchanged global Nginx limit is a scenario before/after
  treatment.

### Assertions added

- `cheap-expensive`: `work=100` and report latency greater than health latency.
- `cache-bypass`: warmed cache hit, bypass miss/fresh work, same digest.
- `identity-key`: pre-seeded fixed key `429`, rotated key `200` with count 1.
- `endpoint-cost-observation`: work values 1/100 and higher-work latency greater.
- `workflow-sequence-observation`: search exposes `demo-1`; product resolves it.
- `retry-amplification`: exact `503 -> 200`, same operation, accepted attempt 2.
- `recovery`: work 50 and teardown health `200` within 1,000 ms.

`scripts/validate_load_scripts.py` now requires the new names and assertion
markers and rejects the two obsolete executable names. The app test suite adds
one complete deterministic scenario-fixture contract test and resets synthetic
state before every app test.

### Protocol claims narrowed

The visible capability is now **Protocol identity foundations**. Executable
support is limited to Python/OpenSSL ClientHello generation, a declared ALPN
configuration change with uncontrolled per-handshake variation, selected outer
TLS fields, raw byte/digest comparison, and fixed-loopback plain HTTP metadata.

Removed unsupported executable claims that the helper parses ALPN values or
reports differing byte offsets. The lab/course map now explicitly says it does
not compare Chrome with Playwright TLS, calculate JA4/JA4H, capture HTTP/2
settings, exercise HTTP/3/QUIC, or measure proxy-induced transport changes.
Those topics remain source-led theory/evidence planning.

### Exercise claims changed

The counted six Python, ten code-review, five threat-model, and five
system-design assignments are now explicitly **portfolio drills**. The page
states they are not independent packaged exercises with a per-case README,
starter, task, artifact, tests/grading criteria, solution, and explanation. The
21-day checkpoint link changed only to the renamed `#six-python-drills` anchor;
checkpoint membership, time, depth, and capability architecture are unchanged.

### Report capability changed

The supported capability is **report template and validated sample**. The
static `lab/reports/synthetic-finding.md` and finding/briefing lab explicitly say
there is no report generator or report-generation command. No generator was
added or claimed.

### Files changed by Phase 3

- Executable assertions/tests: `lab/load/bounded.js`,
  `scripts/validate_load_scripts.py`, and `lab/tests/test_app.py`.
- DDoS truthfulness: the Module 08 index/lessons, bounded-load lab, and both
  working copies of the lab-to-course map.
- Protocol claims: Module 07 naming/ClientHello boundary, the protocol lab,
  capability audit, manifest/navigation/path/progress labels, and one
  browser-evasion index qualifier.
- Exercise/report wording: portfolio drills, 21-day anchor, finding/briefing
  lab, sample report, and rewrite status.
- Status/evidence: `FIX_STATUS.md` and `fix-evidence/phase-3/`.

No foundational instructional sequence was rewritten. No checkpoint lesson,
estimate, prerequisite, time range, depth ceiling, or exit gate changed.

### Phase 3 acceptance results

- `python scripts/validate_sources.py`: exit 0.
- `python scripts/validate_lessons.py`: exit 0; 50 lessons, 11 indexes.
- `python scripts/validate_labs.py`: exit 0; 11 labs, 29 command records.
- `python scripts/validate_load_scripts.py`: exit 0; truthful names/assertions.
- `python scripts/validate_curriculum.py`: exit 0; checkpoint totals unchanged.
- `python scripts/check_internal_links.py`: exit 0; 103 Markdown files.
- `python -m pytest lab/tests -q`: exit 0; 39 tests.
- `ruff check .`: exit 0.
- `mypy .`: exit 0; 31 source files.
- `npm run typecheck`: exit 0.
- `mkdocs build --strict`: exit 0.

Complete stdout, stderr, UTC timestamps, and exit codes are under
`fix-evidence/phase-3/`. The final matrix is `acceptance-summary.txt`.

### Optional local k6 result

`Get-Command k6` found no k6 executable, so the optional local scenario rerun
was skipped exactly as permitted by the phase prompt. No tool was downloaded and
no substitute container was pulled. Node syntax parsing, the load validator,
and deterministic application fixture tests passed. No external target was used.

### Known limitations

- The two observation-only cases do not become mitigation tests without a real
  changed control and before/after assertion.
- Runtime latency checks use intentionally large bounded CPU-work differences;
  they remain local observations, not portable performance thresholds.
- Recovery proves one immediate health response under 1,000 ms, not queue drain,
  dependency recovery, sustained health, or production capacity.
- The protocol lab remains Python/OpenSSL plus plain HTTP only.
- The portfolio drill counts do not represent independently packaged exercises.
- Reporting remains a learner-written template/validated sample, not generated.
- The repository retains pre-existing unrelated source-first work. The Phase 3
  commit is scoped not to absorb that work; clean release integration is Phase 4.

### Exact next phase

Phase 4 is release hygiene and clean integration. It has **not** begun. No push,
deployment, GitHub Pages change, prompt cleanup, or release packaging occurred.

Phase 3 local commit message:

```text
fix: align resilience scenarios and course claims with executable behavior
```
