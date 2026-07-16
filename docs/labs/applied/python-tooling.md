# Python tooling lab

This lab turns local evidence into transparent telemetry and demonstrates bounded
concurrency and retries. It is assigned only after Modules 01-08.

## Commands and expected results

| Command | Service required | Expected result |
|---|---|---|
| `python -m lab.tooling.client telemetry` | no | JSON counts plus limitations |
| `python -m lab.tooling.client concurrent --total 6 --concurrency 2` | local API | six `200` health results |
| `python -m lab.tooling.client retry --target "http://localhost:8080/api/reports/unstable?operation_id=lesson-09" --attempts 3` | local API | first `503`, then `200` |
| `python -m unittest lab.tests.test_tooling -v` | no | three tests pass |

Read the named function before each command. Save output, explain every field,
and distinguish fixture behavior from a general claim. The local target allowlist
and hard attempt/concurrency ceilings execute before repeated traffic.

Use [Python telemetry](../../modules/09-tooling-code-review/01-python-telemetry.md),
[bounded concurrency](../../modules/09-tooling-code-review/02-async-and-bounded-concurrency.md),
and [retry budgets](../../modules/09-tooling-code-review/03-retries-timeouts-and-jitter.md)
for setup, interpretation, failure modes, cleanup, and pass gates.
