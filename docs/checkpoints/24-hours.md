# 24 focused hours

<!-- checkpoint-id: 24-focused-hours -->
<!-- direct-selection-minutes: 180 -->
<!-- prerequisite-closure-minutes: 1300 -->

This Foundation checkpoint follows the course entry path through the first
local Playwright workflow. Its published checkpoint time includes every
prerequisite lesson and artifact for a learner starting from zero.

## Time calculation

- Direct capability-selection time: **180 minutes (3.00 hours)**
- From-zero prerequisite-closure time: **1300 minutes (21.67 hours)**
- Declared cumulative range: **1200-1440 minutes (20-24 hours)**
- Maximum lesson depth: **Foundation**

The direct selection identifies the capability target. It is not the
checkpoint time for a new learner. The validator recursively closes the
prerequisite graph and sums each of the 12 lessons below exactly once.

## Direct capability selection

- `m03-l02` - complete the first local Playwright workflow and its evidence

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

## Required artifacts

Every artifact in the final column is required, including artifacts assigned
by prerequisite lessons. The linked lesson defines its procedure, expected
output, interpretation, cleanup, and pass gate.

## Capability claim

Foundation and informational readiness, not browser-evasion competence.

## What this does not claim

You are not claiming browser-evasion competence, integrated Docker-lab
mastery, protocol-capture competence, production control fidelity, or DDoS
expertise.

## Exit gate

Explain every listed artifact without an answer key, rerun the first local
browser workflow, show its telemetry, and state the boundary claim verbatim.
