# Finding and evidence

<!-- source-ids: nist-sp-800-115, aate-adversarial-control-loop, aate-local-lab -->

## Progress

- Module: 10 - Findings, briefing, and interview practice
- Lesson: 1 of 5
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [Python telemetry as evidence](../09-tooling-code-review/01-python-telemetry.md)
  - Be able to locate raw synthetic observations and state their limitation
- Next lesson: Remediation and exact retest

## Role outcome

Write a reproducible synthetic finding that connects a scoped precondition and
attack action to a protected effect without overstating identity, prevalence, or production impact.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §§8.1-8.3 reporting, mitigation, resolution | Grounds assessment communication | General testing guide; it does not define bot-control or DDoS red-team procedure. |
| COURSE_SYNTHESIS | [Adversarial-control loop](../../methodology/adversarial-control-loop.md) | Steps 11-15 | Structures protected-action evidence, impact, limitations, remediation, and retest | Course synthesis; no cited standard defines the exact fifteen-step sequence. |
| LAB_SPECIFIC | [Finding and briefing lab](../../labs/deep/finding-briefing.md) | challenge replay example and structure | Supplies a complete local model | Deliberately small and vulnerable; results do not generalize to production systems. |

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

**Exact section, chapter, or unit:** read §§8.1 Developing the Final Report, 8.2 Mitigation Recommendations, and 8.3 Post-Testing Activities; use §8.1's audience and evidence considerations as a checklist

**Estimated time:** 55 minutes

**What to focus on:** audience, reproducibility, evidence handling, root cause versus symptom, practical recommendation, residual risk, and cleanup

**What to skip:** tool chapters and assessment techniques already covered in earlier modules

**Expected takeaway:** organize evidence so a technical reviewer can reproduce the claim and a decision-maker can understand its bounded consequence.

## Course bridge

The course finding model adds an explicit protected-effect test and a same-attack
retest. These are Course synthesis choices derived from the offensive-control
loop; NIST does not define this exact page template.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** A changed score, fingerprint, challenge rate, or
    status code is supporting evidence. The main impact claim names the action
    or service effect the adversary achieved.

## Worked example

Weak claim: “The bot detector was bypassed.” Stronger local claim: “A challenge
token issued to `solver-session` was accepted with `attacker-copy`, and the
protected report returned `200`; the token was not bound to session or one-time
use in this synthetic target.” The stronger sentence names precondition, change,
effect, root cause hypothesis, and boundary.

## Guided exercise

### Objective

Rewrite one course exercise result as a one-page finding with a traceable evidence chain.

### Setup

Choose challenge replay, inventory authorization, rate-key rotation, browser
control evasion, or bounded retry amplification. Open raw output and the bundled
synthetic finding. Do not copy its wording for a different case.

### Exact actions or commands

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
exercise result is the method and proof structure; it is not a claim that an external service is vulnerable.

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

## Check your understanding

1. A finding includes the replay request, `200` response, and Session B reservation record. Which item states impact, and which items support the attack path?
2. Why should the finding preserve Session B's `403` blocked baseline before showing the replayed token's accepted result?
3. The evidence suggests missing session binding, but the reviewer has not inspected server code. How should the finding phrase that root cause?
4. Which scope, state, inputs, actions, expected and actual results, and versions make the synthetic finding reproducible?
5. Why should the finding include a legitimate Session A reservation when evaluating remediation for the Session B replay?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The Session B reservation record states the protected business impact.** The request and response support how the replay reached that effect, but they are not a substitute for the committed server-side result.

- **2. The blocked baseline shows that the control existed and that Session B could not normally perform the action.** Comparing that baseline with the replay isolates the changed token condition.

- **3. Describe missing session binding as a hypothesis supported by the replay evidence and name the missing code or telemetry needed to confirm causality.** Do not present an uninspected implementation detail as fact.

- **4. Record the exact authorization boundary, initial state, token and session inputs, ordered procedure, expected and actual outputs, server evidence, software versions, cleanup, and limitations.** Another reviewer should be able to repeat the case.

- **5. The legitimate case protects intended behavior and exposes excessive blocking.** A remediation that rejects both Session B and the properly authorized Session A action would not satisfy the security objective.

</details>

## Next lesson

Continue to [Remediation and exact retest](02-remediation-and-retest.md).
