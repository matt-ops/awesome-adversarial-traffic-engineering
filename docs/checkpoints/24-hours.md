# 24 focused hours

<!-- checkpoint-id: 24-focused-hours -->
<!-- direct-selection-minutes: 285 -->
<!-- prerequisite-closure-minutes: 1250 -->

This Foundation checkpoint follows the technical path from HTTP through the
first local Playwright workflow, isolated browser state, and captured network
evidence. Its published checkpoint time includes every core prerequisite lesson
for a learner starting from zero.

## Time calculation

- Direct capability-selection time: **285 minutes (4.75 hours)**
- From-zero prerequisite-closure time: **1250 minutes (20.83 hours)**
- Declared cumulative range: **1200-1440 minutes (20-24 hours)**
- Maximum lesson depth: **Foundation**

The direct selection identifies the capability target. It is not the
checkpoint time for a new learner. The validator recursively closes the
prerequisite graph and sums each of the 11 lessons below exactly once. Optional
appendix study is not included in checkpoint time.

## Direct capability selection

- `m03-l02` - complete the first local Playwright workflow and its evidence
- `m03-l04` - isolate browser state and preserve request/response network evidence

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

## What you should be able to demonstrate

- Identify an HTTP method, target, headers, status, body, session, and workflow state.
- Run the static search workflow manually and explain its browser-only and server-provided data.
- Build and explain the first local Playwright workflow and its JSON output.
- Compare clean and restored BrowserContexts and explain how network events become evidence.

## Capability claim

Foundation and informational readiness, not browser-evasion competence.

## What this does not claim

You are not claiming browser-evasion competence, integrated Docker-lab
mastery, protocol-capture competence, production control fidelity, or DDoS
expertise.

## Exit gate

Explain the listed concepts without the answer keys, rerun the first local browser workflow, interpret its telemetry, and state the checkpoint boundary claim.
