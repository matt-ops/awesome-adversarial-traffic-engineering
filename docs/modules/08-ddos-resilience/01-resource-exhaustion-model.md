# Resource-exhaustion model

<!-- source-ids: cloudflare-ddos-introduction, aws-builders-library-load-shedding, aate-adversarial-control-loop -->

## Progress

- Module: 08 - DDoS and resilience
- Lesson: 1 of 5
- Depth: Foundation
- Estimated time: 2 hours
- Prerequisites:
  - Request/control/resource path from Module 01
  - Understand the authorization boundary and hard load-envelope controls
- Next lesson: Metrics

## Role outcome

Map a traffic dimension to the resource consumed, health effect, control,
legitimate near-neighbor, safe test, and recovery evidence.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| VENDOR_RESEARCH | [Cloudflare DDoS introduction](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) | operation; common types; volumetric/protocol/application; mitigation | Supplies introductory taxonomy only | Vendor educational overview; canonical page rejected the automated verifier but was confirmed through current browser-search indexing. |
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | Complete article | Connects overload to admission control and critical work | Practitioner guidance from one large provider; adapt mechanisms to the target architecture. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | resource path, service effect, remediation/retest | Defines offensive proof | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

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

### DDoS taxonomy assignment

**Direct link:** [Cloudflare DDoS introduction](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/)  
**Exact section, chapter, or unit:** How it works, Common types, Volumetric, Protocol, Application layer, and Mitigation  
**Estimated time:** 30 minutes  
**What to focus on:** the resource and path targeted by each traffic class, not product names  
**What to skip:** product comparisons and any attack-tool instructions  
**Expected takeaway:** classify a scenario by the finite resource and service path it pressures rather than by traffic volume alone.

### Overload and shedding assignment

**Direct link:** [Using load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)  
**Exact section, chapter, or unit:** Complete article  
**Estimated time:** 40 minutes  
**What to focus on:** overload feedback, admission, critical work, latency, rejection, and recovery  
**What to skip:** organization-specific anecdotes that do not transfer to the local service model  
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

### Exact actions or commands

1. Add bps, pps, new connections/s, concurrent connections, RPS, concurrent
   application work, HTTP streams, CPU, memory, queues, cache ratio, and dependency use.
2. Add p50/p95/p99, errors, timeouts, and recovery time.
3. Name a legitimate near-neighbor and safe test for each application dimension.
4. Mark L3/L4 execution out of local scope.
5. Choose cheap/expensive routes for the first lab.

### Expected output

For each assigned traffic dimension, the worksheet names the application route,
resource consumed, measurable health signal, current control, legitimate
near-neighbor, bounded local comparison, abort condition, recovery observation,
and identical retest. It contains no raw flood, spoofing, reflection, or
amplification procedure.

### Interpretation

The model makes request rate only one input. Equal RPS can produce different CPU,
queue, cache, database, or downstream work, so the claimed service effect must be
tied to the consumed resource and health signal. This is the decision gate for
whether a bounded experiment can answer the hypothesis at all.

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

## Check your understanding

1. The cheap route and expensive route receive the same requests per second, but only the expensive route breaches its latency objective. Why can equal request rates create different impact?
2. An edge begins rejecting excess expensive work before the application collapses. Which useful capacity is load shedding intended to protect?
3. Which percentile metrics in the lesson describe tail latency, and why is p50 still useful as baseline context?
4. Why should the resource model include a legitimate near-neighbor workflow alongside the pressure scenario?
5. Which network-level traffic classes are explicitly excluded from the local application-layer exercises?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Routes can consume different CPU, memory, cache, queue, and dependency work for every request.** Request rate alone therefore does not describe the resource cost or resulting service-health effect.

- **2. Load shedding protects critical useful service capacity by refusing excess work before shared resources collapse.** More deliberate rejection can improve resilience when healthy priority work stays within its objective.

- **3. p95 and p99 describe the slower tail of measured requests, while p50 shows the typical middle observation.** Together they distinguish broad slowdown from a smaller group of severely delayed requests.

- **4. The near-neighbor measures whether controls also harm intended clients or workflows that resemble the pressure traffic.** Resilience improvements should preserve legitimate behavior, not merely reduce attacker success.

- **5. The course excludes Layer 3 and Layer 4 floods, source spoofing, reflection, and amplification.** The executable work stays loopback-only, bounded, and focused on synthetic application-layer resource behavior.

</details>

## Next lesson

[Metrics](02-metrics.md) defines service effect, thresholds, and recovery measurements.
