# Identity coherence

<!-- source-ids: gummy-browsers, fp-inconsistent, fpscanner-project, aate-adversarial-control-loop -->

> **Progress**  
> Module: 06 - Browser-control evasion  
> Lesson: 3 of 5  
> Depth: Applied  
> Estimated time: 4 hours  
> Prerequisites: One-variable experiment  
> Artifact: `artifacts/module-06/coherent-profile.md`  
> Next: Replay and temporal consistency

## Role outcome

Design and evaluate a declared browser-environment profile across related
attributes and contexts while preserving residual contradictions.

## Prerequisites

- [One-variable experiment](02-one-variable-experiments.md)
- Context matrix and signal-family artifact

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PREPRINT_RESEARCH | [Gummy Browsers](https://arxiv.org/abs/2110.10129) | §§3-6; §8 limitations; §9 | Provides spoofing approaches and evaluated results |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | §§5-8.4 | Supports cross-attribute/temporal residual analysis |
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Cross-Context Validation; non-goals | Provides an inspectable target concept |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Coherent-set experiment and residuals | Defines bounded claims |

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

### Coherence research assignment

**Direct link:** [Gummy Browsers](https://arxiv.org/abs/2110.10129) and [FP-Inconsistent](https://arxiv.org/abs/2406.07647)  
**Exact assignment:** Gummy §§3 Attack Model, 4 Implementation, 5 Evaluation Methodology, 6 Results, 8 limitations, 9; FP-Inconsistent §§5 Analysis, 6 Inconsistency Analysis, 7, 8.4 Limitations  
**Estimated time:** 2 hours  
**Focus on:** which attributes/layers were acquired or spoofed, consistency measures, evaluated versions/populations, and unmodified network identity  
**Skip:** reproducing research attacks against external sites  
**Expected takeaway:** design a local profile and enumerate what remains outside its claim.

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

### Actions

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

This is a design artifact; remove real device/customer values.

## Why this matters offensively

Sophisticated controls compare related evidence. A red teamer must test the
assumption coherently, show what still disagrees, and recommend controls that do
not overtrust brittle correlations.

## Required artifact

`artifacts/module-06/coherent-profile.md` with claim, constraints, values,
contexts, legitimate exceptions, residuals, implementation bound, and retest.

## Pass gate

1. What makes a changed set coherent?
2. Why predeclare the set?
3. Does internal consistency prove authenticity?
4. Which layer did Gummy Browsers not fully spoof?
5. Why include legitimate exceptions?

## Answer key

<details><summary>Check your reasoning</summary>

1. Its values jointly express one necessary environment claim and constraints.
2. It prevents result-driven expansion and preserves causal interpretation.
3. No; fabricated or unusual legitimate environments can be consistent.
4. Its limitations include network-layer identity outside the browser spoofing claim.
5. They expose collateral risk and simplistic correlations.

</details>

## Next lesson

[Replay and temporal consistency](04-replay-and-temporal-consistency.md) tests
whether a convincing snapshot survives freshness, binding, and time.

