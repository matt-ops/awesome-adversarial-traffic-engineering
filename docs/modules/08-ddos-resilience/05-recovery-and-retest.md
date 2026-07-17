# Recovery, remediation, and retest

<!-- source-ids: aws-builders-library-load-shedding, k6-thresholds, aate-adversarial-control-loop -->

> **Progress**  
> Module: 08 - DDoS and resilience  
> Lesson: 5 of 5  
> Depth: Deep  
> Estimated time: 3 hours  
> Prerequisites: Bounded load testing  
> Artifact: `artifacts/module-08/recovery-retest.md`  
> Next: Python telemetry

## Role outcome

Measure return to health, recommend resource-specific controls, and replay the
same bounded attack as a remediation acceptance test.

## Prerequisites

- [Bounded load testing](04-bounded-load-testing.md)
- Complete resource, metric, and scenario artifacts

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | Complete article | Supports admission and graceful recovery |
| OFFICIAL_DOCUMENTATION | [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | thresholds and failure | Supplies measurable acceptance criteria |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | impact, remediation, same-attack retest | Defines completion |

## Mental model

```text
pre-test health -> bounded pressure -> threshold/control behavior
                -> traffic stops -> health probes -> recovery time
remediation -> same target/scenario/config/evidence -> compare objective
```

## Required external instruction

### Recovery assignment

**Direct link:** [Using load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)  
**Exact assignment:** reread overload prevention, admission/load shedding, critical work, and recovery discussion in the complete article  
**Estimated time:** 45 minutes  
**Focus on:** local decisions, fail-open/fail-closed effects, critical work, fairness, and proving recovery  
**Skip:** no product implementation is assigned  
**Expected takeaway:** propose resource-specific remediation with a measurable legitimate-health objective.

## Course bridge

Traffic stopping is not recovery. Recovery is the measured return of legitimate
health, queues, dependencies, and error/timeout rates to predeclared objectives.
Shedding may intentionally reject excess requests while improving critical health.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Exact retest preserves adversary objective, path,
    scenario, load envelope, fixed variables, legitimate probe, evidence schema,
    and aborts after remediation.

## Worked example

Remediation may cache fixed report inputs, add endpoint admission, bound retry
budget, and aggregate a workflow identity. The current lab can exactly repeat
`cache-bypass`, `endpoint-cost-observation`, `retry-amplification`, and
`identity-key`; proving a newly implemented endpoint/workflow control requires a
separate before/after configuration plus assertions. Success is protected health
and bounded recovery, not zero rejections.

## Guided exercise

### Objective

Write recovery evidence and one exact remediation retest.

### Setup

Use the verified k6 outputs and teardown health results. No additional pressure is needed.

### Actions

1. Record pre/pressure/post health and timestamped recovery.
2. Separate unexpected errors from intentional shedding.
3. Recommend cache, admission, endpoint, workflow, retry, and dependency controls
   only where the resource map supports them.
4. Define legitimate near-neighbor success and collateral thresholds.
5. Copy the exact scenario/config/evidence schema into the retest plan.

### Expected output

A recovery timeline, evidence limitations, mapped remediation, measurable
criteria, and exact command/config for retest.

### Interpretation

The local teardown assertion proves a `200` health response within 1,000 ms. It
does not measure sustained recovery or queues/dependencies absent from the toy
app. State that limit.

### Common failure modes

- Calling traffic stop recovery
- Recommending generic scaling without bottleneck evidence
- Requiring zero shedding
- Changing test envelope after remediation

### Cleanup

Stop the local stack and preserve outputs/version/config.

## Why this matters offensively

A resilience finding is actionable when it identifies the exhausted resource,
protects legitimate work, and provides the same attack as a regression test.

## Required artifact

`artifacts/module-08/recovery-retest.md` with timeline, health/resources,
remediation mapping, legitimate criteria, exact retest, and limits.

## Pass gate

1. What proves recovery?
2. Can increased rejection indicate better resilience?
3. Why map remediation to resource evidence?
4. What makes retest exact?
5. What does local teardown health not prove?

## Answer key

<details><summary>Check your reasoning</summary>

1. Measured return of legitimate health/resource metrics to objectives after pressure stops.
2. Yes, if controlled shedding protects critical work within criteria.
3. Otherwise the fix may move or miss the bottleneck.
4. Same objective, path, scenario, envelope, fixed inputs, evidence, and aborts.
5. Production queues, dependencies, scale, or sustained recovery.

</details>

## Next lesson

[Open Module 09](../09-tooling-code-review/index.md) to build safe telemetry and
review code for timeout, retry, concurrency, and authorization flaws.
