# Synthetic code-review cases

Review only the bundled application. For each case, trace attacker input to a
decision and protected effect, then locate or design the named test.

## Lab contract

- Authorization boundary: bundled source and in-process synthetic tests only
- Target: `lab/app/main.py`, clients, tooling, and tests
- Adversary objective: locate a security assumption that reaches protected state/work
- Protected action: named per reservation, report, rate-key, or retry case
- Baseline: trace intended decision/effect before proposing the alternate path
- Hypothesis: named missing binding or work-budget invariant in each row
- Changed variable: only authentication/session/action/use key or retry failure class
- Fixed variables: function, fixture state, input schema, effect query, and test environment
- Success: code path plus bounded test demonstrate the effect
- Evidence: line/function trace and negative/positive test design
- Limitations: deliberate local flaws; taxonomy or scanner match alone is not proof
- Cleanup: reset in-process state; no external target exists
- Remediation: enforce the named subject/object/action/resource invariant
- Retest: former attack fails while intended near-neighbor succeeds

| Case | Entry and effect | Evidence to inspect | Required acceptance test |
|---|---|---|---|
| Reservation authorization | `ReserveRequest` changes `INVENTORY` | `reserve()` and workflow-authorization test | unauthenticated mutation denied; authorized reservation succeeds |
| Challenge replay | challenge token authorizes protected report | `challenge()`, `protected_report()`, replay test | wrong session/action/reuse/expiry denied; intended use succeeds once |
| Rate-key rotation | caller `session_id` selects counter key | `limited_report()` and key-rotation test | alternate caller-controlled key cannot reset one principal's budget |
| Retry budget | failed operation repeats local work | `fetch_with_retry()` and tooling tests | non-retryable error stops; fourth attempt rejected; transient case succeeds within budget |

Do not report deliberate fixture behavior as an external vulnerability. The
exercise result is a review method: entry, transformation, decision, effect, proof,
limitation, remediation invariant, and exact retest.
