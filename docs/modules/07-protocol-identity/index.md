# Module 07 - Protocol identity foundations

**Outcome:** use source-led protocol models to reason about browser/TLS/HTTP
coherence, capture real loopback ClientHello records, compare actual available
clients over TLS and HTTP/2, explain what intermediaries can change, and avoid
treating fingerprints as identity proof.

The executable lab compares available Python/OpenSSL, curl, Playwright Chromium,
and Node capabilities on loopback. It does not calculate production JA4, prove a
browser identity, exercise HTTP/3/QUIC, or measure a real proxy chain.

## Foundation

Complete [TLS ClientHello](01-tls-clienthello.md). Explain offered versus selected
values and inspect the real bounded loopback capture output.

## Applied

Complete [JA4 and JA4H](02-ja4-and-ja4h.md). Interpret versioned fingerprints as
observation-point pivots, not identity proof, and compare local HTTP observations.

## Integrated

Complete [HTTP/2](03-http2.md) and [proxies/connection
reuse](04-proxies-and-connection-reuse.md). Map streams, connections,
termination, pooling, and what each observer can actually see.

## Deep

Complete the [local multi-client protocol
comparison](06-local-multi-client-protocol-comparison.md), then [HTTP/3 and
QUIC](05-http3-quic.md). Compare real available clients before explaining stream
and connection-ID semantics, migration/routing purpose, and unjustified identity claims.

Start with [TLS ClientHello](01-tls-clienthello.md).
