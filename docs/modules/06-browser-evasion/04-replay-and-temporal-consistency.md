# Replay and temporal consistency

<!-- source-ids: fpscanner-project, fp-inconsistent, aate-local-lab, aate-adversarial-control-loop -->

> **Progress**  
> Module: 06 - Browser-control evasion  
> Lesson: 4 of 5  
> Depth: Integrated  
> Estimated time: 3 hours  
> Prerequisites: Identity coherence  
> Artifact: `artifacts/module-06/replay-temporal.md`  
> Next: Version drift

## Role outcome

Test sensor and authorization replay separately and identify temporal changes
that invalidate an otherwise coherent snapshot.

## Prerequisites

- [Identity coherence](03-identity-coherence.md)
- Local challenge and control artifacts

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Anti-replay discussion; limits | Provides sensor freshness concepts |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | Temporal inconsistency analysis; §8.4 | Supports cross-time comparison and limits |
| LAB_SPECIFIC | [Control-recon lab](../../labs/integrated/control-recon.md) | nonce and one-use action token | Supplies replay outcomes |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Repeat action, alternatives, retest | Separates replay layers |

## Mental model

| Replayed object | Binding expected | Local result | Meaning |
|---|---|---|---|
| evaluation nonce/payload | uniqueness | repeated nonce `409` | sensor submission reuse rejected |
| control action token | single use | second action `403` | issued authorization consumed |
| older challenge token | session/action/expiry/use absent | cross-session `200` | intentional separate weak binding |
| fingerprint snapshot | time/environment | offline comparison | similarity is not authorization |

## Required external instruction

### Replay/temporal assignment

**Direct link:** [FPScanner](https://github.com/antoinevastel/fpscanner) and [FP-Inconsistent](https://arxiv.org/abs/2406.07647)  
**Exact assignment:** FPScanner anti-replay discussion and non-goals; FP-Inconsistent temporal-inconsistency portions of §§6-8.4  
**Estimated time:** 60 minutes  
**Focus on:** payload freshness, binding, time windows, longitudinal change, and limits  
**Skip:** external replay attempts and unrelated implementation details  
**Expected takeaway:** explain which replay layer a nonce protects and which downstream action may remain weak.

## Course bridge

Freshness proves only that an identifier was not accepted before under the
server's model. Binding determines whether the accepted result belongs to a
session, action, origin, and use. Temporal consistency compares environment
claims across time; legitimate updates and mobility also change them.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Test sensor replay, issued authorization replay, and the
    protected action as separate transitions. Never infer all three from one nonce.

## Worked example

The control lab supports the first one-variable action and rejects its token
reuse. The older challenge lab accepts a token in another synthetic session.
These deliberately opposite results teach that "anti-replay" is not a single
property; inspect binding for the specific object and action.

## Guided exercise

### Objective

Compare two local replay designs and build a temporal observation plan.

### Setup

Use existing control-recon evidence. With local API healthy, the challenge replay
runner is fixed and bounded.

### Actions

1. Verify control artifact's first action `200` and second `403`.
2. Execute `python -m lab.run bypass` and preserve `403` baseline, token issuance,
   cross-session `200`, and returned session.
3. Map nonce/token binding dimensions for both endpoints.
4. Define two observation times with browser/framework versions fixed or recorded.
5. List legitimate temporal changes and a remediation/retest for the weak token.

### Expected output

Control token is single-use; challenge token replays across sessions. The plan
separates environment drift from replay acceptance.

### Interpretation

A strong sensor nonce cannot repair a downstream authorization token that lacks
session/action/use binding. Conversely, replay rejection does not prove identity.

### Common failure modes

- Calling every token the same control
- Omitting the original blocked request
- Treating changed browser version as adversarial temporal inconsistency
- Claiming single-use prevents token theft

### Cleanup

Reset the API. Store only synthetic tokens; they have no external value.

## Why this matters offensively

Real adversaries reuse acquired capability. Red-team replay tests expose where
fresh collection is present but authorization or workflow binding remains weak.

## Required artifact

`artifacts/module-06/replay-temporal.md` with object lifecycles, binding matrix,
two outcomes, temporal plan, alternatives, remediation, and exact retest.

## Pass gate

1. What does nonce replay `409` establish?
2. Why is action-token replay a separate test?
3. What binding is missing in the challenge lab?
4. Can temporal change be legitimate?
5. What must retest repeat?

## Answer key

<details><summary>Check your reasoning</summary>

1. That exact nonce was already consumed in the local evaluation model.
2. Evaluation acceptance and downstream action authorization are different transitions.
3. Session, action, expiry, and one-use binding are absent intentionally.
4. Yes; updates, mobility, privacy settings, and hardware/environment changes occur.
5. Same cross-session token procedure and protected action after binding remediation.

</details>

## Next lesson

[Version drift and residual anomalies](05-version-drift-and-residual-anomalies.md)
turns version metadata and unexplained evidence into a durable retest plan.

