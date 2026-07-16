# Edge and admission controls

<!-- source-ids: aws-waf-app-layer-ddos, aws-waf-rate-based-rules, aws-builders-library-load-shedding, aate-adversarial-control-loop -->

> **Progress**  
> Module: 08 - DDoS and resilience  
> Lesson: 3 of 5  
> Depth: Applied  
> Estimated time: 3 hours  
> Prerequisites: Resilience metrics  
> Artifact: `artifacts/module-08/control-map.md`  
> Next: Bounded load testing

## Role outcome

Map rate aggregation, window, scope, custom keys, endpoint cost, caching, and
load shedding into specific authorized bypass/pressure hypotheses.

## Prerequisites

- [Metrics](02-metrics.md)
- Module 04 rate-key experiment

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [AWS WAF app-layer guidance](https://docs.aws.amazon.com/waf/latest/developerguide/ddos-app-layer-rbr.html) | Complete short page | Shows endpoint-specific application-layer rate protection |
| OFFICIAL_DOCUMENTATION | [AWS WAF rate rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html) | aggregation; windows; scope-down; custom keys | Defines product-specific control semantics |
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | Complete article | Adds admission and graceful overload |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | control hypothesis/action/retest | Structures offensive testing |

## Mental model

| Control | Assumption to test | Local scenario |
|---|---|---|
| per-key rate | key groups one workflow | identity-key |
| endpoint scope | expensive paths need different limit | endpoint-specific |
| workflow-aware | sequence/account ties distributed calls | workflow-aware |
| cache | reusable responses reduce work | cache-bypass |
| admission/shedding | excess work rejected before collapse | recovery/thresholds |

## Required external instruction

### AWS control assignment

**Direct link:** [Application-layer guidance](https://docs.aws.amazon.com/waf/latest/developerguide/ddos-app-layer-rbr.html) and [Rate-based rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html)  
**Exact assignment:** complete short app-layer page; rate-rule Aggregation instances, Evaluation windows, Scope-down statements, Custom keys  
**Estimated time:** 75 minutes  
**Focus on:** aggregation identity, endpoint scope, window semantics, custom-key trust, and product-specific limits  
**Skip:** console deployment and managed-product comparison  
**Expected takeaway:** predict one bypass and one collateral-risk scenario for each control dimension.

## Course bridge

Rate controls count within a defined aggregation/window/scope. Different
application areas can have different cost and legitimate rates. Load shedding
protects critical work even when traffic classification is imperfect.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Pair every control with the protected resource and a
    legitimate near-neighbor. A bypass is meaningful only if resource/service
    effect or protected work changes under fixed safe traffic.

## Worked example

Per-session `session_id` allows rotation; endpoint-specific control distinguishes
health from expensive reports; workflow-aware control would correlate search,
product, and report to a durable identity/state rather than one request key.

## Guided exercise

### Objective

Design the seven local scenario hypotheses before execution.

### Setup

Use the resource/metric plans and load guide.

### Actions

1. For each scenario name resource, fixed count/rate, changed variable, control,
   success, abort, near-neighbor, and recovery.
2. Distinguish cached fixed key from bypassed unique keys.
3. Map one bounded retry to two server requests.
4. Identify expected rejections and threshold treatment.
5. Mark AWS semantics as product-specific, local behavior as synthetic.

### Expected output

Seven pre-registered experiments with no public target and no L3/L4 method.

### Interpretation

The map connects controls to resource assumptions instead of treating rate limit
avoidance as availability impact.

### Common failure modes

- Rotating keys without measuring work/health
- One threshold for cheap and expensive routes
- Treating cache miss as evasion without resource evidence
- Unlimited retries

### Cleanup

No traffic yet.

## Why this matters offensively

Modern application-layer attacks distribute identities and select high-cost
workflows. Control scope and admission behavior are the attack surface.

## Required artifact

`artifacts/module-08/control-map.md` with seven scenario rows and source/limit labels.

## Pass gate

1. What defines an aggregation instance?
2. Why scope by endpoint?
3. How can custom keys be weak?
4. What does load shedding change?
5. What must accompany a rate bypass?

## Answer key

<details><summary>Check your reasoning</summary>

1. The configured key/value combination counted in a window.
2. Application areas have different cost and legitimate traffic.
3. Caller-controlled/cheaply rotated values split one workflow.
4. It rejects excess work to protect critical capacity/recovery.
5. Resource/service or protected-work evidence under fixed safe traffic.

</details>

## Next lesson

[Bounded load testing](04-bounded-load-testing.md) executes the pre-registered
local scenarios under hard tool and application ceilings.

