# Intelligence to emulation and regression

<!-- source-ids: mitre-adversary-emulation-plans, owasp-automated-threats, aate-local-lab, aate-adversarial-control-loop -->
<!-- source-ledger-consistency: strict -->

## Appendix guide

- Appendix: Traffic and Bot Threat Intelligence
- Status: Optional
- Best time to review: before a bounded organization-owned emulation or after remediation planning
- Prior technical lessons required: None
- Return to the core path: [HTTP request and response](../../modules/01-http-edge/01-http-request-response.md)
- Appendix lesson: 3 of 3
- Estimated time: 120 minutes

## Role outcome

Translate confidence-bounded intelligence into a small authorized behavior plan,
then specify blocked baseline, protected result, legitimate near-neighbor, abort
conditions, telemetry, cleanup, and an exact regression without copying a tool or actor label.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MITRE Adversary Emulation Plans](https://attack.mitre.org/resources/adversary-emulation-plans/) | Overview through Emulation Plan Documents | Supports behavior chains tied to an objective | Enterprise examples require translation to bounded traffic workflows. |
| PROJECT_DOCUMENTATION | [OWASP Automated Threats](https://owasp.org/www-project-automated-threats-to-web-applications/) | Login and protected-workflow threat events | Supplies provider-neutral automated-abuse objectives | Taxonomy does not authorize execution or prescribe one control. |
| LAB_SPECIFIC | [Synthetic intelligence analysis](../../labs/course-map.md) | Emulation-plan and exact-regression output in the command record | Supplies deterministic non-network planning evidence | Plan output does not execute traffic or prove a control result. |
| COURSE_SYNTHESIS | [AATE adversarial-control loop](../../methodology/adversarial-control-loop.md) | Objective through remediation and exact retest | Connects behavior intelligence to protected-action evidence | The complete loop is course synthesis, not a quoted standard procedure. |

## Mental model

| Intelligence element | Emulation translation | Regression translation |
|---|---|---|
| protected-report replay sequence | reproduce only `POST /api/challenge`, proof transfer, and `GET /api/reports/protected` | cross-session and repeat replay must fail while first-use same-session succeeds |
| login sequence across accounts | bounded account-state transitions in an owned fixture | hostile sequence blocked; legitimate account flows remain healthy |
| stale client artifact | do not make it the behavior objective | record version and test current/stale near-neighbors |
| ambiguous shared relay | exclude actor claim | include shared-infrastructure legitimate population |

## Required external instruction

### MITRE behavior-plan assignment

**Direct link:** [MITRE Adversary Emulation Plans](https://attack.mitre.org/resources/adversary-emulation-plans/)
**Exact section, chapter, or unit:** Complete overview page through Emulation Plan Documents
**Estimated time:** 20 minutes
**What to focus on:** objectives, chained adversary behavior, observable actions, and adaptations to the tested environment
**What to skip:** copying a named group's full plan or importing tools not needed by the bounded objective
**Expected takeaway:** express the intelligence as a short behavior chain with measurable defensive expectations.

### OWASP objective assignment

**Direct link:** [OWASP Automated Threats](https://owasp.org/www-project-automated-threats-to-web-applications/)
**Exact section, chapter, or unit:** Threat-event descriptions closest to account access and protected-workflow automation
**Estimated time:** 25 minutes
**What to focus on:** adversary objective, workflow preconditions, business effect, and defensive observation points
**What to skip:** external target selection and volume guidance
**Expected takeaway:** name a provider-neutral protected action that can be exercised in an explicitly authorized environment.

## Course bridge

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** An intelligence-informed test remains bounded by
    authorization. The plan names objective, behavior sequence, fixed variables,
    blocked baseline, protected action, legitimate near-neighbor, telemetry,
    ceiling, abort, cleanup, remediation expectation, and exact retest.

Intelligence selects representative behavior; it does not relax safety or turn
indicators into an identity verdict. A regression checks the control objective
and customer outcome against the same populations after remediation.

## Worked example

The protected-report cluster becomes a two-request synthetic plan: obtain a
challenge proof with `POST /api/challenge` in session A, present it from session
B to `GET /api/reports/protected`, and observe whether session B completes the
protected report. The expected remediation binds proof to
session and action. The regression repeats both same-session first use and
cross-session transfer, while a legitimate automation near-neighbor must retain
its documented supported path.

## Optional exercise

### Objective

Generate and critique a deterministic emulation plan and exact regression for
the synthetic protected-report replay cluster without contacting a service.

### Setup

Use Python 3.12+ and the repository fixture. Treat every displayed action as a
plan against an explicitly owned pre-production fixture, not authorization to execute it.

- Required working directory: repository root
- Preflight: confirm Python 3.12+ and the tracked synthetic fixture
- Exact target: fixture analysis only; no emulation action or network request occurs
- Failure guidance: stop if the output loses alternatives, limits, regression fields, or no-network status

### Exact actions or commands

```bash
python -m lab.analysis.traffic_intelligence
```

Review the plan and regression blocks. Confirm the target is a placeholder,
traffic is not sent, attribution remains unsupported, and the plan's member IDs
and confidence are copied from the selected evidence-derived group.

### Expected output

The plan derives its cluster ID, supporting and current evidence, confidence,
contradictions, alternatives, workflow, request sequence, challenge behavior,
protected action, safe approximation, defensive observations, limitations, and
exact regression from the selected group. Its **high** categorical confidence
result is identical in the group, plan, and regression. The regression requires
cross-session and repeat-use replay denial without breaking valid first use.

### Interpretation

The output closes the intelligence loop only as a test contract. Execution and
results remain future work requiring explicit authorization and monitoring. A
behavior-derived regression is more durable than preserving the stale Chromium
132 artifact or blocking a shared relay.

### Common failure modes

- Treating a cluster name or indicator as authorization to execute
- Copying a tool or actor label instead of the observed behavior sequence
- Defining success as a detector score rather than the protected-action result
- Omitting legitimate near-neighbor and cleanup requirements

### Cleanup

The command writes no plan artifact and sends no traffic. Remove any private
organization placeholders before sharing notes.

## Why this matters offensively

Intelligence is operationally useful when it selects a reproducible adversary
behavior and a discriminating next test. The same plan structure helps defenders
repair the overtrusted assumption and prove the repair without encoding stale indicators.

## Check your understanding

1. Why should an emulation plan reproduce the protected-report sequence rather than the stale Chromium 132 artifact?
2. Which protected-action result would prove that cross-session challenge replay succeeded in the synthetic model?
3. Why must the exact regression include same-session first use and a legitimate near-neighbor?
4. What additional condition is required before a generated plan may be executed in pre-production?
5. Which capabilities remain unsupported by the deterministic intelligence command?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The sequence represents the stable adversary behavior and objective, while the browser version is a cheap, time-sensitive artifact.** Testing the sequence produces a durable control expectation and avoids encoding release drift as identity.

- **2. Session B must complete the named protected request using proof issued to session A, with server-side evidence identifying B's accepted action.** Token appearance or a lower score alone would remain intermediate observation.

- **3. Same-session first use checks that remediation preserves the intended proof flow, while the legitimate near-neighbor measures collateral harm.** Replay denial without those controls could merely reflect a broken workflow for everyone.

- **4. The owner must explicitly authorize the named environment, behavior, ceilings, timing, telemetry, abort authority, and cleanup.** A repository-generated plan is not permission and never expands the approved target boundary.

- **5. It does not execute traffic, attribute an actor, validate a commercial control, estimate prevalence, prove production impact, or authorize a target.** It only transforms synthetic evidence into a deterministic bounded plan and regression definition.

</details>

## Continue

- Return to [HTTP request and response](../../modules/01-http-edge/01-http-request-response.md) for the core path.
- For an interview route, open the [Experienced Practitioner Fast Track](../../experienced-practitioner-fast-track.md).
