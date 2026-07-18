# Cross-context consistency

<!-- source-ids: fpscanner-project, fp-inconsistent, chrome-browser-process-model, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 05 - Control reconnaissance
- Lesson: 3 of 5
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [Browser environment](02-browser-environment.md)
  - Module 03 frame/worker collection
- Required artifact: `artifacts/module-05/context-matrix.md`
- Next lesson: Session, behavior, and workflow

## Role outcome

Compare top-page, iframe, and worker observations and identify cross-attribute,
cross-context, and temporal inconsistencies without overgeneralizing them.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Cross-Context Validation; limits and non-goals | Supplies an inspectable implementation concept | Inspectable detection-side implementation; not a complete commercial bot defense. |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | Abstract; 1; 3-7; 8.4; 9 | Supports measured inconsistency categories and limits | Preprint studying a specific dataset, honey-site design, bot population, and selected services; not universal proof. |
| OFFICIAL_DOCUMENTATION | [Chrome process model](https://developer.chrome.com/blog/inside-browser-part1/) | Browser architecture | Grounds separate execution contexts | Historical Chrome architecture article; implementation details evolve. |
| LAB_SPECIFIC | [Control-recon lab](../../labs/integrated/control-recon.md) | Page/frame/worker collectors | Supplies deterministic local evidence | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE adversarial-control loop](../../methodology/adversarial-control-loop.md) | Steps 7-12 | Connects context observations to a falsifiable hypothesis, protected-action result, and residual evidence | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Consistency type | Comparison | Example residual |
|---|---|---|
| Cross-context | same property across realms | page language differs from worker |
| Cross-attribute | related properties in one/combined context | Windows UA with Linux platform |
| Temporal | same environment over trials | platform changes mid-session |
| Cross-layer | browser claim versus protocol/session | Chrome claim with incompatible network behavior |

## Required external instruction

### FP-Inconsistent assignment

**Direct link:** [FP-Inconsistent](https://arxiv.org/abs/2406.07647)  
**Exact section, chapter, or unit:** Abstract; §1 Introduction; §3 Threat Model; §4 Measurement Infrastructure; §5 Analysis; §6 Inconsistency Analysis; §7 FP-Inconsistent; §8 with emphasis on §8.4 Limitations; §9  
**Estimated time:** 90 minutes  
**What to focus on:** measurement design, cross-attribute and temporal categories, evaluated population, and limits on generalization  
**What to skip:** exhaustive table values not needed to explain the method  
**Expected takeaway:** explain why a top-page property patch can leave correlated evidence and why the paper is not universal proof.

## Course bridge

FP-Inconsistent studies inconsistencies in a defined measurement setting and
bot population; its findings are bounded by the threat model, collection design,
and limitations.[^fpi]

[^fpi]: FP-Inconsistent, §§3-8.4.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Preserve raw values per context before computing a
    consistency label. Missing/unavailable is different from mismatch, and a
    mismatch is evidence to investigate rather than identity proof.

## Worked example

```text
page.language=en-US | frame.language=en-US | worker.language=fr-FR
result: observed cross-context mismatch
not proved: why it differs, whether control uses it, or whether caller is abusive
next: repeat cleanly, establish control response, inspect configuration/collection
```

## Guided exercise

### Objective

Build a context matrix from manual and stock automation observations.

### Setup

Use your manual baseline and inspect the `signals` portions of a verified
`lab/telemetry/control-recon.json`. Do not analyze the one-variable trial yet.

### Exact actions or commands

1. Compare language/platform across page, frame, and worker.
2. Record unavailable values separately.
3. Compare UA claim, platform, timezone, viewport, and screen for coherence.
4. Record requested versus actual launch mode and browser version.
5. List alternative explanations for each difference.

### Expected output

A per-population raw matrix and derived consistency table. Verification mode may
show headed requested but headless actual; the artifact makes this explicit.

### Interpretation

Consistency analysis finds residual questions. It does not reveal control weight
until response and protected-action trials test the candidate.

### Common failure modes

- Converting unavailable to an empty mismatch silently
- Comparing manual and automation from different versions without noting it
- Treating one paper's population as every deployment
- Hiding verification-forced headless mode

### Cleanup

No new traffic is needed. Preserve raw before derived data.

## Why this matters offensively

Incomplete modification is a common failure mode of evasion experiments. A
context matrix reveals where the claimed environment becomes internally
contradictory and guides the next falsifiable hypothesis.

## Required artifact

`artifacts/module-05/context-matrix.md` with raw/derived tables, missing-data
policy, versions, alternatives, and source limits.

## Pass gate

1. What differs between cross-context and cross-attribute inconsistency?
2. Why is missing not automatically mismatch?
3. What does the paper's threat model constrain?
4. Why retain raw values?
5. Does a mismatch prove the control uses that signal?

## Answer key

<details><summary>Check your reasoning</summary>

1. Cross-context compares a property across realms; cross-attribute compares related properties.
2. The API may be unavailable or collection may fail; no contradictory value was observed.
3. Which adversaries, collection points, data, and conclusions the evaluation supports.
4. Derived labels can be audited/recomputed and collection errors found.
5. No; a controlled response/action experiment is still required.

</details>

## Next lesson

[Session, behavior, and workflow](04-session-behavior-workflow.md) adds server
state and action sequences that browser-only fingerprint matrices omit.
