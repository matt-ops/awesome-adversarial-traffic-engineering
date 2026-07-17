# Phase 3 DDoS scenario audit

## Name changes

| Before | After | Decision |
|---|---|---|
| `endpoint-specific` | `endpoint-cost-observation` | Renamed because no endpoint-specific quota or admission profile exists. |
| `workflow-aware` | `workflow-sequence-observation` | Renamed because no workflow-aware identity, reservation, unfinished-work, or admission control exists. |

The Nginx edge has one global per-IP rate limit for every request. It is neither
varied nor used as a before/after treatment by these scenarios. No endpoint- or
workflow-specific Nginx control was added.

## `cheap-expensive`

- Scenario name: `cheap-expensive`
- Traffic generated: `GET /health` paired with `GET /api/reports/expensive?work=100`.
- Control actually active: Global per-IP Nginx limit; no route-specific admission control.
- Expected service effect: The bounded report performs deterministic CPU work and takes longer than the health request in the local pair.
- Assertion proving the effect: Report JSON has `work=100`; k6 checks report duration is greater than health duration.
- Protected workflow or resource: Toy application CPU work and the legitimate health route.
- Before/after comparison: Paired route-cost observation under the same iteration/configuration; no control configuration changes.
- Limitation: Single-process synthetic latency is not a capacity or production-control result.

## `cache-bypass`

- Scenario name: `cache-bypass`
- Traffic generated: Setup primes `cache_key=fixed`; each iteration pairs the warmed fixed key with a unique `bypass=true` key.
- Control actually active: The application `CACHEABLE_REPORTS` cache; global per-IP Nginx limit.
- Expected service effect: The fixed request uses cached state while the bypass request performs fresh bounded work and returns the same deterministic result.
- Assertion proving the effect: `cache_hit` is true for fixed and false for bypass; digest prefixes match.
- Protected workflow or resource: Toy report CPU work avoided by the application cache.
- Before/after comparison: Warmed cache path versus explicit bypass path in each iteration.
- Limitation: This is not CDN behavior, cache-key normalization research, or a production-cache mitigation test.

## `identity-key`

- Scenario name: `identity-key`
- Traffic generated: Setup sends two calls with `session_id=fixed`; each iteration pairs the same fixed key with `session_id=rotated-<iteration>`.
- Control actually active: Real synthetic per-session application quota after two accepted calls; global per-IP Nginx limit.
- Expected service effect: The exhausted fixed key is rejected while a caller-rotated key is accepted with its own count.
- Assertion proving the effect: Fixed response is `429`; rotated response is `200` with `session_count=1`.
- Protected workflow or resource: Bounded report work counted by `LIMITED_REPORT_CALLS`.
- Before/after comparison: Same endpoint/work under exhausted versus newly rotated caller-selected keys.
- Limitation: It proves only the exact caller-controlled-key weakness; it does not bypass or compare the separate per-IP Nginx control.

## `endpoint-cost-observation`

- Scenario name: `endpoint-cost-observation`
- Traffic generated: Same report endpoint with `work=1` and `work=100`.
- Control actually active: Global per-IP Nginx limit only; no endpoint-specific quota/admission treatment.
- Expected service effect: The high-work input executes the declared larger bounded work and takes longer locally.
- Assertion proving the effect: JSON bodies preserve work values 1/100; k6 checks high-work duration is greater.
- Protected workflow or resource: Input-dependent toy report CPU work.
- Before/after comparison: Low versus high work on the same endpoint/configuration; observation only.
- Limitation: It does not prove endpoint-specific mitigation, shedding, or an exploitable production cost ratio.

## `workflow-sequence-observation`

- Scenario name: `workflow-sequence-observation`
- Traffic generated: `GET /api/search?q=demo` followed by `GET /api/products/demo-1`.
- Control actually active: Global per-IP Nginx limit only; no workflow-aware quota, identity graph, reservation, or admission control.
- Expected service effect: The first step exposes `demo-1` and the second resolves that same synthetic product.
- Assertion proving the effect: Search results contain `demo-1`; product response has ID `demo-1` and nonnegative availability.
- Protected workflow or resource: Read-only search-to-detail sequence; no protected mutation.
- Before/after comparison: Two ordered observations, not a control before/after comparison.
- Limitation: Sequence continuity does not prove workflow recognition or mitigation.

## `retry-amplification`

- Scenario name: `retry-amplification`
- Traffic generated: The same unique operation is requested once and retried once.
- Control actually active: Deterministic fail-once application fixture and an explicit one-retry client budget; global per-IP Nginx limit.
- Expected service effect: One logical operation produces two requests: deliberate `503`, then accepted attempt 2.
- Assertion proving the effect: First status is `503`; retry is `200` for the same operation with `attempt=2`.
- Protected workflow or resource: Bounded retry/request budget for the toy report operation.
- Before/after comparison: Initial attempt versus exactly one retry; no mitigation profile changes.
- Limitation: It does not model dependency fan-out, side-effect ambiguity, or a general retry library.

## `recovery`

- Scenario name: `recovery`
- Traffic generated: Each iteration calls `GET /api/reports/expensive?work=50`; teardown calls `GET /health`.
- Control actually active: Global per-IP Nginx limit; no queue, load shedding, or endpoint admission treatment.
- Expected service effect: Bounded work completes and immediate post-traffic health returns within the documented local bound.
- Assertion proving the effect: Work body is `50`; teardown health is `200` with duration below 1,000 ms.
- Protected workflow or resource: Immediate toy-app health after bounded report CPU work.
- Before/after comparison: Pressure phase followed by one post-traffic probe; no control change.
- Limitation: One health response does not prove sustained recovery, queue drain, dependency recovery, capacity, or production resilience.
