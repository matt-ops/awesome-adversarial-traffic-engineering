# Proxies and connection reuse

<!-- source-ids: owasp-wstg-map-architecture-v42, mdn-http-overview, ja4-project, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 07 - Protocol identity
- Lesson: 4 of 5
- Depth: Integrated
- Estimated time: 2 hours
- Prerequisites:
  - [HTTP/2](03-http2.md)
  - Module 01 edge map
- Next lesson: HTTP/3 and QUIC

## Role outcome

Identify which proxy/client component owns each TLS/HTTP observation and explain
how pooling/reuse changes identity and rate assumptions.

> A network fingerprint is an analytical pivot, not proof of a specific user or browser.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [OWASP architecture mapping](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture) | Summary; How to Test | Grounds intermediary discovery | Version 4.2 is intentionally pinned and does not model every modern edge service. |
| OFFICIAL_DOCUMENTATION | [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | components; connections | Defines proxy/connection roles | Stop before APIs based on HTTP; it is a browser-platform overview, not an attack guide. |
| PROJECT_DOCUMENTATION | [JA4](https://github.com/FoxIO-LLC/ja4) | observation and version considerations | Grounds fingerprint ownership limits | Fingerprints change with implementations; licensing differs across JA4+ methods; fingerprints are not identity proof. |
| LAB_SPECIFIC | [Protocol lab](../../labs/integrated/protocol-identity.md) | HTTP observation | Supplies fixed local evidence | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | map/control hypothesis | Connects ownership to testing | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Hop | TLS owner | HTTP producer | Reuse scope |
|---|---|---|---|
| browser -> forward proxy | browser or tunnel | browser | browser pool policy |
| proxy -> edge | proxy if terminating | proxy-normalized/forwarded | proxy pool across callers possible |
| edge -> app | edge | edge-normalized request | service pool |

## Required external instruction

### Architecture-mapping assignment

**Direct link:** [OWASP Map Application Architecture](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture)  
**Exact section, chapter, or unit:** Summary, Objectives, and How to Test  
**Estimated time:** 25 minutes  
**What to focus on:** explicit, transparent, and reverse intermediaries; termination points; and the observation available at each hop  
**What to skip:** broad infrastructure scanning and proxy deployment guides  
**Expected takeaway:** draw the intermediary chain and name the component that can create or transform each observation.

### HTTP connection assignment

**Direct link:** [MDN HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)  
**Exact section, chapter, or unit:** Components of HTTP-based systems; HTTP and connections  
**Estimated time:** 20 minutes  
**What to focus on:** client, proxy, server, connection reuse, and why a connection is not the same unit as a request or user  
**What to skip:** browser APIs built on HTTP  
**Expected takeaway:** explain how pooling and reuse decouple connection count from request count and caller count.

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

### Exact actions or commands

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

## Check your understanding

1. A reverse proxy terminates the public TLS connection and starts TLS to the application. Which component produces the ClientHello seen by the application?
2. A pooled HTTP/2 connection carries requests from several application sessions. Why can one connection represent more than one user or workflow identity?
3. A request includes `X-Forwarded-For`. Under which trust boundary can the application treat that header as reliable?
4. The local compatibility helper records a fixed Python client's request and response. What can those observations prove about the broader proxy path?
5. A request-path diagram includes an unverified downstream cache. Why should the cache node remain dashed and labeled hypothetical?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The terminating reverse proxy produces the downstream ClientHello because the proxy acts as the TLS client toward the application.** The application does not see the public client's original handshake.

- **2. Connection pooling and HTTP/2 multiplexing operate independently of cookies, accounts, and workflow state.** Several application identities can therefore share transport, and one identity can move across several connections.

- **3. The header is reliable only when a known trusted intermediary removes untrusted incoming copies and sets the value itself.** Without that sanitizing boundary, the client may supply a false address claim.

- **4. The helper proves only the fixed client's local request and response observations under the recorded environment.** It does not establish unobserved proxy hops, browser behavior, production routing, or identity.

- **5. A dashed label keeps an architecture hypothesis separate from direct observation.** Without evidence, drawing the cache as confirmed would turn a possible component into an unsupported fact.

</details>

## Next lesson

[HTTP/3 and QUIC](05-http3-quic.md) adds encrypted QUIC transport, streams, and
connection identifiers to the deep path.
