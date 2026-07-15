# Start here

## Who this is for

You already work comfortably with networks, security telemetry, incident
analysis, and basic Python. You may be new to browser processes, DOM/Web APIs,
JavaScript asynchronous behavior, Playwright, fingerprint collection,
cross-context consistency, and DDoS red-team engagement design.

## The role

The learner is the authorized adversary. You will map a protected workflow,
reproduce abusive behavior, establish a blocked baseline, identify what a
control appears to rely on, state a falsifiable hypothesis, change a controlled
variable or coherent signal set, repeat the same protected action, and preserve
evidence for remediation and retest.

Detection appears in the path because it is an attack surface. Building a
production detector is not the course objective.

## What the course teaches

- HTTP, browser, DOM, JavaScript, and Playwright foundations needed for the work
- Automated-abuse workflows and provider-authorized attack labs
- Control reconnaissance across browser, protocol, session, and behavior layers
- A progression from one-property experiments to coherent, cross-context tests
- TLS/HTTP identity analysis without treating a fingerprint as identity proof
- DDoS testing through exhausted resources and bounded application-layer load
- Offensive Python, code review, findings, remediation, and exact retest

## What it does not teach

- Testing public, third-party, or production systems without written permission
- Malware, botnet operation, persistence, credential theft, or attack hosting
- Unbounded load generation or Layer 3/4 attack tooling
- Universal stealth, a production-ready detector, or a guarantee of expertise

## One path

```text
method -> HTTP/edge -> browser/JavaScript -> Playwright -> automated abuse
       -> control reconnaissance -> browser evasion -> protocol identity
       -> DDoS/resilience -> tooling/code review -> findings/interview
```

Complete lessons in navigation order. Every lesson names its prerequisites,
source assignment, artifact, pass gate, and next lesson.

## Cumulative checkpoints

The same lessons support four honest review points:

| Review point | Claim |
|---|---|
| About 24 focused hours | Foundation and informational readiness, not domain expertise |
| About 7 cumulative days | Functional hands-on foundation |
| About 21 cumulative days | Interview-loop readiness with a defensible portfolio |
| About 6 cumulative weeks | Practitioner-depth portfolio, not proof of production expertise |

Checkpoint pages are views into this path. They never duplicate lessons.

## Install now

- A current browser with developer tools
- Python 3.12 or newer
- A text editor
- Git for saving your artifacts privately

## Do not install yet

Do not install Docker, Playwright browsers, k6, anti-detect projects, packet
tools, or a WAF stack yet. Each appears only after its prerequisite lesson and
with a target, expected output, failure guidance, and cleanup procedure.

## First lesson

[Begin with the authorized red-team role](modules/00-method/01-red-team-role.md).
