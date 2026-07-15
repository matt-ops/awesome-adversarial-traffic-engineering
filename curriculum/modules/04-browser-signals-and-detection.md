# Module 4: Browser signals and bot detection

## Why this matters

Bot detection fails when one noisy property is treated as proof. Useful decisions combine fallible signals across layers, time, and workflow, then measure error separately for legitimate populations.

## Role outcomes

You can organize browser and traffic signals, reason about claimed identity versus observed behavior, build explainable layered scoring, evaluate precision and recall, and surface privacy, accessibility, replay, and drift risks.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Explain network/reputation, TLS/HTTP, browser/device, session/identity, and behavior/workflow signal families. Explain request-level versus session-level evidence, claimed identity versus observed consistency, precision, recall, false positives, false negatives, and why one property does not prove automation.

### Hands-on outcome

Inspect a small deterministic fixture, score three transparent rules, build a confusion matrix, and compare one rule with a combined score.

### Interview outcome

Explain a layered detector in plain language, including what it observes, why signals can disagree, how thresholds trade errors, and which legitimate users may be harmed.

### Required artifact

One-page browser-signal matrix with family, observation point, stability, forgeability, replay risk, false-positive risk, and safe use.

### Completion test

Given four populations, calculate precision and recall, identify a false positive, explain the base evidence without calling it identity proof, and recommend observe/challenge rather than unsupported blocking.

### Estimated time

3 focused hours.

### Required resources only

- [MDN Web APIs](https://developer.mozilla.org/en-US/docs/Web/API) — `[L1 Foundation]` `[Required]` Navigator, screen, and timing overviews only
- [AATE detection-science concept](../../docs/concepts/detection-science.md) — `[L1 Foundation]` `[Required]`

### Optional deeper resources

- [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector) — `[L2 Applied]` `[Recommended]` research prototype

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Explain navigator and Client Hints, locale/timezone, screen/viewport, canvas/WebGL summaries, automation properties, cross-layer and cross-context consistency, replay, temporal behavior, explainable weights, and per-population evaluation.

### Hands-on outcome

Run the local browser sensor and compare manual, headed, and headless populations. Implement or run naive and cross-layer rules, then report confusion matrices and false-positive rates by population.

### Interview outcome

Defend a shadow-mode launch, progressive actions, reason codes, and why privacy or accessibility populations require explicit measurement.

### Required artifact

Population-labeled detector report with rule reasons, threshold, precision, recall, false-positive rate, and limitations.

### Completion test

Show that a combined rule changes at least one decision, explain whether that change is better, and identify a legitimate population that would be obscured by aggregate metrics.

### Estimated time

5 additional focused hours.

### Required resources only

- [FPScanner](https://github.com/antoinevastel/fpscanner) — `[L2 Applied]` `[Required]` research prototype and limitations
- [CreepJS](https://github.com/abrahamjuliot/creepjs) — `[L2 Applied]` `[Required]` official repository only

### Optional deeper resources

- [OpenWPM](https://github.com/openwpm/OpenWPM) — `[L3 Integrated]` `[Optional]`

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Explain cross-context and temporal consistency, replay resistance, stateful scoring, workflow features, base-rate effects, feature ablation, rule overlap, feedback contamination, enforcement actions, and drift.

### Hands-on outcome

Combine browser, session, protocol, behavior, and workflow evidence for at least four populations. Compare single-signal and multi-signal results, perform feature ablation, and report per-population errors.

### Interview outcome

Design a layered detection pipeline and handle follow-up about latency, explainability, state, privacy, accessibility, drift, challenge bias, rollout, and customer impact.

### Required artifact

Capstone detection evaluation with reason codes, confusion matrices, per-population metrics, ablation, threshold rationale, and remediation/retest criteria.

### Completion test

Reproduce the report from fixtures, show one signal that appears useful in aggregate but harms a population, and choose a rollout action supported by the evidence.

### Estimated time

7 additional focused hours.

### Required resources only

- [AATE cross-layer consistency concept](../../docs/concepts/cross-layer-consistency.md) — `[L3 Integrated]` `[Required]`
- [AATE bot-detection architecture concept](../../docs/concepts/bot-detection-architecture.md) — `[L3 Integrated]` `[Required]`

### Optional deeper resources

- Relevant peer-reviewed browser measurement research — `[L3 Integrated]` `[Optional]`

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Investigate signal drift, version sensitivity, privacy and accessibility effects, confidence calibration, temporal decay, rule overlap, maintenance cost, sampling bias, and framework-independent agent behavior.

### Hands-on outcome

Repeat an experiment across versions or controlled privacy/accessibility configurations, compare at least two detection strategies, analyze overlapping reasons, and calibrate conclusions to the sample.

### Interview outcome

Teach why detection quality is a lifecycle, not a static bypass contest, and defend monitoring, rollback, retraining or rule retirement, and production validation.

### Required artifact

Drift and rule-overlap study with population slices, maintenance implications, privacy analysis, and staged validation plan.

### Completion test

The study demonstrates one changed observation, quantifies its decision effect, separates causality from correlation, and recommends a reversible lifecycle action.

### Estimated time

8–12 additional focused hours.

### Required resources only

- Primary documentation and version notes for the chosen signals — `[L4 Deep]` `[Required]`

### Optional deeper resources

- [Chromium source](https://source.chromium.org/chromium) — `[L4 Deep]` `[Optional]`
- Advanced statistical evaluation appropriate to the question — `[L4 Deep]` `[Optional]`

## Common misconceptions

- `navigator.webdriver` or any other single signal is not proof.
- Uniqueness, stability, and usefulness are different properties.
- High accuracy can hide severe errors when the base rate or population mix changes.
- Challenges alter the observed sample and can contaminate feedback.

## Production limitations

Educational weighted rules lack real population diversity, adversarial adaptation, feature pipelines, privacy governance, online latency constraints, enforcement feedback, drift monitoring, appeal data, and business-impact measurement.

## Interview questions

1. How would you evaluate a browser-fingerprinting defense?
2. What makes a signal replay-resistant, and what does not?
3. How would you avoid blocking accessibility tools or legitimate automation?

## Related lab components

- `lab/sensor/`
- `lab/detectors/rules.py`
- `lab/analysis/analyze.py`
- `lab/fixtures/requests.jsonl`

