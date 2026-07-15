# Synthetic finding: request-local scoring misses workflow context

> Synthetic educational finding; not a production assessment.

## Summary

The fixture detector can identify deliberately obvious high-cost traffic, but its request-local reasons do not establish the account, session, or workflow objective. A production action based only on these reasons could misclassify legitimate automation or fast accessibility-like interaction.

## Evidence

The deterministic fixture produces a perfect small-sample confusion matrix because abuse examples were intentionally constructed around the educational rules. This is validation of implementation consistency, not evidence of general detection quality.

## Recommendation

Keep reasons in observe-only mode, add workflow and population state, expand legitimate fixtures, and require per-population metrics before considering stronger actions.

## Retest

Add browser test automation, accessibility-like, degraded-client, and distributed low-rate fixtures that do not share the seeded rule features. Recalculate metrics and require the documented false-positive ceiling without reducing recall below the agreed synthetic target.

## Limitations

No production traffic, customer data, commercial control, browser sensor, protocol fingerprint, or enforcement feedback was evaluated.

