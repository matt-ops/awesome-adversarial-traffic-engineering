# 21 days cumulative

<!-- checkpoint-id: 21-days -->
<!-- calculated-minutes: 4305 -->

This cumulative Integrated selection adds a blocked baseline, controlled evasion, residual and temporal analysis, supported protocol reasoning, workflow-aware analysis, secure review, reporting, and briefing.

## Time calculation

- Calculated required lesson time: **4305 minutes (71.75 hours)**
- Declared cumulative range: **3600-4800 minutes (60-80 hours)**
- Maximum lesson depth: **Integrated**

The calculation sums each required canonical lesson exactly once. The manifest
validator checks prerequisite existence, cycles, and closure depth separately.
A learner who has not completed a prerequisite should add its full canonical
estimate rather than pretending the checkpoint title absorbs that work.

## Required lessons

| ID | Canonical lesson | Depth | Minutes | Required artifact |
|---|---|---:|---:|---|
| `m00-l01` | [The authorized red-team role](../modules/00-method/01-red-team-role.md) | Foundation | 75 | `artifacts/module-00/role-comparison.md` |
| `m01-l02` | [Sessions and workflows](../modules/01-http-edge/02-sessions-and-workflows.md) | Foundation | 90 | `artifacts/module-01/workflow-map.md` |
| `m02-l03` | [Minimum JavaScript for automation](../modules/02-browser-javascript/03-javascript-core.md) | Foundation | 180 | `artifacts/module-02/javascript-exercise.js` |
| `m03-l02` | [First local Playwright workflow](../modules/03-playwright/02-first-browser.md) | Foundation | 180 | `lab/telemetry/playwright-first-workflow.json` |
| `m04-l01` | [Automated-abuse objectives](../modules/04-automated-abuse/01-abuse-objectives.md) | Foundation | 180 | `artifacts/module-04/abuse-threat-map.md` |
| `m05-l01` | [Five signal families](../modules/05-control-recon/01-signal-families.md) | Foundation | 120 | `artifacts/module-05/signal-matrix.md` |
| `m08-l01` | [Resource-exhaustion model](../modules/08-ddos-resilience/01-resource-exhaustion-model.md) | Foundation | 120 | `artifacts/module-08/resource-model.md` |
| `m09-l01` | [Python telemetry as evidence](../modules/09-tooling-code-review/01-python-telemetry.md) | Foundation | 180 | `artifacts/module-09/telemetry-summary.json` |
| `m10-l01` | [Finding and evidence](../modules/10-findings-interview/01-finding-and-evidence.md) | Foundation | 180 | `artifacts/module-10/finding.md` |
| `m10-l04` | [Public-safe role narrative](../modules/10-findings-interview/04-role-narrative.md) | Foundation | 120 | `artifacts/module-10/role-narrative.md` |
| `m03-l05` | [Frames, workers, and CDP](../modules/03-playwright/05-frames-workers-and-cdp.md) | Applied | 120 | `artifacts/module-03/context-observations.json` |
| `m04-l03` | [Authentication and rate controls](../modules/04-automated-abuse/03-auth-and-rate-controls.md) | Applied | 240 | `artifacts/module-04/auth-rate-evidence.md` |
| `m05-l03` | [Cross-context consistency](../modules/05-control-recon/03-cross-context-consistency.md) | Applied | 180 | `artifacts/module-05/context-matrix.md` |
| `m07-l02` | [JA4 and JA4H as pivots](../modules/07-protocol-identity/02-ja4-and-ja4h.md) | Applied | 180 | `artifacts/module-07/ja4-interpretation.md` |
| `m08-l04` | [Bounded application-layer load testing](../modules/08-ddos-resilience/04-bounded-load-testing.md) | Applied | 240 | `artifacts/module-08/bounded-results.md` |
| `m04-l05` | [Race conditions and resource limits](../modules/04-automated-abuse/05-race-and-resource-limits.md) | Integrated | 240 | `artifacts/module-04/limit-overrun-report.md` |
| `m05-l05` | [Establish the blocked baseline](../modules/05-control-recon/05-blocked-baseline.md) | Integrated | 180 | `artifacts/module-05/blocked-baseline.md` |
| `m06-l01` | [Form an evasion hypothesis](../modules/06-browser-evasion/01-evasion-hypotheses.md) | Integrated | 180 | `artifacts/module-06/evasion-plan.md` |
| `m06-l02` | [One-variable evasion experiment](../modules/06-browser-evasion/02-one-variable-experiments.md) | Integrated | 120 | `lab/telemetry/control-recon.json` |
| `m06-l03` | [Identity coherence](../modules/06-browser-evasion/03-identity-coherence.md) | Integrated | 240 | `artifacts/module-06/coherent-profile.md` |
| `m06-l04` | [Replay and temporal consistency](../modules/06-browser-evasion/04-replay-and-temporal-consistency.md) | Integrated | 180 | `artifacts/module-06/replay-temporal.md` |
| `m07-l03` | [HTTP/2 connections and streams](../modules/07-protocol-identity/03-http2.md) | Integrated | 180 | `artifacts/module-07/http2-map.md` |
| `m07-l04` | [Proxies and connection reuse](../modules/07-protocol-identity/04-proxies-and-connection-reuse.md) | Integrated | 120 | `artifacts/module-07/observation-points.md` |
| `m09-l04` | [Secure code review through an adversary's path](../modules/09-tooling-code-review/04-secure-code-review.md) | Integrated | 300 | `artifacts/module-09/code-review.md` |
| `m10-l03` | [Technical briefing](../modules/10-findings-interview/03-technical-briefing.md) | Integrated | 180 | `artifacts/module-10/briefing.md` |

## Required artifacts

Every artifact in the final column of the required-lessons table is required.
The artifact remains learner-created; its linked lesson defines the procedure,
expected output, interpretation, cleanup, and pass gate.

Use the [Integrated portfolio drill definitions](../labs/deep/portfolio-drills.md#six-python-exercises) for the full Python, code-review, threat-model, system-design, report, executive-summary, and mock set.

## Capability claim

Interview-loop readiness with an integrated, defensible synthetic portfolio.

## What this does not claim

You are not claiming original research, version-drift coverage across releases, production-scale resilience testing, or universal bypass ability.

## Exit gate

Present the blocked baseline, controlled change, protected-action result, residual anomalies, protocol boundaries, resilience evidence, secure-review regressions, six-to-eight-page report, executive summary, and full mock loop.
