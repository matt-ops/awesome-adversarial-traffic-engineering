# Identity coherence

<!-- source-ids: gummy-browsers, fp-inconsistent, fpscanner-project, aate-adversarial-control-loop -->

## Progress

- Module: 06 - Browser-control evasion
- Lesson: 3 of 5
- Depth: Integrated
- Estimated time: 4 hours
- Prerequisites:
  - [One-variable experiment](02-one-variable-experiments.md)
  - Be able to explain the context matrix and five signal families
- Next lesson: Replay and temporal consistency

## Role outcome

Design and evaluate a declared browser-environment profile across related
attributes and contexts while preserving residual contradictions.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PREPRINT_RESEARCH | [Gummy Browsers](https://arxiv.org/abs/2110.10129) | §§3-6; §8 limitations; §9 | Provides spoofing approaches and evaluated results | Research threat model and older browser/tool versions; network-layer identity was not spoofed in the study. |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | §§5-8.4 | Supports cross-attribute/temporal residual analysis | Preprint studying a specific dataset, honey-site design, bot population, and selected services; not universal proof. |
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Cross-Context Validation; non-goals | Provides an inspectable target concept | Observations are valid only for the recorded code and browser versions. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Coherent-set experiment and residuals | Defines bounded claims | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
Declared environment claim
  -> browser/version + OS/platform
  -> locale + language + timezone
  -> viewport + screen + device scale
  -> graphics/runtime summaries
  -> page + frame + worker
  -> protocol/session/behavior expectations
  -> residual anomalies and unsupported layers
```

## Required external instruction

### Gummy Browsers assignment

**Direct link:** [Gummy Browsers](https://arxiv.org/abs/2110.10129)  
**Exact section, chapter, or unit:** §3 Attack Model and Spoofing Methods; §4 Attack Implementation; §5 Dataset and Evaluation Methodology; §6 Results; §8 limitations; §9  
**Estimated time:** 60 minutes  
**What to focus on:** which browser attributes were acquired or spoofed, the evaluated versions/populations, comparison method, and unmodified network identity  
**What to skip:** reproducing the research attacks against external sites  
**Expected takeaway:** define the browser-layer boundary of one coherent local profile and enumerate layers the study did not change.

### FP-Inconsistent assignment

**Direct link:** [FP-Inconsistent](https://arxiv.org/abs/2406.07647)  
**Exact section, chapter, or unit:** §5 Analysis; §6 Inconsistency Analysis; §7 FP-Inconsistent; §8.4 Limitations  
**Estimated time:** 60 minutes  
**What to focus on:** cross-attribute, cross-context, and temporal consistency measures plus dataset, collection, and population limits  
**What to skip:** treating a preprint result as a universal control or production population estimate  
**Expected takeaway:** design a consistency matrix whose residuals and legitimate exceptions remain visible after a coherent-set change.

## Course bridge

Research shows targeted spoofing and inconsistency analysis within defined
datasets and threat models.[^research] The useful lesson is not a stealth recipe;
it is that related attributes and time form constraints which a one-property
change ignores.

[^research]: Gummy Browsers §§3-8 and FP-Inconsistent §§5-8.4.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** A coherent-set change is allowed only when the set
    represents one predeclared environment claim. Record every member, reason,
    collection context, and remaining layer; do not add fields after seeing the result.

## Worked example

A Windows/en-US/Chicago/1280x720 profile links UA/OS claim, platform, language,
locale, timezone, viewport, screen, and context values. It says nothing by itself
about graphics hardware, TLS, connection behavior, account history, or action timing.

## Guided exercise

### Objective

Design—not deploy externally—a coherent local profile and evaluation matrix.

### Setup

Use the local context schema and research assignments. No new package is needed.

### Exact actions or commands

1. Declare one environment claim and every included attribute.
2. Map authoritative source/constraint and page/frame/worker availability.
3. Predict legitimate configurations that violate simple correlations.
4. Compare profile to manual and stock observations offline.
5. List protocol/session/behavior and graphics residuals.
6. Define a local-only implementation and retest plan without claiming completeness.

### Expected output

A constraint table, context matrix, exceptions, residuals, and narrow hypothesis.
No row says that consistency proves a real person.

### Interpretation

Coherence reduces obvious contradictions; it also increases experimental scope
and can create new mismatches. Residuals remain first-class evidence.

### Common failure modes

- Choosing values independently instead of one environment claim
- Adding a stealth library without inventorying its changes
- Ignoring legitimate privacy/VM/RDP/accessibility configurations
- Extending browser coherence claims to network identity

### Cleanup

This is a design exercise; remove real device or customer values from any copy
you choose to keep.

## Why this matters offensively

Sophisticated controls compare related evidence. A red teamer must test the
assumption coherently, show what still disagrees, and recommend controls that do
not overtrust brittle correlations.

## Check your understanding

1. A declared Windows, `en-US`, Chicago profile changes user-agent, platform, language, timezone, viewport, and screen values together. What makes that set a coherent treatment rather than unrelated changes?
2. Why must the learner declare the complete profile and constraints before comparing the treatment with manual and stock observations?
3. The page, frame, and worker values are internally consistent with the declared profile. Does that consistency prove the browser belongs to a genuine person or device?
4. The Gummy Browsers discussion describes browser-layer spoofing. Which evidence layer remains outside a browser-only identity claim?
5. Why should the profile table include legitimate configurations that break simple correlations such as language-to-timezone?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The values jointly express one predeclared environment claim and follow stated constraints across available contexts.** The treatment is coherent only within those declared attributes, not automatically across graphics, protocol, session, or behavior.

- **2. Predeclaration prevents the learner from adding properties after seeing the result and preserves a meaningful comparison.** The target, workflow, version, state, and evidence plan can then remain fixed.

- **3. No.** Fabricated profiles can be internally consistent, and legitimate unusual environments can look inconsistent. Consistency is one observation, not proof of authenticity, identity, or human intent.

- **4. Network and transport identity remain outside the browser-only spoofing claim.** TLS, HTTP behavior, intermediaries, session history, and action timing may still contradict the declared browser environment.

- **5. Legitimate exceptions reveal collateral and false-positive risk in simplistic rules.** Real users can travel, customize settings, use remote desktops, or choose language preferences that do not match timezone assumptions.

</details>

## Next lesson

[Replay and temporal consistency](04-replay-and-temporal-consistency.md) tests
whether a convincing snapshot survives freshness, binding, and time.
