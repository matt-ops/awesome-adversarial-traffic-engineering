# Public-safe role narrative

<!-- source-ids: amazon-security-engineer-interview-prep, amazon-leadership-principles, nist-sp-800-115 -->

> **Progress**
>
> Module: 10 - Findings, briefing, and interview practice
>
> Lesson: 4 of 5
>
> Depth: Foundation
>
> Estimated time: 2 hours
>
> Prerequisites: Technical briefing
>
> Artifact: `artifacts/module-10/role-narrative.md`
>
> Next: Full mock loop

## Role outcome

Explain adversarial traffic engineering in 90 seconds and support it with one
public-safe example of scope, attack, evidence, collaboration, and measurable improvement.

## Prerequisites

- [Technical briefing](03-technical-briefing.md)
- One course artifact you can discuss without confidential information

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Public security-engineer interview guide](https://amazon.jobs/content/en/how-we-hire/security-engineer-interview-prep) | behavioral preparation and technical topics | Grounds structured, technically specific answers |
| OFFICIAL_DOCUMENTATION | [Public engineering-principles rubric](https://www.amazon.jobs/content/en/our-workplace/leadership-principles) | ownership, depth, trust, constructive disagreement, results | Supplies observable behavior prompts |
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | assessment lifecycle and reporting | Grounds scope-to-improvement arc |

## Mental model

| Seconds | Purpose | Example content |
|---:|---|---|
| 0-20 | Role | authorized adversary emulates automated abuse and traffic pressure |
| 20-40 | Method | map path/control, establish baseline, change one variable, prove effect |
| 40-65 | Example | local challenge replay or workflow authorization proof |
| 65-80 | Partnership | evidence, remediation invariant, exact retest |
| 80-90 | Boundary | portfolio demonstrates method, not production tenure or universal bypass |

The narrative is not a list of technologies. It connects adversary objective,
engineering method, protected effect, and defensive improvement. A behavioral
example adds situation, responsibility, actions you personally took, result, and reflection.

## Required external instruction

### Required narrative assignment

**Direct link:** [Public security-engineer interview guide](https://amazon.jobs/content/en/how-we-hire/security-engineer-interview-prep) and [public engineering-principles rubric](https://www.amazon.jobs/content/en/our-workplace/leadership-principles)

**Exact assignment:** read Behavioral preparation; then read Ownership, Dive Deep, Earn Trust, Have Backbone/Disagree and Commit, and Deliver Results; write one observable action from a public-safe course exercise for each

**Estimated time:** 40 minutes

**Focus on:** first-person ownership, technical detail, disagreement supported by evidence, collaboration, measurable result, and reflection

**Skip:** memorizing slogans, inventing work history, confidential examples, and unrelated principles

**Expected takeaway:** connect a real course action to a behavior and technical outcome without exaggerating experience.

## Course bridge

Use only lab facts you can reproduce. It is accurate to say “I designed and ran
a bounded synthetic experiment.” It is not accurate to convert that into
production ownership, external vulnerability discovery, or years of domain experience.

!!! warning "Safety boundary"
    Keep names, internal systems, customer data, employer context, and non-public
    incidents out of the repository and public recording.

## Worked example

“Adversarial traffic engineering tests how automated attackers reach protected
web actions or exhaust application resources. In a local exercise, I first
captured a blocked report baseline, then traced a challenge token through the
code and tested whether it was bound to session. Replaying it from a second
session executed the protected report. I documented the limitation, proposed
subject/action/expiry/nonce binding, and wrote negative and legitimate retest
cases. The value is not just finding a weak check; it is turning the attack into
a measurable regression test.”

## Guided exercise

### Objective

Produce a truthful 90-second role explanation and one three-minute evidence story.

### Setup

Choose one public-safe artifact. Write facts in one column and interpretations in another.

### Actions

1. Draft the five-part 90-second structure from the table.
2. Remove tool lists unless a tool explains a decision.
3. Draft one longer story: context, your responsibility, three concrete actions,
   measurable result, collaboration/recommendation, limitation, and reflection.
4. Map each claimed behavior to a sentence that proves it.
5. Record privately, then check first-person ownership and truthful scope.
6. Replace vague claims such as “improved security” with the exact artifact/result.

### Expected output

A role explanation a non-specialist can follow and a technical example a specialist
can probe, with no confidential or invented experience.

### Interpretation

Course work is legitimate evidence of learning and method. Its limitation is
scale and environment; stating that boundary increases credibility.

### Common failure modes

- Describing only defensive detection work
- Describing only bypass without remediation/retest
- Saying “we” when the question is about your action
- Inventing production impact from a local fixture
- Memorizing wording so tightly that follow-up breaks the narrative

### Cleanup

Delete rough notes containing private context; retain only public-safe course facts.

## Why this matters offensively

The role requires attack thinking and communication. A strong narrative shows
you can emulate an adversary, reason from evidence, and help a control owner close the tested path.

## Required artifact

`artifacts/module-10/role-narrative.md` with 90-second script, three-minute story,
fact/inference table, behavior evidence, truthful limitations, and likely follow-ups.

## Pass gate

1. What makes the role offensive rather than detection-only?
2. Why include remediation and retest?
3. What course experience can you claim accurately?
4. How do you prove personal ownership?
5. What must remain outside a public artifact?
6. Why state the lab limitation voluntarily?

## Answer key

<details><summary>Check your reasoning</summary>

1. The operator emulates an adversary and proves a protected action/service effect.
2. They turn the attack into a measurable defensive improvement and regression check.
3. Exercises actually designed, executed, interpreted, and documented in the synthetic lab.
4. Name your decisions, actions, evidence, tradeoffs, and result in first person.
5. Confidential systems, data, incidents, names, and non-public employer context.
6. It prevents false transfer claims and shows evidence discipline.

</details>

## Next lesson

Continue to [Full mock loop](05-mock-loop.md).
