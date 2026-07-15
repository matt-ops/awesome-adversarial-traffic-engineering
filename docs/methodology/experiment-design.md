# Experiment design

A useful offensive test is a comparison, not a sequence of improvisations.

| Field | Question |
|---|---|
| Objective | Which adversarial outcome matters? |
| Protected action | What server-side state or service effect proves it? |
| Baseline | What happens to the legitimate client and the simplest adversary? |
| Hypothesis | What result do you predict and what would disprove it? |
| Changed variable | What one property or coherent signal set changes? |
| Fixed variables | Which target, workflow, state, versions, and timing stay fixed? |
| Evidence | Which request IDs, traces, state queries, and health metrics prove the result? |
| Limitations | Which confounders and claims remain unresolved? |
| Retest | Can the identical attack be repeated after remediation? |

Changing a detector score is not enough. If the original objective was to
reserve inventory, the experiment must repeat that reservation and verify the
server-side state. If the objective was service degradation, it must measure the
resource, health signal, error/latency effect, and recovery.
