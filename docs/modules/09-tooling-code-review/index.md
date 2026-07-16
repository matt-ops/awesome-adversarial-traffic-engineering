# Module 09 - Tooling and secure code review

**Outcome:** build bounded typed Python telemetry tooling and review offensive
clients/controls for exploitable authorization, timeout, retry, and concurrency flaws.

The sequence begins after all attack domains have produced evidence.

## Foundation

Complete [Python telemetry](01-python-telemetry.md). Parse the fixed JSONL fixture,
explain every transformation, and keep observations, labels, inferences, and limits separate.

## Applied

Complete [async/bounded concurrency](02-async-and-bounded-concurrency.md) and
[retries/timeouts/jitter](03-retries-timeouts-and-jitter.md). Execute the hard
ceilings and preserve the local retry trace.

## Integrated

Complete [secure code review](04-secure-code-review.md). Trace four attacker inputs
through decisions to protected effects and design negative/positive regression tests.

## Deep

Reuse typed telemetry, bounded clients, code-flow tables, and tests in the final
report, remediation acceptance matrix, and exact retest. Complete the six Python
and ten review repetitions in the [portfolio drills](../../labs/deep/portfolio-drills.md).

Start with [Python telemetry as evidence](01-python-telemetry.md).
