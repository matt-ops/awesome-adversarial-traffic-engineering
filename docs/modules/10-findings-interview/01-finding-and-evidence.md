# Finding and evidence

<!-- source-ids: nist-sp-800-115, aate-adversarial-control-loop, aate-local-lab -->

> **Progress**
>
> Module: 10 - Findings, briefing, and interview practice
>
> Lesson: 1 of 5
>
> Depth: Foundation
>
> Estimated time: 3 hours
>
> Prerequisites: Python telemetry as evidence
>
> Artifact: `artifacts/module-10/finding.md`
>
> Next: Remediation and exact retest

## Role outcome

Write a reproducible synthetic finding that connects a scoped precondition and
attack action to a protected effect without overstating identity, prevalence, or production impact.

## Prerequisites

- [Python telemetry as evidence](../09-tooling-code-review/01-python-telemetry.md)
- One synthetic evidence artifact with raw observations and a stated limitation

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §§8.1-8.3 reporting, mitigation, resolution | Grounds assessment communication |
| Course synthesis (`COURSE_SYNTHESIS`) | [Adversarial-control loop](../../methodology/adversarial-control-loop.md) | evidence, impact, limitation, remediation, retest | Structures the local finding |
| LAB_SPECIFIC | [Finding and briefing lab](../../labs/deep/finding-briefing.md) | challenge replay example and structure | Supplies a complete local model |

## Mental model

```text
scope + precondition + exact action + observed control response
                         + protected effect + repeatability
                         + competing explanations + limitations
                         = defensible finding
```

| Section | Question it must answer |
|---|---|
| Summary | What failed, under what boundary, and why it matters? |
| Evidence | What exact observations let another tester reproduce it? |
| Impact | What protected action or service effect was achieved? |
| Limitations | What did the experiment not establish? |
| Recommendation | What invariant should hold, not merely what product to buy? |
| Retest | Which former attack must fail and which legitimate path must pass? |

## Required external instruction

### Required reporting assignment

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)

**Exact assignment:** read §§8.1 Developing the Final Report, 8.2 Mitigation Recommendations, and 8.3 Post-Testing Activities; use §8.1's audience and evidence considerations as a checklist

**Estimated time:** 55 minutes

**Focus on:** audience, reproducibility, evidence handling, root cause versus symptom, practical recommendation, residual risk, and cleanup

**Skip:** tool chapters and assessment techniques already covered in earlier modules

**Expected takeaway:** organize evidence so a technical reviewer can reproduce the claim and a decision-maker can understand its bounded consequence.

## Course bridge

The course finding model adds an explicit protected-effect test and a same-attack
retest. These are Course synthesis choices derived from the offensive-control
loop; NIST does not define this exact page template.

!!! note "Course synthesis"
    A changed score, fingerprint, challenge rate, or status code is supporting
    evidence. The main impact claim names the action or service effect the adversary achieved.

## Worked example

Weak claim: “The bot detector was bypassed.” Stronger local claim: “A challenge
token issued to `solver-session` was accepted with `attacker-copy`, and the
protected report returned `200`; the token was not bound to session or one-time
use in this synthetic target.” The stronger sentence names precondition, change,
effect, root cause hypothesis, and boundary.

## Guided exercise

### Objective

Rewrite one course artifact as a one-page finding with a traceable evidence chain.

### Setup

Choose challenge replay, inventory authorization, rate-key rotation, browser
control evasion, or bounded retry amplification. Open raw output and the bundled
synthetic finding. Do not copy its wording for a different case.

### Actions

1. State target, authorization, lab version, reset condition, and precondition.
2. Record the blocked or unaffected baseline.
3. Record one controlled change and the exact request/action.
4. Name the protected effect and evidence that it occurred.
5. Add repeat count, negative control, residual anomalies, alternate explanations,
   and what the lab cannot generalize.
6. Write root-cause language as evidence or hypothesis, not certainty beyond code/tests.
7. Define a remediation invariant and exact retest criteria.

### Expected output

A reviewer can reproduce the local effect from the finding alone, distinguish
fact from inference, and see an honest boundary around the claim.

### Interpretation

Severity is not a substitute for evidence. In a synthetic target, the useful
artifact is the method and proof structure; it is not a claim that an external service is vulnerable.

### Common failure modes

- Hiding the precondition or reset state
- Calling a status/score change the impact
- Omitting the legitimate near-neighbor case
- Using universal language from one synthetic population
- Recommending a product without a remediation invariant

### Cleanup

Remove secrets if any were accidentally captured, retain synthetic evidence, and stop local services.

## Why this matters offensively

The operator's work changes defensive priorities only when the attack is
reproducible, the effect matters, and the recommendation can be verified.

## Required artifact

`artifacts/module-10/finding.md` with summary, scope, preconditions, steps,
evidence, protected effect, limitations, recommendation invariant, and retest.

## Pass gate

1. What separates supporting evidence from impact?
2. Why include a blocked baseline?
3. How should an unproven root cause be phrased?
4. What makes a finding reproducible?
5. Why include a legitimate near-neighbor?
6. What is the purpose of limitations?

## Answer key

<details><summary>Check your reasoning</summary>

1. Impact is the protected action/service consequence; supporting evidence explains the path.
2. It shows the control existed and isolates the effect of the changed variable.
3. As a hypothesis with supporting and missing evidence.
4. Exact boundary, state, inputs, actions, expected/actual output, and versions.
5. To ensure remediation does not block intended behavior and to expose collateral effects.
6. To prevent unsupported generalization and identify evidence still needed.

</details>

## Next lesson

Continue to [Remediation and exact retest](02-remediation-and-retest.md).
