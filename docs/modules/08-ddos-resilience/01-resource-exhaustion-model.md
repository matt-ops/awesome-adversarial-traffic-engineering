# Resource-exhaustion model

<!-- source-ids: cloudflare-ddos-introduction, aws-builders-library-load-shedding, aate-adversarial-control-loop -->

> **Progress**  
> Module: 08 - DDoS and resilience  
> Lesson: 1 of 5  
> Depth: Foundation  
> Estimated time: 2 hours  
> Prerequisites: Modules 00-07  
> Artifact: `artifacts/module-08/resource-model.md`  
> Next: Metrics

## Role outcome

Map a traffic dimension to the resource consumed, health effect, control,
legitimate near-neighbor, safe test, and recovery evidence.

## Prerequisites

- Request/control/resource path from Module 01
- Authorization and load-envelope safety artifacts

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| VENDOR_RESEARCH | [Cloudflare DDoS introduction](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) | operation; common types; volumetric/protocol/application; mitigation | Supplies introductory taxonomy only |
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | Complete article | Connects overload to admission control and critical work |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | resource path, service effect, remediation/retest | Defines offensive proof |

## Mental model

```text
traffic dimension -> finite resource -> queue/contention -> health signal
                  -> control/admission -> legitimate near-neighbor
                  -> bounded test -> recovery -> remediation retest
```

| Dimension | Candidate resource | Example health signal |
|---|---|---|
| bps/pps | link/device packet work | loss, saturation |
| new/concurrent connections | sockets, handshake CPU/state | accept errors, handshake latency |
| RPS/concurrent work | workers, CPU, queues, dependencies | p95/p99, errors, queue depth |
| streams | connection/flow-control state | resets, stream waits |

## Required external instruction

### DDoS/resource assignment

**Direct link:** [Cloudflare DDoS introduction](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) and [Using load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)  
**Exact assignment:** Cloudflare How it works, Common types, Volumetric, Protocol, Application layer, Mitigation; complete AWS article  
**Estimated time:** 70 minutes  
**Focus on:** classification by resource/path, overload feedback, admission, critical work, and recovery  
**Skip:** product comparisons and any attack-tool instructions  
**Expected takeaway:** explain why equal RPS can produce unequal impact and why successful shedding may increase rejected requests while protecting health.

## Course bridge

Application-layer pressure is dangerous when inexpensive attacker input triggers
disproportionate server work. Load shedding rejects excess work before overload
destroys useful capacity.[^shedding]

[^shedding]: AWS Builders' Library, "Using load shedding to avoid overload."

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE defines success as an authorized service-health or
    resource effect, not traffic volume. Every test names abort and recovery.

## Worked example

Five health requests and five `work=100` report requests have equal count but
unequal CPU work. The useful comparison fixes count while measuring latency and
health. It does not estimate production capacity.

## Guided exercise

### Objective

Build one resource chain for every required dimension.

### Setup

Use your architecture map; no load tool yet.

### Actions

1. Add bps, pps, new connections/s, concurrent connections, RPS, concurrent
   application work, HTTP streams, CPU, memory, queues, cache ratio, and dependency use.
2. Add p50/p95/p99, errors, timeouts, and recovery time.
3. Name a legitimate near-neighbor and safe test for each application dimension.
4. Mark L3/L4 execution out of local scope.
5. Choose cheap/expensive routes for the first lab.

### Expected output

A complete chain per dimension with no raw flood or spoofing procedure.

### Interpretation

The model selects relevant measurements before traffic exists and prevents RPS
from becoming a proxy for every availability mechanism.

### Common failure modes

- Equating high RPS with DDoS success
- Omitting dependencies/cache/queues
- Measuring attack traffic but not legitimate health
- Missing abort/recovery

### Cleanup

No traffic generated.

## Why this matters offensively

Red teams attack capacity assumptions. Resource mapping identifies the lowest-cost
workflow and the evidence needed to recommend targeted controls.

## Required artifact

`artifacts/module-08/resource-model.md` with all dimensions, resources, health,
controls, near-neighbors, safe tests, aborts, and recovery.

## Pass gate

1. Why can equal RPS have different impact?
2. What does load shedding protect?
3. Which metrics describe tail latency?
4. Why include a near-neighbor?
5. What local traffic class is excluded?

## Answer key

<details><summary>Check your reasoning</summary>

1. Routes cause different work/cache/dependency use.
2. Critical useful capacity by refusing excess work before collapse.
3. p95/p99 (and p50 for baseline context).
4. To measure collateral impact on legitimate similar clients/workflows.
5. L3/L4 floods, spoofing, reflection, and amplification.

</details>

## Next lesson

[Metrics](02-metrics.md) defines service effect, thresholds, and recovery measurements.

