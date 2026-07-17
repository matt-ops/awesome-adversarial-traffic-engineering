# Module 07 - Protocol identity foundations

**Outcome:** use source-led protocol models to reason about browser/TLS/HTTP
coherence, generate bounded Python/OpenSSL ClientHello fixtures, observe plain
HTTP metadata, explain what intermediaries can change, and avoid treating
fingerprints as identity proof.

The executable lab does not compare Chrome with Playwright TLS, calculate JA4,
capture HTTP/2 settings, exercise HTTP/3/QUIC, or measure proxy-induced transport
changes. Those topics remain standards/project instruction and evidence plans.

## Foundation

Complete [TLS ClientHello](01-tls-clienthello.md). Explain offered versus selected
values and preserve a generated, socket-free comparison artifact.

## Applied

Complete [JA4 and JA4H](02-ja4-and-ja4h.md). Interpret versioned fingerprints as
observation-point pivots, not identity proof, and compare local HTTP observations.

## Integrated

Complete [HTTP/2](03-http2.md) and [proxies/connection
reuse](04-proxies-and-connection-reuse.md). Map streams, connections, termination,
pooling, and what each observer can actually see.

## Deep

Complete [HTTP/3 and QUIC](05-http3-quic.md). Explain stream and connection-ID
semantics, migration/routing purpose, and identity claims the protocol does not justify.

Start with [TLS ClientHello](01-tls-clienthello.md).
