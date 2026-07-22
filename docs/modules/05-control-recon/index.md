# Module 05 - Control reconnaissance and trusted-signal analysis

**Outcome:** build a control-surface map from manual, browser-automation, and
HTTP-client populations, then establish the blocked baseline required before an
evasion hypothesis.

## Foundation

Complete [signal families](01-signal-families.md) and [browser-environment
collection](02-browser-environment.md). Produce a sourced signal/observation matrix.

## Applied

Complete [cross-context consistency](03-cross-context-consistency.md) and
[session, behavior, and workflow](04-session-behavior-workflow.md). Compare what
the top page, iframe, worker, session, and action expose.

## Integrated

Complete [the blocked baseline](05-blocked-baseline.md) with manual, headed,
headless, and HTTP-client populations and a ranked control hypothesis.

## Deep

Add false-positive populations, repeated trials, version labels, drift risks,
alternate explanations, and the evidence required to distinguish them.

## Canonical offensive outcome

Use this schema for every control hypothesis. A detector score may appear as an
observation, but the exercise ends with the protected-action result and exact
retest—not a classifier-building task.

```text
Observed signal:
Collection location:
What the defense appears to infer:
Attacker control:
Cost to imitate:
Cross-context implications:
Protocol implications:
Session implications:
Blocked baseline:
Hypothesis:
Changed variable or coherent signal set:
Protected-action result:
Residual anomalies:
Alternative explanations:
Remediation:
Retest:
```

Precision, recall, false-positive rate, base-rate effects, ablation, and drift
are supporting analysis only when they expose an overtrusted feature, quantify
collateral impact, or make remediation and retest more meaningful.

Start with [signal families](01-signal-families.md). This module observes and
maps; signal changes wait until Module 06.
