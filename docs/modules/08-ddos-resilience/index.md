# Module 08 - DDoS and resilience

**Outcome:** model application-layer denial through consumed resources, execute
bounded abortable local pressure, measure recovery, and retest controls.

!!! info "Before testing outside the bundled local lab"
    Review the optional [Scope and Rules of Engagement
    appendix](../00-method/02-scope-and-rules.md). The local course can be
    completed without it, but real assessments require explicit owner
    authorization and organization-specific procedures.

## Foundation

Complete [the resource-exhaustion model](01-resource-exhaustion-model.md) and
[metrics](02-metrics.md). Produce the resource chain and predeclared service objectives.

## Applied

Complete [edge controls](03-edge-controls.md) and [bounded load
testing](04-bounded-load-testing.md). Map aggregation key, endpoint, window,
cache/admission behavior, bypass hypothesis, and collateral-risk population,
then run one bounded Layer 7 experiment.

## Integrated

Repeat [bounded load testing](04-bounded-load-testing.md) across the defined
fixed-loopback scenarios within hard target, duration, VU, rate, total,
threshold, abort, dry-run, and recovery controls, then compare the results. Keep
`endpoint-cost-observation` and `workflow-sequence-observation` labeled as
observations; the local stack does not implement those two mitigations.

## Deep

Complete [recovery and retest](05-recovery-and-retest.md). Map remediation to the
exhausted resource, translate bounded evidence into an authorized provider-neutral
pre-production plan, and repeat the same bounded attack with legitimate-health criteria.

## Experiment frame used in this module

| Field | What this module requires |
|---|---|
| Baseline | Measure the cheap route, expensive route, and legitimate-neighbor health before pressure. |
| Changed variable | Apply one bounded scenario or one coherent load shape inside the declared caps. |
| Fixed variables | Keep target, scenario, duration, rate, VUs, request ceiling, data, thresholds, and version fixed. |
| Success condition | Observe the predeclared protected service effect without crossing abort or traffic ceilings. |
| Alternative explanation | Consider client noise, cache state, warm-up, unrelated load, and failed reset or recovery checks. |
| Retest | Repeat the identical bounded scenario after remediation and require both hostile resistance and legitimate health. |

Every run retains the lesson's loopback restriction, hard ceilings, aborting
thresholds, timeouts, cleanup, and recovery check.

Start with the [resource-exhaustion model](01-resource-exhaustion-model.md).
