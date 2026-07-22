# Observe requests with DevTools Network

<!-- source-ids: chrome-devtools-network, aate-local-lab -->

## Progress

- Module: 01 - HTTP and the edge
- Lesson: 3 of 4
- Depth: Foundation
- Estimated time: 80 minutes
- Prerequisites:
  - [Sessions and workflows](02-sessions-and-workflows.md)
  - Chrome or Chromium with DevTools
- Next lesson: Edge request path

## Role outcome

Capture a normal browser trace and explain the initiator, request, response,
timing, and state evidence for each resource.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Chrome DevTools: Inspect network activity](https://developer.chrome.com/docs/devtools/network) | Open panel; log activity; show information; inspect resource details | Defines the observation workflow and panel fields | Chrome UI and labels can change between releases. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Zero-Docker target | Supplies deterministic local requests | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

| DevTools field | Evidence | Does not alone prove |
|---|---|---|
| Name/URL | Requested resource | Business objective |
| Initiator | Script/parser/action that caused request | Human intent |
| Method/status | HTTP operation and outcome | Authorization correctness |
| Headers | Claims and server metadata | Unique identity |
| Payload/response | Inputs and returned representation | Server-side state unless the response says so |
| Timing | Browser-observed phase durations | Root cause without corroboration |

## Required external instruction

### Chrome DevTools assignment

**Direct link:** [Inspect network activity](https://developer.chrome.com/docs/devtools/network)  
**Exact section, chapter, or unit:** Open the Network panel; Log network activity; Show more information; Inspect a resource's details  
**Estimated time:** 25 minutes  
**What to focus on:** preserving the log, disabling cache for a controlled comparison, initiator, headers, payload, response, and timing  
**What to skip:** throttling, request blocking, HAR editing, overrides, and advanced filtering for now  
**Expected takeaway:** capture a resource and explain who initiated it, what crossed the network, what returned, and which inference remains unsupported.

## Course bridge

DevTools observes the browser's side of the exchange. Its Network panel logs
resource requests and exposes request/response details and timing.[^devtools]
The Initiator column is particularly useful: a parser-discovered stylesheet, a
script `fetch`, a frame navigation, and a worker script arise from different
execution paths even if all are `GET` requests.

[^devtools]: Chrome Developers, "Inspect network activity," assigned sections.

!!! warning "Safety boundary"
    The panel can replay or edit requests on any site you visit. This lesson's
    actions are restricted to `127.0.0.1:4173`; observing a page does not grant
    permission to test it.

## Worked example

The static app's initial navigation causes:

```text
document -> styles.css        (parser)
document -> app.js            (parser)
document -> frame.html        (iframe navigation)
app.js   -> worker.js         (Worker constructor)
click    -> inventory.json    (fetch in submit handler)
```

The last edge matters most to the search workflow. `app.js` is code delivery;
`inventory.json` is the data request caused by the learner's action. A later
automation trace should preserve the same causal chain.

## Guided exercise

### Objective

Create a labeled manual baseline trace before introducing automation.

### Setup

Start the loopback static server from Lesson 1 and open
`http://127.0.0.1:4173/`. Open DevTools, select the **Network** panel, enable
**Preserve log**, and click **Clear network log**. Keep **Disable cache**
unchecked for the first load.

### Exact actions or commands

1. Reload the page, type `widget` into **Product name**, click **Search**, and
   confirm that `Found 1 matching product(s).` appears below the form.
2. Record the document, stylesheet, script, frame, worker, and JSON rows.
3. For `inventory.json`, capture General, Request Headers, Response Headers,
   Response, Initiator, and Timing.
4. Click **Clear network log**, check **Disable cache** while DevTools is open,
   and repeat exactly once.
5. Compare request count and transfer/timing observations without claiming a
   performance cause the trace cannot establish.

### Expected output

Six resource families appear. The inventory request is a `GET` returning `200`
and JSON. Its initiator points to the submit handler in `app.js`. With cache
disabled, static resources are requested again rather than satisfied from the
browser cache.

### Interpretation

This is the legitimate manual baseline. Save exact browser version, URL, query,
cache condition, and time so a Playwright trace can be compared without hidden
changes.

### Common failure modes

- Opening DevTools after the activity and missing the initial navigation
- Comparing cached and uncached traces without recording the cache setting
- Reading provisional headers as bytes confirmed on the wire
- Inferring server processing time from total browser timing alone

### Cleanup

Re-enable normal cache behavior, close DevTools if desired, and stop the server.

## Why this matters offensively

A manual trace is the reference population for later control reconnaissance.
Without it, an automation difference can be mistaken for target drift, caching,
different inputs, or a different workflow.

## Check your understanding

1. In the static search trace, `app.js` fetches `inventory.json` after the learner clicks Search. What does the Network panel's Initiator field add to the inventory URL?
2. Why should the learner preserve a manual `widget` search trace before capturing the same workflow with Playwright?
3. The learner repeats the search with Disable cache selected in DevTools. Which request-handling variable changed between the two traces?
4. The Timing panel reports a total browser-observed duration for `inventory.json`. Why can that duration not identify a server root cause by itself?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The Initiator field connects `inventory.json` to the form submit handler in `app.js`.** The URL names the resource, while the initiator explains which browser action or script caused the request.

- **2. The manual trace supplies a legitimate reference using the same target, input, and workflow.** Later automation can be compared against that baseline without guessing which requests and page changes belong to a normal run.

- **3. The changed variable is whether eligible resources may be satisfied from the browser cache while DevTools remains open.** The workflow, input, and target should stay the same for the comparison.

- **4. Browser total time combines queueing, connection, request, response, and client processing observations.** Without correlated server and dependency telemetry, those phases cannot identify which server-side component caused a delay.

</details>

## Next lesson

[Map the edge request path](04-edge-request-path.md) adds intermediaries, trust
boundaries, application work, and dependencies to the browser trace.
