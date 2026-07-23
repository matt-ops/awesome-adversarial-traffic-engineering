# Experienced Practitioner Fast Track

This is a diagnostic route for practitioners who already have uneven experience
across the course. It is not a checkpoint, prerequisite, credential, or shortcut
around evidence. Start each row with the evidence task. If the result is weak,
review the linked canonical lesson; if it is strong, take the next specialty.

## Intended learner

Use this route if you already have meaningful network engineering, incident
response, detection engineering, threat hunting, SOC operations, application
security, or general security-engineering experience, but may be new to browser
automation, bot-control evasion, protocol fingerprints, or bounded adversarial traffic tests.

## What this route can and cannot skip

- Networking or incident-response experience does not prove browser,
  JavaScript, Playwright, challenge-control, or protocol-identity competence.
- Skim a foundation lesson only after completing its evidence check below; a
  weak or incomplete result routes back to the exact canonical lesson.
- Safety boundaries, authorization, loopback target restrictions, caps,
  cleanup, and unsupported-claim limits are never skippable.
- Canonical checkpoint times remain from-zero estimates. They are not a
  personalized estimate for this diagnostic route.

## Evidence-based gap assessment

| Capability area | Exact evidence task | If evidence is weak | If evidence is strong |
|---|---|---|---|
| HTTP request and session reasoning | Annotate method, target, headers, body, status, response headers, client/server session state, and authoritative server effect for one loopback workflow. | [Sessions and workflows](modules/01-http-edge/02-sessions-and-workflows.md) | [Workflow and API mapping](modules/04-automated-abuse/02-workflow-mapping.md) |
| DevTools Network | Capture one local request and identify initiator, timing, request/response fields, redirect behavior, and the matching UI or server result. | [Observe requests with DevTools Network](modules/01-http-edge/03-devtools-network.md) | [Map the edge request path](modules/01-http-edge/04-edge-request-path.md) |
| browser process and JavaScript runtime | Explain top page, iframe, worker, browser process, renderer, event loop, and which context executes one local collection step. | [Browser process model](modules/02-browser-javascript/01-browser-process-model.md) | [Frames, workers, and CDP](modules/03-playwright/05-frames-workers-and-cdp.md) |
| DOM and browser APIs | Read and modify one local DOM value, name the browser API providing it, and distinguish the property from server state. | [DOM and Web APIs](modules/02-browser-javascript/02-dom-and-web-apis.md) | [Browser-environment observations](modules/05-control-recon/02-browser-environment.md) |
| async JavaScript and fetch | Explain promise creation, `await`, fetch response handling, thrown errors, and cleanup in one bounded local request. | [Promises, async, fetch, and errors](modules/02-browser-javascript/04-async-fetch-and-errors.md) | [Network events and evidence](modules/03-playwright/04-network-events.md) |
| Playwright object model | Execute the local browser workflow and distinguish Browser, BrowserContext, Page, Locator, action, and assertion ownership. | [Playwright object model](modules/03-playwright/01-object-model.md) | [First local Playwright workflow](modules/03-playwright/02-first-browser.md) |
| BrowserContexts and storage | Use two local contexts to show cookie/storage isolation, then identify which state is intentionally exported or absent. | [Browser contexts and storage state](modules/03-playwright/03-contexts-and-state.md) | [Replay and temporal consistency](modules/06-browser-evasion/04-replay-and-temporal-consistency.md) |
| network event tracing | Correlate Playwright request and response events with method, URL, status, timing, body boundary, and protected server outcome. | [Network events and evidence](modules/03-playwright/04-network-events.md) | [Challenge Systems and Protected-Action Enforcement](modules/04-automated-abuse/06-challenge-systems-and-protected-action-enforcement.md) |
| workflow and protected-action mapping | Draw one abusive workflow with preconditions, identities, transitions, blocked baseline, protected action, server proof, and reset. | [Workflow and API mapping](modules/04-automated-abuse/02-workflow-mapping.md) | [Authentication and rate controls](modules/04-automated-abuse/03-auth-and-rate-controls.md) |
| challenge proof and enforcement | Trace issue, delivery, proof, verification, binding, protected enforcement, replay, and legitimate near-neighbor impact. | [Challenge Systems and Protected-Action Enforcement](modules/04-automated-abuse/06-challenge-systems-and-protected-action-enforcement.md) | [Replay and temporal consistency](modules/06-browser-evasion/04-replay-and-temporal-consistency.md) |
| control reconnaissance | Compare manual, headed, headless, and HTTP-only populations while keeping missing observations and final actions explicit. | [Establish the blocked baseline](modules/05-control-recon/05-blocked-baseline.md) | [Classifier Evaluation and Adversarial Drift](modules/05-control-recon/06-classifier-evaluation-and-adversarial-drift.md) |
| classifier tradeoffs | Execute the deterministic fixture and explain both thresholds, base-rate workload, near-neighbor cost, delayed labels, and adapted-abuse completions. | [Classifier Evaluation and Adversarial Drift](modules/05-control-recon/06-classifier-evaluation-and-adversarial-drift.md) | [Version drift and residual anomalies](modules/06-browser-evasion/05-version-drift-and-residual-anomalies.md) |
| browser evasion | Pre-register one changed property, fixed variables, protected-action result, residuals, alternatives, and exact remediation retest. | [Form an evasion hypothesis](modules/06-browser-evasion/01-evasion-hypotheses.md) | [Identity coherence](modules/06-browser-evasion/03-identity-coherence.md) |
| protocol identity | Capture real loopback ClientHello records and HTTP/2 settings from available clients, then state observer and attribution limits. | [Local Multi-client Protocol Comparison](modules/07-protocol-identity/06-local-multi-client-protocol-comparison.md) | [HTTP/3 and QUIC](modules/07-protocol-identity/05-http3-quic.md) |
| bounded resilience testing | Define a service objective, hard envelope, automated aborts, mitigation timing, recovery stability, and exact local retest. | [Bounded application-layer load testing](modules/08-ddos-resilience/04-bounded-load-testing.md) | [Recovery, remediation, and retest](modules/08-ddos-resilience/05-recovery-and-retest.md) |
| findings and exact retest | Write one finding with condition, protected effect, evidence, impact bounds, invariant remediation, negative/positive acceptance, and exact retest. | [Finding and evidence](modules/10-findings-interview/01-finding-and-evidence.md) | [Remediation and exact retest](modules/10-findings-interview/02-remediation-and-retest.md) |

## Recommended role-focused route

1. Refresh HTTP evidence with [Sessions and workflows](modules/01-http-edge/02-sessions-and-workflows.md)
   and [DevTools Network](modules/01-http-edge/03-devtools-network.md).
2. Close browser and JavaScript gaps with [Browser process model](modules/02-browser-javascript/01-browser-process-model.md),
   [DOM and Web APIs](modules/02-browser-javascript/02-dom-and-web-apis.md), and
   [Promises, async, fetch, and errors](modules/02-browser-javascript/04-async-fetch-and-errors.md).
3. Execute [First local Playwright workflow](modules/03-playwright/02-first-browser.md)
   and [Network events and evidence](modules/03-playwright/04-network-events.md).
4. Map automated abuse with [Workflow and API mapping](modules/04-automated-abuse/02-workflow-mapping.md).
5. Prove challenge behavior with [Challenge Systems and Protected-Action Enforcement](modules/04-automated-abuse/06-challenge-systems-and-protected-action-enforcement.md).
6. Establish the populations in [Control Reconnaissance](modules/05-control-recon/05-blocked-baseline.md).
7. Quantify operating points in [Classifier Evaluation and Adversarial Drift](modules/05-control-recon/06-classifier-evaluation-and-adversarial-drift.md).
8. Execute [Browser Evasion](modules/06-browser-evasion/02-one-variable-experiments.md)
   only after its falsifiable [hypothesis](modules/06-browser-evasion/01-evasion-hypotheses.md).
9. Compare actual clients in [Protocol Identity](modules/07-protocol-identity/06-local-multi-client-protocol-comparison.md).
10. Execute bounded local evidence and authorized planning through [DDoS and Resilience](modules/08-ddos-resilience/05-recovery-and-retest.md).
11. Finish with [Finding and evidence](modules/10-findings-interview/01-finding-and-evidence.md)
    and [Remediation and exact retest](modules/10-findings-interview/02-remediation-and-retest.md).

Use [the linear path](path.md) whenever a diagnostic exposes more than one weak
dependency. The canonical lesson remains the source of teaching and assessment.

## Interview-focused route

For interview preparation, review the optional [red-team method
appendix](modules/00-method/index.md) and optional [Traffic and Bot Threat
Intelligence appendix](appendices/traffic-bot-threat-intelligence/index.md), then
complete [Technical briefing](modules/10-findings-interview/03-technical-briefing.md),
[Public-safe role narrative](modules/10-findings-interview/04-role-narrative.md),
and the [Full mock loop](modules/10-findings-interview/05-mock-loop.md). Keep every
claim generic, bounded to preserved evidence, and free of employer-specific material.

## Unsupported fast-track claims

Passing a self-check does not establish production experience, authorization for
an external target, universal evasion, commercial-control parity, Internet-scale
resilience, or a hiring outcome. It only routes the next course activity.
