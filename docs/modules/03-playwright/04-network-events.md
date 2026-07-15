# Network events and evidence

<!-- source-ids: playwright-network, mdn-http-overview, aate-local-lab, aate-adversarial-control-loop -->

> **Progress**  
> Module: 03 - Playwright foundations  
> Lesson: 4 of 5  
> Depth: Foundation  
> Estimated time: 105 minutes  
> Prerequisites: Browser contexts and storage state  
> Artifact: `artifacts/module-03/network-evidence.md`  
> Next: Frames, workers, and CDP

## Role outcome

Capture Playwright request/response events, correlate them by URL and action,
and distinguish browser observations from protected-action proof.

## Prerequisites

- [Browser contexts and storage state](03-contexts-and-state.md)
- HTTP message anatomy from Module 01

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Playwright Network](https://playwright.dev/docs/network) | Network events; HTTP authentication; missing events/service workers | Defines observable events and important blind spots |
| OFFICIAL_DOCUMENTATION | [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | HTTP flow and messages | Keeps event objects tied to protocol meaning |
| LAB_SPECIFIC | [First Playwright workflow](../../labs/foundation/first-playwright.md) | Request/response listeners and artifact | Supplies the tested capture implementation |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Evidence, residual anomalies, and proof | Adds trial correlation fields without overstating browser events |

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
**Exact assignment:** Network events; HTTP Authentication; Missing Network Events and Service Workers  
**Estimated time:** 35 minutes  
**Focus on:** listener timing, request/response distinction, page versus context scope, and documented service-worker caveat  
**Skip:** request modification, mocking, WebSockets, and HAR replay until later experiments  
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

### Actions

1. Group events by URL while preserving original order.
2. Pair each request with the corresponding response where possible.
3. Label document, parser asset, frame, worker, and fetch initiator categories
   using the manual trace as corroboration.
4. Record method, status, and whether the body was preserved.
5. Add three fields the script should capture for integrated trials: trial ID,
   population, and workflow step.
6. List four claims the current artifact cannot support.

### Expected output

Local URLs have request/response pairs with `200` in a normal trial. The current
artifact preserves no response bodies or server event IDs and therefore cannot
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

Stop the server. Retain the original artifact unchanged and place analysis in a
separate file.

## Why this matters offensively

Control testing requires a chain of evidence: exact input, control response,
same protected action, and authoritative outcome. Browser events cover a vital
middle segment but must be correlated rather than overclaimed.

## Required artifact

`artifacts/module-03/network-evidence.md` with ordered/pair tables, missing-data
analysis, proposed correlation schema, and four prohibited conclusions.

## Pass gate

1. What is observable at request time that is not yet known?
2. Why can URL-only pairing fail?
3. What scope difference exists between Page and Context listeners?
4. Is a missing response automatically a control rejection?
5. What evidence upgrades a browser event into protected-action proof?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. Method/URL/headers/body intent are visible, but no server outcome exists yet.
2. Concurrent or repeated requests can share a URL and need stronger correlation.
3. Context listeners observe relevant Pages in that context; Page listeners observe that Page.
4. No; failure, interception, worker behavior, or cleanup may explain it.
5. Correlate it with the same trial/action and authoritative server state or service-health effect.

</details>

## Next lesson

[Frames, workers, and CDP](05-frames-workers-and-cdp.md) extends observation to
multiple execution contexts and a version-sensitive browser protocol surface.
