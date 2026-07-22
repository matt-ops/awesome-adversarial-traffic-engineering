# Recovery, remediation, and retest

<!-- source-ids: aws-builders-library-load-shedding, k6-thresholds, aate-adversarial-control-loop -->

## Progress

- Module: 08 - DDoS and resilience
- Lesson: 5 of 5
- Depth: Deep
- Estimated time: 3 hours
- Prerequisites:
  - [Bounded load testing](04-bounded-load-testing.md)
  - Complete the resource model, metric plan, and bounded scenarios
- Next lesson: Python telemetry

## Role outcome

Measure return to health, recommend resource-specific controls, and replay the
same bounded attack as a remediation acceptance test.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | Complete article | Supports admission and graceful recovery | Practitioner guidance from one large provider; adapt mechanisms to the target architecture. |
| OFFICIAL_DOCUMENTATION | [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | thresholds and failure | Supplies measurable acceptance criteria | Tool documentation; AATE adds stricter local target and load ceilings. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | impact, remediation, same-attack retest | Defines completion | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
pre-test health -> bounded pressure -> threshold/control behavior
                -> traffic stops -> health probes -> recovery time
remediation -> same target/scenario/config/evidence -> compare objective
```

## Required external instruction

### Recovery assignment

**Direct link:** [Using load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)  
**Exact section, chapter, or unit:** reread overload prevention, admission/load shedding, critical work, and recovery discussion in the complete article  
**Estimated time:** 45 minutes  
**What to focus on:** local decisions, fail-open/fail-closed effects, critical work, fairness, and proving recovery  
**What to skip:** no product implementation is assigned  
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

### Exact actions or commands

1. Record pre/pressure/post health and timestamped recovery.
2. Separate unexpected errors from intentional shedding.
3. Recommend cache, admission, endpoint, workflow, retry, and dependency controls
   only where the resource map supports them.
4. Define legitimate near-neighbor success and collateral thresholds.
5. Copy the exact scenario/config/evidence schema into the retest plan.

### Expected output

A timestamped recovery timeline records when traffic stops, the next health
sample, latency/error return to the declared objective, and any queue/cache/state
that remains. The plan maps remediation to the exhausted resource, supplies
hostile and legitimate-neighbor criteria, and preserves the exact scenario,
rate, duration, thresholds, and cleanup for retest.

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

## Check your understanding

1. After bounded pressure stops, which measurements show that the legitimate health route and affected resource returned to their objectives?
2. A remediation sheds more expensive requests but keeps critical work healthy. Can the higher controlled rejection rate represent better resilience?
3. Why should a remediation recommendation name the CPU, queue, cache, dependency, or other resource implicated by the experiment?
4. Which objective, path, scenario, envelope, fixed inputs, evidence fields, and aborts must remain the same for an exact resilience retest?
5. The loopback service becomes healthy after Docker teardown and restart. Which production recovery properties does that local observation not prove?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A recovery timeline should show legitimate latency, errors, availability, queue or resource measurements returning within the predefined health objectives.** Merely stopping the load generator does not prove recovery.

- **2. Yes.** Deliberate load shedding can improve resilience when early rejection preserves critical useful capacity and keeps the protected workflow within agreed criteria. The conclusion must include both rejection and health evidence.

- **3. Resource-specific evidence connects the observed bottleneck to the proposed control.** A generic fix can move pressure elsewhere or leave the actual limiting resource unchanged.

- **4. Repeat the same adversary objective, route, scenario configuration, hard envelope, initial state, request inputs, evidence schema, thresholds, and abort conditions.** Only the remediation should differ.

- **5. The local restart does not prove production queue draining, dependency recovery, distributed coordination, autoscaling, sustained stability, or internet-scale behavior.** Those remain explicit limitations outside the synthetic lab.

</details>

## Next lesson

[Open Module 09](../09-tooling-code-review/index.md) to build safe telemetry and
review code for timeout, retry, concurrency, and authorization flaws.
