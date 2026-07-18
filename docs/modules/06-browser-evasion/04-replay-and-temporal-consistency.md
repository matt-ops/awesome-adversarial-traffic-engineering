# Replay and temporal consistency

<!-- source-ids: fpscanner-project, fp-inconsistent, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 06 - Browser-control evasion
- Lesson: 4 of 5
- Depth: Integrated
- Estimated time: 3 hours
- Prerequisites:
  - [Identity coherence](03-identity-coherence.md)
  - Local challenge and control artifacts
- Required artifact: `artifacts/module-06/replay-temporal.md`
- Next lesson: Version drift

## Role outcome

Test sensor and authorization replay separately and identify temporal changes
that invalidate an otherwise coherent snapshot.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Anti-replay discussion; limits | Provides sensor freshness concepts | Observations are valid only for the recorded code and browser versions. |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | Temporal inconsistency analysis; §8.4 | Supports cross-time comparison and limits | Preprint studying a specific dataset, honey-site design, bot population, and selected services; not universal proof. |
| LAB_SPECIFIC | [Control-recon lab](../../labs/integrated/control-recon.md) | nonce and one-use action token | Supplies replay outcomes | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Repeat action, alternatives, retest | Separates replay layers | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Replayed object | Binding expected | Local result | Meaning |
|---|---|---|---|
| evaluation nonce/payload | uniqueness | repeated nonce `409` | sensor submission reuse rejected |
| control action token | single use | second action `403` | issued authorization consumed |
| older challenge token | session/action/expiry/use absent | cross-session `200` | intentional separate weak binding |
| fingerprint snapshot | time/environment | offline comparison | similarity is not authorization |

## Required external instruction

### FPScanner anti-replay assignment

**Direct link:** [FPScanner](https://github.com/antoinevastel/fpscanner)  
**Exact section, chapter, or unit:** anti-replay discussion, payload collection flow, limits, and non-goals  
**Estimated time:** 25 minutes  
**What to focus on:** payload freshness, nonce purpose, collection location, and the downstream action not covered by a sensor nonce  
**What to skip:** external replay attempts and unrelated implementation details  
**Expected takeaway:** explain which exact payload replay a nonce can reject and why an action token still needs independent binding.

### FP-Inconsistent temporal assignment

**Direct link:** [FP-Inconsistent](https://arxiv.org/abs/2406.07647)  
**Exact section, chapter, or unit:** temporal-inconsistency analysis in §§6-7 and §8.4 Limitations  
**Estimated time:** 35 minutes  
**What to focus on:** longitudinal change, observation windows, population/dataset limits, and alternative causes of temporal inconsistency  
**What to skip:** claims beyond the paper's threat model and collection method  
**Expected takeaway:** separate one captured snapshot, replay resistance, and longitudinal identity consistency into different hypotheses.

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

### Exact actions or commands

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
