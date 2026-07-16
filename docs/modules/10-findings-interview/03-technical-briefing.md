# Technical briefing

<!-- source-ids: nist-sp-800-115, amazon-security-engineer-interview-prep, aate-local-lab -->

> **Progress**
>
> Module: 10 - Findings, briefing, and interview practice
>
> Lesson: 3 of 5
>
> Depth: Integrated
>
> Estimated time: 3 hours
>
> Prerequisites: Remediation and exact retest
>
> Artifact: `artifacts/module-10/briefing.md`
>
> Next: Role narrative

## Role outcome

Deliver a five-minute evidence-led briefing, answer skeptical questions, and
separate demonstrated impact from assumptions and next research.

## Prerequisites

- [Remediation and exact retest](02-remediation-and-retest.md)
- A completed finding and retest matrix

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §8.1 audience and final report | Grounds audience-aware communication |
| OFFICIAL_DOCUMENTATION | [Public security-engineer interview guide](https://amazon.jobs/content/en/how-we-hire/security-engineer-interview-prep) | interview format and technical topics | Supplies one public question environment |
| LAB_SPECIFIC | [Finding and briefing lab](../../labs/deep/finding-briefing.md) | timing and evidence checklist | Supplies the rehearsal format |

## Mental model

```text
0:00 context and authorization
0:30 adversary objective and blocked baseline
1:15 controlled change and protected effect
2:30 evidence, repeatability, residual anomalies
3:30 remediation invariant and exact retest
4:20 limitations, decision requested, questions
```

The briefing is not the report read aloud. It is a decision path: what was
tested, what happened, why the effect matters, what evidence supports it, what
remains uncertain, and what action/retest follows. Keep raw detail ready for questions.

## Required external instruction

### Required communication assignment

**Direct link:** [Public security-engineer interview guide](https://amazon.jobs/content/en/how-we-hire/security-engineer-interview-prep)

**Exact assignment:** read Interview format, Technical topics, and Behavioral preparation; list where a reviewer may ask for fundamentals, system reasoning, code, evidence, or a concrete past example

**Estimated time:** 35 minutes

**Focus on:** explaining fundamentals, reasoning aloud, clarifying ambiguous scope, structured examples, and technical depth under follow-up

**Skip:** application logistics, location information, and any employer-specific preparation not relevant to communication

**Expected takeaway:** prepare an evidence narrative that remains coherent when the reviewer changes altitude or challenges an assumption.

## Course bridge

Use the same finding fields, but compress them by decision value. Never remove
the boundary, protected effect, or limitation to save time. Put hashes, raw
requests, timing distributions, and code references in backup notes.

!!! note "Common misconception"
    Confidence is not speaking without uncertainty. It is clearly distinguishing
    what the experiment proved, what it suggests, and what must be tested next.

## Worked example

“Against the reset local fixture, the report was blocked without a token. A
token issued to one session was accepted for another, and the protected report
executed. Code review shows the token store has no session/action/use binding.
The result repeated three times; it does not imply an external control has this
flaw. Bind the authorization to subject, action, expiry, and nonce; the exact
cross-session replay must fail while intended one-time use succeeds.”

This is brief because each sentence does one job: baseline, action/effect, root
cause evidence, repeatability/limit, and acceptance criterion.

## Guided exercise

### Objective

Record and critique a five-minute briefing with two minutes of adversarial questions.

### Setup

Use the timing card in the lab page. Put raw evidence and code references in a
separate backup sheet. Use only synthetic/public-safe material.

### Actions

1. Write one sentence for boundary, objective, baseline, action/effect, evidence,
   limitation, remediation invariant, retest, and decision requested.
2. Reorder those sentences into the five-minute structure.
3. Record one take without slides.
4. Answer: “How do you know?”, “What else explains this?”, “What breaks if we fix
   it?”, and “What exactly will the retest prove?”
5. Compare every claim with the finding. Remove or qualify unsupported statements.
6. Record a second take and note one improved transition and one remaining gap.

### Expected output

A briefing between four and six minutes that names the protected effect before
deep implementation detail, plus concise answers tied to evidence or explicit uncertainty.

### Interpretation

If a question exposes missing evidence, the correct answer is the bounded claim
and next test—not improvising certainty.

### Common failure modes

- Spending the opening on tooling
- Saying “bypass” without naming the effect
- Hiding synthetic scope until asked
- Listing recommendations before explaining root cause
- Treating every question as a challenge to credibility

### Cleanup

Keep private recordings outside the repository; commit only a public-safe outline.

## Why this matters offensively

Red-team findings are contested. Clear evidence and honest uncertainty let an
operator defend the attack path and collaborate on a measurable control improvement.

## Required artifact

`artifacts/module-10/briefing.md` with timed outline, claim/evidence map, four
skeptical questions, bounded answers, and private-recording self-critique.

## Pass gate

1. Why not read the report aloud?
2. Which three items must never be cut for time?
3. How should you answer a question the evidence cannot resolve?
4. Why lead with protected effect rather than tool detail?
5. What belongs in backup notes?
6. What makes a decision request useful?

## Answer key

<details><summary>Check your reasoning</summary>

1. A briefing selects a decision path; the report preserves full reproducibility.
2. Boundary, protected effect, and material limitation.
3. State the bounded claim, missing evidence, and next discriminating test.
4. It establishes relevance before implementation depth.
5. Raw requests, hashes, code references, distributions, and alternate-explanation tests.
6. A named owner/action and objective acceptance/retest criterion.

</details>

## Next lesson

Continue to [Role narrative](04-role-narrative.md).
