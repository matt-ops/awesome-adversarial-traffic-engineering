# Network events and evidence

<!-- source-ids: playwright-network, mdn-http-overview, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 03 - Playwright foundations
- Lesson: 4 of 5
- Depth: Foundation
- Estimated time: 105 minutes
- Prerequisites:
  - [Browser contexts and storage state](03-contexts-and-state.md)
  - HTTP message anatomy from Module 01
- Next lesson: Frames, workers, and CDP

## Role outcome

Capture Playwright request/response events, correlate them by URL and action,
and distinguish browser observations from protected-action proof.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Playwright Network](https://playwright.dev/docs/network) | Network events; HTTP authentication; missing events/service workers | Defines observable events and important blind spots | API behavior is version-sensitive; examples pin the repository version. |
| OFFICIAL_DOCUMENTATION | [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | HTTP flow and messages | Keeps event objects tied to protocol meaning | Stop before APIs based on HTTP; it is a browser-platform overview, not an attack guide. |
| LAB_SPECIFIC | [First Playwright workflow](../../labs/foundation/first-playwright.md) | Request/response listeners and JSON output | Supplies the tested capture implementation | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Evidence, residual anomalies, and proof | Adds trial correlation fields without overstating browser events | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
page action
  -> Playwright Request event: intended method/URL/headers/body
  -> network and server
  -> Playwright Response event: status/headers/body handle
  -> DOM update/assertion
  -> optional server telemetry/state proof
```

No response event may mean request failure, interception, worker behavior, or
premature cleanup. It must not be silently counted as a block.

## Required external instruction

### Playwright network assignment

**Direct link:** [Playwright Network](https://playwright.dev/docs/network)  
**Exact section, chapter, or unit:** Network events; HTTP Authentication; Missing Network Events and Service Workers  
**Estimated time:** 35 minutes  
**What to focus on:** listener timing, request/response distinction, page versus context scope, and documented service-worker caveat  
**What to skip:** request modification, mocking, WebSockets, and HAR replay until later experiments  
**Expected takeaway:** build an event record without claiming that it is a packet capture or complete server audit log.

## Course bridge

Playwright exposes request and response events for browser network activity and
allows listeners at page or context scope.[^pw-network] These objects describe
browser-observed exchanges; they are not a raw transport capture and can have
documented gaps, including service-worker-mediated cases.[^pw-worker-gap]

[^pw-network]: Playwright, "Network," Network events.
[^pw-worker-gap]: Playwright, "Network," Missing Network Events and Service Workers.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Add a trial ID, population, workflow step, monotonic
    sequence, wall-clock time, and protected-action correlation key around raw
    events. URLs alone are ambiguous when the same endpoint is retried.

## Worked example

```typescript
context.on("request", request => events.push({
  kind: "request", method: request.method(), url: request.url()
}));
context.on("response", response => events.push({
  kind: "response", status: response.status(), url: response.url()
}));
```

The listener callbacks execute when events occur and append plain evidence
objects. `request.method()` and `response.status()` are synchronous getters;
reading a response body would be asynchronous. Context-level listeners include
Pages in that context; the Foundation script uses Page scope for one Page.

## Guided exercise

### Objective

Reconcile captured requests and responses and identify unsupported conclusions.

### Setup

Start the static server and execute the first workflow. Open the resulting JSON
without editing it.

### Exact actions or commands

1. Group events by URL while preserving original order.
2. Pair each request with the corresponding response where possible.
3. Label document, parser asset, frame, worker, and fetch initiator categories
   using the manual trace as corroboration.
4. Record method, status, and whether the body was preserved.
5. Add three fields the script should capture for integrated trials: trial ID,
   population, and workflow step.
6. List four claims the current network output cannot support.

### Expected output

Local URLs have request/response pairs with `200` in a normal trial. The current
output preserves no response bodies or server event IDs and therefore cannot
prove server-side mutation, enforcement reason, raw-wire identity, or uniqueness
of the caller.

### Interpretation

The event set is sufficient to reproduce and debug the static search. Stronger
offensive experiments add server telemetry and a protected-action record rather
than inflating what browser events prove.

### Common failure modes

- Sorting events and losing causal order
- Pairing solely by URL when concurrent identical URLs exist
- Treating a missing response as a `403`
- Calling Playwright events a packet capture
- Reading only DOM success and ignoring the exchange

### Cleanup

Stop the server. Keep the original output unchanged while you analyze it. Saving
that analysis in a separate file is optional.

## Why this matters offensively

Control testing requires a chain of evidence: exact input, control response,
same protected action, and authoritative outcome. Browser events cover a vital
middle segment but must be correlated rather than overclaimed.

## Check your understanding

1. A Playwright request event records the method, URL, headers, and body intent. Which server outcome is still unknown at request-event time?
2. Two inventory requests use the same URL during one trial. Why can a URL-only pairing method attach the wrong response to a request?
3. The exercise listens on one Page while another Page exists in the same BrowserContext. Which events would a context-level listener observe that the page-level listener would not?
4. A request event has no matching response event. Why should the learner investigate failure, interception, worker behavior, and cleanup before calling the missing response a control rejection?
5. Which additional evidence would turn a browser request/response event into proof that the protected server action succeeded?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The response status, response body, and resulting server state are not yet known.** A request event shows what the browser attempted to send, not how the server processed the operation.

- **2. Repeated or concurrent requests can share an identical URL, so URL text does not uniquely identify one exchange.** Pairing needs stronger correlation such as request objects, action timing, or trial identifiers.

- **3. A BrowserContext listener can observe relevant network events from every Page in that context.** A Page listener is limited to traffic associated with the single Page where the listener was registered.

- **4. Several non-control causes can prevent a response event from appearing.** Without an HTTP control response or correlated server evidence, labeling the absence as enforcement would overstate what the browser trace shows.

- **5. Correlate the event with the same trial and action, then verify the server record used as the source of truth or the intended service-health effect.** Browser events alone describe traffic, not final protected-action completion.

</details>

## Next lesson

[Frames, workers, and CDP](05-frames-workers-and-cdp.md) extends observation to
multiple execution contexts and a version-sensitive browser protocol surface.
