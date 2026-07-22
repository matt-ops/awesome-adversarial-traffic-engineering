# Bounded application-layer load testing

<!-- source-ids: k6-thresholds, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 08 - DDoS and resilience
- Lesson: 4 of 5
- Depth: Applied
- Estimated time: 4 hours
- Prerequisites:
  - [Edge controls](03-edge-controls.md)
  - k6 installed from official Grafana distribution
  - Healthy local API and approved metric/control map
- Next lesson: Recovery and retest

## Role outcome

Execute seven fixed-loopback scenarios with hard duration/VU/rate/total ceilings,
abort thresholds, dry-run evidence, and scenario-specific interpretation.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | syntax; failure; abort | Grounds executable safety behavior | Tool documentation; AATE adds stricter local target and load ceilings. |
| LAB_SPECIFIC | [Bounded load lab](../../labs/deep/bounded-load.md) | all seven scenarios and ceilings | Supplies tested local script | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Steps 4-15 | Structures the bounded comparison, protected service effect, remediation criteria, and identical retest | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

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
**Exact section, chapter, or unit:** reread syntax, exit/failure, abort-on-fail, latency/error examples immediately before execution  
**Estimated time:** 25 minutes  
**What to focus on:** interpreting threshold output and nonzero exit  
**What to skip:** cloud execution and distributed generators  
**Expected takeaway:** stop/diagnose on threshold failure rather than increasing limits.

## Course bridge

The script validates configuration during initialization, before a traffic
executor exists. Dry run performs one zero-request iteration. Each live iteration
uses at most two requests. Reset/recovery and scenario-specific cache or identity
seeding add at most four lifecycle requests, and the 100-request formula includes
that worst case.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** The seven scenario contracts use the AATE sequence of
    fixed baselines, one declared pair, protected service evidence, limitations,
    remediation criteria, and the same bounded retest. A pair is called a
    control comparison only when the local application implements the control.

!!! warning "Safety boundary"
    Never edit out a guard, use an external target, or raise a ceiling. These are
    educational comparisons, not production capacity tests.

## Worked example

At one iteration/s for one second, a two-request scenario may schedule two
iterations plus setup/teardown and report six HTTP requests. Cache priming can
raise that total to seven; two fixed-key seed calls can raise it to eight. The
ceiling formula accounts for the boundary iteration and the worst-case four
lifecycle requests.

## Guided exercise

### Objective

Execute dry run, then each assigned scenario once at conservative settings.

### Setup

Start/reset the local API. Follow the load guide; preserve console output.

### Exact actions or commands

1. Execute dry run and prove zero network traffic.
2. Set duration `1`, rate `1`, VUs `1` for initial validation.
3. Execute the seven scenario values one at a time.
4. Preserve checks, requests, latency, errors, thresholds, configuration, and recovery.
5. For retry, verify expected `503` is classified and one retry returns `200`.
6. Separate runtime observations, deterministic fixture assertions, and course interpretation.
7. Do not increase load to create a dramatic effect.

### Expected output

All seven scenarios pass their named assertions, thresholds, and immediate
recovery-health checks. The one-second initial envelope ordinarily uses six
requests for two-request scenarios, seven for cache priming, eight for fixed-key
seeding, and four for recovery. `endpoint-cost-observation` and
`workflow-sequence-observation` explicitly report that no mitigation is active.

### Interpretation

Results demonstrate the specifically asserted local fixture behavior and working
safety controls. They do not establish endpoint/workflow mitigation, DDoS
magnitude, sustained recovery, or production protection.

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

## Check your understanding

1. The k6 script receives a non-loopback target or an excessive VU ceiling. When must destination and envelope validation reject the configuration?
2. Why does the lesson include a possible iteration scheduled at the duration boundary when calculating the maximum total work?
3. A latency or error threshold fails during a bounded scenario. What should the operator do instead of increasing the limit and rerunning immediately?
4. The fixture deliberately returns one expected status class. What does expected-status classification change in the result analysis?
5. Seven loopback scenarios complete under fixed ceilings. What may the learner claim from those results, and which production claim remains unsupported?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Validation must reject the target or envelope during script initialization, before traffic executors and workers begin sending requests.** Unsafe configuration should fail closed without relying on operator timing.

- **2. Arrival scheduling can place an iteration exactly at the declared duration boundary.** Including that possibility makes the total-work ceiling conservative and prevents an off-by-one safety underestimate.

- **3. Abort according to the plan, preserve the evidence, confirm recovery, and diagnose the failed criterion.** Raising limits after failure would discard the safety boundary and change the experiment.

- **4. Classification separates deliberate fixture or shedding responses from unexpected failures while preserving both counts.** It changes interpretation, not the actual response or hard safety envelope.

- **5. The learner may claim relative synthetic behavior and verified local safety or control logic under the recorded envelope.** The results do not establish production capacity, internet-scale resilience, or universal control performance.

</details>

## Next lesson

[Recovery and retest](05-recovery-and-retest.md) turns an availability observation
into remediation criteria and an exact post-fix attack.
