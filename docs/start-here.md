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

The same path supports four honest review points. The direct selection names the
capability targets; the from-zero closure is the published checkpoint time for
a new learner because it includes every recursive prerequisite exactly once.

| Review point | Direct selection | From-zero closure | Claim |
|---|---:|---:|---|
| [24 focused hours](checkpoints/24-hours.md) | 3.00 hours | 21.67 hours | Foundation and informational readiness, not browser-evasion competence |
| [7 days](checkpoints/7-days.md) | 9.00 hours | 37.25 hours | Local browser, workflow-mapping, and authorized authentication/rate-control readiness |
| [21 days](checkpoints/21-days.md) | 16.00 hours | 71.25 hours | Integrated experiment, finding, briefing, and role-narrative readiness |
| [6 weeks](checkpoints/6-weeks.md) | 30.00 hours | 119.92 hours | Practitioner-depth portfolio, not proof of production expertise |

Checkpoint pages are views into this path. They never duplicate lessons.
Use the plain [progress table](progress.md) if you want checkboxes; no account or
course platform is required.

## Install now

- A current browser with developer tools
- Python 3.12 or newer
- A text editor
- Git for saving your artifacts privately

## Command platforms

Commands use portable executable names such as `python`, `npm`, `npx`,
`docker`, and `k6`. When a command sets environment variables, the course shows
separate PowerShell and Bash/zsh examples; use the block for your shell.

## Do not install yet

Do not install Docker, Playwright browsers, k6, anti-detect projects, packet
tools, or a WAF stack yet. Each appears only after its prerequisite lesson and
with a target, expected output, failure guidance, and cleanup procedure.

## First lesson

[Begin with the authorized red-team role](modules/00-method/01-red-team-role.md).
