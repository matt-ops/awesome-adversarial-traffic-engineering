# Full mock loop

<!-- source-ids: owasp-wstg-reporting-structure, nist-sp-800-115, aate-adversarial-control-loop -->

## Progress

- Module: 10 - Findings, briefing, and interview practice
- Lesson: 5 of 5
- Depth: Deep
- Estimated time: 5 hours
- Prerequisites:
  - All Modules 00-10
  - Be able to explain a finding, retest, briefing, role narrative, and runnable lab behavior
- Next lesson: Checkpoint and portfolio review

## Role outcome

Complete a timed, evidence-based mock that tests foundations, attack planning,
code, system reasoning, reporting, and rebuttal without hiding gaps.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [OWASP WSTG Reporting Structure](https://owasp.org/www-project-web-security-testing-guide/latest/5-Reporting/01-Reporting_Structure) | Scope; limitations; executive summary; findings; reproducible artifacts | Grounds evidence and communication review categories | The latest WSTG reporting page is development guidance and may change; it is a suggested consultancy-oriented structure, not a mandatory universal format. |
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | planning, execution, reporting, mitigation | Grounds full assessment arc | General testing guide; it does not define bot-control or DDoS red-team procedure. |
| COURSE_SYNTHESIS | [Adversarial-control loop](../../methodology/adversarial-control-loop.md) | experiment sequence and exact retest | Keeps the review tied to the course method | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
10 min fundamentals -> 15 min attack/design -> 10 min code/evidence
-> 10 min finding/briefing -> 10 min behavior/reflection -> 5 min rebuttal

score each answer: correct foundation + explicit assumptions + attack path
                 + observable effect + safety boundary + limitation + next test
```

The mock is diagnostic. A blank or incorrect answer becomes a lesson link and a
new exercise task. Fluent but unsupported answers score lower than slower,
bounded reasoning with the right experiment.

## Required external instruction

### OWASP reporting assignment

**Direct link:** [OWASP WSTG Reporting Structure](https://owasp.org/www-project-web-security-testing-guide/latest/5-Reporting/01-Reporting_Structure)

**Exact section, chapter, or unit:** About This Section; 1.4 Scope; 1.5 Limitations; 2 Executive Summary; 3 Findings; 3.2 Findings Details; Reproducible Test Artifacts

**Estimated time:** 35 minutes

**What to focus on:** whether another person can reproduce the attack, distinguish evidence from inference, understand impact, act on remediation, and run the retest

**What to skip:** consultancy boilerplate and report sections that do not improve the local mock response

**Expected takeaway:** construct review questions from missing or weak report evidence instead of rehearsing generic prompts.

### NIST assessment-lifecycle assignment

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)

**Exact section, chapter, or unit:** §5.2.1 and §§8.1-8.3

**Estimated time:** 25 minutes

**What to focus on:** planning, discovery, attack validation, analysis, reporting, mitigation, and follow-up as one review loop

**What to skip:** technique details not represented in the portfolio example under review

**Expected takeaway:** sample both foundational mechanism questions and applied evidence questions across the complete assessment lifecycle.

## Course bridge

Use the course matrix to sample across HTTP/browser foundations, workflow abuse,
control recon/evasion, protocol identity, resilience, Python/code review, and findings.
Every attack question begins with authorization and immediate recon relevant to
the control; there is no generic recon question repeated for every module.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** The mock loop uses the same fifteen AATE steps as the
    labs so weak baselines, protected-action proof, residual anomalies,
    alternative explanations, remediation criteria, and exact retest are visible.

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

### Exact actions or commands

1. Select two fundamentals prompts, one workflow/control attack, one protocol or
   resilience design, one Python/code review, one finding briefing, and one behavior prompt.
2. Run the 60-minute sequence without notes for the first answer to each prompt.
3. For every answer, record assumptions, evidence, effect, limitation, and missing prerequisite.
4. Challenge two claims with an alternate explanation or collateral-effect question.
5. Map each gap to an exact lesson, source assignment, lab action, and practice repair.
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

## Check your understanding

1. The timed mock includes foundation questions, attack planning, code, system reasoning, reporting, and rebuttal. Which learning gaps is the scorecard intended to diagnose?
2. A mock answer describes changing a browser signal and receiving allow. Which attacker-relevant result must the answer eventually prove?
3. Why should the candidate offer alternate explanations for a successful replay or resilience result during rebuttal?
4. A candidate misses an HTTP foundation question. What exact lesson review, exercise action, and fresh follow-up should repair the gap?
5. Why is a fluent answer with unsupported certainty a weaker result than a bounded answer that names missing evidence?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The scorecard identifies missing foundations, weak attack and evidence reasoning, coding or system gaps, and communication problems.** The purpose is targeted repair, not a credential or permanent pass label.

- **2. The answer must prove the protected server-side action or service-health effect within the authorized boundary.** An allow decision or changed signal remains intermediate control evidence.

- **3. Alternate explanations test causal reasoning and prevent the candidate from treating correlation as proof.** A strong answer names which additional observation would distinguish the competing causes.

- **4. Return to the exact relevant lesson and source section, repeat the guided exercise behavior, explain the expected output, and answer a new applied scenario without relying on memorized wording.**

- **5. Unsupported certainty hides risk and fails when evidence is challenged.** A bounded answer separates demonstrated facts from inference, states limitations, and proposes the next test needed to reduce uncertainty.

</details>

## Next lesson

Use the cumulative checkpoint pages as honest portfolio views, then complete the
final coverage and quality checklists before presenting the course as finished.
