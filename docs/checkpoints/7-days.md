# 7 days cumulative

<!-- checkpoint-id: 7-days -->
<!-- direct-selection-minutes: 885 -->
<!-- prerequisite-closure-minutes: 2210 -->

This cumulative Applied checkpoint extends the first browser workflow through
context and CDP observation, workflow mapping, provider-authorized
authentication/rate-control analysis, and local challenge-proof enforcement.

## Time calculation

- Direct capability-selection time: **885 minutes (14.75 hours)**
- From-zero prerequisite-closure time: **2210 minutes (36.83 hours)**
- Declared cumulative range: **1800-2400 minutes (30-40 hours)**
- Maximum lesson depth: **Applied**

The direct selection identifies five capability targets. It is not the
checkpoint time for a new learner. The validator recursively closes the
prerequisite graph and sums each of the 16 lessons below exactly once, including
the complete 24-hour checkpoint selection. Optional appendix study is not
included in checkpoint time.

## Direct capability selection

- `m03-l02` - first local Playwright workflow
- `m03-l04` - browser-context state and network evidence
- `m03-l05` - frames, workers, and CDP observations
- `m04-l03` - authentication and rate-control evidence
- `m04-l06` - challenge lifecycle, proof binding, protected enforcement, and customer impact

## Required lessons

| ID | Canonical lesson | Depth | Minutes |
|---|---|---:|---:|
| `m01-l01` | [HTTP request and response](../modules/01-http-edge/01-http-request-response.md) | Foundation | 90 |
| `m01-l02` | [Sessions and workflows](../modules/01-http-edge/02-sessions-and-workflows.md) | Foundation | 90 |
| `m01-l03` | [Observe requests with DevTools Network](../modules/01-http-edge/03-devtools-network.md) | Foundation | 80 |
| `m02-l01` | [Browser process model](../modules/02-browser-javascript/01-browser-process-model.md) | Foundation | 80 |
| `m02-l02` | [DOM and Web APIs](../modules/02-browser-javascript/02-dom-and-web-apis.md) | Foundation | 95 |
| `m02-l03` | [Minimum JavaScript for automation](../modules/02-browser-javascript/03-javascript-core.md) | Foundation | 180 |
| `m02-l04` | [Promises, async, fetch, and errors](../modules/02-browser-javascript/04-async-fetch-and-errors.md) | Foundation | 120 |
| `m03-l01` | [Playwright object model](../modules/03-playwright/01-object-model.md) | Foundation | 120 |
| `m03-l02` | [First local Playwright workflow](../modules/03-playwright/02-first-browser.md) | Foundation | 180 |
| `m03-l03` | [Browser contexts and storage state](../modules/03-playwright/03-contexts-and-state.md) | Foundation | 110 |
| `m03-l04` | [Network events and evidence](../modules/03-playwright/04-network-events.md) | Foundation | 105 |
| `m03-l05` | [Frames, workers, and CDP](../modules/03-playwright/05-frames-workers-and-cdp.md) | Applied | 120 |
| `m04-l01` | [Automated-abuse objectives](../modules/04-automated-abuse/01-abuse-objectives.md) | Foundation | 180 |
| `m04-l02` | [Workflow and API mapping](../modules/04-automated-abuse/02-workflow-mapping.md) | Foundation | 180 |
| `m04-l03` | [Authentication and rate controls](../modules/04-automated-abuse/03-auth-and-rate-controls.md) | Applied | 240 |
| `m04-l06` | [Challenge Systems and Protected-Action Enforcement](../modules/04-automated-abuse/06-challenge-systems-and-protected-action-enforcement.md) | Applied | 240 |

## What you should be able to demonstrate

- Demonstrate every capability from the 24 focused hours checkpoint.
- Compare clean and restored BrowserContexts and collect page, frame, worker, and network observations.
- Map the local API and turn bounded reconnaissance into testable hypotheses.
- Run the authorized authentication and rate-key exercises and explain their protected-action evidence.
- Trace the local challenge through proof production and server enforcement, prove the bounded cross-session/repeat-use result, compare deterministic attacker/customer metrics, and define both remediation retests.

## Capability claim

Functional hands-on readiness in local browser, workflow-mapping, provider-authorized authentication/rate-control exercises, and local challenge-proof enforcement testing.

## What this does not claim

You are not claiming commercial solver development, universal challenge bypass,
controlled browser evasion, protocol-identity analysis, bounded load-testing
competence, a complete portfolio, or production experience.

## Exit gate

Reproduce the listed local and provider-authorized behavior, explain the context
observations and workflow map, and distinguish authentication/rate observations
from challenge issuance, proof validation, and the protected-action result.
