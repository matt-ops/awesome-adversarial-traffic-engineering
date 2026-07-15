# Module 5: Edge controls and DDoS resilience

## Why this matters

Traffic volume is only one route to denial of service. The same request rate can create radically different cost depending on connections, streams, cacheability, state changes, queues, and dependencies. Safe research measures the exhausted resource and recovery.

## Role outcomes

You can reason across L3, L4, and L7, choose the right metrics, design bounded local experiments, compare naive and workflow-aware controls, and communicate service and customer tradeoffs.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Explain L3, L4, and L7 at a high level; bps, pps, rps, new connections, concurrency, latency, errors, and recovery; expensive endpoints; rate limits; caching; challenges; load shedding; and flash-crowd ambiguity.

### Hands-on outcome

Use a dry run to compare the planned cost of a cheap and bounded expensive local endpoint. Identify hard request, rate, concurrency, duration, and abort ceilings without generating meaningful load.

### Interview outcome

Explain DDoS by exhausted resource and metric, why equal request rates can have unequal impact, why per-IP limiting is incomplete, and how to bound a local test.

### Required artifact

One-page safe Layer 7 test plan with objective, target, cheap/expensive cases, caps, metrics, abort thresholds, cleanup, and recovery check.

### Completion test

Classify five scenarios by layer, exhausted resource, metric, and mitigation; reject an unsafe rate; and explain attack-versus-flash-crowd uncertainty.

### Estimated time

3 focused hours.

### Required resources only

- [CISA DoS guidance](https://www.cisa.gov/news-events/news/understanding-denial-service-attacks) — `[L1 Foundation]` `[Required]`
- [AATE DDoS-by-resource concept](../../docs/concepts/ddos-by-exhausted-resource.md) — `[L1 Foundation]` `[Required]`

### Optional deeper resources

- [Cloudflare DDoS overview](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) — `[L1 Foundation]` `[Recommended]` vendor-specific overview

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Explain constant rate versus burst, cheap versus expensive work, cache hit/miss, retry amplification, endpoint-specific and workflow-level limits, p50/p95/p99, errors, timeouts, saturation, and recovery time.

### Hands-on outcome

Run a hard-capped local k6 scenario against cheap and expensive endpoints. Compare no control, naive per-IP limiting, and a workflow-aware control while recording latency, errors, in-flight work, and recovery.

### Interview outcome

Defend the traffic envelope, interpret the first saturated metric, and explain why a mitigation may shift pressure or harm legitimate bursts.

### Required artifact

Bounded experiment report with configuration printout, charts or tables, abort evidence, cheap/expensive comparison, mitigation comparison, and limitations.

### Completion test

Reproduce the test within hard caps, identify the bottleneck supported by data, distinguish correlation from root cause, and explain recovery.

### Estimated time

5 additional focused hours.

### Required resources only

- [Grafana k6 documentation](https://grafana.com/docs/k6/latest/) — `[L2 Applied]` `[Required]` local execution and thresholds only
- [AWS Builders’ Library: load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) — `[L2 Applied]` `[Required]` vendor-specific design reference

### Optional deeper resources

- [AWS WAF rate-based rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html) — `[L2 Applied]` `[Recommended]` vendor-specific

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Explain HTTP/2 stream pressure, HTTP/3 and QUIC fundamentals, origin shielding, backpressure, queue management, dependency exhaustion, retries with jitter, graceful degradation, and cross-layer mitigation.

### Hands-on outcome

Run multiple bounded resilience experiments that compare request shape, endpoint cost, caching, retry policy, and naive versus workflow-aware controls. Correlate client, edge, application, and dependency evidence.

### Interview outcome

Design a safe engagement for an edge-protected service, including threat families, baseline, monitoring, customer-impact gates, communication, mitigation ownership, and retest.

### Required artifact

Integrated resilience chapter containing architecture, test matrix, quantitative results, mitigation tradeoffs, recovery, and retest.

### Completion test

Defend why the selected metric represents the constrained resource, show one control displacement effect, and propose a lower-risk retest.

### Estimated time

7 additional focused hours.

### Required resources only

- [AWS DDoS resiliency whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/welcome.html) — `[L3 Integrated]` `[Required]` vendor-specific architecture reference
- [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — `[L3 Integrated]` `[Required]`

### Optional deeper resources

- [Prometheus documentation](https://prometheus.io/docs/) — `[L3 Integrated]` `[Optional]`
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) — `[L3 Integrated]` `[Optional]`

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Investigate anycast, connection and stream admission, origin shielding, queue disciplines, backpressure, dynamic mitigation, dependency isolation, protocol-specific pressure, and control stability.

### Hands-on outcome

Extend one local resilience control—such as admission control, queue cap, cache shielding, or dependency bulkhead—and compare it with the baseline under identical hard-capped traffic.

### Interview outcome

Teach the control’s failure mode, operational cost, observability, legitimate-traffic risk, rollback, and the gap between a single-node lab and distributed production.

### Required artifact

Original resilience extension with model, implementation, measured comparison, failure and recovery evidence, and production-validation proposal.

### Completion test

The extension improves a declared metric without hiding unacceptable errors or shifting unmeasured harm, and the result is reproducible within safety ceilings.

### Estimated time

8–12 additional focused hours.

### Required resources only

- Primary design or protocol sources for the chosen control — `[L4 Deep]` `[Required]`

### Optional deeper resources

- [RFC 9113: HTTP/2](https://www.rfc-editor.org/rfc/rfc9113) — `[L4 Deep]` `[Optional]`
- [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114) — `[L4 Deep]` `[Optional]`
- [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000) — `[L4 Deep]` `[Optional]`

## Common misconceptions

- DDoS is not synonymous with high bandwidth.
- Per-IP limits do not represent accounts, sessions, workflows, streams, or shared networks.
- Low p50 does not rule out severe tail latency or a harmed population.
- A load generator result is not a production capacity guarantee.

## Production limitations

The local lab does not model global anycast, scrubbing, multi-region failover, carrier behavior, CDN scale, real customer bursts, shared-service contention, distributed dependencies, or production incident response.

## Interview questions

1. How do bps, pps, rps, connections, and concurrency map to exhausted resources?
2. How would you distinguish an attack from a flash crowd?
3. Why might rate limiting solve one bottleneck but worsen another?

## Related lab components

- `lab/load/`
- `lab/edge/nginx.conf`
- `lab/app/main.py`
- `lab/safety.py`

