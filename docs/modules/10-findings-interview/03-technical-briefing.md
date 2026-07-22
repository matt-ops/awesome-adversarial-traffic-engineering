# Technical briefing

<!-- source-ids: nist-sp-800-115, google-technical-writing-one, aate-local-lab -->

## Progress

- Module: 10 - Findings, briefing, and interview practice
- Lesson: 3 of 5
- Depth: Integrated
- Estimated time: 3 hours
- Prerequisites:
  - [Remediation and exact retest](02-remediation-and-retest.md)
  - A completed finding and retest matrix
- Next lesson: Role narrative

## Role outcome

Deliver a five-minute evidence-led briefing, answer skeptical questions, and
separate demonstrated impact from assumptions and next research.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §8.1 audience and final report | Grounds audience-aware communication | General testing guide; it does not define bot-control or DDoS red-team procedure. |
| OFFICIAL_DOCUMENTATION | [Google Technical Writing One](https://developers.google.com/tech-writing/one) | Audience; active voice; clear and short sentences; paragraphs; lists and tables | Supports audience-aware, concise technical explanation | General technical-writing instruction; it does not define security finding evidence, severity, or retest requirements. |
| LAB_SPECIFIC | [Finding and briefing lab](../../labs/deep/finding-briefing.md) | timing and evidence checklist | Supplies the rehearsal format | Deliberately small and vulnerable; results do not generalize to production systems. |

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

### Google audience and clarity assignment

**Direct link:** [Google Technical Writing One](https://developers.google.com/tech-writing/one)

**Exact section, chapter, or unit:** Audience; Active voice versus passive voice; Clear sentences; Short sentences; Paragraphs; Lists and tables

**Estimated time:** 45 minutes

**What to focus on:** identifying the decision-maker, naming the actor and action, keeping one idea per sentence, and using a table only when comparison is clearer than prose

**What to skip:** grammar units unrelated to the technical briefing and the optional classroom exercises

**Expected takeaway:** rewrite one finding as a 90-second briefing whose evidence, limitation, and decision remain clear to both an engineer and a non-specialist.

### NIST audience assignment

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)

**Exact section, chapter, or unit:** §8.1 Developing Mitigation Recommendations and §8.2 Reporting Recommendations

**Estimated time:** 20 minutes

**What to focus on:** tying evidence to mitigation, separating technical detail from management-level conclusions, and retaining scope and limitations

**What to skip:** assessment techniques outside the reporting and mitigation sections

**Expected takeaway:** explain which details belong in the spoken decision path and which belong in backup evidence.

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

### Exact actions or commands

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

## Check your understanding

1. A five-minute briefing has a full written finding available. Why should the presenter select an evidence-led decision path instead of reading the report aloud?
2. Time runs short during the briefing. Which boundary, protected effect, and material limitation must remain in the spoken explanation?
3. A stakeholder asks whether the synthetic replay affects production, but the evidence covers only the local lab. How should the presenter answer?
4. Why should the briefing lead with the protected inventory or report effect before describing Playwright, tokens, or implementation details?
5. What owner action and measurable retest criterion make the final decision request useful?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A briefing guides a decision with the most relevant claim, evidence, impact, limitation, and request.** The written report remains the place for complete reproduction details and supporting material.

- **2. Keep the authorized boundary, demonstrated protected effect, and most important limitation.** Removing any of those can make a result sound unauthorized, irrelevant, or broader than the evidence supports.

- **3. Explain that the evidence supports only the synthetic local result, identify the production evidence that is missing, and propose the next authorized discriminating test.** Do not guess or imply transfer.

- **4. The protected effect establishes why the audience should care and what the control failed to prevent.** Tool details are supporting mechanism and can follow after relevance is clear.

- **5. Name the person or team responsible for the remediation and require the former attack to fail without changing the protected server record while legitimate behavior still passes.** The request should be assignable and objectively verifiable.

</details>

## Next lesson

Continue to [Role narrative](04-role-narrative.md).
