# Promises, async, fetch, and errors

<!-- source-ids: mdn-promises, mdn-async-function, mdn-try-catch, mdn-using-fetch, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 02 - Browser and JavaScript foundations
- Lesson: 4 of 4
- Depth: Foundation
- Estimated time: 2 hours
- Prerequisites:
  - [Minimum JavaScript](03-javascript-core.md)
  - Functions, objects, arrays, and conditions
- Next lesson: Playwright object model

## Role outcome

Explain and implement asynchronous request handling that distinguishes network
failure, HTTP failure, parsing failure, and assertion failure.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MDN Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) | Description; chaining; rejection | Defines eventual completion and failure | Reference page; the course uses only the subset needed for browser automation. |
| OFFICIAL_DOCUMENTATION | [MDN async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) | Description; examples | Explains `async` return values and `await` | Reference page; advanced concurrency patterns are out of scope here. |
| OFFICIAL_DOCUMENTATION | [MDN try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch) | Syntax; description; examples | Provides structured error handling | Language reference; the course supplies browser-runner failure examples. |
| OFFICIAL_DOCUMENTATION | [MDN Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) | Making a request; checking status; reading JSON | Separates fulfilled fetch from successful HTTP status | The course does not assign streaming or advanced request-body material at Foundation depth. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Form handler and inventory fetch | Supplies the local implementation | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Control result and protected-action proof | Separates asynchronous failure categories from enforcement conclusions | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
call fetch -> Promise pending
              | fulfilled with Response (even 404/500)
              | rejected for request/network failure
await response.json() -> fulfilled value OR parse rejection
application assertion -> pass OR explicit failure
```

## Required external instruction

### Promise assignment

**Direct link:** [MDN Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)  
**Exact section, chapter, or unit:** Description and Chained Promises  
**Estimated time:** 15 minutes  
**What to focus on:** pending, fulfilled, rejected, handler return values, and how a chain receives the prior result  
**What to skip:** static combinators and advanced subclass behavior  
**Expected takeaway:** draw the fulfilled and rejected path for each Promise in the worked fetch function.

### Async and await assignment

**Direct link:** [MDN async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)  
**Exact section, chapter, or unit:** Description and Examples  
**Estimated time:** 15 minutes  
**What to focus on:** the Promise returned by an async function and the fact that `await` pauses that async function's continuation  
**What to skip:** top-level await and advanced concurrency patterns  
**Expected takeaway:** explain what value each `await` receives and why the browser or Node process can continue other work.

### Error-handling assignment

**Direct link:** [MDN try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)  
**Exact section, chapter, or unit:** Description and The `finally` block  
**Estimated time:** 10 minutes  
**What to focus on:** which thrown or rejected failures enter `catch` and why cleanup belongs in `finally`  
**What to skip:** conditional catch patterns not used by the local script  
**Expected takeaway:** preserve the original failure category while guaranteeing cleanup.

### Fetch assignment

**Direct link:** [MDN Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)  
**Exact section, chapter, or unit:** Making a request; Setting the method; Setting a body; Checking response status; Reading the response body  
**Estimated time:** 25 minutes  
**What to focus on:** request construction, fulfilled `Response` objects for HTTP error statuses, explicit `response.ok` checks, and JSON parsing  
**What to skip:** streaming bodies, upload progress, service workers, and advanced cancellation  
**Expected takeaway:** distinguish request/network rejection, HTTP failure, body-decoding failure, and application assertion failure.

## Course bridge

A Promise represents an eventual value or error. An `async` function always
returns a Promise; `await` resumes that function after the awaited Promise
settles.[^mdn-async] Fetch rejects for failures such as an unusable network
request, but an HTTP `404` or `500` normally fulfills with a `Response`, so code
must inspect `response.ok` or `status`.[^mdn-fetch]

[^mdn-async]: MDN, "async function," Description.
[^mdn-fetch]: MDN, "Using the Fetch API," Checking the response status.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Record transport outcome, HTTP outcome, body/parsing
    outcome, and protected-action assertion separately. A timeout is not a block,
    a `200` is not impact, and a selector assertion is not server state.

## Worked example

```javascript
async function loadInventory() {
  try {
    const response = await fetch("/inventory.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("inventory failed", error);
    throw error;
  }
}
```

The first `await` produces a `Response` or throws a request error. The condition
turns a non-success HTTP response into an explicit error. The second `await`
parses the body. The catch logs context and rethrows so callers cannot mistake
failure for an empty inventory.

## Guided exercise

### Objective

Classify successful, HTTP-error, and unavailable-target outcomes.

### Setup

Start the Foundation server and load `http://127.0.0.1:4173/`. Create
`fetch-observation.js` in a working directory of your choice and paste the worked function into a
DevTools **Sources > Snippets** entry or adapt it in the **Console** panel.

### Exact actions or commands

1. Call `await loadInventory()` and record the returned array.
2. Change the path temporarily to `/missing.json`; call it and record the error.
3. Stop the server and call the function again.
4. Restore `/inventory.json` and the server.
5. Add an `observedAt` timestamp and category (`success`, `http`, `network`, or
   `parse`) to a copied observation record without swallowing the error.

### Expected output

The valid path returns three synthetic objects named `Synthetic Widget`,
`Synthetic Kit`, and `Training Cable`. The missing path reports `HTTP 404`.
With the server stopped, fetch reports a network/request failure; there is no
HTTP status because no response was received.

### Interpretation

The errors correspond to different path locations. Keeping their categories
prevents a failed client, edge block, application error, and malformed evidence
from being counted as the same control result.

### Common failure modes

- Expecting fetch to reject automatically for `404`
- Omitting `await` and logging a pending Promise
- Catching an error and returning `[]`, making failure look like legitimate data
- Assuming `await` blocks every page task

### Cleanup

Restore the correct path and stop the server. If you keep the result, retain
only the local synthetic observations.

## Why this matters offensively

Automation is asynchronous. Incorrect waiting and error classification can
create false bypasses, missed blocks, accidental retry pressure, and reports
whose evidence cannot be reproduced.

## Check your understanding

1. The lesson's `async` function returns a value on success and throws on failure. What does the caller receive in each case?
2. `fetch('/inventory.json')` receives an HTTP `500` response. Does `fetch` normally reject the Promise, and which response property must the code check?
3. The response status is `200`, but `await response.json()` cannot parse the body. Which failure category should the exercise record?
4. The catch block logs an error and then throws the same error again. Why is rethrowing important for the caller?
5. A request times out before any HTTP response arrives. Why should the learner avoid labeling that network failure as a control block?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Calling the `async` function returns a Promise.** A returned value fulfills that Promise, while a thrown error rejects it so callers can await or catch the outcome.

- **2. `fetch` normally fulfills with a Response even for HTTP `500`.** The code must inspect `response.ok` or `response.status` and classify the HTTP failure explicitly.

- **3. Record a body-reading or JSON-parsing failure.** The HTTP exchange succeeded, but the separate asynchronous parse step failed because the returned representation was not valid JSON for the expected operation.

- **4. Rethrowing keeps the operation failed for code higher in the call chain.** Without the throw, logging could accidentally turn the failed request into a misleading successful completion with no usable result.

- **5. A timeout or network error may produce no HTTP response and therefore no observed control decision.** Calling every missing response a block would confuse transport failure with deliberate server enforcement.

</details>

## Next lesson

[Playwright object model](../03-playwright/01-object-model.md) applies these
browser and asynchronous concepts to a controlled automation API.
