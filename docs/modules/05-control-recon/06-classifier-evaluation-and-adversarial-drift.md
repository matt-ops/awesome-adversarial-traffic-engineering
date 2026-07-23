# Classifier Evaluation and Adversarial Drift

<!-- source-ids: scikit-learn-classification-metrics, axelsson-base-rate, google-ml-monitoring, aate-local-lab, aate-adversarial-control-loop -->
<!-- source-ledger-consistency: strict -->

## Progress

- Module: 05 - Control reconnaissance
- Lesson: 6 of 6
- Depth: Integrated
- Estimated time: 3 hours
- Prerequisites:
  - [Establish the blocked baseline](05-blocked-baseline.md)
  - Confusion-matrix arithmetic and the fixed local classifier fixture
- Next lesson: Evasion hypotheses

## Role outcome

Quantify which synthetic populations a threshold catches or harms, identify a
brittle boundary, test an adapted population, and specify the measurements a
defensive team needs after remediation.

> A lower detector score is not offensive success. The protected action remains
> the offensive success criterion.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [scikit-learn metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics) | 3.4.4.6; 3.4.4.9; binary definitions; confusion matrices at thresholds | Defines matrix cells, precision, recall, and threshold-dependent evaluation | General metric documentation; it does not choose a bot-control threshold or cost model. |
| PEER_REVIEWED_RESEARCH | [Axelsson base-rate paper](https://doi.org/10.1145/357830.357849) | Abstract; base-rate model; false-alarm constraint discussion | Grounds the low-base-rate false-positive workload | Historical intrusion-detection model; it does not evaluate this fixture. |
| OFFICIAL_DOCUMENTATION | [Google production ML monitoring](https://developers.google.com/machine-learning/crash-course/production-ml-systems/monitoring) | training-serving skew; model age; live quality; randomization | Supports drift, versioned evaluation, and delayed-label cautions | General ML operations guidance; AATE adds adversarial adaptation and protected-action proof. |
| LAB_SPECIFIC | [Classifier lab](../../labs/integrated/classifier-evaluation.md) | fixture, two score windows, two thresholds, cost fields, and expected output | Supplies deterministic populations and calculations | Synthetic aggregate counts and transparent scores; not a production detector. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | baseline, changed variable, protected effect, remediation, exact retest | Keeps classifier metrics subordinate to the offensive outcome | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

The positive class is known abuse and `score >= threshold` means flagged. A
known legitimate event that is flagged is a false positive. A known abusive
event below threshold is a false negative. An unknown label is neither one: keep
it outside the matrix and report coverage separately.

| Actual label / decision | Flagged | Allowed |
|---|---:|---:|
| Abuse | true positive (TP) | false negative (FN) |
| Legitimate | false positive (FP) | true negative (TN) |
| Unknown or delayed | covered unknown | uncovered unknown |

Every formula needs its population and denominator:

```text
precision = TP / (TP + FP)
recall = TP / (TP + FN)
false-positive rate = FP / (FP + TN)
false-negative rate = FN / (TP + FN)
class base rate = known abuse / all known labels
```

For the fixture's baseline score at threshold `0.50`:

```text
precision = 100 / (100 + 700) = 0.1250
recall = 100 / (100 + 0) = 1.0000
false-positive rate = 700 / (700 + 9300) = 0.0700
false-negative rate = 0 / (100 + 0) = 0.0000
class base rate = 100 / 10100 = 0.0099
```

At scale, a superficially small false-positive rate can still dominate. With
`1,000,000` legitimate events, `1,000` abusive events, `FPR=0.001`, and
`recall=0.90`:

```text
false positives = 1,000,000 * 0.001 = 1,000
true positives = 1,000 * 0.90 = 900
precision = 900 / (900 + 1,000) = 0.4737
```

Flagged volume drives review and challenge cost. Legitimate near-neighbors add
customer friction even when an aggregate false-positive rate looks small.

## Required external instruction

### Classification-metric assignment

**Direct link:** [scikit-learn classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
**Exact section, chapter, or unit:** 3.4.4.6 Confusion matrix and 3.4.4.9.1 Binary classification
**What to focus on:** TP, FP, TN, FN, precision, recall, and matrices at different score thresholds
**What to skip:** multiclass averaging, regression metrics, clustering metrics, and estimator selection
**Estimated time:** 25 minutes
**Expected takeaway:** calculate each rate from named counts and explain which denominator answers which control question.

### Base-rate assignment

**Direct link:** [The base-rate fallacy and the difficulty of intrusion detection](https://doi.org/10.1145/357830.357849)
**Exact section, chapter, or unit:** abstract, base-rate model, and discussion of the false-alarm constraint
**What to focus on:** why rare abuse can make false alerts dominate an apparently accurate detector
**What to skip:** reproducing every historical detector example
**Estimated time:** 25 minutes
**Expected takeaway:** substitute a legitimate population, abuse base rate, recall, and false-positive rate into one alert-workload calculation.

### Drift and delayed-label assignment

**Direct link:** [Production ML monitoring](https://developers.google.com/machine-learning/crash-course/production-ml-systems/monitoring)
**Exact section, chapter, or unit:** Check for training-serving skew; Monitor model age; Test the quality of live model on served data
**What to focus on:** versioned inputs, live-quality monitoring, unavailable labels, and sudden or slow degradation
**What to skip:** product deployment steps and unrelated numerical-stability examples
**Estimated time:** 20 minutes
**Expected takeaway:** name the population, score, label-delay, customer-impact, and protected-action measurements needed after a control change.

## Course bridge

The blocked baseline established that stock automation did not complete the
protected action. Classifier evaluation now asks what the boundary costs across
legitimate, near-neighbor, stock, adapted, and unknown populations. Module 06
then changes a declared client property and repeats the protected action.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** A threshold is an operating decision, not a universal
    quality score. Evaluate the population mix, operational cost, label delay,
    adaptation, protected effect, and exact retest together.

## Worked example

At baseline, threshold `0.75` flags all `100` known abusive events and no known
legitimate events. After adaptation, the `30` adapted events move from score
`0.80` to `0.58`. At `0.75`, precision remains `1.0000`, but recall becomes
`70 / (70 + 30) = 0.7000`. The adapted population's protected completions rise
from `3` when flagged to `28` when allowed. That result invalidates the prior
operating claim for the adapted population; it does not prove the classifier is
ineffective for every population.

## Guided exercise

### Objective

Compare thresholds `0.50` and `0.75` before and after adaptation, quantify cost
and unknown-label coverage, and select the exact remediation measurements.

### Setup

- Required working directory: repository root
- Preflight: confirm Python 3.12 and `lab/fixtures/classifier_tradeoffs.json`
- Exact target: the offline fixture only; the command opens no socket
- Fixture populations: manual legitimate, legitimate automation or
  accessibility-like near-neighbor, stock abuse, adapted abuse, and delayed label

### Exact actions or commands

```powershell
python -m lab.analysis.classifier_tradeoffs
```

1. Read `class_base_rate` and both threshold rows in `windows.baseline`.
2. Compare the same thresholds in `windows.post_adaptation`.
3. Confirm unknown labels appear only in coverage and flagged-volume fields.
4. Compare review, challenge-operation, and near-neighbor costs.
5. Use protected-action completions, not score alone, to state the offensive result.

### Expected output

The known-label base rate is `0.0099`. Baseline threshold `0.50` reports
`TP=100, FP=700, TN=9300, FN=0`, precision `0.125`, recall `1.0`, `900`
total flags including `100` delayed labels, and `700` near-neighbor challenges.
After adaptation, threshold `0.75` reports `TP=70, FP=0, TN=10000, FN=30`,
precision `1.0`, recall `0.7`, and `28` adapted protected completions.

### Interpretation

The higher threshold improves precision and removes near-neighbor challenges,
but adaptation reduces recall and increases adapted protected-action completion.
The lower threshold retains recall while creating `700` known false positives
and an estimated synthetic total operational cost of `$3,162`. Delayed labels
limit certainty because their true matrix cells are not yet known.

### Common failure modes

- Treating all `100` delayed labels as legitimate or abusive to improve a metric
- Calling a lower adapted score success without the protected-action result
- Reporting stock-client recall as if it represented the adapted population
- Choosing a threshold without customer friction and analyst cost

### Cleanup

No file is written and no process remains. If optional shell redirection was
used, remove the generated output from the ignored local directory after review.

## Why this matters offensively

A red teamer needs to show which assumption was overtrusted, who was harmed,
whether adaptation changed a protected result, and what the defender must watch
after remediation. One bypass is bounded evidence about one operating point.

## Check your understanding

1. Why are unknown or delayed labels excluded from all four confusion-matrix cells while still counted in coverage?
2. At threshold `0.75` after adaptation, which substituted counts produce recall `0.70`?
3. Why can a `0.1%` false-positive rate still create more false alerts than true alerts in the million-event example?
4. Which result establishes offensive success for the adapted population, and why is its lower score insufficient?
5. Which customer, analyst, label, drift, and protected-action measures belong in the remediation retest?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Their ground truth is not available, so assigning them to TP, FP, TN, or FN would invent evidence.** Coverage still matters because a threshold may flag or miss the delayed population and add review work before labels arrive.

- **2. Recall is `TP / (TP + FN) = 70 / (70 + 30) = 0.70`.** The stock population remains above the threshold, while the adapted population moves below it and becomes the thirty false negatives.

- **3. The legitimate base is much larger than the abusive base.** `1,000,000 * 0.001` creates `1,000` false alerts, while `1,000 * 0.90` creates only `900` true alerts, so the small rate still dominates workload.

- **4. The adapted client completes twenty-eight protected actions when the higher threshold allows it.** A lower score is merely an intermediate detector observation; the server-side protected result answers whether the adversarial objective succeeded.

- **5. Measure false-positive and false-negative rates by population, near-neighbor challenges, flagged volume, review and challenge cost, delayed-label coverage, score and browser-version drift, stock and adapted protected completions, and the exact post-remediation action result.**

</details>

## Next lesson

[Form an evasion hypothesis](../06-browser-evasion/01-evasion-hypotheses.md)
turns the brittle boundary into a controlled change with abort criteria.
