# Remediation and exact retest

<!-- source-ids: nist-sp-800-115, owasp-code-review-guide, aate-adversarial-control-loop, aate-local-lab -->

## Progress

- Module: 10 - Findings, briefing, and interview practice
- Lesson: 2 of 5
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [Finding and evidence](01-finding-and-evidence.md)
  - The original command, input, state reset, raw evidence, and result
- Next lesson: Technical briefing

## Role outcome

Translate attack evidence into a control invariant and an exact acceptance test
that rejects the former attack while preserving intended behavior.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §§8.2-8.3 | Grounds mitigation and resolution | General testing guide; it does not define bot-control or DDoS red-team procedure. |
| PROJECT_DOCUMENTATION | [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/) | authorization and error/logging review | Grounds invariant review | Broad guide; lessons assign only sections relevant to the local review case. |
| COURSE_SYNTHESIS | [Adversarial-control loop](../../methodology/adversarial-control-loop.md) | Steps 14-15 | Defines measurable remediation criteria and exact-retest acceptance | Course synthesis; no cited standard defines the exact fifteen-step sequence. |
| LAB_SPECIFIC | [Code-review cases](../../labs/deep/code-review.md) | negative and positive cases | Supplies local examples | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

| Retest component | Must remain the same | May change only if documented |
|---|---|---|
| Adversary objective | protected action/service effect | no |
| Attack steps and inputs | former proof path | only to accommodate a documented interface change |
| State and reset | comparable precondition | implementation-specific reset mechanism |
| Observation | effect plus supporting telemetry | added telemetry is allowed |
| Negative result | former attack denied/no effect | exact status may change if the invariant holds |
| Positive result | intended near-neighbor succeeds | representative legitimate identity/workflow |

The recommendation should describe an invariant: “a challenge authorization is
bound to subject, action, nonce, expiry, and one-time use.” The implementation
may use different mechanisms. The retest checks the invariant at the same trust boundary.

## Required external instruction

### Required remediation assignment

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)

**Exact section, chapter, or unit:** reread §8.2 Mitigation Recommendations and §8.3 Post-Testing Activities; extract how recommendations account for root cause, feasibility, compensating controls, validation, and residual risk

**Estimated time:** 40 minutes

**What to focus on:** root-cause alignment, prioritization, owner/action, validation, cleanup, and residual risk

**What to skip:** assessment execution chapters

**Expected takeaway:** write a recommendation that can be implemented in more than one way and verified by objective tests.

## Course bridge

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Exact retest replays the former adversary objective
    and proof, then adds legitimate positive and boundary-negative cases. Do not
    weaken the test by changing the attack population, path, or success
    definition after remediation.

## Worked example

For challenge replay, the negative matrix contains wrong session, wrong action,
second use, expired token, and modified token. The positive case uses the issued
token once for its bound session/action before expiry. The protected report must
not execute for negatives; an error status alone is insufficient if work still occurs.

## Guided exercise

### Objective

Create an executable retest matrix for the finding written in the previous lesson.

### Setup

Copy the original setup, reset, command/request, and expected effect into a new plan.

### Exact actions or commands

1. Name the failed invariant in subject-object-action or resource terms.
2. State the remediation outcome without prescribing a vendor.
3. Preserve the former attack as the first negative case.
4. Add mutation cases for each missing binding or resource assumption.
5. Add at least two legitimate cases adjacent to the attack.
6. Define state/effect evidence, supporting telemetry, threshold, abort, owner, and cleanup.
7. State residual risk and the evidence needed for broader confidence.

### Expected output

A table where every row has precondition, input, expected decision, expected
effect, evidence query, and pass/fail rule. The original attack is recognizable verbatim.

### Interpretation

A retest can pass while residual risk remains—for example, session binding may
work while action binding is absent. Report exactly which invariant was tested.

### Common failure modes

- Testing the implementation detail instead of the security invariant
- Replacing the former attack with an easier case
- Checking only status, not state/work effect
- Omitting positive and collateral-impact tests
- Declaring all variants fixed from one passing row

### Cleanup

Reset local state after each row and preserve results with implementation version.

## Why this matters offensively

An exact retest converts an offensive technique into a durable regression test
and prevents remediation from silently redefining success.

## Check your understanding

1. The proposed challenge fix says a token must be bound to the solving session, protected action, expiry, and one use. What does that remediation invariant express?
2. Why should the regression suite preserve the exact former Session B replay instead of replacing the test with a new generic unauthorized request?
3. The remediated endpoint returns `403`, but server inventory still decreases. Why is the status insufficient evidence that the invariant now holds?
4. Which positive Session A case should accompany the negative Session B replay test?
5. A passing retest covers one token, route, version, and boundary. Why can the result not prove that every possible replay variant is fixed?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The invariant states the security property that must hold regardless of implementation details: only the correct session may use the token for the intended action within its lifetime and use limit.**

- **2. The former replay is the demonstrated failure and provides the closest comparable acceptance case.** Replacing it could miss the exact weak binding that produced the original protected effect.

- **3. A response can deny the client while backend work or state mutation still occurs.** The retest must verify inventory and session records stored by the server, which are the final source of truth, as well as the visible response.

- **4. Session A should solve the challenge and complete the intended protected action once under valid state.** That positive case confirms the fix rejects cross-session use without breaking legitimate behavior.

- **5. The evidence supports only the tested security rule, inputs, variants, environment, and version.** Other routes, token types, timing conditions, or implementations require their own bounded tests and residual-risk statement.

</details>

## Next lesson

Continue to [Technical briefing](03-technical-briefing.md).
