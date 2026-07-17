# 7 days cumulative

<!-- checkpoint-id: 7-days -->
<!-- calculated-minutes: 2385 -->

This cumulative Applied selection adds context/CDP observation, provider-assigned authentication work, cross-context control reconnaissance, basic TLS/HTTP interpretation, and one bounded Layer 7 experiment.

## Time calculation

- Calculated required lesson time: **2385 minutes (39.75 hours)**
- Declared cumulative range: **1800-2400 minutes (30-40 hours)**
- Maximum lesson depth: **Applied**

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

## Required artifacts

Every artifact in the final column of the required-lessons table is required.
The artifact remains learner-created; its linked lesson defines the procedure,
expected output, interpretation, cleanup, and pass gate.

Use the [Applied portfolio drill definitions](../labs/deep/portfolio-drills.md#two-applied-domain-mocks) for three Python drills, four code-review drills, one short report, and two domain mocks.

## Capability claim

Functional hands-on readiness in bounded local and provider-authorized exercises.

## What this does not claim

You are not claiming controlled evasion, cross-time replay analysis, Integrated protocol reasoning, a complete portfolio, or production experience.

## Exit gate

Reproduce the listed local and provider-authorized work with versions, raw output, cleanup, and limitations; show the context matrix, basic protocol interpretation, and bounded-load result.
