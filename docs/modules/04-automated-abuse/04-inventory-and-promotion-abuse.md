# Inventory and promotion abuse

<!-- source-ids: portswigger-business-logic, owasp-automated-threats, playwright-network, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 04 - Automated abuse and workflow attacks
- Lesson: 4 of 5
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [Authentication and rate controls](03-auth-and-rate-controls.md)
  - Successful local API map and Playwright Foundation workflow
- Required artifact: `lab/telemetry/workflow-authorization.json`
- Next lesson: Race and resource limits

## Role outcome

Prove a missing workflow-authorization binding through inventory state and
explain why changing browser transport characteristics cannot repair it.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [PortSwigger business logic](https://portswigger.net/web-security/logic-flaws) | What/why/impact/examples; flawed assumptions about user behavior | Teaches intended-functionality and state-machine flaws | Complete only labs explicitly assigned by a lesson. |
| PROJECT_DOCUMENTATION | [OWASP OAT-005 and OAT-021](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-021_Denial_of_Inventory) | Assigned definition sections | Distinguishes acquisition from holding inventory | The project is a taxonomy and handbook, not an execution methodology. |
| OFFICIAL_DOCUMENTATION | [Playwright Network](https://playwright.dev/docs/network) | Network events | Supports browser-side request evidence | API behavior is version-sensitive; examples pin the repository version. |
| LAB_SPECIFIC | [Workflow-authorization lab](../../labs/applied/workflow-authorization.md) | Entire local exercise | Defines intentional missing binding and state proof | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Baseline through exact retest | Structures the finding | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
expected: authenticated session -> authorized identity -> reserve -> inventory state
actual:   caller JSON identity -----------------------> reserve -> inventory state

browser properties, head mode, and transport do not supply the missing
server-side authenticated-session-to-identity binding.
```

## Required external instruction

### PortSwigger business-logic assignment

**Direct link:** [Business logic vulnerabilities](https://portswigger.net/web-security/logic-flaws)  
**Exact section, chapter, or unit:** What are business logic vulnerabilities?; How do business logic vulnerabilities arise?; Impact; Examples; Making flawed assumptions about user behavior  
**Estimated time:** 50 minutes  
**What to focus on:** intended functionality, invalid state transitions, user-controlled values, and server enforcement  
**What to skip:** complete no labs from this broad topic unless another course lesson names one  
**Expected takeaway:** explain why a syntactically valid request can violate a business invariant and how the server must fix it.

## Course bridge

Business-logic weaknesses arise when an application accepts valid operations in
an invalid order or with unverified assumptions about caller behavior.[^ps-logic]
The local reservation endpoint accepts `identity` from JSON but never requires
the login token or binds it to that identity.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE requires both the unauthenticated request and an
    independent inventory-state query so a success-shaped response cannot be
    mistaken for the protected business effect.

[^ps-logic]: PortSwigger Web Security Academy, "Business logic vulnerabilities," assigned sections.

!!! info "Common misconception"
    This is not a browser-evasion finding. A raw HTTP client, headed browser, or
    headless browser can send the same accepted request. A bot detector might
    reduce reachability, but it cannot make missing application authorization
    correct.

## Worked example

| Proof stage | Evidence |
|---|---|
| Reset | application confirms synthetic reset |
| Initial state | `GET /api/products/demo-1` reports available `5` |
| Authentication | deliberately omitted; no login request/event |
| Protected action | `POST /api/cart/reserve` with caller identity returns `200` |
| Final state | product reports available `4` |
| Limitation | intentional local flaw; one unit; no external target |

## Guided exercise

### Objective

Execute the renamed workflow-authorization exercise and trace proof from request
to authoritative state.

### Setup

Read `lab/clients/playwright/workflow_authorization.ts`. It is fixed to
`localhost:8080`, reserves one unit, and uses a `finally` block for cleanup. Keep
the local API running and resettable.

### Exact actions or commands

1. Predict the initial/final inventory and browser-visible event set.
2. Execute `npm.cmd run playwright:workflow-authorization`.
3. Inspect `lab/telemetry/workflow-authorization.json`.
4. Verify `authenticationPerformed` is false, inventory changes 5 -> 4, and the
   protected action is named.
5. Compare the Page fetch events with `page.request` baseline/final checks and
   explain why only some appear in Page listeners.
6. Draft remediation: derive identity from an authenticated server session,
   authorize the product/action, make reservation atomic, and add a regression
   test rejecting caller identity.

### Expected output

The terminal confirms inventory changed from 5 to 4 without authentication and
names the JSON artifact. The artifact includes objective, action, false
authentication flag, before/reservation/after bodies, browser events, and limit.

### Interpretation

The server's final inventory is authoritative proof. Page network listeners
capture the in-page fetch; APIRequestContext calls are separate and preserved in
the structured before/after fields. Neither headless mode nor browser identity
caused the flaw.

### Common failure modes

- Calling this an anti-bot bypass
- Proving only a `200` without the inventory mutation
- Assuming Page listeners include every APIRequestContext call
- Recommending only a WAF/bot rule instead of server authorization
- Failing to reset and comparing contaminated inventory

### Cleanup

The script closes its Browser. Reset the API after preserving evidence. Stop the
Compose stack if pausing the path.

## Why this matters offensively

Red-team work attacks the full objective. Bypassing a traffic control is only
useful if the application action then succeeds; conversely, missing workflow
authorization remains exploitable regardless of browser sophistication.

## Required artifact

Keep `lab/telemetry/workflow-authorization.json` and write
`artifacts/module-04/workflow-finding-outline.md` with invariant, precondition,
attack path, state proof, impact, client independence, remediation, regression
test, and exact retest.

## Pass gate

1. What server invariant is missing?
2. Why is the final inventory query stronger than the `200` alone?
3. Why do Page listeners omit `page.request` traffic?
4. Would headed mode fix the authorization flaw?
5. What regression test directly validates remediation?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. The reservation identity must derive from and be authorized by an authenticated server-side session.
2. It independently proves the protected state changed rather than only receiving a success-shaped response.
3. APIRequestContext traffic is not initiated by the Page's browser network stack/listeners.
4. No; rendering mode does not add a missing server-side authorization binding.
5. An unauthenticated request and a request naming another identity must fail without changing inventory.

</details>

## Next lesson

[Race and resource limits](05-race-and-resource-limits.md) tests how individually
valid workflow steps violate an invariant when ordering or atomicity fails.
