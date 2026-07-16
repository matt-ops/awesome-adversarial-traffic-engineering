# Form an evasion hypothesis

<!-- source-ids: gummy-browsers, fp-inconsistent, aate-adversarial-control-loop -->

> **Progress**  
> Module: 06 - Browser-control evasion  
> Lesson: 1 of 5  
> Depth: Foundation  
> Estimated time: 3 hours  
> Prerequisites: Module 05 blocked baseline  
> Artifact: `artifacts/module-06/evasion-plan.md`  
> Next: One-variable experiment

## Role outcome

Write a falsifiable, bounded evasion hypothesis that predicts control and
protected-action outcomes while naming residual evidence and alternatives.

## Prerequisites

- [Blocked baseline](../05-control-recon/05-blocked-baseline.md)
- Complete signal, context, and state maps

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PREPRINT_RESEARCH | [Gummy Browsers](https://arxiv.org/abs/2110.10129) | Abstract/Introduction; §3; evaluation framing | Provides an offensive fingerprint-spoofing threat model |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | Threat model; inconsistency analysis; limitations | Supplies residual/coherence questions |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Hypothesis through alternative explanations | Defines the experiment contract |

## Mental model

```text
Because control C appears to rely on signal S,
changing only S from observed baseline A to declared value B,
while fixing target/workflow/state/environment E,
will change decision challenge -> allow and permit protected action P.
Refuted if decision or P does not change; limited by residuals R and alternatives X.
```

## Required external instruction

### Gummy Browsers threat-model assignment

**Direct link:** [Gummy Browsers](https://arxiv.org/abs/2110.10129)  
**Exact assignment:** Abstract and Introduction; §3 Attack Model and Spoofing Methods; skim §5 Dataset and Evaluation Methodology for the comparison design  
**Estimated time:** 70 minutes  
**Focus on:** attacker knowledge/capability, acquisition/spoofing approaches, target fingerprint, success metric, and assumptions  
**Skip:** implementation details and results until Lesson 3  
**Expected takeaway:** separate a research threat model from a universal bypass claim and write your local hypothesis with narrower assumptions.

## Course bridge

Gummy Browsers demonstrates spoofing within its defined threat model and older
tool/browser environment; it explicitly does not establish all cross-layer
identity behavior.[^gummy]

[^gummy]: Gummy Browsers, §§3, 5, and 8 limitations.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE requires both decision change and the original
    protected action. It also requires residual anomalies and competing causes
    even when the hypothesis is supported.

## Worked example

```text
Observation: stock top-page webdriver=true; local reason names it.
Hypothesis: top-page false alone removes the toy reason and issues an action token.
Fixed: browser version, headless mode, locale/timezone, viewport, frame/worker,
       nonce uniqueness, request path, session, protected action.
Support: allow + synthetic report 200.
Refute: challenge or protected report denied.
Residual: framework/network/worker behavior unchanged.
```

## Guided exercise

### Objective

Freeze the one-variable trial before viewing its result.

### Setup

Use the blocked-baseline artifact and transparent local reason. No execution yet.

### Actions

1. State observation separately from inference.
2. Name exact changed property, value, context, and timing.
3. List every fixed variable and abort condition.
4. Predict decision, token, protected action, replay, and context matrix.
5. List at least three residuals and three alternatives.
6. Define the narrow allowed conclusion.

### Expected output

A plan that can be marked supported/refuted without rewriting success after the
fact. It explicitly denies claims about external or production controls.

### Interpretation

If the plan cannot be refuted or does not repeat the action, it is a tuning
exercise rather than an offensive experiment.

### Common failure modes

- Changing a stealth package rather than a named variable/set
- Leaving fixed variables implicit
- Defining success as lower score only
- Omitting the no-change/abort path

### Cleanup

No trial executed. Preserve the pre-registered plan.

## Why this matters offensively

Pre-registration turns evasion from trial-and-error into evidence about a trusted
assumption. It makes a finding reproducible and remediation retestable.

## Required artifact

`artifacts/module-06/evasion-plan.md` with observation, hypothesis, fixed/change,
predictions, support/refute, abort, residuals, alternatives, and conclusion bound.

## Pass gate

1. What two outcomes support an AATE bypass?
2. Why name the context and timing of a change?
3. What makes a hypothesis falsifiable?
4. Why predict replay separately?
5. What limits applying research results elsewhere?

## Answer key

<details><summary>Check your reasoning</summary>

1. Control decision changes as predicted and the same protected action succeeds.
2. Other contexts/times may retain the original value and become residual evidence.
3. A defined observation would refute it under fixed conditions.
4. Initial acceptance and freshness/single-use are different controls.
5. Threat model, versions, data, implementation, signal set, and evaluation target.

</details>

## Next lesson

[One-variable experiment](02-one-variable-experiments.md) executes the deliberately
limited local hypothesis and proves the action once.

