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
2. Execute `npm run playwright:workflow-authorization`.
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
names the generated JSON output. The output includes objective, action, false
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

## Check your understanding

1. The reserve request names `identity` in its JSON body and no login occurs. Which server-side authorization rule is missing from the worked example?
2. The reservation response is `200`, and a later product query shows inventory changed from 5 to 4. Why is the final inventory query stronger proof than the status alone?
3. The Playwright Page listeners show the in-page reserve fetch but omit the baseline and final `page.request` calls. Why are those APIRequestContext calls absent?
4. Would changing the workflow from headless to headed browser mode repair the missing authenticated-session-to-identity binding?
5. What negative and positive cases should a regression test use to verify the reservation authorization fix?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The server must derive the caller's identity from a validated authenticated session and authorize that caller for the product and action.** Trusting the JSON identity lets an unauthenticated client choose who appears to reserve stock.

- **2. The final query independently verifies that authoritative inventory changed, which is the protected business effect.** A `200` response by itself could be misleading or disconnected from a committed reservation.

- **3. `page.request` uses APIRequestContext rather than the Page's browser network stack.** Page request and response listeners therefore do not observe those baseline and final API calls.

- **4. No.** Rendering mode changes browser presentation, not the server's authorization decision. The server must add the missing session-to-identity binding regardless of whether the client runs headed or headless.

- **5. Unauthenticated requests and requests naming another identity must fail without changing inventory, while a properly authenticated and authorized caller must still reserve the intended product.** Both cases test security and legitimate behavior.

</details>

## Next lesson

[Race and resource limits](05-race-and-resource-limits.md) tests how individually
valid workflow steps violate an invariant when ordering or atomicity fails.
