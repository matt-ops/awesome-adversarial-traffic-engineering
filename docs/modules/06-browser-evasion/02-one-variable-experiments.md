# One-variable evasion experiment

<!-- source-ids: rebrowser-bot-detector, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 06 - Browser-control evasion
- Lesson: 2 of 5
- Depth: Integrated
- Estimated time: 2 hours
- Prerequisites:
  - [Form an evasion hypothesis](01-evasion-hypotheses.md)
  - Genuine stock-headless blocked baseline with matching environment
- Required artifact: `lab/telemetry/control-recon.json`
- Next lesson: Identity coherence

## Role outcome

Execute a single-property local evasion, prove the protected action, and state why
the result is not a coherent browser identity or general bypass.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [Rebrowser detector](https://github.com/rebrowser/rebrowser-bot-detector) | navigatorWebdriver and limitations | Documents the observed property as one version-sensitive artifact | Version-sensitive artifact catalog with strong project claims; not a model of every commercial control. |
| LAB_SPECIFIC | [Control-recon lab](../../labs/integrated/control-recon.md) | One-variable trial, action, replay | Supplies transparent enforced behavior | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Change, repeat, prove, residuals | Defines causal comparison | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Stage | Stock headless | One-variable |
|---|---|---|
| Top-page webdriver | true | false after document load |
| Other declared variables | fixed | fixed |
| Local decision | challenge | allow |
| Protected report | not attempted/no token | `200`, action accepted |
| Token replay | unavailable | `403` after first use |

## Required external instruction

### Property-specific assignment

**Direct link:** [Rebrowser navigatorWebdriver test](https://github.com/rebrowser/rebrowser-bot-detector)  
**Exact section, chapter, or unit:** README `navigatorWebdriver` description and current limitations  
**Estimated time:** 20 minutes  
**What to focus on:** what the property exposes, test context, and version sensitivity  
**What to skip:** bypass libraries and unrelated tests  
**Expected takeaway:** explain why removing one test result leaves other automation and coherence evidence.

## Course bridge

The script changes the loaded top page only. It does not claim to patch every
realm, remove framework artifacts, alter TLS/HTTP behavior, create history, or
imitate human behavior. The local control intentionally overrelies on the value.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** The decision shift is counted as a bypass only because
    the same protected report succeeds and the stock comparison remains blocked.

!!! info "Lab-specific behavior"
    The transparent endpoint challenges whenever its submitted top-page value is
    true and otherwise checks only two simple consistency rules. This weakness is
    designed for experimental method, not control realism.

## Worked example

The expected artifact row is `webdriver=false`, `decision=allow`, protected
status `200`, replay `403`. A changed detector score without the `200` would not
meet the pass gate.

## Guided exercise

### Objective

Run the pre-registered treatment and compare it to stock headless.

### Setup

Keep the local API healthy. Confirm versions and actual headless mode match the
baseline. Read the runner's change block and protected/replay calls.

### Exact actions or commands

1. Execute `npm.cmd run playwright:control-recon`.
2. Compare only stock-headless and one-variable trial fields.
3. Verify changed property, decision, token, action body/status, replay status,
   page/frame/worker values, and network evidence.
4. Mark the hypothesis supported or refuted.
5. Record unchanged automation/protocol/session/behavior residuals.

### Expected output

The one-variable trial is allowed, creates one synthetic report with `200`, and
fails token reuse with `403`. Stock headless remains challenged.

### Interpretation

The result proves one transparent local control overtrusted one submitted
property. It does not establish stealth or bypass of another implementation.

### Common failure modes

- Comparing to the requested-headed trial under forced verification
- Omitting the action body
- Claiming replay resistance was bypassed when replay returns `403`
- Generalizing the toy result

### Cleanup

Runner closes browsers; reset the local API and keep the JSON evidence.

## Why this matters offensively

This is the smallest causal bypass experiment: blocked client, one change,
decision shift, same action, authoritative response, and residuals.

## Required artifact

Keep `lab/telemetry/control-recon.json` and add
`artifacts/module-06/one-variable-conclusion.md` with comparison and limitations.

## Pass gate

1. What exactly changed?
2. What proves the protected action?
3. What does replay `403` show?
4. Why is this identity incoherent?
5. What is the maximum allowed conclusion?

## Answer key

<details><summary>Check your reasoning</summary>

1. The loaded top-page `navigator.webdriver` value only.
2. Token-issued trial's `/api/control/protected` returned accepted report `200`.
3. The token is single-use in the local model.
4. Other runtime, framework, protocol, session, and behavioral evidence was not changed to a consistent profile.
5. This property bypassed this transparent local rule under the recorded version/conditions.

</details>

## Next lesson

[Identity coherence](03-identity-coherence.md) replaces a cosmetic property goal
with a declared, internally consistent environment profile and residual analysis.
