# Module 6: Practical Python and secure code review

## Why this matters

Adversarial traffic research depends on small tools that safely collect, transform, and explain evidence. The same role must recognize reliability and security flaws—especially unbounded work—that turn normal failure into an incident.

## Role outcomes

You can write tested, bounded Python for traffic analysis and review security tooling for timeouts, retries, concurrency, authorization, validation, data handling, and resource-exhaustion risks.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Use dictionaries, sets, counters, sorting, grouping, JSONL parsing, and simple sessionization. Explain timeouts, bounded retries, bounded concurrency, type hints, tests, and the risks of missing timeouts, retry loops, and unbounded work.

### Hands-on outcome

Parse the deterministic request fixture, count events, group by session or identity, and identify one suspicious pattern. Review one small client and identify at least three security or reliability issues.

### Interview outcome

Narrate inputs, data structures, edge cases, complexity, error handling, tests, and production improvements; review code as behavior → precondition → impact → fix → regression test → telemetry.

### Required artifact

One Python log-analysis exercise with tests and one secure code-review write-up with at least three findings.

### Completion test

Run the analyzer, explain its grouping, handle a malformed line safely, and identify missing timeout, unbounded retry, and unbounded concurrency in a sample without overclaiming exploitability.

### Estimated time

5 focused hours: 3 hours for Python/log analysis and 2 hours for secure code review.

### Required resources only

- [Python `collections`](https://docs.python.org/3/library/collections.html) — `[L1 Foundation]` `[Required]` Counter and defaultdict only
- [pytest documentation](https://docs.pytest.org/) — `[L1 Foundation]` `[Required]` getting started only
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/) — `[L1 Foundation]` `[Required]` review method overview only

### Optional deeper resources

- [Python logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html) — `[L2 Applied]` `[Recommended]`

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Explain async I/O, semaphores, bounded queues, timeout scopes, retry budgets with jitter, structured logging, deterministic seeds, CLI design, type checking, and regression tests.

### Hands-on outcome

Build an asynchronous local-only client with bounded concurrency, timeout, retry budget, jitter, structured output, and tests. Complete at least three Python drills and four code-review exercises.

### Interview outcome

Defend why the client cannot target remote hosts, how retry budgets prevent amplification, and how tests prove the bounds rather than merely the happy path.

### Required artifact

Async client, test report, three exercise solutions, and four structured code reviews.

### Completion test

Tests reject external targets and excessive concurrency, terminate stalled requests, bound total attempts, and demonstrate stable seeded output.

### Estimated time

6 additional focused hours.

### Required resources only

- [Python asyncio](https://docs.python.org/3/library/asyncio.html) — `[L2 Applied]` `[Required]` tasks, timeout, and synchronization sections
- [mypy](https://mypy.readthedocs.io/) — `[L2 Applied]` `[Required]` getting started only

### Optional deeper resources

- [Semgrep rules](https://github.com/semgrep/semgrep-rules) — `[L2 Applied]` `[Optional]` pattern reference, not a substitute for review

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Explain streaming versus batch tradeoffs, sliding windows, memory bounds, session correlation, stable schemas, partial failure, test fixtures, race conditions, SSRF, broken authorization, unsafe deserialization, sensitive logging, and expensive input.

### Hands-on outcome

Complete six Python exercises and all ten secure-review exercises. Integrate parsers, detectors, metrics, and report export into one deterministic capstone command.

### Interview outcome

Solve a timed practical problem, review unfamiliar code, state realistic preconditions and impact, propose a specific fix, and add a regression test and useful telemetry.

### Required artifact

Six tested Python solutions, ten review packages, and a reproducible capstone analysis CLI.

### Completion test

From a clean fixture, one command produces the same machine-readable metrics and Markdown summary; tests cover malformed input, bounds, authorization, race or resource cases, and logging safety.

### Estimated time

10 additional focused hours.

### Required resources only

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — `[L3 Integrated]` `[Required]` categories represented by the exercises
- [OWASP API Security](https://owasp.org/www-project-api-security/) — `[L3 Integrated]` `[Required]` authorization and resource-consumption categories

### Optional deeper resources

- [PortSwigger Web Security Academy](https://portswigger.net/web-security) — `[L3 Integrated]` `[Optional]` selected relevant labs only

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Evaluate streaming architectures, backpressure, structured CLI interfaces, schema evolution, memory and CPU profiles, async cancellation, framework-specific security controls, and maintainability.

### Hands-on outcome

Turn one capstone script into a reusable typed CLI, benchmark it on larger synthetic fixtures, enforce resource bounds, document extension points, and perform a framework-level security review.

### Interview outcome

Teach the implementation tradeoffs and defend performance, safety, failure semantics, test strategy, and what production hardening remains.

### Required artifact

Versioned reusable tool with tests, benchmark, resource profile, threat model, review findings, and operator guide.

### Completion test

The tool handles a declared maximum fixture within bounded memory and time, cancels safely, emits stable schemas, rejects unsafe inputs, and passes independent review.

### Estimated time

8–12 additional focused hours.

### Required resources only

- Official documentation for the chosen Python and framework APIs — `[L4 Deep]` `[Required]`

### Optional deeper resources

- Profiling and fuzzing documentation appropriate to the tool — `[L4 Deep]` `[Optional]`

## Common misconceptions

- Async does not make work bounded; it can make unbounded work arrive faster.
- Retries without a budget, deadline, and jitter can amplify outages.
- Static analysis findings still need reachable preconditions and realistic impact.
- Passing tests do not prove authorization, safety, or correct production thresholds.

## Production limitations

Small deterministic fixtures do not represent production volume, schema drift, out-of-order streams, sensitive-data rules, deployment controls, dependency behavior, or on-call operational needs.

## Interview questions

1. How would you sessionize a large JSONL stream within bounded memory?
2. What makes an asynchronous client safe under partial failure?
3. How do you communicate a code-review finding from vulnerable behavior through regression test?

## Related lab components

- `lab/clients/safe_client.py`
- `lab/analysis/analyze.py`
- `lab/detectors/rules.py`
- `exercises/python/`
- `exercises/code-review/`

