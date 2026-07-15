# Module 2: Automated abuse and threat modeling

## Why this matters

Automation is a means, not the business objective. Effective research starts with the actor, asset, workflow, desired outcome, observable behavior, existing control, and legitimate populations that may look similar.

## Role outcomes

You can model automated abuse across accounts, sessions, identities, and workflows and turn the model into testable hypotheses, telemetry needs, layered controls, and false-positive questions.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Explain credential stuffing, account creation abuse, scraping, scalping, denial of inventory, promotion abuse, and application-layer denial of service. Distinguish malicious automation from a malicious business outcome.

### Hands-on outcome

Inspect the synthetic login, account, search, product, reservation, promotion, and expensive-report workflows and map six abuse types to their target state changes or costs.

### Interview outcome

Structure an abuse answer as actor → goal → workflow → observable behavior → control → false-positive risk → validation.

### Required artifact

A six-row threat map containing attacker goal, target workflow, observable signal, likely control, and false-positive risk.

### Completion test

Explain how scraping differs from scalping, how denial of inventory differs from volumetric DDoS, and why one IP-based control is insufficient for at least two workflows.

### Estimated time

2 focused hours.

### Required resources only

- [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/) — `[L1 Foundation]` `[Required]` taxonomy overview and six selected threats

### Optional deeper resources

- [OWASP API Security](https://owasp.org/www-project-api-security/) — `[L2 Applied]` `[Recommended]`

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Explain stateful, distributed low-rate, replay, multi-identity, and multi-stage abuse. Identify signals at request, session, account, device-like, workflow, and global scopes.

### Hands-on outcome

Expand the threat map to at least ten abuse cases. Generate bounded synthetic account, inventory, and promotion events and identify where naive per-IP controls miss intent.

### Interview outcome

Design layered controls for low-rate promotion abuse without assuming shared households, accessibility tools, privacy software, or carrier NAT are malicious.

### Required artifact

Ten-row workflow-aware threat map plus one state diagram for a multi-step abuse case.

### Completion test

For three cases, identify the minimal state needed for detection, the cost of collecting it, and a legitimate population at risk.

### Estimated time

3 additional focused hours.

### Required resources only

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) — `[L2 Applied]` `[Required]` relevant workflow sections

### Optional deeper resources

- [PortSwigger business logic vulnerabilities](https://portswigger.net/web-security/logic-flaws) — `[L2 Applied]` `[Recommended]`

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Model account graphs, replay, identity cycling, distributed low-rate behavior, stage transitions, agent behavior, and the interaction between abuse prevention and service resilience.

### Hands-on outcome

Build one multi-stage synthetic case spanning account creation, product search, inventory reservation, and promotion redemption. Compare request-local, session-aware, and workflow-aware detection.

### Interview outcome

Defend which controls belong at edge, application, account, and analyst layers and how feedback contamination or rule overlap can hide failures.

### Required artifact

Capstone abuse model with assets, actors, trust boundaries, stages, telemetry, controls, residual risk, and validation plan.

### Completion test

Demonstrate one case that evades a naive request-rate rule but is visible through bounded workflow evidence, then quantify false positives by population.

### Estimated time

4 additional focused hours.

### Required resources only

- [AATE automated-abuse concept](../../docs/concepts/automated-abuse.md) — `[L3 Integrated]` `[Required]`
- [Threat-model template](../../templates/threat-model.md) — `[L3 Integrated]` `[Required]`

### Optional deeper resources

- [OWASP Automated Threats ontology materials](https://owasp.org/www-project-automated-threats-to-web-applications/) — `[L3 Integrated]` `[Optional]`

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Investigate adaptive or agentic automation, distributed identity graphs, replay, control displacement, attacker economics, and how mitigations change behavior rather than simply remove it.

### Hands-on outcome

Form an original abuse hypothesis, vary one control, and compare attacker outcome, defender cost, customer friction, and alternative explanations using local synthetic populations.

### Interview outcome

Teach how a workflow-level hypothesis becomes a controlled research plan and defend why the result may not generalize across businesses or populations.

### Required artifact

Original abuse research note with competing hypotheses, experiment, measured result, limitation, remediation, and staged validation proposal.

### Completion test

The work distinguishes automation signals from business harm, compares at least two control strategies, and identifies how an adaptive actor could change the observed behavior.

### Estimated time

6–8 additional focused hours.

### Required resources only

- Primary sources specific to the chosen abuse workflow — `[L4 Deep]` `[Required]`

### Optional deeper resources

- [BrowserGym](https://github.com/ServiceNow/BrowserGym) — `[L4 Deep]` `[Optional]` research framework only
- [WebArena](https://github.com/web-arena-x/webarena) — `[L4 Deep]` `[Optional]` research framework only

## Common misconceptions

- “Bot” does not imply malicious, and “human” does not imply legitimate.
- Scraping, scalping, inventory denial, and DDoS differ by objective and state, even when requests overlap.
- Residential-looking IPs and realistic browsers do not erase workflow evidence.
- A challenge can add customer harm without stopping the abusive outcome.

## Production limitations

Synthetic accounts and workflows lack real conversion behavior, identity diversity, customer support signals, legal constraints, fraud loss, adversary adaptation, and global graph scale. Local results establish method, not production thresholds.

## Interview questions

1. How would you detect distributed low-rate promotion abuse?
2. Which signals identify an abusive outcome without proving automation?
3. How do controls differ for scraping, scalping, and denial of inventory?

## Related lab components

- `lab/app/main.py`
- `lab/fixtures/requests.jsonl`
- `lab/detectors/rules.py`
- `templates/threat-model.md`

