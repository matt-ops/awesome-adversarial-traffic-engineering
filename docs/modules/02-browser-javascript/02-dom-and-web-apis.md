# DOM and Web APIs

<!-- source-ids: mdn-dom, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 02 - Browser and JavaScript foundations
- Lesson: 2 of 4
- Depth: Foundation
- Estimated time: 95 minutes
- Prerequisites:
  - [Browser process model](01-browser-process-model.md)
  - Ability to open Elements and Console in DevTools
- Next lesson: JavaScript core

## Role outcome

Distinguish HTML, the live DOM, JavaScript language objects, and browser Web APIs
while locating the elements and state used by an automated workflow.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MDN: Document Object Model](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) | Concepts and usage; DOM tree; DOM and JavaScript; Accessing the DOM | Separates the document object model from source text and language | API reference; the course bridge supplies the offensive workflow context. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Search form, results, frame, worker | Supplies concrete nodes and APIs | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Protected-action evidence | Prevents DOM observations from being overstated as impact | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

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
**Exact section, chapter, or unit:** Concepts and usage; DOM tree; DOM and JavaScript; Accessing the DOM  
**Estimated time:** 30 minutes  
**What to focus on:** nodes, elements, documents, tree relationships, selectors, and mutation  
**What to skip:** exhaustive interface lists and SVG-specific references  
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

Start the Foundation server, load `http://127.0.0.1:4173/`, and open the
**Elements** and **Console** panels in DevTools. Work only in this local document.

### Exact actions or commands

1. In **Elements**, locate `form`, `input`, `button`, `#status`, `#results`, and
   the `iframe`.
2. In **Console**, evaluate `document.querySelectorAll("form *").length`.
3. Evaluate the worked-example code. Confirm that **Product name** displays
   `widget`, the status remains `Enter a product name.`, and no result appears.
4. Call `document.querySelector("#search-form").requestSubmit()`.
5. Confirm that the status is `Found 1 matching product(s).`, inspect the new
   `#results li` node containing `Synthetic Widget — 5 available`, and evaluate
   `localStorage.getItem("aate-last-query")`.
6. Classify each used object as JavaScript language, DOM, or another Web API.

### Expected output

The input becomes `widget`; submitting changes the status to
`Found 1 matching product(s).`, creates one list item containing
`Synthetic Widget — 5 available`, and stores `widget`. The number of form
descendants depends on the current markup and should be recorded rather than
memorized.

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

## Check your understanding

1. The static page loads from HTML and then JavaScript changes the status element after a search. Why can the live DOM differ from the original HTML source?
2. The browser provides `fetch` and `document.querySelector` to page code. Are those functions part of the JavaScript language itself, or browser Web APIs?
3. `document.querySelector('#product-name')` finds no matching element. What value does the call return?
4. A script sets the Product name element's `.value` to `widget`, but no search request occurs. Which separate form action is still required?
5. The page displays a success-shaped message after an attempted protected action. What evidence is needed before claiming that server-side state changed?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The browser parses HTML into a live DOM tree, and scripts can add, remove, or change nodes and properties afterward.** View Source shows the original text, while DevTools Elements shows the current tree.

- **2. They are Web APIs supplied by the browser host environment, not built-in JavaScript language features.** JavaScript code calls those APIs to interact with the document and the network.

- **3. `querySelector` returns `null` when no element matches the selector.** Code should handle that possibility before reading properties or calling methods on the returned value.

- **4. The script must dispatch the form's submit behavior, such as clicking the Search button or calling an appropriate submission method.** Changing an input property alone does not run the submit handler.

- **5. Capture the resulting HTTP exchange and verify the authoritative server-side record or service effect.** A rendered message is controlled by browser code and may not reflect whether the protected action completed.

</details>

## Next lesson

[JavaScript core](03-javascript-core.md) teaches the language structures used in
the page and the first Playwright program.
