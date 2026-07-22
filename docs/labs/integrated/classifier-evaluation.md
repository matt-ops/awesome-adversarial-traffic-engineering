# Classifier-threshold and adversarial-drift lab

- Authorization boundary: offline synthetic aggregate fixture only
- Required working directory: repository root
- Target: `lab/fixtures/classifier_tradeoffs.json`; no socket or service
- Objective: calculate threshold tradeoffs before and after an adapted abusive population changes score
- Protected action: compare synthetic stock and adapted abuse completions, not only score or decision
- Baseline: fixed baseline-window scores, populations, labels, thresholds, and cost model
- Hypothesis: the high threshold will look precise at baseline but miss adapted abuse after drift
- Changed variable: score window changes from `baseline` to `post-adaptation`
- Fixed variables: populations, ground-truth labels, thresholds, protected completion rules, and cost fields
- Thresholds: `0.50` and `0.75`
- Success criterion: protected-action completion, not a lower detector score
- Evidence: confusion matrices, rates, volumes, costs, delayed-label coverage, and protected completions
- Limitation: synthetic aggregate scores do not train, validate, or represent a production classifier
- Remediation: version and monitor the relied-upon signals while preserving legitimate near-neighbor outcomes
- Retest: repeat the exact fixture schema and both operating points after a declared rule or signal change
- Output: deterministic JSON to standard output; saving is optional
- Cleanup: none unless the learner optionally redirects output

## Preflight

Confirm Python 3.12 and the tracked fixture:

```powershell
python --version
python -c "from pathlib import Path; assert Path('lab/fixtures/classifier_tradeoffs.json').is_file()"
```

## Exact command

```powershell
python -m lab.analysis.classifier_tradeoffs
```

The command calculates known-label confusion matrices, precision, recall,
false-positive and false-negative rates, flags, costs, near-neighbor challenges,
unknown-label coverage, and stock/adapted protected completions for both score
windows. Unknown labels never enter the matrix.

## Expected comparison

| Window | Threshold | TP | FP | TN | FN | Precision | Recall | Flags | Near-neighbor challenges | Stock completions | Adapted completions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.50 | 100 | 700 | 9,300 | 0 | 0.125 | 1.0 | 900 | 700 | 7 | 3 |
| baseline | 0.75 | 100 | 0 | 10,000 | 0 | 1.0 | 1.0 | 100 | 0 | 7 | 3 |
| post-adaptation | 0.50 | 100 | 700 | 9,300 | 0 | 0.125 | 1.0 | 900 | 700 | 7 | 3 |
| post-adaptation | 0.75 | 70 | 0 | 10,000 | 30 | 1.0 | 0.7 | 70 | 0 | 7 | 28 |

The low threshold's synthetic post-adaptation cost is `$2,250` review,
`$72` challenge operation, `$840` near-neighbor impact, and `$3,162` total.
The separate million-event base-rate example produces `1,000` false alerts and
`900` true alerts, for precision `0.4737`.

## Failure guidance

- `FileNotFoundError`: return to the repository root.
- A changed metric: inspect fixture counts, label handling, and `>=` threshold semantics.
- An unknown label in the matrix: stop; the analysis contract has been violated.
- A saved output file appears under a tracked path: remove it and keep optional diagnostics local.

## Interpretation and retest

The `0.75` threshold is attractive at baseline but loses the adapted population.
Remediation must compare stock and adapted completions, near-neighbor friction,
flag volume, cost, delayed-label coverage, and versioned score distributions.
Repeat this exact fixture and schema after the declared rule or signal change.
