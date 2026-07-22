# Recovery, remediation, and retest

<!-- source-ids: nist-sp-800-115, aws-builders-library-load-shedding, k6-thresholds, aate-adversarial-control-loop -->

## Progress

- Module: 08 - DDoS and resilience
- Lesson: 5 of 5
- Depth: Deep
- Estimated time: 4 hours
- Prerequisites:
  - [Bounded load testing](04-bounded-load-testing.md)
  - Complete the resource model, metric plan, and bounded scenarios
- Next lesson: Python telemetry

## Role outcome

Measure return to health, recommend resource-specific controls, and replay the
same bounded attack as a remediation acceptance test.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | Sections 3.2, 5.2, and Appendix B Rules of Engagement template | Supports authorization, communication, execution boundaries, incident handling, and reporting | General technical-testing guidance; the environment owner must supply actual pre-production approvals and operating details. |
| PRACTITIONER_PERSPECTIVE | [AWS Load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) | Complete article | Supports admission and graceful recovery | Practitioner guidance from one large provider; adapt mechanisms to the target architecture. |
| OFFICIAL_DOCUMENTATION | [k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | thresholds and failure | Supplies measurable acceptance criteria | Tool documentation; AATE adds stricter local target and load ceilings. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | impact, remediation, same-attack retest | Defines completion | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
pre-test health -> bounded pressure -> threshold/control behavior
                -> traffic stops -> health probes -> recovery time
remediation -> same target/scenario/config/evidence -> compare objective
```

## Required external instruction

### Recovery assignment

**Direct link:** [Using load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
**Exact section, chapter, or unit:** reread overload prevention, admission/load shedding, critical work, and recovery discussion in the complete article
**Estimated time:** 45 minutes
**What to focus on:** local decisions, fail-open/fail-closed effects, critical work, fairness, and proving recovery
**What to skip:** no product implementation is assigned
**Expected takeaway:** propose resource-specific remediation with a measurable legitimate-health objective.

### Rules-of-engagement assignment

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)
**Exact section, chapter, or unit:** Sections 3.2 and 5.2, then Appendix B Rules of Engagement template
**Estimated time:** 35 minutes
**What to focus on:** authorization, named systems, excluded systems, timing, communication, incident handling, data handling, and stop authority
**What to skip:** technique catalogs unrelated to bounded application-layer resilience
**Expected takeaway:** identify every owner-supplied approval and operating field that must be complete before a pre-production test begins.

## Course bridge

Traffic stopping is not recovery. Recovery is the measured return of legitimate
health, queues, dependencies, and error/timeout rates to predeclared objectives.
Shedding may intentionally reject excess requests while improving critical health.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Exact retest preserves adversary objective, path,
    scenario, load envelope, fixed variables, legitimate probe, evidence schema,
    and aborts after remediation.

## Worked example

Remediation may cache fixed report inputs, add endpoint admission, bound retry
budget, and aggregate a workflow identity. The current lab can exactly repeat
`cache-bypass`, `endpoint-cost-observation`, `retry-amplification`, and
`identity-key`; proving a newly implemented endpoint/workflow control requires a
separate before/after configuration plus assertions. Success is protected health
and bounded recovery, not zero rejections.

## From bounded local evidence to an authorized pre-production test plan

The local `endpoint-cost-observation` can support a *hypothesis* that an expensive
pre-production workflow deserves bounded pressure and recovery measurement. It
does not establish pre-production capacity, blast radius, safe request rate,
dependency behavior, or authorization. Translate it with this provider-neutral
plan; leave every owner field as a placeholder until the named owner approves it.

1. **Test question and explicit non-goals.** Ask whether the owner-approved
   `{PREPRODUCTION_PROTECTED_WORKFLOW}` breaches its `{SERVICE_SPECIFIC_LATENCY_OBJECTIVE}`
   under one staged application-layer resource hypothesis. Explicitly exclude
   capacity certification, public or production targets, Layer 3/4 pressure,
   control bypass exploration, autoscaling claims, and any route not named here.
2. **System owner and written authorization.** Record `{SYSTEM_OWNER}`,
   `{TEST_LEAD}`, `{OPERATIONS_LEAD}`, and the signed or ticketed
   `{AUTHORIZATION_REFERENCE}`. Approval must cover environment, routes,
   identities, data, envelope, telemetry, timing, cleanup, and stop authority
   before traffic, configuration change, credential use, or telemetry access.
3. **Change window, incident contacts, and stop authority.** Record
   `{APPROVED_WINDOW}`, `{CHANGE_REFERENCE}`, `{INCIDENT_COMMANDER}`, on-call
   acknowledgements, notification channel, escalation path, and the exact stop
   phrase. The test lead, operations lead, and incident commander may stop
   independently; silence or a missing acknowledgement is no-go.
4. **Target topology and observation points.** Fill `{PREPRODUCTION_ENVIRONMENT_ID}`,
   `{PRIVATE_OR_LOOPBACK_TARGET}`, `{APPROVED_ROUTES}`, `{APPROVED_TEST_ACCOUNTS}`,
   client-to-edge-to-service hops, queues, caches, downstream dependencies, DNS
   and dependency ownership, region, build/configuration versions, and the
   observer responsible for each signal. Revalidate redirects and resolution.
5. **Baseline window and legitimate service objectives.** Define a quiet
   `{BASELINE_WINDOW}`, the cheap-route control, legitimate near-neighbor, and
   operator health probe. Record request, error, latency, saturation, queue,
   cache, dependency, shedding, and workflow objectives before pressure; a
   client timeout alone is not the service effect.
6. **Resource hypothesis.** Translate `endpoint-cost-observation` only into the
   bounded claim that expensive uncached work may consume `{HYPOTHESIZED_RESOURCE}`
   faster than the cheap route. List local response and recovery observations,
   plus unknown pre-production capacity, autoscaling, queue, cache, dependency,
   control, and background-traffic behavior.
7. **Traffic envelope.** Let the owner fill `{MAX_VUS}`, `{MAX_REQUEST_RATE}`,
   `{MAX_TOTAL_REQUESTS}`, `{MAX_DURATION}`, `{REQUEST_TIMEOUT}`, ramp steps, and
   retry prohibition or budget. These are hard ceilings, not targets to reach;
   the lowest approved stop condition wins.
8. **Expected mitigation and activation timing.** Name `{EXPECTED_MITIGATION}`,
   its observation point, trigger input, intended rejection or degradation
   behavior, and `{OWNER_APPROVED_ACTIVATION_OBJECTIVE}`. Measure first pressure,
   first activation, stable activation, legitimate impact, and deactivation;
   controlled shedding can be success when protected work remains healthy.
9. **Circuit breakers and abort thresholds.** Predeclare numeric `{LATENCY_ABORT}`,
   `{ERROR_ABORT}`, `{SATURATION_ABORT}`, `{QUEUE_ABORT}`,
   `{LEGITIMATE_HEALTH_ABORT}`, and `{DEPENDENCY_ABORT}`. The test lead,
   operations lead, and incident commander can stop independently; automation
   stops on the first breached threshold or lost telemetry.
10. **Rollback and recovery procedure.** Stop generators, revoke test
    credentials, clear synthetic state, restore `{PRETEST_CONFIGURATION}` through
    the approved change path, drain test queues, confirm excluded systems received
    no test traffic, and retain an owner-confirmed cleanup timestamp. Traffic
    stopping is time zero, not recovery; continue passive health probes until all
    declared latency, error, saturation, queue, dependency, and legitimate-
    workflow objectives remain healthy for `{RECOVERY_STABILITY_WINDOW}`.
11. **Dependencies and collateral-impact measurements.** Name every in-scope
    queue, cache, database, downstream service, autoscaling signal, and shared
    component; assign its owner and abort. Continue measurements after the front
    end is healthy because dependencies and queues can recover later. Unknown or
    unowned recursive dependencies remain excluded.
12. **Customer or legitimate-neighbor protection.** Define the bounded hostile
    workflow, a cheap-route control, a legitimate near-neighbor on the expensive
    route, privacy-safe identifiers, credentials, reset state, and success/abort
    criteria. No customer data, unrelated tenant, or shared third-party service
    is permitted; controlled rejection must not violate the approved objective.
13. **Evidence schema and clock synchronization.** Assign `{TELEMETRY_OWNER}`;
    verify host, load-generator, and monitoring clocks against `{CLOCK_SOURCE}`.
    Store configuration, versions, timestamps, aggregate signals, activation and
    abort events, recovery series, limitations, and owner decisions under
    `{AUTHORIZED_EVIDENCE_LOCATION}` with access and retention rules. Report
    local facts, pre-production observations, and inference separately.
14. **Exact remediation retest.** Name `{REMEDIATION_CHANGE}` and repeat the same
    test question, environment, routes, populations, fixed inputs, envelope,
    expected mitigation timing, thresholds, evidence schema, cleanup, and
    recovery criteria. Accept only when hostile pressure is handled as intended,
    legitimate work remains within objective, and recovery meets the same
    stability window. Any envelope change requires new approval.
15. **Limitations that remain after the test.** Record that a local relative cost
    is not production capacity, a healthy loopback endpoint is not distributed
    recovery, one pre-production window does not establish Internet scale or
    every workload, and observed control activation does not prove identity or
    universal mitigation. Production, public targets, Layer 3/4 behavior, real
    customer effects, and excluded dependencies remain untested.

Before those steps, list `{EXCLUDED_HOSTS}`, `{EXCLUDED_ROUTES}`, production,
public Internet targets, customer data, unrelated tenants, and any path without
a verified owner. Redirects or DNS resolution outside scope cause an abort.
Execution begins with target/exclusion validation, telemetry-only dry run, one
functional request, the baseline window, and the smallest approved ramp step.
Change only one envelope dimension at a time; never improvise another route,
identity, rate, duration, retry policy, or bypass.

The go/no-go record must show every placeholder resolved, all named owners
acknowledged, telemetry and automated aborts verified, and exclusions rechecked.
Otherwise the output remains a plan and no traffic is sent.

## Guided exercise

### Objective

Write recovery evidence, complete a provider-neutral pre-production plan review,
and define one exact remediation retest without sending additional traffic.

### Setup

Use the verified k6 outputs and teardown health results. No additional pressure is needed.

### Exact actions or commands

1. Record pre/pressure/post health and timestamped recovery.
2. Separate unexpected errors from intentional shedding.
3. Recommend cache, admission, endpoint, workflow, retry, and dependency controls
   only where the resource map supports them.
4. Define legitimate near-neighbor success and collateral thresholds.
5. Copy the exact scenario/config/evidence schema into the retest plan.
6. Walk through all fifteen pre-production plan items and mark unresolved owner
   fields `NO-GO`; do not replace placeholders with invented organization data.

### Expected output

A timestamped recovery timeline records when traffic stops, the next health
sample, latency/error return to the declared objective, and any queue/cache/state
that remains. The plan maps remediation to the exhausted resource, supplies
hostile and legitimate-neighbor criteria, and preserves the exact scenario,
rate, duration, thresholds, and cleanup for retest.
The pre-production plan separates local evidence from unknown target behavior,
contains explicit exclusions, named stop authority, automated thresholds,
recovery stability, cleanup, and an unchanged remediation-acceptance retest.

### Interpretation

The local teardown assertion proves a `200` health response within 1,000 ms. It
does not measure sustained recovery or queues/dependencies absent from the toy
app. State that limit.

### Common failure modes

- Calling traffic stop recovery
- Recommending generic scaling without bottleneck evidence
- Requiring zero shedding
- Changing test envelope after remediation

### Cleanup

Stop the local stack. Keep only an approved private summary if needed; do not
commit generated telemetry, credentials, certificates, or audit material.

## Why this matters offensively

A resilience finding is actionable when it identifies the exhausted resource,
protects legitimate work, and provides the same attack as a regression test.

## Check your understanding

1. After bounded pressure stops, which measurements show that the legitimate health route and affected resource returned to their objectives?
2. A remediation sheds more expensive requests but keeps critical work healthy. Can the higher controlled rejection rate represent better resilience?
3. Which unresolved authorization, owner, telemetry, abort, target, or exclusion fields make the pre-production plan a no-go?
4. Which objective, path, scenario, envelope, fixed inputs, evidence fields, and aborts must remain the same for an exact resilience retest?
5. The loopback service becomes healthy after Docker teardown and restart. Which production activation, dependency, queue, and distributed-recovery properties remain unproved?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A recovery timeline should show legitimate latency, errors, availability, queue or resource measurements returning within the predefined health objectives.** Merely stopping the load generator does not prove recovery.

- **2. Yes.** Deliberate load shedding can improve resilience when early rejection preserves critical useful capacity and keeps the protected workflow within agreed criteria. The conclusion must include both rejection and health evidence.

- **3. Any missing written authorization, accountable owner acknowledgement, target or exclusion validation, required telemetry, clock check, circuit breaker, numeric abort, stop authority, cleanup path, or incident contact leaves the plan `NO-GO`.** A plan template never supplies permission.

- **4. Repeat the same adversary objective, route, scenario configuration, hard envelope, initial state, request inputs, evidence schema, thresholds, and abort conditions.** Only the remediation should differ.

- **5. The local restart does not prove mitigation activation timing, production queue draining, dependency recovery, distributed coordination, autoscaling, sustained stability, or Internet-scale behavior.** Those remain explicit limitations outside the synthetic lab and require separate owner-approved evidence.

</details>

## Next lesson

[Open Module 09](../09-tooling-code-review/index.md) to build safe telemetry and
review code for timeout, retry, concurrency, and authorization flaws.
