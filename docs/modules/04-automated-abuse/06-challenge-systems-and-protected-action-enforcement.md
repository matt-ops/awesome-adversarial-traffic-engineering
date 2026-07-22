# Challenge Systems and Protected-Action Enforcement

<!-- source-ids: owasp-automated-threats, rfc-9576, w3c-captcha-accessibility, cloudflare-turnstile-validation, usenix-modern-captchas, playwright-network, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 04 - Automated abuse and workflow attacks
- Lesson: 4 of 6
- Depth: Applied
- Estimated time: 4 hours
- Prerequisites:
  - [Authentication and rate controls](03-auth-and-rate-controls.md)
  - [Network events and evidence](../03-playwright/04-network-events.md)
- Next lesson: Inventory and promotion abuse

## Role outcome

Map a challenge from trigger through protected-action enforcement, test distinct
bypass hypotheses in the local fixture, measure adversary and customer impact,
define remediation, and specify an exact negative and legitimate-positive retest.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [OWASP Automated Threats](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-009_CAPTCHA_Defeat.html) | OAT-009 Summary, Description, Examples, Symptoms, and Countermeasures | Names CAPTCHA defeat as one automated-threat event and distinguishes ways a challenge can fail | Taxonomy and guidance, not proof that a specific control is bypassable. |
| STANDARD | [RFC 9576](https://www.rfc-editor.org/rfc/rfc9576.html) | Sections 1-3, 6, and 7 | Supplies a concrete challenge, issuance, presentation, and redemption architecture with origin/privacy considerations | Privacy Pass is one token architecture, not a universal challenge implementation. |
| OFFICIAL_DOCUMENTATION | [W3C CAPTCHA accessibility note](https://www.w3.org/TR/turingtest/) | Sections 2-4 and Status | Supports accessibility, privacy, proof-of-work, heuristic, and alternative-challenge analysis | Draft Note rather than a normative standard; it does not measure this fixture. |
| OFFICIAL_DOCUMENTATION | [Cloudflare token validation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/) | Mandatory server-side validation; token characteristics; response fields | Shows deployed expiry, single-use, hostname, action, and server-verification concerns | Vendor-specific semantics; the lab neither contacts nor imitates this service. |
| PEER_REVIEWED_RESEARCH | [Searles et al., USENIX Security 2023](https://www.usenix.org/conference/usenixsecurity23/presentation/searles) | Sections 3-6 and 8 | Supports measuring solve time, perception, task context, and abandonment | Particular participants, sites, and challenge types; not universal economics. |
| OFFICIAL_DOCUMENTATION | [Playwright Network](https://playwright.dev/docs/network) | Network events and request/response inspection | Supports browser-level document, script, API, and callback tracing | API details depend on the pinned Playwright/browser version. |
| LAB_SPECIFIC | [Challenge-systems lab](../../labs/applied/challenge-systems.md) | Both local commands and expected responses | Supplies deterministic weak-token and browser-trace evidence | Deliberately weak, provider-neutral fixture; not a commercial system. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Blocked baseline through exact retest | Connects challenge observations to protected-action success, remediation, and retest | No cited source defines this course's exact fifteen-step sequence. |

## Mental model

CAPTCHA is one challenge type. A control can instead require JavaScript
execution, proof of work, browser state, device attestation, a queue or managed
interstitial, or step-up verification. Whatever its interface, trace every
transition separately:

```text
request or workflow
  -> risk decision
  -> challenge issued
  -> challenge delivered
  -> proof produced
  -> proof verified
  -> protected action allowed or denied
  -> proof expires, is reused, or is transferred
```

The last server-side action is the offensive criterion. Seeing a challenge,
changing a risk score, receiving a proof token, or reaching a callback is only
intermediate evidence.

### Binding and enforcement questions

| Transition or object | Question to answer | Weak-fixture observation |
|---|---|---|
| Risk decision | Which population and reason trigger challenge? | No risk engine; absence of an accepted token is the implicit decision. |
| Challenge delivery | Document, iframe, script, interstitial, queue, or step-up? | Same-document provider-neutral form; no visual widget or iframe. |
| Proof production | Which request and browser callback produce proof? | `POST /api/challenge` after form submission. |
| Proof binding | Session, action, origin, nonce, expiry, and one-use? | All six are absent. |
| Verification | Which server component validates proof? | `GET /api/reports/protected` checks set membership. |
| Protected action | What state or response proves success? | HTTP `200`, report fields, and returned Session B identifier. |
| Reuse or transfer | What happens on another context or use? | Cross-session first use and identical second use both return `200`. |

## Required external instruction

### OWASP challenge-defeat assignment

**Direct link:** [OWASP OAT-009 CAPTCHA Defeat](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-009_CAPTCHA_Defeat.html)

**Exact section, chapter, or unit:** Summary Defining Characteristics, Description, Other Names and Examples, Symptoms, and Countermeasures

**Estimated time:** 25 minutes

**What to focus on:** separate challenge solving, implementation failure, alternate workflow, and human relay as different threat hypotheses

**What to skip:** active work against any site and solver implementation

**Expected takeaway:** explain why “CAPTCHA bypass” is not one universal technique and why protected-action evidence is still required.

### Privacy Pass lifecycle assignment

**Direct link:** [RFC 9576](https://www.rfc-editor.org/rfc/rfc9576.html)

**Exact section, chapter, or unit:** Sections 1 Introduction, 2 Terminology, 3 Architecture Overview, 6 Security Considerations, and 7 Privacy Considerations

**Estimated time:** 35 minutes

**What to focus on:** challenge, issuance, presentation/redemption, origin context, replay/linkability considerations, and deployment choices

**What to skip:** cryptographic construction details not needed to map the HTTP lifecycle

**Expected takeaway:** identify which party produces and verifies a proof and which application-specific bindings remain outside the generic architecture.

### Accessibility and customer-impact assignment

**Direct link:** [W3C Inaccessibility of CAPTCHA](https://www.w3.org/TR/turingtest/)

**Exact section, chapter, or unit:** Sections 2 Current Landscape, 3 Accessibility Challenges, 4 Alternatives, and Status of This Document

**Estimated time:** 35 minutes

**What to focus on:** visual/audio barriers, cognitive and language effects, privacy implications, proof of work, heuristics, and alternatives

**What to skip:** treating the draft note as a normative conformance standard or a quantitative production benchmark

**Expected takeaway:** include accessibility, privacy-tool, and legitimate-automation impact in control success criteria rather than treating them as side effects.

### Empirical metrics assignment

**Direct link:** [USENIX Security 2023 paper](https://www.usenix.org/conference/usenixsecurity23/presentation/searles)

**Exact section, chapter, or unit:** Sections 3 CAPTCHA Deployment Study, 4 User Study, 5 Results, 6 Task Abandonment, and 8 Limitations

**Estimated time:** 40 minutes

**What to focus on:** solve time, task context, user perception, abandonment, confounders, and study limits

**What to skip:** copying point estimates into a production forecast without matching the study population and design

**Expected takeaway:** design a measurement plan that joins security outcomes with friction and abandonment instead of reporting challenge rate alone.

## Course bridge

Start from the protected action and work backward. Record the challenged and
unchallenged populations, observed trigger reasons, proof path, storage, binding,
verification point, and final action. Then form one falsifiable hypothesis for
one failure mode.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Treat risk decision, challenge completion, proof
    validation, and protected-action enforcement as separate transitions. A
    challenge decision is an observation; a protected server-side result is the
    success criterion.

!!! warning "Local-only safety boundary"
    Execute only against `http://localhost:8080`. The course never requests
    external provider keys, paid solver APIs, public-target automation, or a
    real third-party challenge.

### Nine separate offensive hypotheses

Do not collapse this surface into one “bypass.” Predeclare the expected evidence
and refuting result for each applicable case:

1. **Challenge-trigger avoidance:** hold the protected workflow fixed and test
   whether one population or path avoids issuance.
2. **Authorized synthetic completion:** use browser automation to complete only
   the course-owned synthetic challenge and trace the callback.
3. **Cross-session replay:** produce proof in Session A and present it in Session B.
4. **Cross-action replay:** present proof to a distinct protected action only
   when an assigned fixture exposes one.
5. **Missing binding:** test session, action, origin, nonce, expiry, and one-use
   independently where the fixture supports the dimension.
6. **Alternate enforcement path:** repeat the same objective through an endpoint
   or workflow that might omit verification.
7. **Refresh, retry, and identity rotation:** compare challenge and action results
   under one declared refresh, retry, or synthetic identity change at a time.
8. **Missing protected-action enforcement:** submit the final request directly
   without trusting the client-side widget or callback.
9. **Abuse displacement:** measure whether denied attempts move to another
   workflow instead of disappearing.

The bundled weak fixture executes authorized completion, cross-session replay,
missing binding, direct server enforcement, and repeat use. It does not expose a
second challenge-gated action, controllable expiry clock, risk-score engine, or
identity-rotation model. Those are planned future experiments, not claimed results.

### Remediation invariant

Use an unpredictable proof produced after the intended challenge, bind it to the
server-recognized session or subject, exact action and relevant parameters,
expected origin, unique nonce, short expiry, and atomic one-use consumption.
Verify it at every server-side path that performs the protected action. Define
safe retry behavior, minimize collection, and provide an accessible legitimate
path that receives equivalent security review.

Vendor documentation can demonstrate one deployed pattern: server-side
verification plus expiry, single use, and returned hostname/action checks. It
does not prove those semantics exist in another provider or local integration.

### Metrics and customer impact

Calculate these from the same observation window and denominator:

| Metric | Deterministic definition in this lesson |
|---|---|
| Challenge issuance rate | challenges issued / workflow attempts |
| Solve or bypass rate | solves plus bypasses / workflow attempts |
| Protected-action completion | completed protected actions / workflow attempts |
| Challenge abandonment | abandoned challenged attempts / workflow attempts |
| Added latency | total challenge-added milliseconds / workflow attempts |
| Repeated challenge rate | repeated challenges / challenges issued |
| Attacker time or cost | attacker seconds or dollars / successful protected actions |
| Legitimate false positive | challenged legitimate near-neighbor attempts / attempts |
| Accessibility/privacy/automation impact | near-neighbor minus manual completion, abandonment, issuance, and latency |
| Stopped or displaced | direct and alternate-workflow attacker successes reported separately |

The local dataset compares `manual-legitimate-user`,
`legitimate-automation-or-accessibility-like-client`,
`stock-automated-attacker`, and `adapted-or-replaying-attacker`. The second row
is deliberately a composite test proxy. It is not evidence about real disabled
people, privacy-tool users, or production test automation.

### Advanced work stays optional

Visual CAPTCHA model training, audio solver development, commercial solver
integration, vendor-specific reverse engineering, and testing a real third-party
challenge remain elective or Deep extensions. They are not required by this
lesson or any checkpoint, and they do not support a universal-bypass claim.

## Worked example

The local challenge accepts the fixed synthetic answer `AATE`, returns one
deterministic bearer token, and adds that token to a server set. The protected
route asks only whether the header value is present in the set. It does not
compare the requesting session, action, origin, nonce, time, or prior use.

```text
Session B GET protected without proof -> 403
Session A POST fixed answer           -> 200 + proof
Session B GET protected with proof    -> 200 + returned session-b
Session B repeats identical GET       -> 200 + returned session-b
```

This result proves the local protected action accepted transferred, reused proof.
It does not prove that a commercial challenge, another application, or another
token format has the same weakness.

## Guided exercise

### Objective

Trace the complete weak-control lifecycle in HTTP and a browser, prove
cross-session and repeat-use acceptance, calculate security and customer-impact
metrics, and define remediation plus exact retests.

### Setup

Start the bundled Compose lab, verify `/health`, and reset state. Keep the target,
Session A/Session B names, protected route, `work=10`, answer, request order, and
evidence fields fixed. No external challenge service is contacted.

### Exact actions or commands

1. Run `python -m lab.run bypass`.
2. Confirm Session B's no-token baseline is `403` and record its response.
3. Confirm Session A's challenge response contains the token and Session A.
4. Confirm Session B presents that token and receives `200` with returned
   `session-b`; confirm the identical second request also receives `200`.
5. Run `npm run playwright:challenge-flow` and inspect its document, external
   local script, API request/response, storage-key, callback, proof, verification,
   and protected-action trace.
6. Confirm the browser trace honestly reports no visual widget, iframe, cookies,
   external request, cross-action case, or controllable expiry case.
7. Run `python -m lab.analysis.challenge_metrics` and compare all four populations.
8. State the absent session, action, origin, nonce, expiry, and one-use bindings.
9. Define the remediation invariant and the exact negative and legitimate-positive retest.

### Expected output

The HTTP runner prints `403, 200, 200, 200` across blocked baseline, solve,
cross-session first use, and identical second use. The browser trace includes the
challenge document and script, empty cookie/local-storage names, a session-storage
proof key, form callback, `POST /api/challenge`, two accepted protected requests,
and returned `session-b`. Metrics show the stock attacker mostly stopped, the
adapted attacker succeeding and displacing abuse, and the legitimate near-neighbor
paying greater challenge, abandonment, latency, and false-positive costs.

### Interpretation

The defense technically challenges traffic but fails operationally in the
synthetic comparison: cheap replay restores attacker completion, legitimate
near-neighbor completion falls, abandonment rises, and some abuse moves to an
alternate workflow. The exact local cause is weak proof binding and reuse plus
the dataset's declared displacement. Accessibility and privacy-tool effects remain
synthetic test proxies, not measured claims about real populations.

### Common failure modes

- Reporting token issuance or a changed decision without the protected response
- Describing all nine hypotheses as one universal CAPTCHA bypass
- Claiming an iframe, visual widget, expiry, or cross-action result the fixture lacks
- Dividing metrics by inconsistent denominators or hiding alternate-workflow success
- Treating the composite near-neighbor row as research about real accessibility populations

### Cleanup

Call `POST /api/reset`, close the browser runner, and stop the course Compose
stack. The generated trace is ignored by Git; no learner artifact is mandatory.

## Why this matters offensively

Challenge systems sit directly on valuable workflows, but their visible friction
can distract from the server invariant. A defensible red-team result proves the
protected effect, identifies one failed binding or enforcement transition, and
shows whether remediation stops abuse without transferring unacceptable cost to
legitimate people and automation.

## Check your understanding

1. Session A produces the local proof and Session B completes the protected report twice; which six proof properties are absent?
2. Why is a challenge decision or successful callback insufficient evidence of offensive success?
3. Which browser observations must the local Playwright trace record, and which visual elements must the trace explicitly report as absent?
4. The synthetic stock attacker completes 5% of protected actions while the adapted attacker completes 70% and succeeds 20% through another workflow; what operational conclusion follows?
5. What exact negative and legitimate-positive results should a remediation retest require?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Session, action, origin, nonce, expiry, and one-use properties are absent.** The fixed token is accepted as transferable bearer proof, is not scoped to a protected operation, has no freshness or origin context, and remains in the accepted set after use.

- **2. Those events are intermediate control observations rather than the protected effect.** Offensive success requires the protected server-side action to accept the treatment and return or mutate the expected authoritative result; otherwise the control may still enforce the workflow later.

- **3. Record the challenge-triggering request, document, local script, network events, cookie and browser-storage names, proof production, form callback, server verification point, and final protected response.** Report honestly that the fixture contains no visual widget, iframe, cookies, or external provider request.

- **4. The challenge suppresses the stock client but does not stop the adapted population, and some abuse is displaced to another workflow.** Security reporting must include the high adapted completion and alternate-workflow rate rather than presenting the stock result as overall prevention.

- **5. Session B must receive `403` when presenting Session A's proof on both first and repeated attempts, while Session A must complete the intended protected action exactly once before expiry.** Repeat the same endpoint, parameters, reset state, identities, request order, and evidence fields.

</details>

## Next lesson

[Inventory and promotion abuse](04-inventory-and-promotion-abuse.md) applies the
same protected-action discipline to business-state transitions.
