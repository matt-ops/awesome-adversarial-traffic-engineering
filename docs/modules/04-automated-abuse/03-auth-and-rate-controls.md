# Authentication and rate controls

<!-- source-ids: portswigger-authentication-path, owasp-automated-threats, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 04 - Automated abuse and workflow attacks
- Lesson: 3 of 5
- Depth: Applied
- Estimated time: 4 hours
- Prerequisites:
  - [Workflow and API mapping](02-workflow-mapping.md)
  - Active local lab for local exercises
  - A free PortSwigger Web Security Academy account for the assigned provider lab
- Next lesson: Inventory and promotion abuse

## Role outcome

Execute authorized authentication and rate-key experiments, distinguish their
objectives, and prove whether the controlled action remains accepted.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [PortSwigger authentication path](https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities) | Authentication, password login, brute force, flawed protection, rate limiting, named lab | Provides an authorized realistic target and technique instruction | Use only provider-assigned targets and synthetic provider data. |
| PROJECT_DOCUMENTATION | [OWASP OAT-008](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-008_Credential_Stuffing) | Summary; Description; names/examples | Keeps known-pair testing distinct from guessing | The project is a taxonomy and handbook, not an execution methodology. |
| LAB_SPECIFIC | [Integrated local app](../../labs/applied/local-api.md) | Credential and rate-limit runners | Supplies bounded synthetic patterns | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Baseline, changed variable, proof, residual evidence | Structures comparable trials | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Experiment | Fixed | Changed | Protected action | Proof |
|---|---|---|---|---|
| Synthetic credential pattern | endpoint and five fixed pairs | username/pair pattern | login accepted | status plus attempt summary |
| Fixed-key rate baseline | route, work, three requests | none | report accepted | `200, 200, 429` |
| Rotated-key trial | route, work, three requests | caller `session_id` only | report accepted | `200, 200, 200` |
| Provider IP-block lab | provider target/account/instructions | provider-taught request source behavior | provider login | Academy lab completion and notes |

## Required external instruction

### PortSwigger authentication assignment

**Direct link:** [Authentication vulnerabilities learning path](https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities)  
**Exact section, chapter, or unit:** What is authentication?; Authentication versus authorization; Vulnerabilities in password-based login; Brute-force attacks; Flawed brute-force protection; User rate limiting; Lab: Broken brute-force protection, IP block  
**Estimated time:** 2 hours  
**What to focus on:** credential outcome versus authorization, how the provider's control keys attempts, the blocked baseline, changed request property, and successful login  
**What to skip:** all later authentication labs/topics not named above  
**Expected takeaway:** complete the assigned lab on its issued target and explain precisely which rate-control assumption was bypassed.

## Course bridge

Authentication establishes an identity claim; authorization decides whether
that identity may perform an action. Rate controls count actions within an
aggregation key and window. A key under adversary control can split one hostile
workflow across counters even when each individual counter behaves as designed.

PortSwigger's assigned lab provides the detailed, legal practice environment.
The local credential runner uses only five fixed synthetic attempts; it is for
pattern/evidence analysis, not acquiring credentials.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Treat the aggregation key as the changed variable and
    the accepted report or login as the protected action; absence of a rate
    response is not sufficient proof.

!!! warning "Safety boundary"
    Use only course synthetic accounts or the exact Academy lab host and
    credentials. Do not use real leaked pairs, public login endpoints, or an
    unassigned provider host.

## Worked example

```text
fixed synthetic identity:   200, 200, 429
rotated caller session_id:  200, 200, 200
fixed: route, work, count, timing order, application reset
changed: session_id value per request
conclusion: caller-controlled key partitions one workflow across counters
limitation: no network-source rotation and no production control
```

The protected action is an accepted expensive report, not merely avoidance of
`429`. Each `200` body contains the synthetic report result and session count.

## Guided exercise

### Objective

Preserve comparable local authentication/rate evidence and complete the one
provider-assigned control lab.

### Setup

Verify local health. Read the two runner functions so their five credential
attempts and six rate requests are known before execution.

### Exact actions or commands

1. Execute `python -m lab.run credential` once and preserve all five outcomes
   plus `/api/auth/attempts` summary.
2. Label three failures across users as spraying-shaped and the known-pair
   attempts as stuffing-shaped, without claiming account compromise beyond the
   synthetic accepted pair.
3. Execute `python -m lab.run ratelimit` once.
4. Record fixed versus changed variables and accepted report bodies/statuses.
5. Complete only the named PortSwigger lab and record its issued host, baseline,
   changed property, protected login result, and provider completion signal.

### Expected output

Local authentication reports five attempts, four failures, three users, and two
sessions. Local rate output is `[200, 200, 429]` for fixed and `[200, 200, 200]`
for rotated keys. The Academy marks its assigned lab solved when its procedure
completes on the issued target.

### Interpretation

The local rate result demonstrates a weak aggregation key, not IP rotation or
generic rate-limit defeat. The provider lab adds realistic instruction under the
provider's authorization and has its own exact assumptions.

### Common failure modes

- Calling every failed-login sequence credential stuffing
- Using real credential material
- Changing timing, route, work, and key simultaneously
- Treating absence of `429` as proof without the report body
- Applying provider-lab steps to any other host

### Cleanup

Reset the local lab with `curl.exe -X POST http://localhost:8080/api/reset` in
PowerShell or `curl -X POST http://localhost:8080/api/reset` in Bash or zsh.
Close the Academy lab according to its interface and retain no provider session
secrets in the repository.

## Why this matters offensively

Controls frequently bind decisions to a single identity dimension. Controlled
testing reveals whether one adversary workflow can escape that grouping while
preserving the same action and evidence.

## Check your understanding

1. The local login accepts a known synthetic credential pair, while the report endpoint decides whether that caller may run an expensive action. How do authentication and authorization differ in these two decisions?
2. The fixed-key rate trial returns `200, 200, 429`, while the rotated-key trial returns `200, 200, 200`. Which single request value changes in the rotated trial?
3. Why must the learner inspect each `200` response body instead of treating the rotated status sequence alone as proof of three accepted reports?
4. The credential exercise sends five predefined synthetic pairs and obtains no outside secrets. Why should the result not be described as credential theft?
5. Which provider controls confine the assigned PortSwigger authentication exercise legally and technically?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Authentication establishes which identity the server recognizes, while authorization decides whether that identity and state permit a particular action.** A valid login therefore does not automatically authorize every protected report or business operation.

- **2. Only the caller-supplied `session_id` aggregation value changes from request to request.** The route, work, request count, order, reset state, and protected report action remain fixed.

- **3. A `200` can be success-shaped without containing the expected protected result.** The response body and server summary confirm that each expensive report was actually accepted under the rotated keys.

- **4. The exercise starts with a small fixed set of course-owned synthetic values and reports controlled outcomes.** It neither acquires nor exfiltrates real credentials, so a credential-theft claim would misrepresent the activity.

- **5. The provider issues a specific lab host, scenario, account or data, and approved procedure, then supplies a completion signal.** Testing must stay inside that assigned environment rather than moving to arbitrary systems.

</details>

## Next lesson

[Inventory and promotion abuse](04-inventory-and-promotion-abuse.md) moves the
previous browser authorization exercise to its correct business-workflow home.
