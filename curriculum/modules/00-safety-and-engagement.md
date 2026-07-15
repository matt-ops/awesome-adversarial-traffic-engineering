# Module 0: Safety and red-team engagement discipline

## Why this matters

Adversarial traffic research can create the failure it is meant to study. Authorization, scope, hard limits, monitoring, evidence handling, remediation, and retest are engineering requirements—not paperwork after the test.

## Role outcomes

You can turn a security question into a controlled engagement that produces useful evidence without exposing customers, unrelated systems, or third parties to uncontrolled risk.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Explain authorization, explicit scope and exclusions, objectives, hard rate and duration limits, abort conditions, evidence handling, customer-impact awareness, remediation, and retest. Explain why a test that harms customers is a failed engagement.

### Hands-on outcome

Review `SAFETY.md`, run the target validator in dry-run mode, and classify five example targets or configurations as allowed or rejected.

### Interview outcome

Answer “How would you safely test an edge control?” by leading with authority, objectives, environment, caps, monitoring, abort, recovery, evidence, and retest.

### Required artifact

One-page safe engagement checklist naming the owner, local target, exclusions, cap values, monitoring signals, abort decision, evidence location, cleanup, and retest owner.

### Completion test

Given an ambiguous test request, identify the missing authority or control, refuse unsafe execution, and rewrite it as a bounded local experiment. Show that an external URL and an excessive rate are rejected.

### Estimated time

1.5 focused hours.

### Required resources only

- [`SAFETY.md`](../../SAFETY.md) — `[L1 Foundation]` `[Required]`
- [Authorization and scope](../../docs/safety/authorization-and-scope.md) — `[L1 Foundation]` `[Required]`

### Optional deeper resources

- [Research ethics](../../docs/safety/research-ethics.md) — `[L2 Applied]` `[Recommended]`

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Distinguish scope, rules of engagement, test cases, traffic envelope, service health, stop authority, rollback, recovery validation, data retention, and escalation communications.

### Hands-on outcome

Write and tabletop a complete engagement plan for the local expensive-endpoint experiment. Trigger a simulated abort condition and record the stop, recovery check, and decision to resume or close.

### Interview outcome

Defend conservative caps and explain how a technically interesting scenario can be redesigned when monitoring or recovery ownership is missing.

### Required artifact

Completed engagement plan and tabletop record using [`templates/engagement-plan.md`](../../templates/engagement-plan.md).

### Completion test

A peer can execute the dry run, identify the stop authority, locate every cap, and complete recovery validation without asking for unstated assumptions.

### Estimated time

2 additional focused hours.

### Required resources only

- [Load-testing guardrails](../../docs/safety/load-testing-guardrails.md) — `[L2 Applied]` `[Required]`

### Optional deeper resources

- [CISA denial-of-service guidance](https://www.cisa.gov/news-events/news/understanding-denial-service-attacks) — `[L2 Applied]` `[Recommended]`

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Explain how safety decisions change across browser collection, protocol capture, stateful abuse, detection enforcement, load testing, data handling, and retesting.

### Hands-on outcome

Govern the integrated capstone with a runbook, live decision log, preflight evidence, monitored abort signals, cleanup, and recovery evidence. Record every deviation from the plan.

### Interview outcome

Handle follow-up about partial authorization, noisy telemetry, changing production conditions, shared dependencies, and disagreement over aborting a test.

### Required artifact

Capstone safety package: signed-off synthetic scope, preflight, decision log, abort/recovery evidence, and sanitized evidence index.

### Completion test

An independent review can reconstruct what was authorized, what ran, when limits were approached, why the test stopped, what recovered, and which claims remain unsupported.

### Estimated time

3 additional focused hours distributed across the capstone.

### Required resources only

- [Experiment log template](../../templates/experiment-log.md) — `[L3 Integrated]` `[Required]`
- [Evidence index template](../../templates/evidence-index.md) — `[L3 Integrated]` `[Required]`

### Optional deeper resources

- [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) — `[L3 Integrated]` `[Optional]`

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Reason about staged validation, blast-radius reduction, representative environments, data minimization, stop authority under uncertainty, and the gap between local evidence and production decisions.

### Hands-on outcome

Design a production-validation proposal for the original research question using simulation, shadow observation, tiny cohorts, progressive thresholds, rollback, and decision owners. Do not execute it.

### Interview outcome

Defend the proposal to skeptical service, privacy, detection, and incident-response stakeholders and state what evidence would cancel the work.

### Required artifact

Research-governance appendix and staged production-validation proposal.

### Completion test

The proposal has explicit authority boundaries, smallest useful blast radius, measurable success and harm criteria, reversible stages, named owners, and a no-go path.

### Estimated time

4 additional focused hours.

### Required resources only

- Completed Integrated safety package — `[L4 Deep]` `[Required]`

### Optional deeper resources

- Organization-specific change, privacy, and incident procedures, if authorized — `[L4 Deep]` `[Optional]`

## Common misconceptions

- “It is only a test” does not reduce customer or dependency impact.
- A low request rate is not automatically safe; endpoint cost and shared state matter.
- Authorization is not transferable across targets, time windows, identities, or techniques.
- Cleanup is not recovery validation, and a mitigation is not complete without a retest.

## Production limitations

The local validator and caps demonstrate mechanisms, not enterprise authorization, global traffic controls, legal review, service ownership, incident command, or production recovery. Apply real organizational processes before any non-local work.

## Interview questions

1. What belongs in a DDoS or bot-defense engagement plan?
2. Which conditions make you stop a test even if the objective is unmet?
3. How do you preserve evidence while minimizing sensitive data?

## Related lab components

- `lab/safety.py`
- `lab/clients/safe_client.py`
- `lab/tests/test_safety.py`
- `templates/engagement-plan.md`

