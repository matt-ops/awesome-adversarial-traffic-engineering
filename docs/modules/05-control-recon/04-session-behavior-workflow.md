# Session, behavior, and workflow signals

<!-- source-ids: fpscanner-project, aate-adversarial-control-loop, aate-local-lab -->

## Progress

- Module: 05 - Control reconnaissance
- Lesson: 4 of 5
- Depth: Applied
- Estimated time: 2 hours
- Prerequisites:
  - [Cross-context consistency](03-cross-context-consistency.md)
  - Module 04 workflow/rate artifacts
- Required artifact: `artifacts/module-05/state-behavior-map.md`
- Next lesson: Establish the blocked baseline

## Role outcome

Map replay, session binding, timing, sequence, rate, and resource-use evidence
alongside browser signals for the same adversary objective.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Anti-replay discussion; limits/non-goals | Supplies nonce/timestamp concepts and boundaries | Observations are valid only for the recorded code and browser versions. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Workflow map, fixed variables, repeat action | Joins browser and server evidence | Course synthesis; no cited standard defines the exact fifteen-step sequence. |
| LAB_SPECIFIC | [Local API guide](../../labs/applied/local-api.md) | Challenge, rate, telemetry, protected control | Supplies stateful examples | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

| Surface | Question | Evidence |
|---|---|---|
| Session binding | is proof tied to session/action? | cross-session replay result |
| Freshness | can payload/token be reused? | nonce/timestamp/use record |
| Sequence | were required steps completed? | state-transition log |
| Velocity | how quickly/repeatedly? | timestamps and aggregation key |
| Resource pattern | what work is induced? | endpoint/dependency/health metrics |

## Required external instruction

### FPScanner anti-replay assignment

**Direct link:** [FPScanner](https://github.com/antoinevastel/fpscanner)  
**Exact section, chapter, or unit:** Anti-replay discussion and Limits/non-goals; reread Cross-Context Validation only where it interacts with payload collection  
**Estimated time:** 30 minutes  
**What to focus on:** freshness, nonce, timestamp, binding, and what replay resistance does not establish  
**What to skip:** installation and unrelated detection tests  
**Expected takeaway:** distinguish making a sensor payload fresh from authorizing the downstream business action.

## Course bridge

Browser evidence is one input to a server decision. Server state can bind a
sensor result to a session, action, time window, nonce, or single use. Behavior
adds ordered actions and timing. Workflow evidence asks whether the caller
completed prerequisites and whether the final action changed authoritative state.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Draw browser, protocol, session, behavior, and protected
    action as correlated layers. A convincing property change can still fail at
    replay, account, rate, or workflow enforcement.

## Worked example

The local control consumes a unique nonce and issues an action token once. A
second evaluation with the same nonce returns `409`; a second protected action
with the used token returns `403`. This models freshness/use, not cryptographic
sensor integrity or a production challenge.

## Guided exercise

### Objective

Add session and behavior fields to the control-surface map.

### Setup

Use the local OpenAPI map and existing challenge/rate/control tests. No new
traffic is required.

### Exact actions or commands

1. Map issuance, storage, presentation, verification, consumption, and expiry
   for challenge and control tokens.
2. Map rate key, counter, window assumption, and accepted action.
3. Add workflow order and server evidence for reservation/report actions.
4. Identify which client-controlled values look like identity but are not bound.
5. Add one replay and one temporal hypothesis for later testing.

### Expected output

A state diagram showing tokens/nonces and action transitions, plus a behavior
table tied to server evidence rather than a fingerprint alone.

### Interpretation

This completes the candidate control surface. The next lesson freezes inputs and
records actual stock decisions before a bypass hypothesis is executed.

### Common failure modes

- Calling a fresh sensor payload authorization
- Ignoring action-token consumption
- Treating a rotated caller key as a new adversary
- Inferring behavior from one event

### Cleanup

No service change occurred. Keep secrets and real session IDs out of artifacts.

## Why this matters offensively

Adversarial automation must maintain state and complete workflows. Controls that
combine runtime and server evidence may expose a client that only patches the
visible browser surface.

## Required artifact

`artifacts/module-05/state-behavior-map.md` with token lifecycles, binding table,
behavior sequence, server proof, candidate hypotheses, and limits.

## Pass gate

1. What does a nonce prevent when enforced correctly?
2. Does freshness authorize a business action?
3. What makes a rate key weak?
4. Why correlate sequence with server state?
5. What does token consumption add?

## Answer key

<details><summary>Check your reasoning</summary>

1. Reuse of the same accepted payload/transaction identifier.
2. No; authorization is a separate server decision.
3. The adversary can cheaply choose/rotate it without changing the underlying workflow identity.
4. Requests can occur without completing intended transitions or the objective.
5. It bounds one authorization result to one accepted use in this model.

</details>

## Next lesson

[Establish the blocked baseline](05-blocked-baseline.md) captures the required
population matrix and freezes the evasion experiment.
