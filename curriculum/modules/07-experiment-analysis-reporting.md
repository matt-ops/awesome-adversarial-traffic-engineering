# Module 7: Experimental method, detection analysis, and reporting

## Why this matters

A bypass demonstration is not yet a defensible finding. Useful research controls variables, preserves evidence, tests alternative explanations, quantifies error, recommends a specific change, and defines a retest that can prove improvement.

## Role outcomes

You can design reproducible experiments, evaluate detection and service effects, write technical and executive findings, define measurable remediation, and retest without overstating local evidence.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Explain hypothesis, baseline, variable, control, test matrix, evidence, alternative explanation, precision, recall, false-positive analysis, finding, remediation, validation, limitation, and retest.

### Hands-on outcome

Use the deterministic fixture to compare one transparent rule with a baseline and write the result as hypothesis → test → evidence → limitation → recommendation → retest.

### Interview outcome

Give a concise technical finding that separates observation, inference, impact, and unproven claims.

### Required artifact

One synthetic red-team finding with evidence, a false-positive consideration, a specific recommendation, and measurable retest.

### Completion test

A reviewer can identify the hypothesis, changed variable, baseline, evidence, alternative explanation, supported conclusion, and condition that would show the remediation worked.

### Estimated time

1.5 focused hours.

### Required resources only

- [Finding template](../../templates/finding.md) — `[L1 Foundation]` `[Required]`
- [AATE findings and retesting concept](../../docs/concepts/findings-and-retesting.md) — `[L1 Foundation]` `[Required]`

### Optional deeper resources

- [Experiment log template](../../templates/experiment-log.md) — `[L2 Applied]` `[Recommended]`

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Explain repeatability, deterministic fixtures, control populations, test matrices, chart/table selection, confidence limits in small samples, reason codes, technical impact, customer impact, root cause, and validation criteria.

### Hands-on outcome

Run one controlled local experiment, produce a table or chart, calculate appropriate detector or service metrics, write a full finding, and give a five-minute briefing.

### Interview outcome

Handle follow-up that challenges causality, sample representativeness, false positives, severity, feasibility of remediation, and what the test did not simulate.

### Required artifact

Experiment log, evidence index, result table or chart, full finding, and briefing notes.

### Completion test

The experiment reproduces from a clean fixture, the chart matches machine-readable output, and every claim points to evidence or is explicitly labeled an inference or limitation.

### Estimated time

4 additional focused hours.

### Required resources only

- [Technical report template](../../templates/technical-report.md) — `[L2 Applied]` `[Required]`
- [Evidence index template](../../templates/evidence-index.md) — `[L2 Applied]` `[Required]`

### Optional deeper resources

- [pandas documentation](https://pandas.pydata.org/docs/) — `[L2 Applied]` `[Optional]` selected analysis tasks

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Explain feature ablation, rule overlap, base-rate effects, per-population metrics, drift, evidence provenance, executive versus engineering needs, remediation ownership, success metrics, and staged retesting.

### Hands-on outcome

Run the complete capstone; compare at least four populations and multiple controls; produce a six-to-eight-page synthetic technical report, one-page executive summary, evidence index, measurable remediation, and retest.

### Interview outcome

Defend the complete evidence chain under skeptical technical, customer-impact, privacy, and leadership follow-up.

### Required artifact

Capstone report package and five-minute technical briefing.

### Completion test

Every figure is reproducible, per-population errors are visible, limitations constrain the conclusion, recommendations name owners and success metrics, and the retest could falsify the claimed improvement.

### Estimated time

8 additional focused hours.

### Required resources only

- [Executive-summary template](../../templates/executive-summary.md) — `[L3 Integrated]` `[Required]`
- [Retest-plan template](../../templates/retest-plan.md) — `[L3 Integrated]` `[Required]`

### Optional deeper resources

- [OpenTelemetry documentation](https://opentelemetry.io/docs/) — `[L3 Integrated]` `[Optional]` provenance and correlation context

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Design reproducible original research; reason about confidence calibration, sensitivity, drift, rule overlap, version effects, sampling bias, negative results, peer review, and production validation.

### Hands-on outcome

Investigate one original question, compare alternatives, improve the capstone based on its limitations, rerun after a defensive change, and publish a sanitized portfolio-quality research package.

### Interview outcome

Teach the result, state where confidence ends, defend negative or ambiguous evidence, and propose the smallest safe next validation step.

### Required artifact

Reproducible research paper, data dictionary, machine-readable summary, improved artifact, retest result, and public-safe briefing.

### Completion test

An independent reviewer can reproduce the result, audit evidence provenance, understand competing explanations, and reach the same bounded conclusion.

### Estimated time

10–15 additional focused hours.

### Required resources only

- Primary sources and implementation/version documentation for the selected question — `[L4 Deep]` `[Required]`

### Optional deeper resources

- Statistical methods appropriate to the chosen design — `[L4 Deep]` `[Optional]`

## Common misconceptions

- A plausible mechanism is not evidence that it caused the result.
- More charts do not compensate for missing controls or population labels.
- A recommendation without a measurable retest is incomplete.
- Severity should not be inflated to compensate for weak evidence.

## Production limitations

The lab lacks production scale, customer populations, privacy and retention controls, cross-team ownership, business metrics, natural incidents, adversary adaptation, and deployment risk. Report those gaps explicitly.

## Interview questions

1. How do you distinguish a demonstration from a defensible finding?
2. What alternative explanations would you test first?
3. How do you define a retest that proves defensive improvement?

## Related lab components

- `lab/analysis/analyze.py`
- `lab/fixtures/requests.jsonl`
- `lab/reports/`
- `templates/`

