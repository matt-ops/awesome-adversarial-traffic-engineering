# Module 07 - Protocol identity

**Outcome:** compare claimed browser identity with TLS and HTTP behavior, explain
what intermediaries can change, and avoid treating fingerprints as identity proof.

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
