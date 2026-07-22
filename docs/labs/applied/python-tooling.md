# Python tooling lab

This lab turns local evidence into transparent telemetry and demonstrates bounded
concurrency and retries. It is assigned only after Modules 01-08.

## Lab contract

- Authorization boundary: offline fixture or fixed loopback API
- Target: `lab/fixtures/requests.jsonl` and `http://localhost:8080`
- Adversary objective: build safe, inspectable tooling for attack evidence
- Protected action: none for telemetry/health; retry reaches the accepted synthetic operation
- Baseline: deterministic fixture counts and one local health request
- Hypothesis: explicit work/attempt ceilings produce reproducible evidence without unbounded traffic
- Changed variable: concurrency or retry attempt within the assigned command
- Fixed variables: fixture, URL, seed, timeout, total work, and output schema
- Success: expected JSON shape; six health results; or `503 -> 200` within two attempts
- Evidence: terminal JSON and tooling unit tests
- Limitations: standard-library local client, small fixture, no production latency distribution
- Cleanup: reset/stop the local API; offline telemetry needs none
- Remediation: unsafe clients gain local validation and explicit total/concurrency/timeout/attempt budgets
- Retest: rerun the same command plus rejection boundary tests

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
for setup, interpretation, failure modes, cleanup, and knowledge checks.
