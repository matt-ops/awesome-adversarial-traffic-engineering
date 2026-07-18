# Establish the blocked baseline

<!-- source-ids: rebrowser-bot-detector, fpscanner-version-note, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 05 - Control reconnaissance
- Lesson: 5 of 5
- Depth: Integrated
- Estimated time: 3 hours
- Prerequisites:
  - [Session, behavior, and workflow](04-session-behavior-workflow.md)
  - Healthy local API and manual baseline artifact
- Required artifact: `artifacts/module-05/blocked-baseline.md`
- Next lesson: Evasion hypotheses

## Role outcome

Record manual, stock headed, stock headless, and HTTP-client populations with
versions, signal matrices, control decisions, and protected-action outcomes.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [Rebrowser detector](https://github.com/rebrowser/rebrowser-bot-detector) | README tests and limitations | Identifies version-sensitive stock automation observations | Version-sensitive artifact catalog with strong project claims; not a model of every commercial control. |
| VERSION_SENSITIVE | [FPScanner observation record](https://github.com/antoinevastel/fpscanner) | Commit/package/browser/options/output fields | Defines reproducibility metadata | Observations are valid only for the recorded code and browser versions. |
| LAB_SPECIFIC | [Control-recon lab](../../labs/integrated/control-recon.md) | HTTP and browser commands; expected decisions | Supplies the transparent local control | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Legitimate and blocked baselines; fixed variables | Gates evasion on comparable evidence | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Population | Execution | Required record | Expected local control result |
|---|---|---|---|
| Manual Chrome | human action | manual JS/HTTP/version | observation reference; do not submit fabricated automation data |
| Stock headed | Playwright visible | page/frame/worker/events | challenge in a genuine headed learner run |
| Stock headless | Playwright headless | same schema | challenge |
| Python HTTP | no renderer/DOM | HTTP response and absent browser APIs | page fetch only; cannot produce browser context matrix |

## Required external instruction

### Rebrowser baseline-version assignment

**Direct link:** [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector)  
**Exact section, chapter, or unit:** README overview, current limitations, and the named test descriptions used in the signal matrix  
**Estimated time:** 20 minutes  
**What to focus on:** framework/browser versions and the difference between a requested population label and the behavior actually observed  
**What to skip:** installation and bypass packages  
**Expected takeaway:** state which documented test behavior your recorded version is expected to expose.

### FPScanner reproducibility assignment

**Direct link:** [FPScanner](https://github.com/antoinevastel/fpscanner)  
**Exact section, chapter, or unit:** version-sensitive observation record: commit SHA, package version, browser version, enabled options, and observed output  
**Estimated time:** 15 minutes  
**What to focus on:** the minimum metadata another operator needs to reproduce a browser-control baseline  
**What to skip:** unrecorded current-main behavior and external execution  
**Expected takeaway:** produce a baseline record that can be repeated after browser or framework drift.

## Course bridge

A blocked baseline proves that the stock adversarial population does not perform
the protected action under the current control. It is the comparison point for
a later change. Manual and HTTP populations reveal near-neighbor behavior and
collection gaps; they are not substitutes for the blocked stock client.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE requires population, versions, control decision,
    and protected-action outcome in one comparison before changing any signal.

!!! warning "Safety boundary"
    The browser runner is fixed to localhost. `AATE_HEADLESS=1` is only automated
    verification; because it forces the requested headed trial to run headless,
    that artifact cannot be claimed as a genuine headed baseline.

## Worked example

```text
stock-headless: webdriver=true -> challenge -> no token -> action not attempted
one-variable:   excluded until Module 06
required conclusion: stock headless is blocked by this transparent local rule
prohibited: commercial controls block Playwright or the signal proves automation
```

## Guided exercise

### Objective

Complete the four-population baseline and freeze an evasion plan.

### Setup

Use the control-lab guide. Execute the headed learner run without the verification
environment variable on a workstation with a visible browser.

### Exact actions or commands

1. Preserve the manual baseline.
2. Execute the bounded HTTP-only command and record that JavaScript contexts are absent.
3. Execute `npm.cmd run playwright:control-recon` and isolate only stock-headed
   and stock-headless records; do not interpret one-variable yet.
4. Verify requested/actual head mode, versions, contexts, decisions, and absence
   of protected action for challenged trials.
5. Freeze target, workflow, context configuration, evidence schema, and candidate
   single changed property.

### Expected output

Stock populations report `challenge` and no protected action. HTTP returns the
HTML but executes no frame/worker JS. Manual values remain the reference.

### Interpretation

The evasion gate passes only when the headed trial actually ran headed and all
populations have explicit missing-data handling and comparable versions.

### Common failure modes

- Treating forced verification as headed
- Including the changed trial in the baseline
- Calling missing JavaScript values suspicious values
- Omitting protected-action status

### Cleanup

The runner closes browsers. Reset the local API and retain versioned evidence.

## Why this matters offensively

Without a blocked baseline, an allowed result may be normal behavior rather than
a bypass. Population discipline makes the later causal claim defensible.

## Required artifact

`artifacts/module-05/blocked-baseline.md` with four populations, environment,
raw signals, control/action outcomes, missing-data rules, fixed variables, and
the withheld hypothesis.

## Pass gate

1. Why exclude one-variable from the baseline?
2. What invalidates a claimed headed baseline?
3. Why include HTTP-only behavior?
4. What proves the stock client is blocked?
5. Which variables are frozen before evasion?

## Answer key

<details><summary>Check your reasoning</summary>

1. It is the treatment condition and would contaminate the reference.
2. Actual launch mode was headless, including forced verification mode.
3. It exposes browser-dependent observations and a non-rendering near-neighbor.
4. The control challenges it and it receives no token/protected action.
5. Target, workflow, state, context, versions, timing plan, and evidence schema except the declared change.

</details>

## Next lesson

[Evasion hypotheses](../06-browser-evasion/01-evasion-hypotheses.md) turns the
candidate trusted signal into a falsifiable prediction and abort criteria.
