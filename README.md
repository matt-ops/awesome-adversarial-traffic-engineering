# Adversarial Traffic Engineering

A source-first, red-team course for automated adversaries, browser-control
evasion, traffic-control testing, bounded application-layer pressure, findings,
remediation, and exact retest.

## Start

**[Start the path](docs/start-here.md)**

Then use the **Next lesson** link at the bottom of each page. Every lesson gives
you one required source assignment, one guided exercise, one artifact, a pass
gate, and an explained answer key.

Do not install the full lab stack first. The course introduces browser tooling,
Docker, and load tools only after their prerequisites.

## Local rewrite state

The source-first rewrite is being developed on a local branch. See
[`REWRITE_STATUS.md`](REWRITE_STATUS.md). The former course is preserved under
`archive/v1-course/` and is not part of learner navigation.

## Safety

Use only the bundled loopback target, your own non-routable isolated target, or
the exact target assigned by a training provider. Never test unrelated public or
production services. The executable boundary is documented in
[`docs/safety/`](docs/safety/).
