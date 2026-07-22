# Experimental method before attack execution

<!-- source-ids: nist-sp-800-115, owasp-wstg-entry-points-v42, aate-adversarial-control-loop, aate-local-lab -->

## Appendix guide

- Appendix: Red-team method and engagement practice
- Status: Optional
- Best time to review: before an informational or interview; before a
  provider-hosted assessment; before an organization-owned engagement; or
  before the integrated capstone
- Prior technical lessons required: None
- Return to the core path: [HTTP request and response](../01-http-edge/01-http-request-response.md)
- Appendix lesson: 3 of 3
- Estimated time: 100 minutes

## Role outcome

Design a baseline, falsifiable hypothesis, controlled change, protected-action
proof, limitation statement, remediation criterion, and identical retest before
executing the attack.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §5.2.1 and §§8.1–8.3 | Connects attack validation to analysis, reporting, and mitigation | General testing guide; it does not define bot-control or DDoS red-team procedure. |
| PROJECT_DOCUMENTATION | [OWASP Identify Application Entry Points](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/06-Identify_Application_Entry_Points) | Summary, objectives, requests, responses | Grounds the map in observable application exchanges | Version 4.2 is intentionally pinned; examples are general web testing guidance. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Steps 3–15 | Defines the role-specific experiment sequence | Course synthesis; no cited standard defines the exact fifteen-step sequence. |
| LAB_SPECIFIC | [AATE lab behavior](../../safety/index.md) | Synthetic challenge and traffic boundary | Supplies a safe worked scenario without executing it yet | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

```text
map -> legitimate baseline -> adversary baseline -> prediction
    -> one change/coherent set -> same action -> state/health proof
    -> residual anomalies -> limited claim -> remediation criteria -> same retest
```

| Variable class | Challenge-replay example |
|---|---|
| Changed | Session presenting the captured token |
| Fixed | Target, action, token, method, request body, app version, run window |
| Measured | Status, response session, request ID, server-side authorization result |
| Confounder | State reset failed or token changed between runs |

## Required external instruction

### NIST attack, analysis, and reporting assignment

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)  
**Exact section, chapter, or unit:** §5.2.1 Penetration Testing Phases and §§8.1-8.3  
**Estimated time:** 30 minutes  
**What to focus on:** how attack validation feeds discovery and how analysis, reporting, mitigation, and resolution constrain the final claim  
**What to skip:** technique sections outside the assigned penetration-test and post-testing areas  
**Expected takeaway:** connect one validated action to evidence, impact, mitigation criteria, and follow-up rather than stopping at a success status.

### OWASP entry-point mapping assignment

**Direct link:** [OWASP WSTG-INFO-06 v4.2](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/06-Identify_Application_Entry_Points)  
**Exact section, chapter, or unit:** Summary; Test Objectives; How to Test; Requests; Responses  
**Estimated time:** 20 minutes  
**What to focus on:** methods, targets, parameters, headers, cookies, redirects, response status, response content, and where state enters the workflow  
**What to skip:** sections after Responses and any active technique outside the synthetic plan  
**Expected takeaway:** produce the concrete request/response map needed to hold the workflow fixed during a controlled attack experiment.

## Course bridge

OWASP directs the tester to capture requests, responses, headers, parameters,
methods, and application behavior before deeper testing.[^owasp-entry] NIST's
Attack and Reporting phases make validation and analysis part of the same
assessment lifecycle.[^nist-analysis]

[^owasp-entry]: OWASP WSTG v4.2, WSTG-INFO-06, “How to Test,” “Requests,” and “Responses.”
[^nist-analysis]: NIST SP 800-115, §5.2.1 and §§8.1–8.3.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** An AATE hypothesis predicts three linked observations:
    what the control will do, whether the same protected action will succeed,
    and what residual evidence will remain. A changed property without that
    prediction is mutation, not an experiment.

Use one changed variable when it represents one independent claim. Use a
**deliberately coherent signal set** when a single environment claim necessarily
spans related values. For example, changing claimed platform while deliberately
holding locale, timezone, screen, and graphics values inconsistent is a useful
one-variable experiment; it is not a coherent browser identity.

## Worked example

### Claim under test

The local challenge token may not be bound to the session that solved it.

| Step | Planned evidence |
|---|---|
| Legitimate baseline | Solver session completes challenge and intended report once |
| Blocked baseline | Second session without token receives `403` |
| Hypothesis | If the token is bearer-only, presenting solver token from second session returns `200` |
| Changed variable | Requesting session ID |
| Fixed variables | Same token, route, method, work value, app version, reset state |
| Protected-action proof | Response says authorized and names the second session |
| Residual anomalies | Token value, expiry, action binding, one-time use, server telemetry |
| Alternative explanation | Application reset or shared global state intentionally makes every token valid |
| Remediation | Random token bound to session, action, nonce, expiry, and single use |
| Retest | Repeat the same second-session replay; require `403` while intended use remains `200` |

The hypothesis can fail: the second session may remain blocked. That is useful
evidence if the baseline, token, state, and request are correct.

## Optional exercise

### Objective

Write the complete experiment before touching the challenge endpoint.

### Setup

Use the synthetic engagement boundary and challenge scenario above in a
temporary experiment plan. Docker is not required.

### Exact actions or commands

Fill these fields in order:

1. authorization boundary and abort condition;
2. adversary objective and protected action;
3. request/control/state map using only documented lab behavior;
4. legitimate and blocked baselines;
5. falsifiable hypothesis;
6. changed and fixed variables;
7. five evidence fields and expected values;
8. at least two alternative explanations;
9. impact and claim limitation;
10. remediation success criteria and identical retest.

Mark every mapped fact `documented`, `observed`, or `inferred`. At this stage,
lab source and tests support documented facts; no live observation has occurred.

### Expected output

The plan must make the result decidable before execution. It should state that a
second-session `200` plus a response naming that session supports the replay
hypothesis, while `403` under a valid fixed token refutes it. It should not state
that success proves a weakness in another system.

### Interpretation

If you cannot say which result refutes the hypothesis, the claim is not
falsifiable. If more than one uncontrolled property changes, split the run or
name the change as one coherent set and explain why its members belong together.

### Common failure modes

- Writing the conclusion before the test
- Omitting the blocked baseline
- Letting state, version, or request body drift between conditions
- Treating a response code without response/session state as complete proof
- Recommending “add more signals” without measurable hostile and benign outcomes

### Cleanup

No live service was started. Preserve the plan for the later challenge lab. If
it contains organization-specific details, keep that copy outside the public
repository and retain only the synthetic version here.

## Why this matters offensively

Evasion work invites uncontrolled tweaking. A predeclared hypothesis and fixed
evidence schema prevent the operator from selecting only successful mutations or
confusing correlation with causation. The same structure makes remediation
measurable and the retest defensible.

## Check your understanding

1. The challenge-token hypothesis predicts that Session B will receive `200` when presenting Session A's token. Which result would refute the hypothesis under the fixed conditions?
2. After changing only the requesting session, why must the operator repeat the same protected endpoint, method, token, and body used in the baseline?
3. A browser treatment changes locale, timezone, and language together to express one declared regional profile. When can those three properties count as one coherent treatment?
4. The replay returns `200`, but the application may have shared global state after an incomplete reset. Is the shared-state possibility a residual anomaly or an alternative explanation?
5. After token-binding remediation, which parts of the original Session B replay must remain unchanged for the retest to be comparable?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A `403` for Session B's replayed protected request would refute the prediction, provided the token, route, state reset, and other fixed variables were correct.** A refutable outcome is what makes the hypothesis falsifiable.

- **2. Keeping the protected action and other inputs fixed isolates the requesting session as the meaningful change.** If the route, body, or objective also changes, a different workflow could explain the outcome.

- **3. The properties count as one treatment when they jointly express the predeclared regional claim and all unrelated target, workflow, state, and version variables stay fixed.** The set must not expand after seeing the result.

- **4. Shared global state is an alternative explanation because it offers a competing cause for the `200` result.** A residual anomaly is an observation that still looks inconsistent after the main result, such as an unchanged worker value.

- **5. Repeat the same objective, Session B blocked baseline, captured-token procedure, endpoint, method, body, fixed state, and evidence fields.** The corrected result should reject Session B while preserving the intended Session A action.

</details>

## Continue

- Continue through the appendix by reviewing its [methodology
  references](index.md#methodology-references) when you want more methodology depth.
- Return to [HTTP request and response](../01-http-edge/01-http-request-response.md)
  to begin the core technical path.
