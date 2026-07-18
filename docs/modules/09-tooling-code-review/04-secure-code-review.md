# Secure code review through an adversary's path

<!-- source-ids: owasp-code-review-guide, owasp-api-security-top-10, semgrep-public-rules, pytest-documentation, aate-local-lab -->

## Progress

- Module: 09 - Tooling and secure code review
- Lesson: 4 of 4
- Depth: Integrated
- Estimated time: 5 hours
- Prerequisites:
  - [Retries, timeouts, and jitter](03-retries-timeouts-and-jitter.md)
  - [Workflow and API mapping](../04-automated-abuse/02-workflow-mapping.md)
  - Read basic Python conditionals, collections, functions, and tests
- Required artifact: `artifacts/module-09/code-review.md`
- Next lesson: Finding and evidence

## Role outcome

Review a request path from attacker-controlled input to protected effect, form a
code-backed abuse hypothesis, and convert it into a bounded regression test.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/) | objectives, threat modeling, authentication, authorization, error handling/logging | Grounds the review workflow | Broad guide; lessons assign only sections relevant to the local review case. |
| PROJECT_DOCUMENTATION | [OWASP API Security Top 10](https://owasp.org/API-Security/) | API1, API2, API4, API6 | Supplies risk lenses, not proof | Risk taxonomy; it does not replace code-specific proof and tests. |
| PROJECT_DOCUMENTATION | [Semgrep Registry](https://semgrep.dev/explore) | one Python security rule example | Shows automation's limited role | Example automation only; never the primary teacher or proof of exploitability. |
| OFFICIAL_DOCUMENTATION | [pytest assertions](https://docs.pytest.org/en/stable/how-to/assert.html) | result assertions | Grounds regression proof | Only the features used by the code-review exercises are assigned. |
| LAB_SPECIFIC | [Code-review lab](../../labs/deep/code-review.md) | four deliberate local cases | Supplies exact targets and outputs | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

| Review step | Question | Evidence |
|---|---|---|
| Entry | What can the caller control? | route, body/query/header model |
| Transformation | Is input normalized, trusted, or used as a key? | assignments and helpers |
| Decision | What condition grants/denies? | branch and state lookup |
| Effect | What protected state/work changes? | mutation, response, dependency call |
| Alternate path | Can the same effect bypass the decision? | sibling routes and workflows |
| Proof | What smallest test demonstrates impact? | precondition, action, postcondition |
| Fix gate | What invariant should remediation enforce? | negative and positive tests |

A taxonomy tells you where to look. The code establishes a hypothesis. A test
that reaches a protected effect establishes local impact. A scanner match alone
does none of those things.

## Required external instruction

### Code-review method assignment

**Direct link:** [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)  
**Exact section, chapter, or unit:** Introduction/Objectives, Threat Modeling, Authentication, Authorization, and Error Handling and Logging  
**Estimated time:** 65 minutes  
**What to focus on:** trust boundaries, subject/object/action, protected effects, alternate paths, and log usefulness  
**What to skip:** full-language checklists, tool installation, and sections unrelated to the local Python cases  
**Expected takeaway:** follow one untrusted value through transformation and a security decision to a protected effect, then define exploit and remediation tests.

### API risk-lens assignment

**Direct link:** [OWASP API Security Top 10](https://owasp.org/API-Security/)  
**Exact section, chapter, or unit:** API1, API2, API4, and API6 pages  
**Estimated time:** 45 minutes  
**What to focus on:** object authorization, authentication, resource consumption, and sensitive business-flow effects  
**What to skip:** the other API categories and any attempt to treat category membership as proof  
**Expected takeaway:** use each category as a review prompt, then name the code and test evidence still required to establish a real local finding.

## Course bridge

The synthetic application contains deliberate flaws: reservation changes
inventory without authentication; challenge tokens are fixed and unbound;
caller-chosen session IDs partition a weak limit; a fail-once route exposes retry
behavior. Each case is local, deterministic, and covered by tests.

!!! note "Source-backed fact"
    OWASP categories organize risk. They do not prove that a particular code path
    is exploitable or determine its business impact.

## Worked example

`challenge()` returns a fixed token and stores only the token. `protected_report()`
checks membership in the token set but never checks the requesting session,
action, expiry, or use count. Hypothesis: a token issued to `solver-session` can
authorize `attacker-copy`. The existing test sends that alternate session and
expects `200`; the protected report response is stronger proof than a token-score change.

## Guided exercise

### Objective

Complete four code reviews and write one new failing remediation test design.

### Setup

Open `lab/app/main.py`, `lab/clients/safe_client.py`, `lab/tooling/client.py`,
and `lab/tests/test_app.py`. Use [the case guide](../../labs/deep/code-review.md).

### Exact actions or commands

1. Review reservation: trace `product_id`, `quantity`, inventory check, mutation,
   and missing subject/authorization decision.
2. Review challenge replay: trace answer, returned token, token store, session
   input, protected effect, and missing bindings.
3. Review rate-key rotation: trace caller-controlled `session_id` into the
   counter key and show how a new key resets the local limit.
4. Review retry handling: identify retryable statuses, maximum attempts, timeout,
   side-effect assumptions, and the test that rejects attempt four.
5. For each case, record entry, decision, effect, proof, limitation, remediation
   invariant, and exact negative/positive test.
6. Inspect one Semgrep Python rule; state what pattern it finds and what manual
   reasoning remains. Do not present the match as a finding.

### Expected output

Four review tables tied to exact functions and tests. Each contains a protected
effect and a remediation acceptance test; none relies only on a taxonomy label or tool match.

### Interpretation

The most important distinction is “weak-looking code” versus “demonstrated
protected effect.” Some missing checks are intentional product behavior; others
are controlled elsewhere. The reviewer must map the full path and test the hypothesis.

### Common failure modes

- Reporting a category without a code path
- Stopping at an HTTP status without checking state/effect
- Ignoring alternate routes or upstream controls
- Recommending a fix without a legitimate positive test
- Treating a static-analysis match as exploitability proof

### Cleanup

Reset local state. Keep line/function references rather than copying large code blocks.

## Why this matters offensively

Red-team engineers often build tooling and review controls. Code review reveals
where identity, authorization, resource, and retry assumptions can be challenged;
runtime proof shows whether the assumption reaches an attacker-relevant effect.

## Required artifact

`artifacts/module-09/code-review.md` containing four complete review tables, one
data-flow diagram, exact test designs, a scanner-limit note, and scope limitations.

## Pass gate

1. What is the difference between a risk category and a finding?
2. What three elements define an authorization decision?
3. Why is a protected effect stronger than a status change?
4. What must a remediation test include?
5. What can a static-analysis match establish?
6. Why review alternate paths?

## Answer key

<details><summary>Check your reasoning</summary>

1. A category guides inspection; a finding has target-specific evidence, impact, scope, and reproduction.
2. Subject, object, and action, plus the policy/context used to decide.
3. It proves the adversary achieved the action or service effect the control should prevent.
4. The former attack as a negative test and legitimate near-neighbor behavior as a positive test.
5. That code resembles the rule's pattern; not reachability, exploitability, or impact.
6. The same effect may be reachable without the reviewed decision or may be controlled elsewhere.

</details>

## Next lesson

Continue to [Module 10: Finding and evidence](../10-findings-interview/01-finding-and-evidence.md).
