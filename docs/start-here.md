# Start here

## Who this is for

This path assumes no prior browser automation, bot-control, fingerprinting,
protocol-identity, or DDoS red-team experience. It teaches the web request path,
browser processes, DOM/Web APIs, JavaScript, and Playwright before asking you to
use the integrated lab. Basic computer use and willingness to run documented
local commands are the only entry requirements; when Python or TypeScript first
appears, the lesson explains the code used or assigns the exact prerequisite.

This is "from zero" for adversarial traffic engineering, not a promise that one
short checkpoint replaces years of engineering practice. Follow the path in
order and take longer than the estimated time whenever a prerequisite is new.

!!! danger "Safety boundary"
    Use only the bundled loopback lab, an isolated target you own, or an exact
    provider-assigned target. Never test an unrelated public or production
    service. Keep every destination check, traffic cap, timeout, abort
    condition, cleanup step, and redirect restriction in place.

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
HTTP/edge -> browser/JavaScript -> Playwright -> automated abuse
          -> control reconnaissance -> browser evasion -> protocol identity
          -> DDoS/resilience -> tooling/code review -> findings/interview
```

Complete lessons in navigation order. Every lesson names its prerequisites,
source assignment, guided exercise, knowledge check, and next lesson.

## Cumulative checkpoints

The same path supports four honest review points. The direct selection names the
capability targets; the from-zero closure is the published checkpoint time for
a new learner because it includes every recursive prerequisite exactly once.

| Review point | Direct selection | From-zero closure | Claim |
|---|---:|---:|---|
| [24 focused hours](checkpoints/24-hours.md) | 4.75 hours | 20.83 hours | HTTP, session, browser, JavaScript, Playwright state, and network-evidence readiness |
| [7 days](checkpoints/7-days.md) | 14.75 hours | 36.83 hours | Local browser, workflow, authentication/rate, and challenge-proof enforcement readiness |
| [21 days](checkpoints/21-days.md) | 21.75 hours | 70.83 hours | Integrated challenge/replay experiment, finding, briefing, and role-narrative readiness |
| [6 weeks](checkpoints/6-weeks.md) | 35.75 hours | 119.50 hours | Practitioner-depth portfolio, not proof of production expertise |

Checkpoint pages are views into this path. They never duplicate lessons.
Use the plain [progress table](progress.md) if you want checkboxes; no account or
course platform is required.

## Install now

- A current browser with developer tools
- Python 3.12 or newer
- A text editor
- Git for cloning the repository and optionally saving your own work

## Command platforms

Commands use portable executable names such as `python`, `npm`, `npx`,
`docker`, and `k6`. When a command sets environment variables, the course shows
separate PowerShell and Bash/zsh examples; use the block for your shell.

## Do not install yet

Do not install Docker, Playwright browsers, k6, anti-detect projects, packet
tools, or a WAF stack yet. Each appears only after its prerequisite lesson and
with a target, expected output, failure guidance, and cleanup procedure.

## First lesson

[Begin with HTTP request and response](modules/01-http-edge/01-http-request-response.md).

## Optional red-team method appendix

The technical path begins with HTTP.

Review the optional [red-team method and engagement practice
appendix](modules/00-method/index.md) when you want deeper instruction on
authorization, Rules of Engagement, formal experiment planning, or interview
methodology. It is recommended before testing outside the bundled local lab and
before the final mock loop, but it is not a prerequisite for the technical path.
