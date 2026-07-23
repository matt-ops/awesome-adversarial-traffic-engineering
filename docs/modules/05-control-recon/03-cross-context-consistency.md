# Cross-context consistency

<!-- source-ids: fpscanner-project, fp-inconsistent, chrome-browser-process-model, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 05 - Control reconnaissance
- Lesson: 3 of 6
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [Browser environment](02-browser-environment.md)
  - Module 03 frame/worker collection
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
show headed requested but headless actual; the result record makes this explicit.

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

## Check your understanding

1. The page reports `en-US`, the frame reports `en-US`, and the worker reports `fr-FR`. Is that a cross-context or cross-attribute inconsistency, and why?
2. The worker does not expose a page-only API, so the matrix records the value as unavailable. Why should unavailable not be labeled as a mismatch?
3. A research paper evaluates a specific browser version, adversary, collection point, and dataset. How do those facts limit use of the paper's consistency results?
4. Why should the exercise retain raw page, frame, and worker values after deriving a consistency label?
5. Does the `en-US` versus `fr-FR` mismatch prove the local control collects or enforces on language consistency?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The language difference is cross-context because the same property is compared across page, frame, and worker realms.** Cross-attribute analysis would compare related but different properties, such as language and timezone.

- **2. Unavailable means the API did not exist or collection failed, so no contradictory value was observed.** Labeling absence as mismatch would confuse missing evidence with an actual disagreement.

- **3. The threat model defines which adversaries, environments, data, and conclusions the evaluation supports.** Applying the result elsewhere requires a new hypothesis and evidence rather than assuming the paper covers every browser or control.

- **4. Raw values let another reviewer recompute the label, find collection errors, and see exactly which contexts disagreed.** A derived label alone hides details that may matter during retest.

- **5. No.** The mismatch is an observation that may motivate a controlled experiment. A control-use claim requires a measured decision change and, for a bypass, successful repetition of the protected action.

</details>

## Next lesson

[Session, behavior, and workflow](04-session-behavior-workflow.md) adds server
state and action sequences that browser-only fingerprint matrices omit.
