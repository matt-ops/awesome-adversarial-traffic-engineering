# Progress

Mark a lesson complete when you can explain its knowledge check and reproduce the guided exercise behavior. No evidence file or saved path is required. You may add a completion date or a short private note if that helps you remember where to resume.

## Module 01 - HTTP and the edge

- [ ] [HTTP request and response](modules/01-http-edge/01-http-request-response.md)
- [ ] [Sessions and workflows](modules/01-http-edge/02-sessions-and-workflows.md)
- [ ] [Observe requests with DevTools Network](modules/01-http-edge/03-devtools-network.md)
- [ ] [Map the edge request path](modules/01-http-edge/04-edge-request-path.md)

## Module 02 - Browser and JavaScript foundations

- [ ] [Browser process model](modules/02-browser-javascript/01-browser-process-model.md)
- [ ] [DOM and Web APIs](modules/02-browser-javascript/02-dom-and-web-apis.md)
- [ ] [Minimum JavaScript for automation](modules/02-browser-javascript/03-javascript-core.md)
- [ ] [Promises, async, fetch, and errors](modules/02-browser-javascript/04-async-fetch-and-errors.md)

## Module 03 - Playwright foundations

- [ ] [Playwright object model](modules/03-playwright/01-object-model.md)
- [ ] [First local Playwright workflow](modules/03-playwright/02-first-browser.md)
- [ ] [Browser contexts and storage state](modules/03-playwright/03-contexts-and-state.md)
- [ ] [Network events and evidence](modules/03-playwright/04-network-events.md)
- [ ] [Frames, workers, and CDP](modules/03-playwright/05-frames-workers-and-cdp.md)

## Module 04 - Automated abuse and workflow attacks

- [ ] [Automated-abuse objectives](modules/04-automated-abuse/01-abuse-objectives.md)
- [ ] [Workflow and API mapping](modules/04-automated-abuse/02-workflow-mapping.md)
- [ ] [Authentication and rate controls](modules/04-automated-abuse/03-auth-and-rate-controls.md)
- [ ] [Challenge Systems and Protected-Action Enforcement](modules/04-automated-abuse/06-challenge-systems-and-protected-action-enforcement.md)
- [ ] [Inventory and promotion abuse](modules/04-automated-abuse/04-inventory-and-promotion-abuse.md)
- [ ] [Race conditions and resource limits](modules/04-automated-abuse/05-race-and-resource-limits.md)

## Module 05 - Control reconnaissance and trusted-signal analysis

- [ ] [Five signal families](modules/05-control-recon/01-signal-families.md)
- [ ] [Browser-environment observations](modules/05-control-recon/02-browser-environment.md)
- [ ] [Cross-context consistency](modules/05-control-recon/03-cross-context-consistency.md)
- [ ] [Session, behavior, and workflow signals](modules/05-control-recon/04-session-behavior-workflow.md)
- [ ] [Establish the blocked baseline](modules/05-control-recon/05-blocked-baseline.md)

## Module 06 - Browser-control evasion experiments

- [ ] [Form an evasion hypothesis](modules/06-browser-evasion/01-evasion-hypotheses.md)
- [ ] [One-variable evasion experiment](modules/06-browser-evasion/02-one-variable-experiments.md)
- [ ] [Identity coherence](modules/06-browser-evasion/03-identity-coherence.md)
- [ ] [Replay and temporal consistency](modules/06-browser-evasion/04-replay-and-temporal-consistency.md)
- [ ] [Version drift and residual anomalies](modules/06-browser-evasion/05-version-drift-and-residual-anomalies.md)

## Module 07 - Protocol identity foundations

- [ ] [TLS ClientHello](modules/07-protocol-identity/01-tls-clienthello.md)
- [ ] [JA4 and JA4H as pivots](modules/07-protocol-identity/02-ja4-and-ja4h.md)
- [ ] [HTTP/2 connections and streams](modules/07-protocol-identity/03-http2.md)
- [ ] [Proxies and connection reuse](modules/07-protocol-identity/04-proxies-and-connection-reuse.md)
- [ ] [HTTP/3 and QUIC](modules/07-protocol-identity/05-http3-quic.md)

## Module 08 - DDoS and resilience

- [ ] [Resource-exhaustion model](modules/08-ddos-resilience/01-resource-exhaustion-model.md)
- [ ] [Resilience metrics and thresholds](modules/08-ddos-resilience/02-metrics.md)
- [ ] [Edge and admission controls](modules/08-ddos-resilience/03-edge-controls.md)
- [ ] [Bounded application-layer load testing](modules/08-ddos-resilience/04-bounded-load-testing.md)
- [ ] [Recovery, remediation, and retest](modules/08-ddos-resilience/05-recovery-and-retest.md)

## Module 09 - Tooling and secure code review

- [ ] [Python telemetry as evidence](modules/09-tooling-code-review/01-python-telemetry.md)
- [ ] [Async and bounded concurrency](modules/09-tooling-code-review/02-async-and-bounded-concurrency.md)
- [ ] [Retries, timeouts, and jitter](modules/09-tooling-code-review/03-retries-timeouts-and-jitter.md)
- [ ] [Secure code review through an adversary's path](modules/09-tooling-code-review/04-secure-code-review.md)

## Module 10 - Findings, briefing, and interview practice

- [ ] [Finding and evidence](modules/10-findings-interview/01-finding-and-evidence.md)
- [ ] [Remediation and exact retest](modules/10-findings-interview/02-remediation-and-retest.md)
- [ ] [Technical briefing](modules/10-findings-interview/03-technical-briefing.md)
- [ ] [Public-safe role narrative](modules/10-findings-interview/04-role-narrative.md)
- [ ] [Full mock loop](modules/10-findings-interview/05-mock-loop.md)

## Checkpoint progress

The checkpoints remain cumulative and validator-backed. Mark one complete when you can demonstrate its required lesson capabilities and exit behavior.

Optional appendix study is not included in checkpoint time.

| Checkpoint | Depth ceiling | Direct targets | Closure lessons | From-zero time | Complete |
|---|---:|---:|---:|---:|---:|
| [24 focused hours](checkpoints/24-hours.md) | Foundation | 2 | 11 | 20.83 hours | [ ] |
| [7 days](checkpoints/7-days.md) | Applied | 5 | 16 | 36.83 hours | [ ] |
| [21 days](checkpoints/21-days.md) | Integrated | 8 | 29 | 70.83 hours | [ ] |
| [6 weeks](checkpoints/6-weeks.md) | Deep | 12 | 45 | 119.50 hours | [ ] |

Canonical direct membership, prerequisite closure, and both time calculations live in `curriculum/manifest.yaml` and are enforced by `scripts/validate_curriculum.py`.

## Optional appendix - Red-team method and engagement practice

Use these optional checkboxes only if you choose the deeper methodology review.
They do not affect core completion or checkpoint closure.

- [ ] [The authorized red-team role](modules/00-method/01-red-team-role.md)
- [ ] [Scope and Rules of Engagement](modules/00-method/02-scope-and-rules.md)
- [ ] [Experimental method before attack execution](modules/00-method/03-experimental-method.md)
