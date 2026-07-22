# Module 05 - Control reconnaissance and trusted-signal analysis

**Outcome:** build a control-surface map from manual, browser-automation, and
HTTP-client populations, establish the blocked baseline, and evaluate how
classifier thresholds, base rates, collateral cost, and adversarial drift change
the operating point before an evasion hypothesis. Challenge issuance, proof
flow, customer friction, and the protected enforcement point remain separate observations.

## Foundation

Complete [signal families](01-signal-families.md) and [browser-environment
collection](02-browser-environment.md). Produce a sourced signal/observation matrix.

## Applied

Complete [cross-context consistency](03-cross-context-consistency.md) and
[session, behavior, and workflow](04-session-behavior-workflow.md). Compare what
the top page, iframe, worker, session, and action expose.

## Integrated

Complete [the blocked baseline](05-blocked-baseline.md) with manual, headed,
headless, and HTTP-client populations, then execute [classifier evaluation and
adversarial drift](06-classifier-evaluation-and-adversarial-drift.md) against the
deterministic fixture.

## Deep

Add false-positive populations, repeated trials, version labels, drift risks,
alternate explanations, and the evidence required to distinguish them.

## Canonical offensive outcome

Use this schema for every control hypothesis. A detector score may appear as an
observation, but the exercise ends with the protected-action result and exact
retest. The classifier lesson evaluates a supplied deterministic score fixture;
it does not train or claim a deployable model.

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
Challenge populations and observed trigger reasons:
Challenge type and delivery surface:
Token, cookie, and storage flow:
Protected-action enforcement point:
Solve, abandonment, or bypass outcome:
Legitimate accessibility/privacy/automation near-neighbor:
Residual anomalies:
Alternative explanations:
Remediation:
Retest:
```

Precision, recall, false-positive rate, false-negative rate, base-rate effects,
operational cost, and drift are required classifier evidence. They support an
offensive conclusion only when they expose an overtrusted feature, quantify
collateral impact, or make remediation and retest more meaningful.

## Experiment frame used in this module

| Field | What this module requires |
|---|---|
| Baseline | Record legitimate and blocked populations before changing a signal. |
| Changed variable | Name the one observable property or declared coherent signal set under test. |
| Fixed variables | Hold target, workflow, state reset, browser version, timing window, and evidence fields constant. |
| Success condition | Repeat the same protected action; a score change alone is not success. |
| Alternative explanation | Name another cause, such as reset failure, version drift, or a second changed signal. |
| Retest | Repeat the exact protected action after remediation with the same populations and evidence fields. |

Start with [signal families](01-signal-families.md). This module observes and
maps; signal changes wait until Module 06.
