# Proxies and connection reuse

<!-- source-ids: owasp-wstg-map-architecture-v42, mdn-http-overview, ja4-project, aate-local-lab, aate-adversarial-control-loop -->

> **Progress**  
> Module: 07 - Protocol identity  
> Lesson: 4 of 5  
> Depth: Integrated  
> Estimated time: 2 hours  
> Prerequisites: HTTP/2  
> Artifact: `artifacts/module-07/observation-points.md`  
> Next: HTTP/3 and QUIC

## Role outcome

Identify which proxy/client component owns each TLS/HTTP observation and explain
how pooling/reuse changes identity and rate assumptions.

## Prerequisites

- [HTTP/2](03-http2.md)
- Module 01 edge map

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PROJECT_DOCUMENTATION | [OWASP architecture mapping](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture) | Summary; How to Test | Grounds intermediary discovery |
| OFFICIAL_DOCUMENTATION | [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | components; connections | Defines proxy/connection roles |
| PROJECT_DOCUMENTATION | [JA4](https://github.com/FoxIO-LLC/ja4) | observation and version considerations | Grounds fingerprint ownership limits |
| LAB_SPECIFIC | [Protocol lab](../../labs/integrated/protocol-identity.md) | HTTP observation | Supplies fixed local evidence |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | map/control hypothesis | Connects ownership to testing |

## Mental model

| Hop | TLS owner | HTTP producer | Reuse scope |
|---|---|---|---|
| browser -> forward proxy | browser or tunnel | browser | browser pool policy |
| proxy -> edge | proxy if terminating | proxy-normalized/forwarded | proxy pool across callers possible |
| edge -> app | edge | edge-normalized request | service pool |

## Required external instruction

### Intermediary assignment

**Direct link:** [OWASP Map Application Architecture](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture) and [MDN HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)  
**Exact assignment:** OWASP Summary/Objectives/How to Test; MDN Components of HTTP-based systems and HTTP and connections  
**Estimated time:** 45 minutes  
**Focus on:** explicit/transparent/reverse intermediaries, termination, forwarded claims, pooling, and observation point  
**Skip:** broad infrastructure scanning and proxy deployment guides  
**Expected takeaway:** attribute each fingerprint/header/connection feature to the component that actually produced it.

## Course bridge

Connection reuse improves efficiency but decouples request count from connection
count. A proxy can multiplex multiple callers or create many upstream connections.
Forwarded source headers are claims unless a trusted intermediary sets/sanitizes them.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Every signal record gets `observed_at`, `produced_by`,
    `possibly_transformed_by`, and `reuse_scope` before it is used in a bypass claim.

## Worked example

The local Python helper sends no `Accept-Language`, uses a fixed UA, and observes
HTTP/1.1. That describes the helper-to-local edge path. It does not describe a
browser, an upstream TLS fingerprint, or what a production CDN would forward.

## Guided exercise

### Objective

Annotate protocol ownership on the existing edge map.

### Setup

Start local API and use the fixed HTTP helper once.

### Actions

1. Execute `python -m lab.protocol.compare http`.
2. Record client response version and server-visible version/headers.
3. Add browser, forward proxy, reverse proxy, app hops to an overlay.
4. Mark termination, pooling, normalization, and trusted header source.
5. Write two weak aggregation hypotheses and required proof.

### Expected output

Local HTTP `200` with observed version/fields, plus a generic overlay clearly
separating observed local facts from hypothetical intermediaries.

### Interpretation

Attribution to the producing component prevents blaming a browser for a proxy
fingerprint or relying on caller-controlled forwarded identity.

### Common failure modes

- Treating `X-Forwarded-For` as independently verified
- Assuming one connection per session
- Extending local HTTP/1.1 to every path
- Hiding hypothetical proxy nodes

### Cleanup

Helper closes connection; stop API if pausing.

## Why this matters offensively

Proxy rotation and connection behavior affect controls only at specific hops.
Mapping ownership reveals which identity dimensions actually change and which remain.

## Required artifact

`artifacts/module-07/observation-points.md` with hop table, local output, ownership,
reuse scopes, hypotheses, proof, and limitations.

## Pass gate

1. Who produces downstream TLS after termination?
2. Why can one connection carry multiple identities?
3. When is a forwarded header reliable?
4. What does the local helper prove?
5. Why label hypothetical hops?

## Answer key

<details><summary>Check your reasoning</summary>

1. The terminating intermediary acting as the downstream TLS client.
2. Pools/multiplexing and application sessions are separate lifecycles.
3. When a trusted intermediary sanitizes and sets it under a known boundary.
4. Only the fixed Python client's local HTTP request/response observations.
5. To prevent architecture hypotheses from becoming unsupported facts.

</details>

## Next lesson

[HTTP/3 and QUIC](05-http3-quic.md) adds encrypted QUIC transport, streams, and
connection identifiers to the deep path.

