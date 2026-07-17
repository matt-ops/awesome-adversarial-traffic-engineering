# 24 focused hours

<!-- checkpoint-id: 24-focused-hours -->
<!-- calculated-minutes: 1425 -->

This is the minimum Foundation selection for role, method, HTTP/workflow, browser/JavaScript, first non-Docker Playwright, automated-abuse, signal-family, resource-model, Python-analysis, finding, and role-narrative readiness.

## Time calculation

- Calculated required lesson time: **1425 minutes (23.75 hours)**
- Declared cumulative range: **1200-1440 minutes (20-24 hours)**
- Maximum lesson depth: **Foundation**

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

## Required artifacts

Every artifact in the final column of the required-lessons table is required.
The artifact remains learner-created; its linked lesson defines the procedure,
expected output, interpretation, cleanup, and pass gate.

## Capability claim

Foundation and informational readiness, not browser-evasion competence.

## What this does not claim

You are not claiming browser-evasion competence, integrated Docker-lab mastery, protocol-capture competence, production control fidelity, or DDoS expertise.

## Exit gate

Explain every listed artifact without an answer key, rerun the first local browser workflow, show one small telemetry analysis and one synthetic finding, give the role narrative, and state the boundary claim verbatim.
