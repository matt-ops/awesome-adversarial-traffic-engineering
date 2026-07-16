# Full mock loop

<!-- source-ids: amazon-security-engineer-interview-prep, amazon-leadership-principles, nist-sp-800-115, aate-adversarial-control-loop -->

> **Progress**
>
> Module: 10 - Findings, briefing, and interview practice
>
> Lesson: 5 of 5
>
> Depth: Deep
>
> Estimated time: 5 hours
>
> Prerequisites: Public-safe role narrative
>
> Artifact: `artifacts/module-10/mock-loop.md`
>
> Next: Checkpoint and portfolio review

## Role outcome

Complete a timed, evidence-based mock that tests foundations, attack planning,
code, system reasoning, reporting, and rebuttal without hiding gaps.

## Prerequisites

- All Modules 00-10
- Finding, retest, briefing, role narrative, and runnable lab artifacts

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Public security-engineer interview guide](https://amazon.jobs/content/en/how-we-hire/security-engineer-interview-prep) | interview format, technical topics, behavioral preparation | Grounds session categories |
| OFFICIAL_DOCUMENTATION | [Public engineering-principles rubric](https://www.amazon.jobs/content/en/our-workplace/leadership-principles) | selected observable behaviors | Grounds reflection prompts |
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | planning, execution, reporting, mitigation | Grounds full assessment arc |
| Course synthesis (`COURSE_SYNTHESIS`) | [Adversarial-control loop](../../methodology/adversarial-control-loop.md) | experiment sequence and exact retest | Keeps mock tied to course method |

## Mental model

```text
10 min fundamentals -> 15 min attack/design -> 10 min code/evidence
-> 10 min finding/briefing -> 10 min behavior/reflection -> 5 min rebuttal

score each answer: correct foundation + explicit assumptions + attack path
                 + observable effect + safety boundary + limitation + next test
```

The mock is diagnostic. A blank or incorrect answer becomes a lesson link and a
new artifact task. Fluent but unsupported answers score lower than slower,
bounded reasoning with the right experiment.

## Required external instruction

### Required format assignment

**Direct link:** [Public security-engineer interview guide](https://amazon.jobs/content/en/how-we-hire/security-engineer-interview-prep)

**Exact assignment:** reread Interview format and Technical topics; turn each listed topic relevant to this course into one fundamentals question and one applied follow-up

**Estimated time:** 30 minutes

**Focus on:** coding, security fundamentals, system design, ambiguity clarification, structured communication, and concrete examples

**Skip:** employer logistics and topics outside the course capability map

**Expected takeaway:** assemble a balanced mock that exposes weak prerequisites instead of rehearsing only favorite attacks.

## Course bridge

Use the course matrix to sample across HTTP/browser foundations, workflow abuse,
control recon/evasion, protocol identity, resilience, Python/code review, and findings.
Every attack question begins with authorization and immediate recon relevant to
the control; there is no generic recon question repeated for every module.

## Worked example

Prompt: “A headed workflow succeeds but your headless workflow is challenged.
How do you proceed?” A strong answer clarifies scope, captures comparable
requests and top/iframe/worker signals, establishes blocked baselines, lists
ranked hypotheses, changes one variable, verifies the protected action, inspects
residual anomalies, and defines remediation/retest. It does not start by naming a stealth package.

## Guided exercise

### Objective

Run, score, and repair one full mock loop.

### Setup

Use the scorecard in [the lab page](../../labs/deep/finding-briefing.md). Ask a
partner to choose prompts or shuffle them yourself. Keep recordings private.

### Actions

1. Select two fundamentals prompts, one workflow/control attack, one protocol or
   resilience design, one Python/code review, one finding briefing, and one behavior prompt.
2. Run the 60-minute sequence without notes for the first answer to each prompt.
3. For every answer, record assumptions, evidence, effect, limitation, and missing prerequisite.
4. Challenge two claims with an alternate explanation or collateral-effect question.
5. Map each gap to an exact lesson, source assignment, lab action, and artifact repair.
6. Repeat only failed sections after completing repairs; do not memorize the answer key.

### Expected output

A scored transcript outline with evidence references, at least three concrete
repairs, and a second-attempt comparison for failed sections.

### Interpretation

The mock does not certify expertise. It tests whether the learner can retrieve
foundations, reason offensively, bound experiments, and defend evidence under follow-up.

### Common failure modes

- Practicing only browser bypass questions
- Jumping to tools before tracing request/control/effect
- Treating a fingerprint as identity proof
- Designing availability tests without hard ceilings and recovery
- Hiding missing knowledge instead of assigning a repair

### Cleanup

Delete private recordings/transcripts; keep a public-safe gap and repair log.

## Why this matters offensively

Real engagements and technical interviews are open-ended. The operator must join
foundations, attack lifecycle, tooling, evidence, and communication while constraints change.

## Required artifact

`artifacts/module-10/mock-loop.md` with prompt set, scorecard, evidence links,
gaps, exact repairs, repeated-section results, and current limitations.

## Pass gate

1. What is the mock designed to diagnose?
2. What must every attack answer eventually prove?
3. Why include alternate explanations?
4. How should a failed answer be repaired?
5. Why is fluent unsupported certainty a poor result?
6. What does passing the mock not prove?

## Answer key

<details><summary>Check your reasoning</summary>

1. Missing foundations, weak attack/evidence reasoning, and communication gaps.
2. An attacker-relevant protected action or service effect within scope.
3. They test causal reasoning and prevent premature conclusions.
4. Exact lesson/source, lab action, artifact, then a fresh applied follow-up.
5. It cannot withstand evidence questions and conceals risk.
6. Production experience, universal bypass ability, or complete domain expertise.

</details>

## Next lesson

Use the cumulative checkpoint pages as honest portfolio views, then complete the
final coverage and quality checklists before presenting the course as finished.
