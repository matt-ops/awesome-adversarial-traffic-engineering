# 7 days cumulative

<!-- checkpoint-id: 7-days -->
<!-- direct-selection-minutes: 540 -->
<!-- prerequisite-closure-minutes: 2235 -->

This cumulative Applied checkpoint extends the first browser workflow through
context and CDP observation, workflow mapping, and provider-authorized
authentication and rate-control analysis.

## Time calculation

- Direct capability-selection time: **540 minutes (9.00 hours)**
- From-zero prerequisite-closure time: **2235 minutes (37.25 hours)**
- Declared cumulative range: **1800-2400 minutes (30-40 hours)**
- Maximum lesson depth: **Applied**

The direct selection identifies three capability targets. It is not the
checkpoint time for a new learner. The validator recursively closes the
prerequisite graph and sums each of the 18 lessons below exactly once, including
the complete 24-hour checkpoint selection.

## Direct capability selection

- `m03-l02` - first local Playwright workflow
- `m03-l05` - frames, workers, and CDP observations
- `m04-l03` - authentication and rate-control evidence

## Required lessons

| ID | Canonical lesson | Depth | Minutes | Required artifact |
|---|---|---:|---:|---|
| `m00-l01` | [The authorized red-team role](../modules/00-method/01-red-team-role.md) | Foundation | 75 | `artifacts/module-00/role-comparison.md` |
| `m00-l02` | [Scope and Rules of Engagement](../modules/00-method/02-scope-and-rules.md) | Foundation | 90 | `artifacts/module-00/engagement-plan.md` |
| `m00-l03` | [Experimental method before attack execution](../modules/00-method/03-experimental-method.md) | Foundation | 100 | `artifacts/module-00/experiment-plan.md` |
| `m01-l01` | [HTTP request and response](../modules/01-http-edge/01-http-request-response.md) | Foundation | 90 | `artifacts/module-01/request-anatomy.md` |
| `m01-l02` | [Sessions and workflows](../modules/01-http-edge/02-sessions-and-workflows.md) | Foundation | 90 | `artifacts/module-01/workflow-map.md` |
| `m01-l03` | [Observe requests with DevTools Network](../modules/01-http-edge/03-devtools-network.md) | Foundation | 80 | `artifacts/module-01/manual-trace.md` |
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

## Required artifacts

Every artifact in the final column is required, including artifacts assigned
by prerequisite lessons. The linked lesson defines its procedure, expected
output, interpretation, cleanup, and pass gate.

## Capability claim

Functional hands-on readiness in local browser, workflow-mapping, and provider-authorized authentication and rate-control exercises.

## What this does not claim

You are not claiming controlled evasion, protocol-identity analysis, bounded
load-testing competence, a complete portfolio, or production experience.

## Exit gate

Reproduce the listed local and provider-authorized work with versions, raw
output, cleanup, and limitations; show the context observations, workflow map,
and authentication and rate-control evidence.
