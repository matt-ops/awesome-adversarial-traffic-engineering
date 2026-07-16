# Five signal families

<!-- source-ids: fpscanner-project, rebrowser-bot-detector, aate-adversarial-control-loop -->

> **Progress**  
> Module: 05 - Control reconnaissance  
> Lesson: 1 of 5  
> Depth: Foundation  
> Estimated time: 2 hours  
> Prerequisites: Module 04  
> Artifact: `artifacts/module-05/signal-matrix.md`  
> Next: Browser environment

## Role outcome

Classify candidate control observations into five families and estimate attacker
control, imitation cost, collateral risk, and the evidence required to test them.

## Prerequisites

- [Module 04](../04-automated-abuse/index.md)
- One mapped protected workflow and authoritative proof source

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Description; Features; What It Detects; constraints | Supplies inspectable signal categories and explicit limits |
| PROJECT_DOCUMENTATION | [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector) | README overview; test categories and named artifact tests | Shows current automation-artifact probes |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Trusted-signal enumeration through protected-action proof | Organizes detection surfaces for offensive testing |

## Mental model

| Family | Examples | Attacker influence | Common weak inference |
|---|---|---|---|
| Network/transport | source path, TLS, connection reuse, HTTP version | proxy/client stack can change some | fingerprint equals person |
| HTTP claims | UA, Accept-Language, Fetch metadata, header order | often directly or indirectly changeable | claim equals implementation |
| Browser runtime | webdriver, platform, APIs, viewport, graphics, contexts | values can be patched but coherence is costly | one value proves automation |
| Session/state | cookies, tokens, nonce, account, history | reuse/rotation constrained by server binding | new key equals new adversary |
| Behavior/workflow | sequence, timing, concurrency, resource use, outcome | automation controls actions but objective constrains them | fast behavior is always abusive |

## Required external instruction

### Detection-target assignment

**Direct link:** [FPScanner](https://github.com/antoinevastel/fpscanner) and [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector)  
**Exact assignment:** FPScanner Description, open-source/real-world constraints, Features, What It Detects; Rebrowser README overview, What are the tests?, runtimeEnableLeak, sourceUrlLeak, mainWorldExecution, navigatorWebdriver, bypassCsp, viewport, window.dummyFn  
**Estimated time:** 60 minutes  
**Focus on:** observation surface, execution context, required instrumentation, version dependency, and project-stated limits  
**Skip:** installation, bypass packages, issue-thread claims, and unrelated repository files  
**Expected takeaway:** place every named test in a signal family and explain why it is evidence rather than identity proof.

## Course bridge

FPScanner is an inspectable detection-side project; Rebrowser catalogs current
automation artifacts. Neither represents every commercial control, and both are
version-sensitive.[^projects]

[^projects]: FPScanner and Rebrowser Bot Detector READMEs, assigned sections.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Rank each signal by attacker control, cost to imitate,
    legitimate variability, cross-context reach, protocol/session dependence,
    and whether changing it can plausibly affect the protected action.

## Worked example

`navigator.webdriver` is a browser-runtime property. It is easy to observe and
sometimes easy to change, so treating it as decisive creates a cheap bypass and
can classify benign automation. A stronger test asks whether it changes the
decision, then whether the same action succeeds, while recording frame, worker,
protocol, session, and behavioral residuals.

## Guided exercise

### Objective

Create a control-surface matrix before inspecting the local rule.

### Setup

Use the two assigned source lists. Do not install either project yet.

### Actions

1. Add at least three signals to each family.
2. Record collection point, caller influence, imitation cost, legitimate
   variability, cross-context/protocol implications, and likely drift.
3. Mark direct project statements versus your hypotheses.
4. Select one candidate for a blocked-baseline experiment; do not change it.
5. Name the protected action and authoritative proof the experiment would need.

### Expected output

At least fifteen classified signals with no claim that one proves identity. The
selected candidate includes an observation plan and a withheld bypass hypothesis.

### Interpretation

The matrix maps what a control *could* consume. Only trial evidence reveals what
the local control actually relies on.

### Common failure modes

- Treating project test names as universal commercial behavior
- Ignoring session/workflow signals because they are not JavaScript properties
- Equating easy spoofing with guaranteed bypass
- Omitting legitimate clients with similar values

### Cleanup

No target was contacted. Keep the public artifact free of proprietary rules.

## Why this matters offensively

Control reconnaissance narrows experimentation. It prevents random stealth
changes and identifies overtrusted, inconsistent, or low-cost assumptions whose
failure can be proved through the original adversary objective.

## Required artifact

`artifacts/module-05/signal-matrix.md` with the fields used above, source label,
candidate trusted signal, protected action, and prohibited conclusion.

## Pass gate

1. Which family contains a TLS fingerprint?
2. Why is a UA string a claim rather than implementation proof?
3. Where does a challenge nonce belong?
4. Why record legitimate variability?
5. What turns a signal change into an offensive bypass result?

## Answer key

<details><summary>Check your reasoning</summary>

1. Network/transport.
2. The client constructs or influences it and other layers may contradict it.
3. Session/state, with possible workflow implications.
4. It exposes collateral/false-positive risk and limits the inference.
5. The control decision changes and the same protected action succeeds with authoritative proof.

</details>

## Next lesson

[Browser environment](02-browser-environment.md) collects concrete runtime
values and records which execution context produced each one.

