# Race conditions and resource limits

<!-- source-ids: portswigger-race-conditions-path, aate-adversarial-control-loop -->

## Progress

- Module: 04 - Automated abuse and workflow attacks
- Lesson: 5 of 5
- Depth: Integrated
- Estimated time: 4 hours
- Prerequisites:
  - [Inventory and promotion abuse](04-inventory-and-promotion-abuse.md)
  - PortSwigger account and Burp Suite familiarity from the assigned path
- Required artifact: `artifacts/module-04/limit-overrun-report.md`
- Next lesson: Control reconnaissance

## Role outcome

Detect and prove an authorized limit-overrun race by correlating concurrent
requests with the invariant and resulting server state.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [PortSwigger race conditions path](https://portswigger.net/web-security/learning-paths/race-conditions) | Limit overruns; Repeater method; named lab; methodology; rate/resource limits | Supplies detailed technique and a provider-authorized target | Use only provider-assigned targets. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Hypothesis, one coherent change, proof, remediation, retest | Structures concurrency evidence and conclusions | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
Invariant: promotion may be redeemed once.

request A: check unused -------- apply -------- mark used
request B:      check unused -------- apply -------- mark used
                       ^ race window ^

Both requests are individually valid; overlapping non-atomic transitions can
produce two benefits while the intended invariant permits one.
```

## Required external instruction

### PortSwigger race assignment

**Direct link:** [Race conditions learning path](https://portswigger.net/web-security/learning-paths/race-conditions)  
**Exact section, chapter, or unit:** Limit overrun race conditions; Detecting and exploiting limit overrun race conditions with Burp Repeater; Lab: Limit overrun race conditions; Methodology; Abusing rate or resource limits  
**Estimated time:** 2 hours  
**What to focus on:** identifying the invariant, synchronizing requests using the provider method, proving state/benefit, and ruling out sequential behavior  
**What to skip:** multi-endpoint and partial-construction attacks not included in the assigned sections  
**Expected takeaway:** complete the named provider lab and explain check/use timing, concurrency evidence, state proof, and atomic remediation.

## Course bridge

A race condition exists when outcome depends on interleaving concurrent
operations. Limit overruns commonly arise when validation and state update are
not one atomic operation. The relevant comparison is not merely concurrent
versus sequential status codes; it is whether the protected invariant is
violated in authoritative state.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE treats synchronized concurrency as one declared
    coherent change and requires the same account, action, input, and evidence
    schema in the sequential comparison and post-fix retest.

!!! warning "Safety boundary"
    Concurrency is restricted to the PortSwigger-issued lab and its taught tool
    settings. Do not redirect synchronized requests to any unassigned host. The
    AATE local application does not claim to reproduce this race.

## Worked example

| Trial | Requests | Timing | Result | Allowed conclusion |
|---|---:|---|---|---|
| Legitimate | 1 | single | one redemption | normal baseline |
| Sequential negative | 2 | A completes before B | one success, one reject | limit works sequentially |
| Concurrent | 2 | synchronized per provider method | two benefits/state changes | invariant violated under concurrency |
| Uncorrelated | 2 | unknown | two `200`s | insufficient without account/state proof |

## Guided exercise

### Objective

Complete the provider limit-overrun lab and produce a defensible race finding.

### Setup

Launch only the named Academy lab. Record its issued hostname and scenario in a
private working note. Read the provider's Repeater synchronization instructions
before sending the bounded request group.

### Exact actions or commands

1. Define the one-use or bounded-resource invariant in one sentence.
2. Capture one legitimate action and the resulting account/state value.
3. Capture a sequential second action and rejection/state result.
4. Follow the provider's exact concurrent Repeater procedure for the named lab.
5. Preserve requests, responses, concurrency method, and final account/state.
6. Explain alternative causes and why the sequential comparison matters.
7. Propose an atomic transaction/conditional update and repeat the same attack
   concept as the remediation acceptance test.

### Expected output

The Academy marks the lab solved. Evidence shows the provider's protected
one-use/limit invariant was exceeded under its synchronized request procedure,
not merely that multiple responses arrived.

### Interpretation

Concurrency is the coherent changed condition; target, account, action, and
input stay fixed. Exact state proof and a sequential comparison distinguish a
race from an ordinary missing limit or repeated valid action.

### Common failure modes

- Sending more traffic than the provider instructions require
- Recording only response codes
- Omitting the sequential negative control
- Calling any duplicate action a race without timing dependence
- Suggesting client-side locking rather than an atomic server update

### Cleanup

Close the Academy lab and Burp project according to provider guidance. Do not
commit session cookies, host-specific secrets, or screenshots with account data.

## Why this matters offensively

Automated adversaries compress time and coordinate actions that humans cannot.
Race testing attacks a state invariant rather than a fingerprint, and it often
requires accurate workflow, timing, and authoritative evidence.

## Required artifact

`artifacts/module-04/limit-overrun-report.md` with authorization, invariant,
legitimate/sequential/concurrent trials, synchronization method, state proof,
alternative explanations, impact, atomic remediation, regression test, and
exact retest.

## Pass gate

1. What distinguishes a race from an ordinary repeated action?
2. Why is a sequential second request a useful control?
3. Why are two `200` responses insufficient proof?
4. What server property must remediation provide?
5. What should the exact retest preserve?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. The invalid outcome depends on overlapping/interleaved operations against shared state.
2. It shows the intended limit works when operations do not overlap.
3. They may not represent two benefits or final invariant violation; authoritative state is required.
4. Validation and state transition must be atomic for the protected invariant.
5. Same account/state, action, inputs, synchronization method, request group, and evidence schema after the fix.

</details>

## Next lesson

[Open Module 05](../05-control-recon/index.md) to map the signal families a
traffic control may rely on before attempting any evasion.
