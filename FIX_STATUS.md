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
