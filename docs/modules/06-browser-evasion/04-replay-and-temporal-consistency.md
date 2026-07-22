# Replay and temporal consistency

<!-- source-ids: fpscanner-project, fp-inconsistent, owasp-automated-threats, rfc-9576, cloudflare-turnstile-validation, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 06 - Browser-control evasion
- Lesson: 4 of 5
- Depth: Integrated
- Estimated time: 3 hours
- Prerequisites:
  - [Identity coherence](03-identity-coherence.md)
  - [Challenge systems and protected-action enforcement](../04-automated-abuse/06-challenge-systems-and-protected-action-enforcement.md)
- Next lesson: Version drift

## Role outcome

Test sensor and challenge-proof replay separately, connect proof binding to the
protected enforcement point, and identify temporal changes that invalidate an
otherwise coherent snapshot.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Anti-replay discussion, payload flow, limits, and non-goals | Provides sensor freshness concepts | Observations are valid only for recorded code and browser versions. |
| PREPRINT_RESEARCH | [FP-Inconsistent](https://arxiv.org/abs/2406.07647) | Sections 6-7 and 8.4 Limitations | Supports cross-time comparison and limits | Specific dataset, honey-site, bot population, and services; not universal proof. |
| PROJECT_DOCUMENTATION | [OWASP OAT-009](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-009_CAPTCHA_Defeat.html) | Description, Symptoms, and Countermeasures | Distinguishes challenge solving and workflow/enforcement failures | Taxonomy and guidance; not evidence that every challenge accepts replay. |
| STANDARD | [RFC 9576](https://www.rfc-editor.org/rfc/rfc9576.html) | Sections 3, 6, and 7 | Supplies challenge, issuance, redemption context, and replay/privacy considerations | Privacy Pass is one architecture, not a universal challenge-token design. |
| OFFICIAL_DOCUMENTATION | [Cloudflare token validation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/) | Mandatory server validation, token characteristics, and response fields | Provides a deployed example of expiry, single use, hostname, and action validation | Vendor-specific behavior; this lesson neither contacts nor imitates the service. |
| LAB_SPECIFIC | [Challenge-systems lab](../../labs/applied/challenge-systems.md) | HTTP and browser replay commands | Supplies deterministic proof and protected-action outcomes | Deliberately weak provider-neutral fixture; results do not generalize. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Repeat action, alternatives, remediation, and retest | Separates replay layers and exact retest | No cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
challenge trigger
  -> challenge proof
  -> proof binding
  -> protected-action enforcement
  -> replay and exact retest
```

| Replayed object | Binding expected | Local result | Meaning |
|---|---|---|---|
| Evaluation nonce/payload | uniqueness | repeated nonce `409` | sensor submission reuse rejected |
| Control action token | single use | second action `403` | issued authorization consumed |
| Challenge token | session/action/origin/nonce/expiry/use | cross-session and second-use `200` | intentionally weak bearer proof |
| Fingerprint snapshot | time/environment | offline comparison | similarity is not authorization |

| Challenge-proof comparison | Local executable support | Required observation |
|---|---|---|
| First use | Yes | Session B presents Session A proof; protected response is `200` with `session-b`. |
| Second use | Yes | Session B repeats the identical request; response remains `200`. |
| Cross-session use | Yes | Issuing session is `session-a`; protected server result returns `session-b`. |
| Cross-action use | No | Planned future experiment requiring a second distinct challenge-gated action. |
| Expired use | No | Planned future experiment requiring expiry metadata and a controllable clock. |
| Intended legitimate use after remediation | No remediated fixture | Exact future positive retest: Session A succeeds once before expiry. |

## Required external instruction

### FPScanner anti-replay assignment

**Direct link:** [FPScanner](https://github.com/antoinevastel/fpscanner)  
**Exact section, chapter, or unit:** anti-replay discussion, payload collection flow, limits, and non-goals  
**Estimated time:** 25 minutes  
**What to focus on:** payload freshness, nonce purpose, collection location, and the downstream action not covered by a sensor nonce  
**What to skip:** external replay attempts and unrelated implementation details  
**Expected takeaway:** explain which payload replay a nonce can reject and why an action token still needs independent binding.

### FP-Inconsistent temporal assignment

**Direct link:** [FP-Inconsistent](https://arxiv.org/abs/2406.07647)  
**Exact section, chapter, or unit:** temporal-inconsistency analysis in Sections 6-7 and 8.4 Limitations

**Estimated time:** 35 minutes  
**What to focus on:** longitudinal change, observation windows, population/dataset limits, and alternative causes of temporal inconsistency  
**What to skip:** claims beyond the paper's threat model and collection method  
**Expected takeaway:** separate one captured snapshot, replay resistance, and longitudinal identity consistency into different hypotheses.

### Privacy Pass redemption-context assignment

**Direct link:** [RFC 9576](https://www.rfc-editor.org/rfc/rfc9576.html)

**Exact section, chapter, or unit:** Sections 3 Architecture Overview, 6 Security Considerations, and 7 Privacy Considerations

**Estimated time:** 30 minutes

**What to focus on:** challenge inputs, issuance, token presentation/redemption, origin context, replay considerations, and application choices

**What to skip:** assuming Privacy Pass properties apply to every CAPTCHA or challenge

**Expected takeaway:** name the exact redemption context a proof should authorize and the privacy tradeoff introduced by stronger binding.

### Deployed token-validation assignment

**Direct link:** [Cloudflare server-side validation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/)

**Exact section, chapter, or unit:** Mandatory server-side validation, Siteverify overview, Token characteristics, and hostname/action validation

**Estimated time:** 20 minutes

**What to focus on:** server verification, expiry, single use, action, hostname, and safe retry/idempotency concerns

**What to skip:** keys, API calls, widget integration, or treating vendor semantics as universal

**Expected takeaway:** define negative replay and legitimate-positive use tests without contacting the vendor.

## Course bridge

Freshness proves only that an identifier was not accepted before under the
server's model. Binding determines whether the accepted result belongs to a
session, action, origin, nonce, validity window, and use. Temporal consistency
compares environment claims across time; legitimate updates and mobility also
change them. Challenge issuance is an observation; the protected result remains
the offensive criterion.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Test sensor replay, challenge-proof replay, issued
    authorization replay, and the protected action as separate transitions.
    Never infer all four from one nonce or challenge decision.

## Worked example

The control lab rejects reuse of its one-variable action token. The challenge
lab accepts Session A's proof twice in Session B. These opposite results teach
that “anti-replay” is not one property: inspect trigger, proof, binding,
enforcement, and the exact protected action. Cross-action, expiry, and
post-remediation cases remain explicitly planned because the fixture cannot
execute them.

## Guided exercise

### Objective

Compare two local replay designs, trace first/second/cross-session proof use,
and build exact supported and planned temporal tests.

### Setup

Use existing control-recon evidence. With the local API healthy, the HTTP and
browser challenge runners are fixed and bounded.

### Exact actions or commands

1. Verify the control output's first action `200` and second action `403`.
2. Execute `python -m lab.run bypass` and preserve the `403` baseline, Session A
   token response, Session B first-use `200`, identical second-use `200`, and returned session.
3. Execute `npm run playwright:challenge-flow` and connect challenge trigger,
   proof production, browser storage, absent bindings, protected enforcement,
   cross-session replay, and exact repeat.
4. Map nonce and token binding dimensions for both local designs.
5. Mark cross-action and expired use as planned future experiments; do not report results.
6. Define two observation times with browser/framework versions fixed or recorded.
7. List legitimate temporal changes and define remediation, Session B negative
   retest, and Session A one-use legitimate-positive retest.

### Expected output

The control token is single-use; the challenge token replays across sessions and
on an identical second request. The trace reports unsupported cross-action,
expiry, and remediated-positive cases as future work and separates environment
drift from replay acceptance.

### Interpretation

A strong sensor nonce cannot repair downstream authorization that lacks
session/action/origin/nonce/expiry/use binding. Conversely, replay rejection
does not prove identity, and challenge issuance does not prove protected
enforcement. Conclusions stay scoped to each object and local action.

### Common failure modes

- Calling every token the same control
- Omitting the original blocked request or returned server session
- Treating a changed browser version as adversarial temporal inconsistency
- Claiming single-use prevents proof theft
- Reporting cross-action or expiry results the fixture cannot execute

### Cleanup

Reset the API. Store only synthetic local proof values; they have no external value.

## Why this matters offensively

Real adversaries reuse acquired capability. Red-team replay tests expose where
fresh collection is present but authorization or workflow binding remains weak,
while exact positive tests prevent remediation from breaking intended clients.

## Check your understanding

1. The local evaluation endpoint accepts a nonce once and returns `409` when the same nonce is evaluated again. What does the `409` establish about that nonce?
2. Why does the lesson test replay of the downstream action token separately from replay of the evaluation nonce?
3. In the challenge lab, Session B reuses Session A's token and completes the protected request twice. Which proof properties are intentionally missing?
4. A browser's timezone or network address changes between two observations. Can that temporal change have a legitimate explanation?
5. After challenge-token remediation, what must the retest repeat to show that cross-session replay is rejected while intended use still works?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The `409` establishes that the exact nonce was already consumed by an accepted evaluation in the local model.** It does not describe the later action token's rules, challenge proof, requesting session, protected endpoint, or another system.

- **2. Evaluation acceptance and protected-action authorization are separate transitions with separate objects.** A nonce can be single-use while a resulting token has weak binding, or the reverse, so both require independent protected-action evidence.

- **3. Session, action, origin, nonce, expiry, and one-use properties are intentionally absent from the synthetic challenge token.** Another session can transfer the bearer proof, reach the protected action, and repeat the identical request without consumption.

- **4. Yes. Updates, travel, mobile networks, privacy settings, accessibility tools, and hardware changes can alter observations over time.** Temporal differences require recorded context and alternatives before being treated as adversarial inconsistency.

- **5. Repeat Session B's blocked baseline, Session A's proof production, the same cross-session first and second presentations, protected response, and returned session evidence.** Require both Session B attempts to fail while Session A succeeds exactly once before expiry.

</details>

## Next lesson

[Version drift and residual anomalies](05-version-drift-and-residual-anomalies.md)
turns version metadata and unexplained evidence into a durable retest plan.
