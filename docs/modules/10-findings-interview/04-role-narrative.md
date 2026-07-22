# Public-safe role narrative

<!-- source-ids: google-technical-writing-one, nist-sp-800-115 -->

## Progress

- Module: 10 - Findings, briefing, and interview practice
- Lesson: 4 of 5
- Depth: Foundation
- Estimated time: 2 hours
- Prerequisites:
  - [Finding and evidence](01-finding-and-evidence.md)
  - One course exercise you can discuss without confidential information
- Next lesson: Full mock loop

## Role outcome

Explain adversarial traffic engineering in 90 seconds and support it with one
public-safe example of scope, attack, evidence, collaboration, and measurable improvement.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Google Technical Writing One](https://developers.google.com/tech-writing/one) | Audience; active voice; clear and short sentences; paragraphs | Grounds a concise, first-person technical narrative | General technical-writing instruction; it does not define security finding evidence, severity, or retest requirements. |
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | assessment lifecycle and reporting | Grounds scope-to-improvement arc | General testing guide; it does not define bot-control or DDoS red-team procedure. |

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

### Google narrative assignment

**Direct link:** [Google Technical Writing One](https://developers.google.com/tech-writing/one)

**Exact section, chapter, or unit:** Audience; Active voice versus passive voice; Clear sentences; Short sentences; Paragraphs

**Estimated time:** 35 minutes

**What to focus on:** first-person actor/action sentences, concrete evidence, one causal claim at a time, and explicit limitations

**What to skip:** optional classroom exercises and examples unrelated to technical narratives

**Expected takeaway:** connect a reproducible course action to a technical decision and result without converting lab work into experience you do not have.

### NIST lifecycle assignment

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)

**Exact section, chapter, or unit:** §5.2.1 Penetration Testing Phases and §§8.1-8.3

**Estimated time:** 25 minutes

**What to focus on:** how planning, discovery, attack validation, reporting, mitigation, and follow-up form one evidence-backed story

**What to skip:** technique catalogs that are not part of the role narrative

**Expected takeaway:** narrate one exercise as scope, obstacle, decision, evidence, limitation, remediation, and retest rather than as a tool demonstration.

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

Choose one public-safe course exercise. Write facts in one column and interpretations in another.

### Exact actions or commands

1. Draft the five-part 90-second structure from the table.
2. Remove tool lists unless a tool explains a decision.
3. Draft one longer story: context, your responsibility, three concrete actions,
   measurable result, collaboration/recommendation, limitation, and reflection.
4. Map each claimed behavior to a sentence that proves it.
5. Record privately, then check first-person ownership and truthful scope.
6. Replace vague claims such as “improved security” with the exact observed result.

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

## Check your understanding

1. A role narrative describes mapping a control and measuring precision but never attempts the protected action. Which missing activity keeps the story from demonstrating offensive work?
2. Why should the narrative include remediation criteria and an exact retest after describing the authorized attack?
3. Which course experience may the learner claim accurately when every exercise occurred in the synthetic local lab?
4. How can the learner use first-person decisions, actions, evidence choices, and tradeoffs to show personal ownership without exposing confidential details?
5. Why should the learner voluntarily state that the synthetic result does not prove production experience or universal bypass ability?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The story must include authorized adversary emulation that attempts and proves an attacker-relevant protected action or service effect.** Detection analysis alone does not demonstrate offensive completion.

- **2. Remediation and retest turn attack evidence into a measurable defensive improvement and regression check.** They show that the learner can help close the weakness, not merely demonstrate it once.

- **3. The learner may claim exercises personally designed, executed, interpreted, and documented in the synthetic environment.** Production scale, employer incidents, and universal control knowledge remain outside the supported claim.

- **4. Describe the choices made, commands or analyses performed, evidence preserved, alternatives considered, and outcome in first person.** Keep system names, customer data, incidents, credentials, and non-public employer context out of the narrative.

- **5. The limitation prevents false transfer claims and demonstrates evidence discipline.** A candid boundary makes the supported skills more credible and shows where additional supervised production experience would be needed.

</details>

## Next lesson

Continue to [Full mock loop](05-mock-loop.md).
