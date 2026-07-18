# Version drift and residual anomalies

<!-- source-ids: fpscanner-version-note, rebrowser-bot-detector, fp-inconsistent, gummy-browsers, aate-adversarial-control-loop -->

## Progress

- Module: 06 - Browser-control evasion
- Lesson: 5 of 5
- Depth: Deep
- Estimated time: 4 hours plus later repeat
- Prerequisites:
  - [Replay and temporal consistency](04-replay-and-temporal-consistency.md)
  - At least one complete baseline/treatment artifact
- Required artifact: `artifacts/module-06/version-drift-study.md`
- Next lesson: Protocol identity

## Role outcome

Repeat a versioned browser experiment, separate control drift from client drift,
and preserve residual anomalies that limit the bypass claim.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| VERSION_SENSITIVE | [FPScanner record](https://github.com/antoinevastel/fpscanner) | commit/package/browser/options/output | Defines minimum version metadata | Observations are valid only for the recorded code and browser versions. |
| PROJECT_DOCUMENTATION | [Rebrowser detector](https://github.com/rebrowser/rebrowser-bot-detector) | current tests and limitations | Demonstrates framework/browser artifact drift | Version-sensitive artifact catalog with strong project claims; not a model of every commercial control. |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | §8.4 limitations and conclusion | Bounds inconsistency claims | Preprint studying a specific dataset, honey-site design, bot population, and selected services; not universal proof. |
| PREPRINT_RESEARCH | [Gummy Browsers](https://arxiv.org/abs/2110.10129) | §8 limitations and §9 | Shows version/threat-model limits of spoofing results | Research threat model and older browser/tool versions; network-layer identity was not spoofed in the study. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | exact retest and alternatives | Structures drift attribution | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Changed between runs | Attribution possible |
|---|---|
| browser only | client-version effect candidate |
| Playwright only | framework effect candidate |
| control code/rules only | control drift candidate |
| multiple untracked | result changed; cause unresolved |

## Required external instruction

### Rebrowser version-sensitive assignment

**Direct link:** [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector)  
**Exact section, chapter, or unit:** current limitations and descriptions of the tests used by the course baseline  
**Estimated time:** 20 minutes  
**What to focus on:** the browser/framework versions and implementation artifacts on which each documented check depends  
**What to skip:** unsupported issue-thread claims and bypass packages  
**Expected takeaway:** name which client component/version must be recorded before a detection or evasion observation is reproducible.

### FP-Inconsistent limitations assignment

**Direct link:** [FP-Inconsistent](https://arxiv.org/abs/2406.07647)  
**Exact section, chapter, or unit:** §8.4 Limitations and §9 Conclusion  
**Estimated time:** 20 minutes  
**What to focus on:** evaluated populations, collection method, time range, and conclusions that do not transfer automatically  
**What to skip:** treating the measured prevalence as a universal current rate  
**Expected takeaway:** constrain a drift claim to the paper's measured conditions and your newly recorded run.

### Gummy Browsers limitations assignment

**Direct link:** [Gummy Browsers](https://arxiv.org/abs/2110.10129)  
**Exact section, chapter, or unit:** §8 Discussion and limitations; §9 Conclusion  
**Estimated time:** 25 minutes  
**What to focus on:** dated browser/tool versions, unmodified network identity, and the evaluation boundary  
**What to skip:** reproducing attacks against external targets  
**Expected takeaway:** write a drift claim that names the changed component, unchanged residual layers, and unresolved causal alternatives.

## Course bridge

Automation artifacts and browser behavior evolve. Research conclusions remain
tied to their threat models, code, versions, and data. Recording versions is not
administrative decoration; it is part of the causal evidence.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE changes one version-bearing component per retest
    when attribution matters and preserves every unresolved residual.

!!! info "Version-sensitive observation"
    Retain Playwright lockfile version, browser product/version, OS, control code
    commit, source project commit, launch flags, and actual head mode.

## Worked example

Run A uses browser 149, Playwright 1.61.1, local control commit X. Run B changes
only browser. If webdriver exposure changes, client drift is a candidate. If the
control also changed, the cause is confounded until isolated.

## Guided exercise

### Objective

Design and, when a second version is available, execute an exact drift comparison.

### Setup

Copy the original artifact immutably. Use a later pinned browser/framework or a
clearly labeled static fixture; never overwrite Run A.

### Exact actions or commands

1. Record complete environment/control/source versions for Run A.
2. Declare one version variable for Run B.
3. Repeat stock and treatment workflows with identical state/evidence schema.
4. Diff raw signals, decisions, action outcomes, errors, and timing.
5. Classify resolved and unresolved residuals.
6. Update remediation/retest criteria without claiming permanence.

### Expected output

A two-run table with one declared version change or a labeled study plan awaiting
that version. Conclusions name drift candidates, confounders, and limits.

### Interpretation

An unchanged bypass is evidence only for both recorded environments. A changed
result prompts attribution work; it does not prove the original was false.

### Common failure modes

- Updating lockfile/browser/control together
- Overwriting original telemetry
- Calling a fixture a live-version result
- Hiding residual contradictions after action success

### Cleanup

Remove temporary browser binaries only through their package manager if desired;
keep lock/version and public-safe evidence.

## Why this matters offensively

Red teams must repeat capability after fixes and platform changes. Drift-aware
evidence prevents brittle tricks from becoming durable security conclusions.

## Required artifact

`artifacts/module-06/version-drift-study.md` with two environments, one change,
raw diff, decisions/actions, residuals, confounders, and future retest trigger.

## Pass gate

1. Why is a browser version part of evidence?
2. What makes a drift comparison confounded?
3. Does an unchanged result prove permanence?
4. Why keep residual anomalies after success?
5. How should a static fixture be labeled?

## Answer key

<details><summary>Check your reasoning</summary>

1. Observable properties and automation artifacts can change with implementation.
2. Multiple uncontrolled version/control/environment changes prevent attribution.
3. No; it supports only recorded runs and conditions.
4. They limit the claim and may remain useful to the control/remediation.
5. As a simulated comparison input, not a live execution of that version.

</details>

## Next lesson

[Open Module 07](../07-protocol-identity/index.md) to compare browser claims with
TLS and HTTP behavior rather than stopping at JavaScript coherence.
