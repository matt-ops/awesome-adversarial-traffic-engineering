# Integrated and deep portfolio drills

This single page supplies the additional repetitions required by the Integrated
and Deep exit ramps. It reuses completed lessons; it does not introduce a second path.

These are rubric-driven **portfolio drills**, not independently packaged
exercises. A packaged exercise would have its own README, starter material,
learner task, expected artifact, tests or grading criteria, solution, and
explanation. The counted lists below reuse shared course code, tests, lessons,
and answer guidance and therefore make no package claim.

## Lab contract

- Authorization boundary: bundled source/fixtures/loopback target and named provider assignments only
- Target: the exact local file, function, endpoint, or assigned provider target in each row
- Adversary objective: build repeated evidence across attack, tooling, design, and communication domains
- Protected action: named by each selected workflow/control/resource case
- Baseline: copy the relevant completed module baseline before extending it
- Hypothesis: one falsifiable sentence per drill before execution/review
- Changed variable: one declared value or one deliberately coherent set
- Fixed variables: target/version/reset/evidence schema and all unrelated inputs
- Success: the row's artifact meets its stated proof and limitation requirement
- Evidence: code/test output, review trace, threat model, design diagram, or report section
- Limitations: repetition increases practice, not production scale or universal coverage
- Cleanup: stop/reset local services and keep private material outside the repository
- Remediation: state the failed invariant and measurable legitimate/hostile outcomes
- Retest: repeat the original attack with the same success definition after the change

## Six Python drills

Complete all six. Existing code is the teacher: read the named function, explain
it, run its test, then make the stated artifact or test extension.

| # | Code and exact action | Required evidence |
|---:|---|---|
| 1 | `load_jsonl()` in `lab/analysis/analyze.py`: add a temporary malformed line outside the repository and confirm the error names file/line; restore the original input | parser trace, observed error, and why partial line location matters |
| 2 | `summarize()` in `lab/tooling/client.py`: calculate fixture population/label counts and add a local test for one missing-population record | JSON summary, denominator, and passing test |
| 3 | `bounded_fetch()`: run totals 6 with concurrency 1 and 2; test that concurrency 6 is rejected before requests | two traces, rejected boundary, task/semaphore diagram |
| 4 | `fetch_with_retry()`: prove `503 -> 200`, add a mocked `403` one-attempt test, and retain the fourth-attempt rejection | status/attempt/delay trace and two safety assertions |
| 5 | `generate_client_hello()`/`parse_outer_fields()` in `lab/protocol/compare.py`: compare default/ALPN, then add a parser rejection test for a non-handshake record | byte/field comparison and passing negative test |
| 6 | `validate_local_url()`/`LoadEnvelope.validate()` in `lab/safety.py`: add parameterized cases for credentials, non-loopback IP, rate-total mismatch, and excessive expensive work | test matrix explaining which check executes before traffic |

## Two Applied domain mocks

Run each for 25 minutes, then use the Module 10 scorecard and repair the weakest answer.

1. **Automated adversary and browser control:** trace a protected workflow,
   compare manual/headed/headless/HTTP populations, state a blocked-baseline
   hypothesis, change one controlled signal relationship, prove the action, and
   answer one false-positive and one alternate-explanation challenge.
2. **Application-layer resilience:** map traffic dimension to resource and health,
   choose one bounded scenario, state ceilings/abort/recovery, interpret shedding
   versus failure, and define remediation plus exact hostile/legitimate retest.

Artifact: two prompt/answer outlines, evidence links, scorecards, and exact repairs.

## Ten code-review drills

Use the [secure code-review method](../../modules/09-tooling-code-review/04-secure-code-review.md).
For every row record entry, transformation, decision, protected effect, proof,
limitation, remediation invariant, negative test, legitimate positive test, and telemetry.

| # | Review target | Adversary question |
|---:|---|---|
| 1 | `reserve()` | Can an unauthenticated request mutate inventory? |
| 2 | `challenge()` plus `protected_report()` | Is authorization bound to subject, action, expiry, nonce, and use count? |
| 3 | `limited_report()` | Can a caller-selected key reset one principal's budget? |
| 4 | `fetch_with_retry()` | Which failures repeat work, and what bounds attempts/time? |
| 5 | `validate_local_url()` | Can URL parsing, credentials, alternate IP notation, or host normalization escape the allowlist? |
| 6 | `LoadEnvelope.validate()` | Can individually valid values combine into excessive total/expensive work? |
| 7 | `/api/control/observe` and `/api/control/protected` | Are top/frame/worker observations joined to one session and token use? |
| 8 | `cacheable_report()` | Can caller-controlled bypass/cache keys force repeated expensive work? |
| 9 | `unstable_report()` | Are operation identity and side effects safe under retry/replay? |
| 10 | `lab/load/bounded.js` | Do setup, scenario requests, retries, and teardown fit the worst-case formula and recovery gate? |

## Five threat-model drills

Use the same compact structure for each: adversary objective, protected action,
entry points, assets/state, trust boundaries, preconditions, abuse sequence,
controls/assumptions, effect evidence, legitimate near-neighbor, and retest.

| Model | Required module evidence |
|---|---|
| Credential/account abuse | Module 04 auth attempts, identities, sessions, and provider-assigned lab |
| Inventory/promotion workflow | request/state diagram and `5 -> 4` authorization proof |
| Browser-control evasion | Module 05 population matrix plus Module 06 action/replay evidence |
| Cross-layer protocol identity | browser claim, ClientHello/HTTP observer, intermediary boundary, and fingerprint limits |
| Application-resource exhaustion | Module 08 resource chain, seven bounded scenarios, collateral population, and recovery |

## Five system-design drills

For each design, draw components/trust boundaries and specify inputs, state,
decision, failure mode, observability, privacy/accessibility risk, degradation,
remediation migration, hostile tests, and legitimate tests.

| Design | Required design decision |
|---|---|
| Session/action-bound challenge | token subject/action/nonce/expiry/use binding and replay telemetry |
| Workflow-aware rate control | server-derived identity, endpoint/workflow key, window, fairness, and fail mode |
| Resilient report service | cache/admission, work budget, retry owner, dependency isolation, shedding, and recovery objective |
| Cross-context browser observation | page/frame/worker collection, session join, freshness, versioning, and accessible/privacy-preserving alternatives |
| Evidence and retest pipeline | immutable raw capture, derived metrics, decision log, artifact version, access control, cleanup, and regression ownership |

## Integrated report package

Expand the Module 10 finding into six to eight pages plus a one-page executive
summary. Required order:

1. Authorization, scope, target/version, and adversary objective
2. Immediate recon and request/control/resource map
3. Legitimate and blocked baselines
4. Hypothesis, changed/fixed variables, and safety envelope
5. Protected action or service-effect evidence
6. Residual anomalies, legitimate populations, and alternate explanations
7. Root cause evidence, remediation invariant, and exact negative/positive retest
8. Limitations, residual risk, cleanup, and owner

The executive summary names the consequence, bounded evidence, action requested,
and retest criterion without tool-level detail.

## Deep research package

Complete these after the Integrated report:

1. **Original research question:** one falsifiable question that changes a
   control assumption, identity relationship, version, or legitimate population.
2. **Browser-version drift:** repeat one blocked/evasion experiment with a pinned
   second browser/framework version or approved version fixture.
3. **Deeper runtime instrumentation:** add one read-only observation across
   frame, worker, or CDP boundary and explain its observer effects.
4. **Deeper protocol comparison:** add one declared runtime/intermediary/version
   condition and preserve observation-point limits.
5. **Privacy/accessibility false-positive study:** select at least two legitimate
   privacy/accessibility-like fixture populations; compare control outcome and collateral risk.
6. **Identity-coherence study:** change one deliberately coherent profile, list
   every relationship, and record residual anomalies.
7. **Remediation implementation:** implement one local invariant, run the exact
   former attack and legitimate positive matrix, and preserve the diff/tests.
8. **Public-safe portfolio:** publish only synthetic facts, reproducible method,
   evidence, limits, and learning; omit private recordings and confidential context.
9. **Additional mocks:** run two new domain combinations and repair every failed prerequisite.
10. **First-90-day research proposal:** define questions, stakeholder/control
    dependencies, lab prerequisites, evidence, safety/rollback, milestones, and non-claims.

## Validation commands

| Command | Expected result |
|---|---|
| `python -m unittest discover -s lab/tests -v` | all baseline and added regression tests pass |
| `python -m mypy lab scripts` | strict types pass |
| `python -m ruff check lab scripts` | lint/security rules pass |
| `npm run typecheck` | browser client types pass |

If an extension changes course code, do not accept the portfolio until these
checks and the relevant former attack/legitimate retest both pass.
