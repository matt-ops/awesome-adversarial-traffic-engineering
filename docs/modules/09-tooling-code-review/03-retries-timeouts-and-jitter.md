# Retries, timeouts, and jitter

<!-- source-ids: python-standard-library, aws-builders-library-timeouts-retries-jitter, aate-local-lab -->

## Progress

- Module: 09 - Tooling and secure code review
- Lesson: 3 of 4
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [Async and bounded concurrency](02-async-and-bounded-concurrency.md)
  - Local `/api/reports/unstable` fixture running
- Next lesson: Secure code review

## Role outcome

Recognize and reproduce client-side retry amplification, then implement a bounded
timeout, attempt budget, exponential backoff, and jitter for the local fixture.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PRACTITIONER_PERSPECTIVE | [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) | timeouts, retries/backoff, jitter, conclusion | Grounds failure and amplification behavior | Practitioner guidance from one large provider; timeout values and retry policy require target-specific measurement. |
| OFFICIAL_DOCUMENTATION | [Python `asyncio.sleep`](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep) | cooperative delay | Grounds the lab scheduling primitive | Lessons link to the exact subsection used; not all Python documentation is assigned. |
| LAB_SPECIFIC | [Python tooling lab](../../labs/applied/python-tooling.md) | deterministic fail-once route | Supplies bounded observation | Deliberately small and vulnerable; results do not generalize to production systems. |

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

**Exact section, chapter, or unit:** read Timeouts; Retries and backoff; Jitter; and Conclusion, including the layered-retry example and token-bucket discussion

**Estimated time:** 65 minutes

**What to focus on:** timeout selection, side effects after timeout, overload amplification, retry location, capped exponential backoff, jitter purpose, and a finite retry budget

**What to skip:** provider SDK configuration and service-specific percentile values

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

### Exact actions or commands

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

## Check your understanding

1. A client times out while waiting, but the server already accepted the operation. Why does the timeout not prove that server-side work stopped?
2. Which attempt budget, deadline, concurrency, and rate limits bound the extra work created by retries?
3. Two clients use the same exponential backoff but add random jitter. What does jitter change, and which maximum does jitter not change?
4. An application client, service proxy, and SDK each retry twice. Why can those independent layers multiply the total attempts?
5. The local fixture returns `403` for an authorization decision. Why should the retry policy stop instead of treating `403` as a transient failure?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A timeout only proves that the caller stopped waiting before its deadline.** The server, queue, or dependency may continue processing accepted work after the client has abandoned the response.

- **2. A finite per-operation attempt budget and overall deadline cap retries, while concurrency and rate ceilings bound simultaneous and scheduled work.** All limits should be enforced before another attempt starts.

- **3. Jitter changes when clients begin later attempts, reducing synchronized retry bursts.** It does not increase or reduce the configured maximum number of attempts by itself.

- **4. Each outer layer can repeat every attempt made by the layer below, creating multiplicative amplification.** Retry ownership and budgets must therefore be coordinated across the full request path.

- **5. `403` represents the exercise's authorization outcome rather than the declared transient failure class.** Repeating the same unauthorized request adds load without changing the missing permission.

</details>

## Next lesson

Continue to [Secure code review](04-secure-code-review.md).
