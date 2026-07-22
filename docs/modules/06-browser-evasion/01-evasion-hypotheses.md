# Form an evasion hypothesis

<!-- source-ids: gummy-browsers, fp-inconsistent, aate-adversarial-control-loop -->

## Progress

- Module: 06 - Browser-control evasion
- Lesson: 1 of 5
- Depth: Integrated
- Estimated time: 3 hours
- Prerequisites:
  - [Blocked baseline](../05-control-recon/05-blocked-baseline.md)
  - Complete signal, context, and state maps
- Next lesson: One-variable experiment

## Role outcome

Write a falsifiable, bounded evasion hypothesis that predicts control and
protected-action outcomes while naming residual evidence and alternatives.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PREPRINT_RESEARCH | [Gummy Browsers](https://arxiv.org/abs/2110.10129) | Abstract/Introduction; §3; evaluation framing | Provides an offensive fingerprint-spoofing threat model | Research threat model and older browser/tool versions; network-layer identity was not spoofed in the study. |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | Threat model; inconsistency analysis; limitations | Supplies residual/coherence questions | Preprint studying a specific dataset, honey-site design, bot population, and selected services; not universal proof. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Hypothesis through alternative explanations | Defines the experiment contract | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

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
**Exact section, chapter, or unit:** Abstract and Introduction; §3 Attack Model and Spoofing Methods; skim §5 Dataset and Evaluation Methodology for the comparison design  
**Estimated time:** 70 minutes  
**What to focus on:** attacker knowledge/capability, acquisition/spoofing approaches, target fingerprint, success metric, and assumptions  
**What to skip:** implementation details and results until Lesson 3  
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

Use the blocked-baseline observations and transparent local reason. Do not run
the treatment yet.

### Exact actions or commands

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

## Check your understanding

1. The stock-headless baseline is challenged when top-page `navigator.webdriver` is true. Which two predicted outcomes must occur before the treatment supports the lesson's bypass hypothesis?
2. The treatment changes top-page `navigator.webdriver` before page code runs. Why must the plan name both the execution context and timing of that change?
3. Which observed outcome would refute the prediction that the one-variable treatment receives an action token and completes the synthetic report?
4. Why should the plan predict action-token replay separately from first-use acceptance?
5. A published browser-evasion result used another version, signal set, and target. Which limits prevent importing the published result as proof for the local experiment?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The local decision must change as predicted and the same protected report must succeed in the server's report record.** A decision change without that server-side result would remain control observation rather than offensive completion.

- **2. Other contexts or earlier collection times may retain the original value and expose a residual inconsistency.** Naming context and timing makes the treatment reproducible and keeps the hypothesis narrow.

- **3. A challenge decision or a denied protected report would refute the prediction under otherwise fixed conditions.** The hypothesis must define failure before the learner sees the treatment result.

- **4. Initial evaluation acceptance and later token freshness or single-use enforcement are different transitions.** The first action can succeed while replay remains correctly blocked, as the local model demonstrates.

- **5. The external result has a different threat model, versions, data, implementation, observed signals, and evaluation target.** It may inform a hypothesis but cannot replace local execution and evidence.

</details>

## Next lesson

[One-variable experiment](02-one-variable-experiments.md) executes the deliberately
limited local hypothesis and proves the action once.
