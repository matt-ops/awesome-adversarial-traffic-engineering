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

## Check your understanding

1. A static rule flags code that reads `identity` from a request body. What additional target-specific evidence is required before the risk category becomes a finding?
2. For the reservation path, which subject, object, action, and policy facts should the code review trace through the authorization decision?
3. Why does a verified inventory change provide stronger evidence than a changed status or detector label during the reviewed attack path?
4. Which negative former-attack case and positive legitimate case should the remediation regression test include?
5. Why should the reviewer inspect alternate routes to the same inventory effect after finding one weak reservation path?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A finding needs reachable code, a reproducible scoped input, the resulting protected effect, impact, and limitations.** A pattern match only shows that code resembles a risk category.

- **2. Trace the authenticated caller as subject, the product or inventory record as object, reservation as action, and the server's permission and workflow state as policy context.** Client claims must not replace those facts.

- **3. Inventory change proves the adversary reached the protected business effect the control should prevent.** A status or label can change without committing state and may come from another layer.

- **4. The former unauthenticated or cross-identity reservation must fail without inventory change, while an authenticated authorized reservation must still succeed.** Both cases turn the security rule into a measurable acceptance test.

- **5. Another route may reach the same protected effect without the reviewed check or may enforce the rule elsewhere.** Alternate-path review prevents a narrow patch from leaving an equivalent bypass.

</details>

## Next lesson

Continue to [Module 10: Finding and evidence](../10-findings-interview/01-finding-and-evidence.md).
