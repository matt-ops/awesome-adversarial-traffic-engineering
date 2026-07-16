# Bounded application-layer load testing

<!-- source-ids: k6-thresholds, aate-local-lab, aate-adversarial-control-loop -->

> **Progress**  
> Module: 08 - DDoS and resilience  
> Lesson: 4 of 5  
> Depth: Integrated  
> Estimated time: 4 hours  
> Prerequisites: Edge and admission controls  
> Artifact: `artifacts/module-08/bounded-results.md`  
> Next: Recovery and retest

## Role outcome

Execute seven fixed-loopback scenarios with hard duration/VU/rate/total ceilings,
abort thresholds, dry-run evidence, and scenario-specific interpretation.

## Prerequisites

- [Edge controls](03-edge-controls.md)
- k6 installed from official Grafana distribution
- Healthy local API and approved metric/control map

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | syntax; failure; abort | Grounds executable safety behavior |
| LAB_SPECIFIC | [Bounded load lab](../../labs/deep/bounded-load.md) | all seven scenarios and ceilings | Supplies tested local script |
| Course synthesis (`COURSE_SYNTHESIS`) | [AATE loop](../../methodology/adversarial-control-loop.md) | controlled experiments and proof | Structures comparison |

## Mental model

| Guard | Hard local value |
|---|---:|
| target | localhost/127.0.0.1:8080 only |
| duration | <=15 seconds |
| VUs | <=5 |
| effective request rate | <=10/s |
| worst-case total | <=100 including setup/teardown |
| safety thresholds | checks, p95, unexpected errors; abort-on-fail |

## Required external instruction

### k6 execution assignment

**Direct link:** [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/)  
**Exact assignment:** reread syntax, exit/failure, abort-on-fail, latency/error examples immediately before execution  
**Estimated time:** 25 minutes  
**Focus on:** interpreting threshold output and nonzero exit  
**Skip:** cloud execution and distributed generators  
**Expected takeaway:** stop/diagnose on threshold failure rather than increasing limits.

## Course bridge

The script validates configuration during initialization, before a traffic
executor exists. Dry run performs one zero-request iteration. Each live iteration
uses at most two requests; setup/teardown add reset/recovery checks.

!!! warning "Safety boundary"
    Never edit out a guard, use an external target, or raise a ceiling. These are
    educational comparisons, not production capacity tests.

## Worked example

At one iteration/s for one second, a two-request scenario may schedule two
iterations plus setup/teardown and report six HTTP requests. The ceiling formula
accounts for the boundary iteration and two lifecycle requests.

## Guided exercise

### Objective

Execute dry run, then each assigned scenario once at conservative settings.

### Setup

Start/reset the local API. Follow the load guide; preserve console output.

### Actions

1. Execute dry run and prove zero network traffic.
2. Set duration `1`, rate `1`, VUs `1` for initial validation.
3. Execute the seven scenario values one at a time.
4. Preserve checks, requests, latency, errors, thresholds, configuration, and recovery.
5. For retry, verify expected `503` is classified and one retry returns `200`.
6. Do not increase load to create a dramatic effect.

### Expected output

All seven scenarios pass thresholds and recovery health. Initial verified runs
used six requests for two-request scenarios and four for recovery.

### Interpretation

Results demonstrate relative local behavior and working safety controls. They do
not establish DDoS magnitude or production protection.

### Common failure modes

- Treating setup/teardown requests as invisible
- Raising load after a weak effect
- Allowing expected `503` to fail the error threshold
- Comparing scenarios with different configs silently

### Cleanup

Stop k6, reset app, and stop Compose. No process should continue generating traffic.

## Why this matters offensively

Bounded tests prove control/resource assumptions safely. The quality is in the
comparison and evidence, not traffic volume.

## Required artifact

`artifacts/module-08/bounded-results.md` with seven configs/results, request
counts, thresholds, effects, limitations, and no-production-capacity claim.

## Pass gate

1. When are target/ceiling checks evaluated?
2. Why include a boundary iteration in total math?
3. What should happen on threshold failure?
4. What does expected-status classification do?
5. What may the local results claim?

## Answer key

<details><summary>Check your reasoning</summary>

1. Script initialization, before traffic executor setup.
2. Arrival scheduling may include an iteration at the duration boundary.
3. Abort, preserve evidence, diagnose; do not raise limits.
4. Separates deliberate fixture response from unexpected request failure.
5. Relative synthetic behavior and safety/control logic only.

</details>

## Next lesson

[Recovery and retest](05-recovery-and-retest.md) turns an availability observation
into remediation criteria and an exact post-fix attack.
