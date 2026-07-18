# Playwright object model

<!-- source-ids: microsoft-learn-playwright, playwright-browser-contexts, aate-adversarial-control-loop -->

## Progress

- Module: 03 - Playwright foundations
- Lesson: 1 of 5
- Depth: Foundation
- Estimated time: 2 hours
- Prerequisites:
  - [Module 02](../02-browser-javascript/index.md)
  - Promises, `async`/`await`, DOM selectors, frames, and browser processes
- Required artifact: `artifacts/module-03/object-model.md`
- Next lesson: First local browser

## Role outcome

Explain Browser, BrowserContext, Page, and Locator lifecycles and choose the
correct object boundary for an isolated browser workflow.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Microsoft Learn: Build with Playwright](https://learn.microsoft.com/en-us/training/modules/build-with-playwright/) | Units 1-4 now; all eight by next lesson | Provides the beginner learning sequence and test mental model | Test-automation framing; the course bridge translates the objects into adversarial workflows. |
| OFFICIAL_DOCUMENTATION | [Playwright Isolation](https://playwright.dev/docs/browser-contexts) | What is test isolation?; How Playwright achieves isolation | Defines BrowserContext as an isolated session-like environment | Examples follow the current Playwright test API and can change by version. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Fixed variables and trial state | Defines how contexts represent deliberately isolated populations | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
Browser (one launched browser process family)
  +-- BrowserContext A (cookies/storage/permissions for population A)
  |     +-- Page 1 (one tab/document lifecycle)
  |           +-- Locator (a re-evaluated way to find an element)
  +-- BrowserContext B (isolated population B)
        +-- Page 2
```

An object is not the same thing as the browser concept it represents: a Locator
is a Playwright handle for finding/acting, not a DOM node captured forever.

## Required external instruction

### Microsoft Learn, first half

**Direct link:** [Build your first end-to-end test with Playwright](https://learn.microsoft.com/en-us/training/modules/build-with-playwright/)  
**Exact section, chapter, or unit:** Units 1-4: Introduction; What is Playwright?; How Playwright works; Set up your environment  
**Estimated time:** 50 minutes  
**What to focus on:** browser automation purpose, supported languages/browsers, test anatomy, and setup concepts  
**What to skip:** no linked modules beyond this eight-unit module; do not copy its target into AATE  
**Expected takeaway:** describe the lifecycle from launch through context, page, locator/action, assertion, and cleanup.

### Isolation assignment

**Direct link:** [Playwright Isolation](https://playwright.dev/docs/browser-contexts)  
**Exact section, chapter, or unit:** What is test isolation?; How Playwright achieves test isolation  
**Estimated time:** 20 minutes  
**What to focus on:** clean-slate state and why a new context is cheaper than a whole browser  
**What to skip:** multi-user examples until Lesson 3  
**Expected takeaway:** explain which state a BrowserContext isolates and why separate adversarial populations need deliberate contexts.

## Course bridge

Playwright launches a `Browser`; a `BrowserContext` provides an isolated browser
session with its own cookies, local storage, and related state; a `Page` models a
tab; and a `Locator` describes how to find an element when an action or assertion
occurs.[^pw-isolation]

[^pw-isolation]: Playwright, "Isolation," What is test isolation? and How Playwright achieves test isolation.

Actions and navigation return Promises because the browser work completes
asynchronously. Playwright adds waiting around actionable elements, but the
operator must still define what workflow completion means. A visible line of
text may be a useful UI assertion; a protected action needs authoritative state.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Use one context per deliberately isolated identity or
    population. Reusing a context means reusing its state; creating a new page in
    the same context does not create a clean identity.

## Worked example

```typescript
const browser = await chromium.launch();
const context = await browser.newContext();
const page = await context.newPage();
const query = page.locator("#query");
await query.fill("widget");
await context.close();
await browser.close();
```

| Line | Object/async meaning |
|---|---|
| `chromium.launch()` | asynchronously starts Chromium and returns Browser |
| `browser.newContext()` | creates isolated storage/cookie state |
| `context.newPage()` | creates a Page inside that state boundary |
| `page.locator(...)` | defines a re-evaluated element query; no action yet |
| `query.fill(...)` | waits for actionability, then changes the input |
| close calls | explicitly release context then browser resources |

## Guided exercise

### Objective

Design the object tree for two controlled populations before writing code.

### Setup

Use paper or `artifacts/module-03/object-model.md`. No service is needed.

### Exact actions or commands

1. Draw one Browser containing manual-equivalent and clean-state contexts.
2. Put an initial and follow-up Page inside each context.
3. Add locators for query, search button, status, and first result.
4. Mark which state is shared by pages within a context and isolated across
   contexts.
5. Add creation, action, assertion, and cleanup order.

### Expected output

The two populations use two contexts, not merely two pages. Pages within one
context share cookie/storage state. Every created context and Browser has a
matching cleanup step.

### Interpretation

This design prevents an accidental state carryover from being mistaken for a
control bypass or different identity. Later lessons test the state directly.

### Common failure modes

- Calling BrowserContext an OS process guarantee
- Assuming two pages in one context have isolated cookies
- Treating a Locator as a permanently captured DOM element
- Omitting `await` or cleanup

### Cleanup

No process was launched. Keep the design as the artifact.

## Why this matters offensively

State isolation is experimental control. It decides whether a challenge token,
session cookie, local value, or cached resource was carried into the next trial.
An unexplained context lifecycle invalidates replay and evasion conclusions.

## Required artifact

`artifacts/module-03/object-model.md` with the object tree, lifecycle table,
shared/isolated state, and one invalid design with an explanation of its bias.

## Pass gate

1. What is the Browser object's responsibility?
2. Which object is the primary isolation boundary for cookies and storage?
3. Does a new Page in an existing context create a clean session?
4. Why is a Locator not a frozen DOM node?
5. Which asynchronous resources require explicit cleanup?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. It represents and controls the launched browser instance from which contexts are created.
2. BrowserContext.
3. No; pages in a context share that context's state.
4. It describes how Playwright resolves an element at action/assertion time.
5. At minimum the contexts and Browser; pages may also be closed explicitly when their lifecycle ends earlier.

</details>

## Next lesson

[First local browser workflow](02-first-browser.md) implements this lifecycle
against the already-understood static application.
