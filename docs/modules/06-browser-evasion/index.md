# Module 06 - Browser-control evasion experiments

**Outcome:** form a falsifiable bypass hypothesis, vary one property or a
declared coherent set, repeat the protected action, and report residual anomalies
without claiming universal stealth.

## Seven-stage progression

Complete these stages in order. Earlier control-recon lessons are referenced
instead of duplicated; later protocol lessons provide the network evidence that
a browser-only exercise cannot teach.

| Stage | Canonical instruction | Required evidence before continuing |
|---:|---|---|
| 1. Baselines | [Blocked baseline](../05-control-recon/05-blocked-baseline.md) | Manual Chrome, stock headed Playwright, stock headless Playwright, and Python HTTP client; exact browser/Playwright versions, request/response behavior, sensor output, protected-action result, and control decision |
| 2. One observable property | [One-variable experiment](02-one-variable-experiments.md) | Predeclared property, fixed variables, changed toy decision, protected-action proof, and explicit statement that one change is not a coherent identity |
| 3. Cross-context consistency | [Cross-context lesson](../05-control-recon/03-cross-context-consistency.md) plus the fourth trial in the [control-recon lab](../../labs/integrated/control-recon.md) | Top page, same-origin iframe, and worker matrix; challenged frame-only contradiction after the successful one-variable condition |
| 4. Coherent environment profile | [Identity coherence](03-identity-coherence.md) | Browser claim, platform, Client Hints, locale, timezone, screen, viewport, graphics summary, storage/session state, context coverage, and remaining anomalies |
| 5. Replay and temporal consistency | [Replay and temporal consistency](04-replay-and-temporal-consistency.md) | Challenge trigger, proof, session/action/origin/nonce/expiry/use binding, protected enforcement, first/second/cross-session results, exact retest, and future labels for unsupported cross-action and expired cases |
| 6. Browser and protocol coherence | [TLS ClientHello](../07-protocol-identity/01-tls-clienthello.md), [JA4/JA4H](../07-protocol-identity/02-ja4-and-ja4h.md), [HTTP/2](../07-protocol-identity/03-http2.md), and [intermediary effects](../07-protocol-identity/04-proxies-and-connection-reuse.md) | Source-led browser/protocol coherence model and future evidence plan; the executable local lab generates Python/OpenSSL fixtures and plain-HTTP metadata, not browser TLS/HTTP2 captures |
| 7. Version drift | [Version drift and residual anomalies](05-version-drift-and-residual-anomalies.md) | Repeated prior experiment with a changed browser/framework version or deterministic drift fixture, including changed and unchanged evidence |

An allow decision is not enough. Every stage that changes a condition repeats
the same protected action, preserves residual anomalies and alternative
explanations, and states the exact remediation retest.

## Experiment frame used in this module

| Field | What this module requires |
|---|---|
| Baseline | Capture the same protected action for manual, stock headed, stock headless, and HTTP-client populations. |
| Changed variable | Change one property or one predeclared coherent set. |
| Fixed variables | Keep target, action, session procedure, state, browser version, run window, and evidence schema fixed. |
| Success condition | The protected server-side action succeeds under the treatment; an allow label is intermediate evidence. |
| Alternative explanation | Test whether reset state, timing, token behavior, version drift, or another signal explains the result. |
| Retest | Repeat the identical baseline and treatment after the control invariant changes. |

## Foundation

No browser-evasion lesson is a Foundation requirement. Foundation ends with
signal-family and informational readiness, not browser-evasion competence.

## Applied

No browser-evasion lesson is an Applied requirement. Applied work establishes
the local populations and control observations needed by the Integrated gate.

## Integrated

Complete [evasion hypotheses](01-evasion-hypotheses.md), [one-variable
experiments](02-one-variable-experiments.md), [identity
coherence](03-identity-coherence.md), and [replay and temporal
consistency](04-replay-and-temporal-consistency.md). Join protected-action proof
with token/session/action/time behavior and residual anomalies.

## Deep

Complete [version drift and residual anomalies](05-version-drift-and-residual-anomalies.md).
Repeat across declared versions and report transfer limits rather than universal stealth.

Begin only after the blocked-baseline gate in Module 05.
