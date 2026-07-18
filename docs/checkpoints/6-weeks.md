# 6 weeks cumulative

<!-- checkpoint-id: 6-weeks -->
<!-- direct-selection-minutes: 1800 -->
<!-- prerequisite-closure-minutes: 7195 -->

This cumulative Deep checkpoint extends the Integrated path through version
drift, protocol identity through connection reuse, bounded-load recovery,
secure code review, and the existing finding and briefing path.

## Time calculation

- Direct capability-selection time: **1800 minutes (30.00 hours)**
- From-zero prerequisite-closure time: **7195 minutes (119.92 hours)**
- Declared cumulative range: **5400-7200 minutes (90-120 hours)**
- Maximum lesson depth: **Deep**

The direct selection identifies ten capability targets. It is not the
checkpoint time for a new learner. The validator recursively closes the
prerequisite graph and sums each of the 47 lessons below exactly once, including
the complete earlier checkpoint selections.

## Direct capability selection

- `m03-l02` - first local Playwright workflow
- `m03-l05` - frames, workers, and CDP observations
- `m04-l03` - authentication and rate-control evidence
- `m06-l02` - one-variable evasion experiment
- `m10-l03` - technical briefing
- `m10-l04` - public-safe role narrative
- `m06-l05` - version-drift and residual-anomaly study
- `m07-l04` - protocol and connection-reuse observation points
- `m08-l05` - recovery, remediation, and exact retest
- `m09-l04` - secure code review through the adversary's path

## Required lessons

| ID | Canonical lesson | Depth | Minutes | Required artifact |
|---|---|---:|---:|---|
| `m00-l01` | [The authorized red-team role](../modules/00-method/01-red-team-role.md) | Foundation | 75 | `artifacts/module-00/role-comparison.md` |
| `m00-l02` | [Scope and Rules of Engagement](../modules/00-method/02-scope-and-rules.md) | Foundation | 90 | `artifacts/module-00/engagement-plan.md` |
| `m00-l03` | [Experimental method before attack execution](../modules/00-method/03-experimental-method.md) | Foundation | 100 | `artifacts/module-00/experiment-plan.md` |
| `m01-l01` | [HTTP request and response](../modules/01-http-edge/01-http-request-response.md) | Foundation | 90 | `artifacts/module-01/request-anatomy.md` |
| `m01-l02` | [Sessions and workflows](../modules/01-http-edge/02-sessions-and-workflows.md) | Foundation | 90 | `artifacts/module-01/workflow-map.md` |
| `m01-l03` | [Observe requests with DevTools Network](../modules/01-http-edge/03-devtools-network.md) | Foundation | 80 | `artifacts/module-01/manual-trace.md` |
| `m01-l04` | [Map the edge request path](../modules/01-http-edge/04-edge-request-path.md) | Applied | 100 | `artifacts/module-01/request-path.svg` |
| `m02-l01` | [Browser process model](../modules/02-browser-javascript/01-browser-process-model.md) | Foundation | 80 | `artifacts/module-02/browser-process-map.md` |
| `m02-l02` | [DOM and Web APIs](../modules/02-browser-javascript/02-dom-and-web-apis.md) | Foundation | 95 | `artifacts/module-02/dom-inventory.md` |
| `m02-l03` | [Minimum JavaScript for automation](../modules/02-browser-javascript/03-javascript-core.md) | Foundation | 180 | `artifacts/module-02/javascript-exercise.js` |
| `m02-l04` | [Promises, async, fetch, and errors](../modules/02-browser-javascript/04-async-fetch-and-errors.md) | Foundation | 120 | `artifacts/module-02/fetch-observation.js` |
| `m03-l01` | [Playwright object model](../modules/03-playwright/01-object-model.md) | Foundation | 120 | `artifacts/module-03/object-model.md` |
| `m03-l02` | [First local Playwright workflow](../modules/03-playwright/02-first-browser.md) | Foundation | 180 | `lab/telemetry/playwright-first-workflow.json` |
| `m03-l03` | [Browser contexts and storage state](../modules/03-playwright/03-contexts-and-state.md) | Foundation | 110 | `artifacts/module-03/context-state.md` |
| `m03-l04` | [Network events and evidence](../modules/03-playwright/04-network-events.md) | Foundation | 105 | `artifacts/module-03/network-evidence.md` |
| `m03-l05` | [Frames, workers, and CDP](../modules/03-playwright/05-frames-workers-and-cdp.md) | Applied | 120 | `artifacts/module-03/context-observations.json` |
| `m04-l01` | [Automated-abuse objectives](../modules/04-automated-abuse/01-abuse-objectives.md) | Foundation | 180 | `artifacts/module-04/abuse-threat-map.md` |
| `m04-l02` | [Workflow and API mapping](../modules/04-automated-abuse/02-workflow-mapping.md) | Foundation | 180 | `artifacts/module-04/local-api-map.md` |
| `m04-l03` | [Authentication and rate controls](../modules/04-automated-abuse/03-auth-and-rate-controls.md) | Applied | 240 | `artifacts/module-04/auth-rate-evidence.md` |
| `m04-l04` | [Inventory and promotion abuse](../modules/04-automated-abuse/04-inventory-and-promotion-abuse.md) | Applied | 180 | `lab/telemetry/workflow-authorization.json` |
| `m05-l01` | [Five signal families](../modules/05-control-recon/01-signal-families.md) | Foundation | 120 | `artifacts/module-05/signal-matrix.md` |
| `m05-l02` | [Browser-environment observations](../modules/05-control-recon/02-browser-environment.md) | Foundation | 120 | `artifacts/module-05/manual-browser-baseline.json` |
| `m05-l03` | [Cross-context consistency](../modules/05-control-recon/03-cross-context-consistency.md) | Applied | 180 | `artifacts/module-05/context-matrix.md` |
| `m05-l04` | [Session, behavior, and workflow signals](../modules/05-control-recon/04-session-behavior-workflow.md) | Applied | 120 | `artifacts/module-05/state-behavior-map.md` |
| `m05-l05` | [Establish the blocked baseline](../modules/05-control-recon/05-blocked-baseline.md) | Integrated | 180 | `artifacts/module-05/blocked-baseline.md` |
| `m06-l01` | [Form an evasion hypothesis](../modules/06-browser-evasion/01-evasion-hypotheses.md) | Integrated | 180 | `artifacts/module-06/evasion-plan.md` |
| `m06-l02` | [One-variable evasion experiment](../modules/06-browser-evasion/02-one-variable-experiments.md) | Integrated | 120 | `lab/telemetry/control-recon.json` |
| `m06-l03` | [Identity coherence](../modules/06-browser-evasion/03-identity-coherence.md) | Integrated | 240 | `artifacts/module-06/coherent-profile.md` |
| `m06-l04` | [Replay and temporal consistency](../modules/06-browser-evasion/04-replay-and-temporal-consistency.md) | Integrated | 180 | `artifacts/module-06/replay-temporal.md` |
| `m06-l05` | [Version drift and residual anomalies](../modules/06-browser-evasion/05-version-drift-and-residual-anomalies.md) | Deep | 240 | `artifacts/module-06/version-drift-study.md` |
| `m07-l01` | [TLS ClientHello](../modules/07-protocol-identity/01-tls-clienthello.md) | Foundation | 180 | `artifacts/module-07/clienthello.md` |
| `m07-l02` | [JA4 and JA4H as pivots](../modules/07-protocol-identity/02-ja4-and-ja4h.md) | Applied | 180 | `artifacts/module-07/ja4-interpretation.md` |
| `m07-l03` | [HTTP/2 connections and streams](../modules/07-protocol-identity/03-http2.md) | Integrated | 180 | `artifacts/module-07/http2-map.md` |
| `m07-l04` | [Proxies and connection reuse](../modules/07-protocol-identity/04-proxies-and-connection-reuse.md) | Integrated | 120 | `artifacts/module-07/observation-points.md` |
| `m08-l01` | [Resource-exhaustion model](../modules/08-ddos-resilience/01-resource-exhaustion-model.md) | Foundation | 120 | `artifacts/module-08/resource-model.md` |
| `m08-l02` | [Resilience metrics and thresholds](../modules/08-ddos-resilience/02-metrics.md) | Foundation | 120 | `artifacts/module-08/metric-plan.md` |
| `m08-l03` | [Edge and admission controls](../modules/08-ddos-resilience/03-edge-controls.md) | Applied | 180 | `artifacts/module-08/control-map.md` |
| `m08-l04` | [Bounded application-layer load testing](../modules/08-ddos-resilience/04-bounded-load-testing.md) | Applied | 240 | `artifacts/module-08/bounded-results.md` |
| `m08-l05` | [Recovery, remediation, and retest](../modules/08-ddos-resilience/05-recovery-and-retest.md) | Deep | 180 | `artifacts/module-08/recovery-retest.md` |
| `m09-l01` | [Python telemetry as evidence](../modules/09-tooling-code-review/01-python-telemetry.md) | Foundation | 180 | `artifacts/module-09/telemetry-summary.json` |
| `m09-l02` | [Async and bounded concurrency](../modules/09-tooling-code-review/02-async-and-bounded-concurrency.md) | Applied | 180 | `artifacts/module-09/concurrency-trace.md` |
| `m09-l03` | [Retries, timeouts, and jitter](../modules/09-tooling-code-review/03-retries-timeouts-and-jitter.md) | Applied | 180 | `artifacts/module-09/retry-budget.md` |
| `m09-l04` | [Secure code review through an adversary's path](../modules/09-tooling-code-review/04-secure-code-review.md) | Integrated | 300 | `artifacts/module-09/code-review.md` |
| `m10-l01` | [Finding and evidence](../modules/10-findings-interview/01-finding-and-evidence.md) | Foundation | 180 | `artifacts/module-10/finding.md` |
| `m10-l02` | [Remediation and exact retest](../modules/10-findings-interview/02-remediation-and-retest.md) | Applied | 180 | `artifacts/module-10/retest-plan.md` |
| `m10-l03` | [Technical briefing](../modules/10-findings-interview/03-technical-briefing.md) | Integrated | 180 | `artifacts/module-10/briefing.md` |
| `m10-l04` | [Public-safe role narrative](../modules/10-findings-interview/04-role-narrative.md) | Foundation | 120 | `artifacts/module-10/role-narrative.md` |

## Required artifacts

Every artifact in the final column is required, including artifacts assigned
by prerequisite lessons. The linked lesson defines its procedure, expected
output, interpretation, cleanup, and pass gate.

## Capability claim

Practitioner-depth portfolio, not proof of production expertise.

## What this does not claim

You are not claiming production expertise, universal stealth, Internet-scale
load testing, or that synthetic evidence transfers unchanged to a real control
stack. This checkpoint does not include the separate race-condition,
HTTP/3-and-QUIC, or full-mock-loop branches.

## Exit gate

Present the controlled browser experiments, version-drift study, protocol and
connection-reuse observations, bounded resilience test and exact recovery
retest, secure-review regressions, synthetic finding, briefing, and public-safe
role narrative.
