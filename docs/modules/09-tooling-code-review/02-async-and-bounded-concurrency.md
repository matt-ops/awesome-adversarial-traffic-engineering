# Async and bounded concurrency

<!-- source-ids: python-standard-library, pytest-documentation, aate-local-lab -->

## Progress

- Module: 09 - Tooling and secure code review
- Lesson: 2 of 4
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [Python telemetry as evidence](01-python-telemetry.md)
  - Local synthetic API setup from [the lab page](../../labs/applied/local-api.md)
- Next lesson: Retries, timeouts, and jitter

## Role outcome

Build a local request population with explicit total-work and in-flight ceilings,
then explain where concurrency begins, waits, and ends.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Python documentation](https://docs.python.org/3/) | `asyncio` coroutines and tasks; `Semaphore`; `gather`; `to_thread` | Grounds the concurrency model and the exact APIs used by the bounded client | Lessons link to the exact subsection used; not all Python documentation is assigned. |
| OFFICIAL_DOCUMENTATION | [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) | How to parametrize fixtures and test functions | Grounds ceiling boundary tests | Only the features used by the code-review exercises are assigned. |
| LAB_SPECIFIC | [Python tooling lab](../../labs/applied/python-tooling.md) | bounded concurrency command | Supplies observed output | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

| Term | Meaning | Bound in the lab |
|---|---|---|
| Coroutine | Pausable async function invocation | one `one(sequence)` per requested item |
| Task | Scheduled coroutine | gathered into one result list |
| Semaphore | Permit counter around the scarce operation | at most `concurrency` fetches in flight |
| Thread handoff | Runs blocking `urllib` away from the event loop | one handoff per admitted fetch |
| Total work | All operations created | validated by `LoadEnvelope.total_requests` |

Concurrency is not request rate. Six tasks with a semaphore of two can still
complete in a burst if each response is fast. A safe client therefore needs
separate ceilings for in-flight work, total work, duration, and rate whenever
it produces repeated traffic.

## Required external instruction

### Coroutine and task assignment

**Direct link:** [`asyncio` coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html)  
**Exact section, chapter, or unit:** Coroutines, Creating Tasks, Running Tasks Concurrently (`gather` only), and Running in Threads  
**Estimated time:** 45 minutes  
**What to focus on:** coroutine versus execution, task scheduling, result ordering, exception propagation, and blocking I/O handoff  
**What to skip:** subprocesses, queues, streams, low-level event loops, and cross-thread scheduling  
**Expected takeaway:** trace one operation from coroutine creation through task scheduling, thread handoff, response, and gathered result.

### Semaphore assignment

**Direct link:** [Synchronization primitives](https://docs.python.org/3/library/asyncio-sync.html)  
**Exact section, chapter, or unit:** Semaphore and the warning that asyncio synchronization primitives are not thread-safe  
**Estimated time:** 25 minutes  
**What to focus on:** permit acquisition, release on exceptional paths, and why an in-flight ceiling differs from a total-work ceiling  
**What to skip:** Event, Condition, Barrier, and thread synchronization APIs  
**Expected takeaway:** identify the precise code region protected by the semaphore and prove its maximum simultaneous occupancy.

## Course bridge

`bounded_fetch()` validates the local URL and a conservative envelope before it
creates tasks. `async with semaphore` releases a permit even when a request
raises. `gather()` returns results in input order, which is not proof they
completed in that order.

!!! warning "Safety boundary"
    The exercise targets only the bundled loopback service. Its ceilings are
    educational defaults, not authorization to direct concurrent traffic elsewhere.

## Worked example

For `total=6` and `concurrency=2`, six tasks exist but only two may enter the
fetch region. If task 1 takes 200 ms and task 2 takes 20 ms, task 2 can free the
next permit first while the final `gather()` list still places result 1 before
result 2. Sequence labels preserve planned order; timestamps reveal completion.

## Guided exercise

### Objective

Observe bounded concurrency and distinguish task count, in-flight count, rate,
and output order.

### Setup

Start the local API as described in the lab page and confirm `/health` returns
`200`. Open `bounded_fetch()` before executing it.

### Exact actions or commands

1. Mark the target validation, envelope validation, semaphore, thread handoff,
   and gather call in the source.
2. Execute `python -m lab.tooling.client concurrent --total 6 --concurrency 2`.
3. Confirm six sequence values and successful health responses.
4. Repeat with `--concurrency 1`; compare meaning, not just elapsed time.
5. Try `--concurrency 6`; record the rejection and the ceiling that caused it.
6. Add a timeline diagram showing created, admitted, completed, and serialized.

### Expected output

The first two commands return six result objects. The excessive concurrency
case raises a safety error before any request is issued.

### Interpretation

Successful requests prove only that the local client respected its tested
envelope and the fixture answered. They do not demonstrate a production-safe
rate, distributed-load behavior, or precise simultaneous execution.

### Common failure modes

- Calling `async def` code concurrent before it is scheduled
- Using task count as the in-flight ceiling
- Calling blocking I/O directly inside the event loop
- Assuming `gather()` output order is completion order
- Raising concurrency to compensate for an unexplained timeout

### Cleanup

Stop the local API after saving the trace.

## Why this matters offensively

Browser agents and abuse clients coordinate parallel workflows. An operator who
cannot bound work may create an accidental availability test, contaminate the
experiment, or mistake client queueing for a target control.

## Check your understanding

1. The exercise creates a coroutine object for one local fetch. What must happen before the coroutine begins executing inside the event loop?
2. A semaphore has a limit of three around the fetch operation. Which simultaneous work does that semaphore bound?
3. Why does the async client call `asyncio.to_thread()` around the blocking `urllib` request?
4. Tasks finish in a different order from the input list, but `asyncio.gather()` returns an ordered result list. Which order does `gather()` preserve?
5. Before creating any concurrent tasks, which authorization, destination, and hard-envelope checks must pass?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The coroutine must be awaited directly or scheduled as a task while an event loop is running.** Creating the coroutine object alone does not execute the fetch body.

- **2. The semaphore bounds fetch operations that have entered its protected region at the same time.** It limits in-flight concurrency, not necessarily requests started per second.

- **3. `urllib` blocks the calling thread while waiting for I/O.** Moving that call to a worker thread prevents the blocking operation from freezing the event loop and unrelated coroutines.

- **4. `gather()` returns results in the order of the input awaitables, not completion order.** Separate timing evidence is needed when the learner wants to analyze which request finished first.

- **5. Written authorization, fixed loopback target validation, redirect safety, total-work bounds, concurrency bounds, timeouts, and abort conditions must be validated before task creation can produce network activity.**

</details>

## Next lesson

Continue to [Retries, timeouts, and jitter](03-retries-timeouts-and-jitter.md).
