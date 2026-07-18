# Resilience metrics and thresholds

<!-- source-ids: k6-thresholds, aws-builders-library-load-shedding, aate-adversarial-control-loop -->

## Progress

- Module: 08 - DDoS and resilience
- Lesson: 2 of 5
- Depth: Foundation
- Estimated time: 2 hours
- Prerequisites:
  - [Resource model](01-resource-exhaustion-model.md)
  - Basic percentiles and error-rate interpretation
- Required artifact: `artifacts/module-08/metric-plan.md`
- Next lesson: Edge controls

## Role outcome

Define baseline, health objective, threshold, abort, recovery, and limitations
before generating bounded traffic.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | syntax; failure; abort-on-fail; examples | Defines executable pass/fail criteria | Tool documentation; AATE adds stricter local target and load ceilings. |
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | metrics/admission/recovery discussion | Frames rejection versus protected health | Practitioner guidance from one large provider; adapt mechanisms to the target architecture. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | predictions, evidence, retest | Prevents post-hoc success criteria | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Metric | Question | Caveat |
|---|---|---|
| p50/p95/p99 | distribution/tail latency | tiny samples make high percentiles unstable |
| error/timeout rate | completed/rejected/absent service | expected shedding must be tagged separately |
| queue/CPU/memory/cache/dependency | resource cause candidate | correlation needs server telemetry |
| recovery time | return to objective after stop | surviving traffic is not recovery |

## Required external instruction

### k6 threshold assignment

**Direct link:** [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/)  
**Exact section, chapter, or unit:** threshold syntax; failure behavior; abort-on-fail behavior; latency/error examples  
**Estimated time:** 40 minutes  
**What to focus on:** metric expression, exit status, abort delay, and predeclared thresholds  
**What to skip:** cloud outputs and custom metric development  
**Expected takeaway:** explain each local threshold and how it fails safely.

## Course bridge

k6 thresholds turn selected metrics into pass/fail conditions and can abort on
failure.[^k6]

[^k6]: Grafana k6 documentation, "Thresholds," assigned sections.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Distinguish test safety aborts from the service objective.
    The local `p95<1000ms` ceiling protects the exercise; a real engagement's
    objective comes from approved SLOs and telemetry owners.

## Worked example

The script aborts when checks fall below 95%, HTTP failures reach 20%, or p95
exceeds 1000 ms. A retry scenario marks the designed first `503` expected so the
failure metric measures surprises rather than the fixture contract.

## Guided exercise

### Objective

Write a metric/threshold plan and inspect dry-run behavior.

### Setup

Read the load guide and script safety block before executing k6.

### Exact actions or commands

1. Define legitimate and adversarial health metrics and sample limits.
2. Define safety thresholds/abort and objective thresholds separately.
3. Execute the documented dry run.
4. Verify zero network bytes/requests and printed configuration.
5. Explain expected versus unexpected `503` accounting.

### Expected output

Dry-run prints configuration and zero network traffic. The plan includes tails,
errors, timeouts, resource telemetry, and recovery.

### Interpretation

A threshold is meaningful only when the metric scope, expected statuses, sample
size, observation window, and abort behavior are declared. A p95 from a tiny
sample is unstable; an intentional 429 or 503 can be a correct control outcome
rather than generic failure; and client latency cannot substitute for the
resource and recovery telemetry named by the hypothesis.

### Common failure modes

- Choosing thresholds after seeing results
- Counting designed shedding as tool failure without labels
- Claiming p99 from tiny samples as capacity
- Omitting exit/abort evidence

### Cleanup

Remove `AATE_DRY_RUN` only when the next lesson authorizes a real local scenario.

## Why this matters offensively

Predeclared service effects and aborts keep resilience testing safe and findings
defensible.

## Required artifact

`artifacts/module-08/metric-plan.md` with baselines, objectives, safety thresholds,
resource metrics, sample limits, abort, and recovery.

## Pass gate

1. What does p95 mean?
2. Why tag expected `503`?
3. What is threshold exit status for?
4. Why separate safety and service thresholds?
5. What proves dry-run safety?

## Answer key

<details><summary>Check your reasoning</summary>

1. 95% of measured values are at or below it.
2. So deliberate fixture/shedding behavior is not counted as unexpected failure.
3. Automation and operators can detect a failed criterion.
4. One protects the experiment; one evaluates approved resilience objectives.
5. Printed configuration plus zero network bytes/requests.

</details>

## Next lesson

[Edge controls](03-edge-controls.md) maps aggregation windows, custom keys,
endpoint scope, and admission behavior to bypass hypotheses.
