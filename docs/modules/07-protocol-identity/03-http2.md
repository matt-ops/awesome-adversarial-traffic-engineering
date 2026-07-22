# HTTP/2 connections and streams

<!-- source-ids: rfc-9113, ja4-project, aate-adversarial-control-loop -->

## Progress

- Module: 07 - Protocol identity
- Lesson: 3 of 5
- Depth: Integrated
- Estimated time: 3 hours
- Prerequisites:
  - [JA4 and JA4H](02-ja4-and-ja4h.md)
  - HTTP request/session distinction from Module 01
- Next lesson: Proxies and connection reuse

## Role outcome

Explain HTTP/2 framing, streams, multiplexing, and connection state and identify
which observations may reflect a client implementation or intermediary.

> A network fingerprint is an analytical pivot, not proof of a specific user or browser.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) | §2 and §5 | Defines framing/streams and stream lifecycle | Selected protocol sections only; implementation fingerprinting is separate. |
| PROJECT_DOCUMENTATION | [JA4 project](https://github.com/FoxIO-LLC/ja4) | JA4H technical details | Connects HTTP behavior to fingerprint pivots | Fingerprints change with implementations; licensing differs across JA4+ methods; fingerprints are not identity proof. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | cross-layer hypotheses and limits | Frames offensive comparisons | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

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
**Exact section, chapter, or unit:** §2 HTTP/2 Protocol Overview and §5 Streams and Multiplexing  
**Estimated time:** 80 minutes  
**What to focus on:** binary frames, connection versus stream, identifiers/states, multiplexing, and flow-control scope  
**What to skip:** frame-by-frame chapters, HPACK details, priority history, and error catalogs  
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

### Exact actions or commands

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

## Check your understanding

1. A single HTTP/2 connection carries several request and response streams at once. Which protocol feature allows those streams to share the connection?
2. A Playwright BrowserContext lives longer than one transport connection. Why should the context not be treated as an HTTP/2 connection?
3. An edge proxy terminates HTTP/2 and opens a new downstream connection. Which stream and connection observations can change at that boundary?
4. A rate rule counts HTTP/2 connections, while the protected workflow spans several streams and sessions. Why must the aggregation unit be named explicitly?
5. The local helper reports an observed HTTP version from a fixed Python request. Does that exercise capture or claim an HTTP/2 browser trace?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Multiplexing allows independent HTTP/2 streams to share one connection without waiting for each other to finish.** Stream identifiers and connection state must still be interpreted at the correct observation point.

- **2. BrowserContext is an application storage and isolation boundary, while transport connections have separate pooling, reuse, and lifetime rules.** One context can use multiple connections, and one connection can carry multiple requests.

- **3. The proxy can replace TLS, connection settings, stream ordering, header compression state, and downstream request behavior.** Services behind termination observe the intermediary's connection rather than the original client connection.

- **4. Request, stream, connection, session, and workflow keys have different lifecycles and rotation costs.** An unstated unit makes bypass and collateral-impact claims impossible to evaluate precisely.

- **5. No.** The helper honestly reports the protocol observed for its local Python client. It does not create or preserve an HTTP/2 browser capture, so the lesson keeps that limitation explicit.

</details>

## Next lesson

[Proxies and connection reuse](04-proxies-and-connection-reuse.md) makes the
observation-point and lifecycle consequences operational.
