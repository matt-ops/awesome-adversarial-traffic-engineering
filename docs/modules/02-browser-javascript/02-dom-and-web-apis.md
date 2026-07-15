# DOM and Web APIs

<!-- source-ids: mdn-dom, aate-local-lab, aate-adversarial-control-loop -->

> **Progress**  
> Module: 02 - Browser and JavaScript foundations  
> Lesson: 2 of 4  
> Depth: Foundation  
> Estimated time: 95 minutes  
> Prerequisites: Browser process model  
> Artifact: `artifacts/module-02/dom-inventory.md`  
> Next: JavaScript core

## Role outcome

Distinguish HTML, the live DOM, JavaScript language objects, and browser Web APIs
while locating the elements and state used by an automated workflow.

## Prerequisites

- [Browser process model](01-browser-process-model.md)
- Ability to open Elements and Console in DevTools

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MDN: Document Object Model](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) | Concepts and usage; DOM tree; DOM and JavaScript; Accessing the DOM | Separates the document object model from source text and language |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Search form, results, frame, worker | Supplies concrete nodes and APIs |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Protected-action evidence | Prevents DOM observations from being overstated as impact |

## Mental model

```text
HTML bytes --parse--> live Document tree
                         | query/select/mutate
JavaScript code ---------+
                         | call
Web APIs: fetch, storage, events, workers, timers, navigator
```

JavaScript is the language. The DOM and `fetch`, storage, events, and workers are
host-provided browser APIs available to JavaScript.

## Required external instruction

### MDN DOM assignment

**Direct link:** [Document Object Model (DOM)](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)  
**Exact assignment:** Concepts and usage; DOM tree; DOM and JavaScript; Accessing the DOM  
**Estimated time:** 30 minutes  
**Focus on:** nodes, elements, documents, tree relationships, selectors, and mutation  
**Skip:** exhaustive interface lists and SVG-specific references  
**Expected takeaway:** explain how parsed markup becomes a live object tree and how code locates and changes it.

## Course bridge

The DOM represents a document as nodes with relationships that scripts can
query and mutate.[^mdn-dom] The source HTML is input to parsing; the current DOM
can differ after scripts add text, remove elements, or update attributes.

[^mdn-dom]: MDN, "Document Object Model (DOM)," Concepts and usage, DOM tree, and DOM and JavaScript.

`document.querySelector("#query")` calls a DOM method and returns the matching
element. `localStorage.getItem(...)` calls a storage Web API. `fetch(...)` uses a
network Web API and returns a JavaScript `Promise`. These are adjacent concepts,
but naming the layer prevents confusion when automation operates the DOM while
network interception observes HTTP.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** A DOM locator proves that automation found a rendered
    interface object. It does not prove the underlying request, server state, or
    protected action. Preserve DOM and network/server evidence separately.

## Worked example

```javascript
const query = document.querySelector("#query");
query.value = "widget";
query.dispatchEvent(new Event("input", { bubbles: true }));
```

Line 1 asks the document for an element whose `id` is `query`. Line 2 changes the
live input object's value property. Line 3 creates and dispatches an input event
that bubbles through ancestors. It does not submit the form or fetch inventory;
those require the submit event path in `app.js`.

## Guided exercise

### Objective

Inventory the document nodes and Web APIs that implement the search workflow.

### Setup

Start the Foundation server, load the page, and open DevTools Elements and
Console. Work only in this local document.

### Actions

1. In Elements locate `form`, `input`, `button`, `#status`, `#results`, and the
   `iframe`.
2. In Console evaluate `document.querySelectorAll("form *").length`.
3. Evaluate the worked-example code and observe that text changes but no result
   appears yet.
4. Call `document.querySelector("#search-form").requestSubmit()`.
5. Inspect the new `#results li` node and read `localStorage.getItem("aate-last-query")`.
6. Classify each used object as JavaScript language, DOM, or another Web API.

### Expected output

The input becomes `widget`; submitting changes status to `Found 1 item`, creates
one list item, and stores `widget`. The number of form descendants depends on the
current markup and should be recorded rather than memorized.

### Interpretation

DOM mutation proves client-side workflow progress. The inventory request and
response establish data retrieval; neither alone creates server-side inventory
state in this static target.

### Common failure modes

- Calling HTML source and live DOM identical after script execution
- Calling `fetch` a JavaScript language keyword
- Treating a selector match as authorization evidence
- Dispatching `input` and expecting the form to submit automatically

### Cleanup

Clear local storage with `localStorage.removeItem("aate-last-query")`, close
DevTools, and stop the server.

## Why this matters offensively

Browser automation interacts with locators and events, while controls may
observe Web API values, execution contexts, and resulting requests. Knowing the
object boundary lets an operator tell a UI artifact from an enforcement result
and recognize when a page-only modification misses another context.

## Required artifact

Create `artifacts/module-02/dom-inventory.md` with the DOM path for each workflow
element, its selector, event, producing code, related request, and layer
classification.

## Pass gate

1. How does the live DOM differ from HTML source?
2. Is `fetch` part of the JavaScript language itself?
3. What does `querySelector` return?
4. Why did changing `.value` not submit the form?
5. What additional evidence is needed beyond a rendered success message?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. The DOM is the parsed, live tree and can be changed after the source is loaded.
2. No; it is a Web API supplied by the browser host environment.
3. The first matching Element, or `null` when no match exists.
4. Property mutation does not inherently dispatch the form's submit action.
5. Capture the resulting HTTP exchange and, for a protected action, authoritative server-side state or service effect.

</details>

## Next lesson

[JavaScript core](03-javascript-core.md) teaches the language structures used in
the page and the first Playwright program.
