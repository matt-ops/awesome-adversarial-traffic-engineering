# Retries, timeouts, and jitter

<!-- source-ids: python-standard-library, aws-builders-library-timeouts-retries-jitter, aate-local-lab -->

> **Progress**
>
> Module: 09 - Tooling and secure code review
>
> Lesson: 3 of 4
>
> Depth: Applied
>
> Estimated time: 3 hours
>
> Prerequisites: Async and bounded concurrency
>
> Artifact: `artifacts/module-09/retry-budget.md`
>
> Next: Secure code review

## Role outcome

Recognize and reproduce client-side retry amplification, then implement a bounded
timeout, attempt budget, exponential backoff, and jitter for the local fixture.

## Prerequisites

- [Async and bounded concurrency](02-async-and-bounded-concurrency.md)
- Local `/api/reports/unstable` fixture running

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PRACTITIONER_PERSPECTIVE | [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) | timeouts, retries/backoff, jitter, conclusion | Grounds failure and amplification behavior |
| OFFICIAL_DOCUMENTATION | [Python `asyncio.sleep`](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep) | cooperative delay | Grounds the lab scheduling primitive |
| LAB_SPECIFIC | [Python tooling lab](../../labs/applied/python-tooling.md) | deterministic fail-once route | Supplies bounded observation |

## Mental model

```text
one logical operation
  attempt 1 --503--> delay(base + jitter)
  attempt 2 --200--> stop

maximum calls = logical operations × attempts per retrying layer
three layers × three attempts each can cause 3 × 3 × 3 = 27 calls
```

A timeout limits waiting; it does not cancel work already accepted by a remote
service. A retry repeats an operation; it is safe only when failure class,
side effects, and idempotency are understood. Backoff increases spacing. Jitter
desynchronizes clients. None of those mechanisms replaces an attempt budget.

## Required external instruction

### Required resilience assignment

**Direct link:** [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

**Exact assignment:** read Timeouts; Retries and backoff; Jitter; and Conclusion, including the layered-retry example and token-bucket discussion

**Estimated time:** 65 minutes

**Focus on:** timeout selection, side effects after timeout, overload amplification, retry location, capped exponential backoff, jitter purpose, and a finite retry budget

**Skip:** provider SDK configuration and service-specific percentile values

**Expected takeaway:** decide whether a failure is retryable, where retry belongs, and the maximum calls one logical operation can produce.

## Course bridge

The local route returns `503` once for each new `operation_id`, then `200`.
`fetch_with_retry()` accepts at most three attempts, a two-second timeout, and a
quarter-second base delay. It records each status and the planned delay. Its
seed makes the teaching trace reproducible; real clients should avoid synchronized schedules.

!!! note "Common misconception"
    Jitter does not reduce the maximum number of requests. It changes their
    timing. The attempt budget bounds work; backoff and jitter shape arrival.

## Worked example

Suppose a browser action calls API A, which calls B, which calls C. Each layer
uses three total attempts. A persistent failure at C can produce 27 calls to C
for one browser action. Moving retry ownership to one layer with three attempts
reduces that maximum to three. The correct owner depends on side effects,
deadlines, visibility, and whether earlier work can be safely repeated.

## Guided exercise

### Objective

Capture a fail-once retry trace and calculate its work and time budgets.

### Setup

Start/reset the local API. Open `fetch_with_retry()` and the `unstable_report()`
route side by side.

### Actions

1. Choose a fresh `operation_id` by appending it to the target query string.
2. Execute `python -m lab.tooling.client retry --target "http://localhost:8080/api/reports/unstable?operation_id=lesson-09" --attempts 3`.
3. Identify status, retryability decision, next delay, and stop condition.
4. Repeat the same operation ID; explain why the first response is now `200`.
5. Calculate maximum request count and maximum client wait from the configured bounds.
6. Try `--attempts 4`; verify rejection happens before traffic.
7. Write a test case for a non-retryable `403` that must stop after one attempt.

### Expected output

For a fresh operation, the trace contains `503` followed by `200`; the second
event ends the loop. Reusing the operation ID returns `200` immediately. Four
attempts are rejected with `attempts must be 1..3`.

### Interpretation

The route is stateful and deterministic. Its result teaches retry mechanics; it
does not estimate real failure rates, network timeout distribution, or a safe
production policy.

### Common failure modes

- Retrying every status, including authorization failures
- Retrying a side-effecting operation without idempotency evidence
- Multiplying attempts at multiple layers
- Choosing a timeout without connection and request-path measurements
- Adding jitter but omitting a total deadline or attempt budget

### Cleanup

Reset or stop the local API and save the two traces.

## Why this matters offensively

Retry policy is part of the attack surface. An adversary can look for expensive,
retryable failures or client behaviors that multiply one action into many backend
calls. A safe red-team proof bounds that observation instead of inducing an outage.

## Required artifact

`artifacts/module-09/retry-budget.md` with the trace, failure classification,
attempt formula, maximum wait, retry owner, idempotency question, and limitations.

## Pass gate

1. Does timeout prove the server stopped work?
2. What bounds retry-generated work?
3. What does jitter change?
4. Why can layered retries amplify load?
5. When is `503` not enough to justify a retry?
6. Why should `403` stop in this exercise?

## Answer key

<details><summary>Check your reasoning</summary>

1. No. The caller stopped waiting; accepted server work may continue.
2. A finite attempt/operation budget, plus a deadline and concurrency/rate ceilings.
3. Attempt timing across clients, reducing synchronization; not the maximum count.
4. Each layer can repeat every attempt made by the layer below it.
5. When the operation has unsafe side effects, the deadline is exhausted, or overload makes retries harmful.
6. It is an authorization decision, not the fixture's transient failure class.

</details>

## Next lesson

Continue to [Secure code review](04-secure-code-review.md).
