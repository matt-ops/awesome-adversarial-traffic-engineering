# Edge and admission controls

<!-- source-ids: aws-waf-app-layer-ddos, aws-waf-rate-based-rules, aws-builders-library-load-shedding, aate-adversarial-control-loop -->

## Progress

- Module: 08 - DDoS and resilience
- Lesson: 3 of 5
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [Metrics](02-metrics.md)
  - Module 04 rate-key experiment
- Next lesson: Bounded load testing

## Role outcome

Map rate aggregation, window, scope, custom keys, endpoint cost, caching, and
load shedding into specific authorized bypass/pressure hypotheses.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [AWS WAF app-layer guidance](https://docs.aws.amazon.com/waf/latest/developerguide/ddos-app-layer-rbr.html) | Complete short page | Shows endpoint-specific application-layer rate protection | AWS-specific implementation guidance, not a universal control model. |
| OFFICIAL_DOCUMENTATION | [AWS WAF rate rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html) | aggregation; windows; scope-down; custom keys | Defines product-specific control semantics | Product-specific semantics; local labs model the assumptions rather than AWS itself. |
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | Complete article | Adds admission and graceful overload | Practitioner guidance from one large provider; adapt mechanisms to the target architecture. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | control hypothesis/action/retest | Structures offensive testing | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Control | Assumption to test | Local scenario |
|---|---|---|
| per-key rate | key groups one workflow | identity-key |
| endpoint scope | expensive paths may need different admission | `endpoint-cost-observation` (observation only) |
| workflow-aware | sequence/account can tie distributed calls | `workflow-sequence-observation` (observation only) |
| cache | reusable responses reduce work | cache-bypass |
| admission/shedding | excess work can be rejected before collapse | source-led design only; local recovery is an observation |

## Required external instruction

### Application-layer protection assignment

**Direct link:** [Application-layer guidance](https://docs.aws.amazon.com/waf/latest/developerguide/ddos-app-layer-rbr.html)  
**Exact section, chapter, or unit:** Complete short page  
**Estimated time:** 25 minutes  
**What to focus on:** endpoint-specific protection, application-layer request cost, and the relationship between rules and protected paths  
**What to skip:** console deployment and managed-product comparison  
**Expected takeaway:** map a protected endpoint to its expensive resource and state what a broad request count would miss.

### Rate-control semantics assignment

**Direct link:** [Rate-based rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html)  
**Exact section, chapter, or unit:** Aggregation instances, Evaluation windows, Scope-down statements, and Custom keys  
**Estimated time:** 50 minutes  
**What to focus on:** aggregation identity, endpoint scope, window semantics, custom-key trust, and product-specific limits  
**What to skip:** console deployment and rule creation walkthroughs  
**Expected takeaway:** predict one bypass and one collateral-risk scenario for each aggregation, scope, window, and key choice.

## Course bridge

Rate controls count within a defined aggregation/window/scope. Different
application areas can have different cost and legitimate rates. Load shedding
protects critical work even when traffic classification is imperfect.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Pair every control with the protected resource and a
    legitimate near-neighbor. A bypass is meaningful only if resource/service
    effect or protected work changes under fixed safe traffic.

## Worked example

Per-session `session_id` allows rotation. The local lab observes route/input cost
and a search-to-product sequence, but it does not implement endpoint-specific or
workflow-aware admission. A real workflow-aware control would correlate search,
product, and protected work to durable server-derived identity/state rather than
one request key.

## Guided exercise

### Objective

Design the seven local scenario hypotheses before execution.

### Setup

Use the resource/metric plans and load guide.

### Exact actions or commands

1. For each scenario name resource, fixed count/rate, changed variable, control,
   success, abort, near-neighbor, and recovery.
2. Distinguish cached fixed key from bypassed unique keys.
3. Map one bounded retry to two server requests.
4. Identify expected rejections and threshold treatment.
5. Mark AWS semantics as product-specific, local behavior as synthetic.

### Expected output

The exercise result contains seven pre-registered local experiments: cheap/expensive at
equal rate, cache hit/bypass, fixed/rotated synthetic identity,
`endpoint-cost-observation`, `workflow-sequence-observation`, bounded retry
amplification, and immediate recovery. Each row names the actual control (or
explicitly `none`), expected statuses, deterministic assertion, runtime
observation, collateral population, abort, and retest; no public target or L3/L4
method appears.

### Interpretation

The map distinguishes defeating an aggregation key from causing a protected
service effect. A rotated key can show that a limiter trusts attacker-controlled
input, while the resource may remain healthy. The finding needs both the control
result and the measured resource/legitimate-neighbor consequence.

### Common failure modes

- Rotating keys without measuring work/health
- One threshold for cheap and expensive routes
- Treating cache miss as evasion without resource evidence
- Unlimited retries

### Cleanup

No traffic yet.

## Why this matters offensively

Modern application-layer attacks distribute identities and select high-cost
workflows. Control scope and admission behavior are the attack surface.

## Check your understanding

1. A rate limit counts requests by `session_id` within a fixed window. Which configured fields define one aggregation instance?
2. Why should the control map distinguish cheap and expensive endpoints instead of applying one unexplained request limit everywhere?
3. A custom rate key comes directly from a caller-controlled header. How can cheap rotation of that value split one hostile workflow across counters?
4. The edge starts load shedding for expensive work. What service behavior should improve if the load-shedding policy is effective?
5. A rotated-key trial avoids `429`. Which resource, service, or protected-work evidence must accompany the status change before claiming an impactful bypass?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The configured key, its observed value, the counting window, and the applicable route or scope define one aggregation instance.** Each distinct cheap value may otherwise receive a separate counter.

- **2. Endpoints consume different resources and have different legitimate traffic patterns.** Per-endpoint analysis can protect expensive work without imposing unnecessary collateral limits on cheap or critical routes.

- **3. If the server accepts the untrusted header as the key, the caller can choose a new value for each request.** One workflow then appears as many identities and avoids a per-value counter.

- **4. Critical legitimate work should remain within its latency and error objectives, and recovery should improve because excess expensive work is rejected earlier.** Rejection count alone is not the resilience goal.

- **5. Show accepted expensive work, resource consumption, or a measured service-health effect under the fixed safe envelope.** Avoiding `429` without downstream impact proves only a control response change.

</details>

## Next lesson

[Bounded load testing](04-bounded-load-testing.md) executes the pre-registered
local scenarios under hard tool and application ceilings.
