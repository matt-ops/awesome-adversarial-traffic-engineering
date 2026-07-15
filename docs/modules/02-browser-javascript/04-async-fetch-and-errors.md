# Promises, async, fetch, and errors

<!-- source-ids: mdn-promises, mdn-async-function, mdn-try-catch, mdn-using-fetch, aate-local-lab, aate-adversarial-control-loop -->

> **Progress**  
> Module: 02 - Browser and JavaScript foundations  
> Lesson: 4 of 4  
> Depth: Foundation  
> Estimated time: 2 hours  
> Prerequisites: Minimum JavaScript  
> Artifact: `artifacts/module-02/fetch-observation.js`  
> Next: Playwright object model

## Role outcome

Explain and implement asynchronous request handling that distinguishes network
failure, HTTP failure, parsing failure, and assertion failure.

## Prerequisites

- [Minimum JavaScript](03-javascript-core.md)
- Functions, objects, arrays, and conditions

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MDN Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) | Description; chaining; rejection | Defines eventual completion and failure |
| OFFICIAL_DOCUMENTATION | [MDN async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) | Description; examples | Explains `async` return values and `await` |
| OFFICIAL_DOCUMENTATION | [MDN try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch) | Syntax; description; examples | Provides structured error handling |
| OFFICIAL_DOCUMENTATION | [MDN Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) | Making a request; checking status; reading JSON | Separates fulfilled fetch from successful HTTP status |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Form handler and inventory fetch | Supplies the local implementation |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Control result and protected-action proof | Separates asynchronous failure categories from enforcement conclusions |

## Mental model

```text
call fetch -> Promise pending
              | fulfilled with Response (even 404/500)
              | rejected for request/network failure
await response.json() -> fulfilled value OR parse rejection
application assertion -> pass OR explicit failure
```

## Required external instruction

### MDN asynchronous bridge

**Direct link:** [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), [async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function), [try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch), and [Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)  
**Exact assignment:** Promise Description/chaining/rejection; async function Description/examples; try...catch Syntax/Description/examples; Fetch Making a request, checking response status, and reading JSON  
**Estimated time:** 65 minutes  
**Focus on:** what each Promise settles with, why `await` pauses one async function rather than the browser, and why HTTP errors need an explicit status check  
**Skip:** Promise combinators, streaming bodies, upload progress, service workers, and advanced cancellation  
**Expected takeaway:** predict each success/failure path in a fetch function and preserve a useful error category.

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

Start the Foundation server. Create `artifacts/module-02/fetch-observation.js`
and paste the worked function into DevTools Sources Snippets or adapt it in the
Console.

### Actions

1. Call `await loadInventory()` and record the returned array.
2. Change the path temporarily to `/missing.json`; call it and record the error.
3. Stop the server and call the function again.
4. Restore `/inventory.json` and the server.
5. Add an `observedAt` timestamp and category (`success`, `http`, `network`, or
   `parse`) to a copied observation record without swallowing the error.

### Expected output

The valid path returns two synthetic objects. The missing path reports
`HTTP 404`. With the server stopped, fetch reports a network/request failure;
there is no HTTP status because no response was received.

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

Restore the correct path, stop the server, and retain only the local synthetic
observations in the artifact.

## Why this matters offensively

Automation is asynchronous. Incorrect waiting and error classification can
create false bypasses, missed blocks, accidental retry pressure, and reports
whose evidence cannot be reproduced.

## Required artifact

`artifacts/module-02/fetch-observation.js` plus a Markdown table showing the four
outcome categories, whether a Response exists, the available evidence, and the
allowed conclusion.

## Pass gate

1. What does an `async` function return?
2. Does fetch normally reject for HTTP `500`?
3. What does `await response.json()` add to the failure model?
4. Why rethrow after logging an error?
5. Why classify timeout/network failure separately from a control block?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. It returns a Promise, fulfilled with the returned value or rejected by a thrown error.
2. No; it normally fulfills with a Response whose status must be checked.
3. Body reading/parsing is another asynchronous operation that can reject.
4. Callers still need to observe failure rather than receive a misleading success value.
5. No HTTP control response may exist, so causes and conclusions differ.

</details>

## Next lesson

[Playwright object model](../03-playwright/01-object-model.md) applies these
browser and asynchronous concepts to a controlled automation API.
