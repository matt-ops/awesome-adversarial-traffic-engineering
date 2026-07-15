# Module 1: Web request path and network fundamentals

## Why this matters

Every abuse, signal, capacity limit, and control sits somewhere on the request path. A researcher who cannot trace the path will confuse claims made by the client with observations made by the edge or application.

## Role outcomes

You can trace a browser request through DNS, transport, TLS, edge, WAF or bot defense, load balancer, application, and dependencies; identify telemetry and exhaustion points; and explain how protocol or middlebox behavior affects observations.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Explain DNS, TCP at a functional level, the purpose of TLS, an HTTP request and response, cookies and sessions, reverse proxy, CDN, WAF, load balancer, application, dependencies, latency, error rate, and basic capacity metrics.

### Hands-on outcome

Send a request to the local `/health` endpoint, inspect request and response headers, and mark where request IDs, session state, latency, and errors are observed.

### Interview outcome

Draw and narrate `Client → DNS → CDN/edge → WAF/bot defense → load balancer → application → dependencies`, including one telemetry point, one control, and one resource limit at each relevant hop.

### Required artifact

One request-path architecture diagram with trust boundaries, telemetry sources, control points, and possible exhaustion points.

### Completion test

Trace one search request and explain basic TLS purpose, cookie/session state, response status, and where latency or capacity can be consumed without using protocol acronyms as the explanation.

### Estimated time

3 focused hours.

### Required resources only

- [MDN overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — `[L1 Foundation]` `[Required]`
- [AATE edge architecture concept](../../docs/concepts/edge-architecture.md) — `[L1 Foundation]` `[Required]`

### Optional deeper resources

- [MDN cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies) — `[L1 Foundation]` `[Recommended]`

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Explain TLS ClientHello, ServerHello, certificate validation, ALPN, connection reuse, HTTP/1.1 versus HTTP/2 at a practical level, and how proxies change observable properties.

### Hands-on outcome

Capture or use provided local fixtures to compare manual Chrome, Playwright Chromium, Python, and curl. Record TLS/HTTP version, ALPN where visible, headers, connection reuse, and limitations.

### Interview outcome

Explain why a transport or HTTP fingerprint is a pivot rather than identity proof and why the observation point must be named.

### Required artifact

Four-client protocol comparison table with observation point, evidence, uncertainty, and possible middlebox effects.

### Completion test

Given two different client traces, identify supported differences, at least two alternative explanations, and one unsafe identity inference.

### Estimated time

3 additional focused hours.

### Required resources only

- [JA4 technical details](https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md) — `[L2 Applied]` `[Required]`
- [Wireshark documentation](https://www.wireshark.org/docs/) — `[L2 Applied]` `[Required]`

### Optional deeper resources

- [RFC 9113: selected HTTP/2 overview and concepts](https://www.rfc-editor.org/rfc/rfc9113) — `[L2 Applied]` `[Recommended]`

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Connect browser, session, protocol, edge, application, cache, queue, and dependency telemetry. Explain HTTP/2 multiplexing, observable HTTP/3/QUIC fundamentals, anycast, origin shielding, and blind spots.

### Hands-on outcome

Correlate four client populations across request IDs and session IDs. Add an HTTP/2 comparison and map cheap and expensive endpoints to cache and dependency behavior.

### Interview outcome

Design telemetry for a layered bot and resilience system, including collection cost, privacy, cardinality, retention, missing data, and proxy effects.

### Required artifact

Cross-layer telemetry map and correlation report for the integrated capstone.

### Completion test

Reconstruct one client session from edge to dependency evidence and state which claims fail if any observation layer is missing.

### Estimated time

4 additional focused hours.

### Required resources only

- [RFC 9113: HTTP/2](https://www.rfc-editor.org/rfc/rfc9113) — `[L3 Integrated]` `[Required]` selected sections only
- [AATE protocol concept](../../docs/concepts/http2-http3-quic.md) — `[L3 Integrated]` `[Required]`

### Optional deeper resources

- [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000) — `[L3 Integrated]` `[Optional]` overview only

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Investigate implementation and version effects in TLS, HTTP/2, HTTP/3/QUIC, connection migration, resumption, proxies, and middleboxes. Distinguish standardized behavior from implementation fingerprints.

### Hands-on outcome

Extend the protocol lab around one narrow question, such as connection reuse differences or proxy-induced observation changes. Compare versions or observation points and preserve reproducible fixtures.

### Interview outcome

Defend what a protocol feature can and cannot say about a client, how it drifts, and what production sampling would be required.

### Required artifact

Reproducible protocol or implementation comparison with captures, parser output, alternatives, and transfer limitations.

### Completion test

A second person can reproduce the comparison and reaches the same limited conclusion without relying on an unverified fingerprint implementation.

### Estimated time

6–10 additional focused hours.

### Required resources only

- Relevant implementation documentation or source for the chosen question — `[L4 Deep]` `[Required]`

### Optional deeper resources

- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446) — `[L4 Deep]` `[Optional]`
- [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114) — `[L4 Deep]` `[Optional]`
- [Chromium source](https://source.chromium.org/chromium) — `[L4 Deep]` `[Optional]`

## Common misconceptions

- TLS encrypts content; it does not hide every transport or handshake observation.
- JA4-like values are not stable person or device identifiers.
- Header order, ALPN, or an HTTP version alone does not prove a browser.
- Equal request rates can create unequal service cost.

## Production limitations

Local Nginx and fixture captures cannot reproduce global DNS, anycast routing, commercial CDN normalization, carrier networks, proxy diversity, TLS termination chains, production cardinality, or HTTP/3 deployment behavior.

## Interview questions

1. Trace a request from browser to a dependency and back.
2. How can a proxy change what a detector observes?
3. Why can per-connection controls break under multiplexing?

## Related lab components

- `lab/edge/nginx.conf`
- `lab/app/main.py`
- `lab/fixtures/requests.jsonl`
- `lab/protocol/`

