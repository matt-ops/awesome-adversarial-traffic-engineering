# Synthetic code-review cases

Review only the bundled application. For each case, trace attacker input to a
decision and protected effect, then locate or design the named test.

| Case | Entry and effect | Evidence to inspect | Required acceptance test |
|---|---|---|---|
| Reservation authorization | `ReserveRequest` changes `INVENTORY` | `reserve()` and workflow-authorization test | unauthenticated mutation denied; authorized reservation succeeds |
| Challenge replay | challenge token authorizes protected report | `challenge()`, `protected_report()`, replay test | wrong session/action/reuse/expiry denied; intended use succeeds once |
| Rate-key rotation | caller `session_id` selects counter key | `limited_report()` and key-rotation test | alternate caller-controlled key cannot reset one principal's budget |
| Retry budget | failed operation repeats local work | `fetch_with_retry()` and tooling tests | non-retryable error stops; fourth attempt rejected; transient case succeeds within budget |

Do not report deliberate fixture behavior as an external vulnerability. The
artifact is a review method: entry, transformation, decision, effect, proof,
limitation, remediation invariant, and exact retest.
