# HTTP/2 connections and streams

<!-- source-ids: rfc-9113, ja4-project, aate-adversarial-control-loop -->

> **Progress**  
> Module: 07 - Protocol identity  
> Lesson: 3 of 5  
> Depth: Integrated  
> Estimated time: 3 hours  
> Prerequisites: JA4 and JA4H  
> Artifact: `artifacts/module-07/http2-map.md`  
> Next: Proxies and connection reuse

## Role outcome

Explain HTTP/2 framing, streams, multiplexing, and connection state and identify
which observations may reflect a client implementation or intermediary.

## Prerequisites

- [JA4 and JA4H](02-ja4-and-ja4h.md)
- HTTP request/session distinction from Module 01

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| STANDARD | [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) | §2 and §5 | Defines framing/streams and stream lifecycle |
| PROJECT_DOCUMENTATION | [JA4 project](https://github.com/FoxIO-LLC/ja4) | JA4H technical details | Connects HTTP behavior to fingerprint pivots |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | cross-layer hypotheses and limits | Frames offensive comparisons |

## Mental model

```text
one HTTP/2 connection
  -> connection-level settings/state
  -> stream 1: request/response frames
  -> stream 3: request/response frames (overlapping)
  -> flow control and stream lifecycle
```

## Required external instruction

### HTTP/2 assignment

**Direct link:** [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113)  
**Exact assignment:** §2 HTTP/2 Protocol Overview and §5 Streams and Multiplexing  
**Estimated time:** 80 minutes  
**Focus on:** binary frames, connection versus stream, identifiers/states, multiplexing, and flow-control scope  
**Skip:** frame-by-frame chapters, HPACK details, priority history, and error catalogs  
**Expected takeaway:** trace two overlapping requests without treating streams as connections or sessions.

## Course bridge

HTTP/2 multiplexes streams over one connection; streams have identifiers and
lifecycles while some settings/state belong to the connection.[^h2]

[^h2]: RFC 9113 §§2 and 5.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Record whether a feature is request-, stream-,
    connection-, session-, or workflow-scoped. An evasion that rotates requests
    may still reuse one observable connection.

## Worked example

Two report requests on streams 1 and 3 can overlap on one TLS connection. A
per-connection limit sees one aggregation unit; per-request session IDs can look
different. A terminating proxy can create a different downstream connection and
stream pattern.

## Guided exercise

### Objective

Map a fictional two-request workflow across connection/stream/session layers.

### Setup

Use an offline diagram; the current local edge reports HTTP/1.1 and does not
pretend to be an HTTP/2 capture lab.

### Actions

1. Draw TLS connection, connection settings, streams 1/3, requests, and responses.
2. Add application session and rate key separately.
3. Insert a terminating proxy and redraw downstream boundaries.
4. Mark observable client-implementation behaviors as hypotheses.
5. Define the capture/provider resource needed to validate them.

### Expected output

A layer-correct map showing multiplexed streams, proxy replacement, and no claim
that stream pattern identifies a person.

### Interpretation

The standard teaches protocol structure. Actual fingerprint behavior needs an
approved capture or provider assignment with recorded implementations.

### Common failure modes

- Calling a stream a TCP connection
- Treating application session as HTTP/2 state
- Ignoring proxy termination
- Inventing local HTTP/2 evidence

### Cleanup

No target contacted.

## Why this matters offensively

Browser and alternate-client stacks differ beyond header strings. Connection and
stream behavior can expose incoherence or weak aggregation assumptions.

## Required artifact

`artifacts/module-07/http2-map.md` with scopes, proxy boundaries, hypotheses,
required evidence, and limitations.

## Pass gate

1. Can multiple streams share one connection?
2. Is a BrowserContext an HTTP/2 connection?
3. What can a terminating proxy change?
4. Why scope a rate feature explicitly?
5. Does this local lab capture HTTP/2?

## Answer key

<details><summary>Check your reasoning</summary>

1. Yes; multiplexing is central to HTTP/2.
2. No; browser state and transport connections have different lifecycles.
3. TLS and HTTP/2 connection/stream behavior observed downstream.
4. Request, stream, connection, session, and workflow aggregation have different bypass behavior.
5. No; it honestly reports its observed HTTP version.

</details>

## Next lesson

[Proxies and connection reuse](04-proxies-and-connection-reuse.md) makes the
observation-point and lifecycle consequences operational.

