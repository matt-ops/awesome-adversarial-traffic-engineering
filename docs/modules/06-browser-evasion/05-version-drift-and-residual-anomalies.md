# Version drift and residual anomalies

<!-- source-ids: fpscanner-version-note, rebrowser-bot-detector, fp-inconsistent, gummy-browsers, aate-adversarial-control-loop -->

> **Progress**  
> Module: 06 - Browser-control evasion  
> Lesson: 5 of 5  
> Depth: Deep  
> Estimated time: 4 hours plus later repeat  
> Prerequisites: Replay and temporal consistency  
> Artifact: `artifacts/module-06/version-drift-study.md`  
> Next: Protocol identity

## Role outcome

Repeat a versioned browser experiment, separate control drift from client drift,
and preserve residual anomalies that limit the bypass claim.

## Prerequisites

- [Replay and temporal consistency](04-replay-and-temporal-consistency.md)
- At least one complete baseline/treatment artifact

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| VERSION_SENSITIVE | [FPScanner record](https://github.com/antoinevastel/fpscanner) | commit/package/browser/options/output | Defines minimum version metadata |
| PROJECT_DOCUMENTATION | [Rebrowser detector](https://github.com/rebrowser/rebrowser-bot-detector) | current tests and limitations | Demonstrates framework/browser artifact drift |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | §8.4 limitations and conclusion | Bounds inconsistency claims |
| PREPRINT_RESEARCH | [Gummy Browsers](https://arxiv.org/abs/2110.10129) | §8 limitations and §9 | Shows version/threat-model limits of spoofing results |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | exact retest and alternatives | Structures drift attribution |

## Mental model

| Changed between runs | Attribution possible |
|---|---|
| browser only | client-version effect candidate |
| Playwright only | framework effect candidate |
| control code/rules only | control drift candidate |
| multiple untracked | result changed; cause unresolved |

## Required external instruction

### Drift assignment

**Direct link:** [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector), [FP-Inconsistent](https://arxiv.org/abs/2406.07647), and [Gummy Browsers](https://arxiv.org/abs/2110.10129)  
**Exact assignment:** Rebrowser current limitations/test descriptions; FP-Inconsistent §8.4 and §9; Gummy §8 and §9  
**Estimated time:** 65 minutes  
**Focus on:** dated implementations, evaluated populations, browser/framework evolution, unobserved layers, and non-universality  
**Skip:** external target testing and unsupported issue-thread claims  
**Expected takeaway:** write a drift claim that names exactly which component changed and which cause remains unresolved.

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

### Actions

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
