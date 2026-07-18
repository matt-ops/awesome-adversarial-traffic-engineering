# First local Playwright workflow

<!-- source-ids: microsoft-learn-playwright, aate-local-lab -->

## Progress

- Module: 03 - Playwright foundations
- Lesson: 2 of 5
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [Playwright object model](01-object-model.md)
  - Complete JavaScript/async prerequisites from Module 02
  - Node 22 or later and npm; use `node --version` and `npm --version` to verify
- Required artifact: `lab/telemetry/playwright-first-workflow.json`
- Next lesson: Contexts and state

## Role outcome

Execute, explain, and verify a headed Playwright workflow against a loopback
application without Docker.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Microsoft Learn: Build with Playwright](https://learn.microsoft.com/en-us/training/modules/build-with-playwright/) | All eight units | Provides guided beginner setup, first test, debugging, and completion check | Test-automation framing; the course bridge translates the objects into adversarial workflows. |
| LAB_SPECIFIC | [First Playwright workflow](../../labs/foundation/first-playwright.md) | Entire commented source described there | Supplies a tested, fixed-target local workflow | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

| Phase | Playwright operation | Observable proof |
|---|---|---|
| Arrange | launch, context, page, listeners | browser opens; listeners active before navigation |
| Act | navigate, fill, click | requests occur and DOM changes |
| Assert | wait for `Found 1`, read result/storage | exact expected values captured |
| Preserve | serialize network artifact | JSON contains target, result, state, events |
| Cleanup | close context and Browser | no browser process intentionally left running |

## Required external instruction

### Complete Microsoft Learn module

**Direct link:** [Build your first end-to-end test with Playwright](https://learn.microsoft.com/en-us/training/modules/build-with-playwright/)  
**Exact section, chapter, or unit:** Complete all eight units in order, including its knowledge check  
**Estimated time:** 75 minutes  
**What to focus on:** test lifecycle, locators, assertions, execution, debugging, and cleanup; translate concepts to the AATE script rather than copying its public target  
**What to skip:** linked follow-on modules and cloud/browser-grid material  
**Expected takeaway:** explain every object and asynchronous step in `first_workflow.ts` before executing it.

## Course bridge

The first script deliberately uses library objects directly instead of a test
runner fixture so their ownership is visible. The target is a constant loopback
URL, and the exercise runs **without Docker**. The script does not accept an
arbitrary target.

### Every import

```typescript
import { chromium, type Request, type Response } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";
```

- `@playwright/test` is the pinned npm package in `package-lock.json`.
  `chromium` is a runtime launcher object. `Request` and `Response` are
  TypeScript-only type imports: the compiler checks how the event objects are
  used, then erases those imports from emitted JavaScript.
- `node:fs/promises` is a Node standard-library module, not another package to
  download. `mkdir` creates the artifact directory; `writeFile` serializes the
  evidence. The `/promises` form makes both operations awaitable.

### Browser, BrowserContext, Page, and Locator

| Object | Created by | Owns or represents | Why this exercise needs it |
|---|---|---|---|
| `Browser` | `chromium.launch()` | One Chromium process tree controlled by Playwright | Establishes the actual browser population and version boundary |
| `BrowserContext` | `browser.newContext()` | An isolated cookie/cache/storage partition inside that Browser | Gives the workflow a deliberate identity/state boundary |
| `Page` | `context.newPage()` | One tab/document and its frames, workers, events, and navigation | Hosts the protected workflow and network observers |
| `Locator` | `page.locator(selector)` | A re-resolved query for an element, not a stored DOM node | Performs actions and waits against the current DOM state |

A `BrowserContext` is not a tab and not merely an incognito label. It is the
isolation container whose cookies and origin storage influence later requests.
`context.storageState()` can serialize cookies and local-storage snapshots for
deliberate reuse. This first script only *reads* one local-storage value; the
next lesson exports and restores state so the security consequences are clear.

### Every asynchronous step

`await` pauses `main` until the Promise settles; it does not block the browser's
network or renderer threads. Each use has a specific completion meaning:

1. `await chromium.launch(...)` waits for the controlled Browser to start.
2. `await browser.newContext()` waits for a fresh isolated state container.
3. `await context.newPage()` waits for a Page attached to that context.
4. `await page.goto(...)` waits for navigation and the declared `networkidle`
   condition, bounded by five seconds. It does not prove application success.
5. `await locator.fill("widget")` waits until the input is actionable and its
   value is replaced.
6. `await locator.click()` waits until the button is actionable and dispatches
   the click; the application response can still be pending.
7. `await locator.waitFor()` waits for status text containing `Found 1`, the
   local UI completion condition.
8. `await locator.textContent()` reads the first result after that condition.
9. `await page.evaluate(...)` executes the provided function in the page realm
   and returns the origin's `localStorage` value to Node.
10. `await mkdir(...)` ensures the evidence directory exists.
11. `await writeFile(...)` waits until the JSON bytes are written; without it,
    the process could exit before the artifact is complete.
12. `await context.close()` releases pages and context-owned state.
13. `await browser.close()` terminates the controlled Browser.

The `request` and `response` listeners are registered *synchronously* before
`goto`. Their callbacks run when Playwright emits events. A request event proves
the client began an HTTP exchange; its response partner adds status and URL. An
event pair still does not prove a protected business action, which is why the
script separately preserves the rendered result and storage observation.

!!! warning "Safety boundary"
    The script is fixed to `http://127.0.0.1:4173`. Do not generalize it into an
    arbitrary-target runner. Provider labs are used only when a later lesson
    names the provider target and allowed action.

## Worked example

The core action sequence is:

```typescript
await page.goto(BASE_URL, { waitUntil: "networkidle", timeout: 5_000 });
await page.locator("#query").fill("widget");
await page.locator("#search").click();
await page.locator("#status").filter({ hasText: "Found 1" }).waitFor();
```

`goto` navigates and bounds waiting to five seconds. `fill` resolves the input
Locator and changes its value. `click` dispatches the user-like button action.
The last line narrows the status Locator to expected text and waits for it. It is
a UI completion assertion, while the following reads and network events form
the exercise evidence.

Use this manual and automated comparison after the run:

| Question | Manual DevTools trace | Playwright artifact |
|---|---|---|
| Which action was performed? | You record the typed query and click | Script source plus `result` record the fixed action and outcome |
| Which resources were requested? | Network panel rows and request details | Ordered local request/response event objects |
| Which client state changed? | Application/Storage panel shows `aate-last-query` | `storedQuery` contains `widget` |
| What can be replayed? | Exported or copied request if you deliberately preserve it | Nothing beyond recorded metadata in this first exercise |
| What does it prove? | One observed manual workflow | One repeatable automated workflow—not evasion or authorization bypass |

## Guided exercise

### Objective

Complete the tested headed workflow and reconcile it with the manual trace.

### Setup

From the repository root, dependency installation resolves the pinned packages
in `package-lock.json`. Browser installation downloads the matching Chromium if
it is not already present.

```powershell
npm.cmd install
npx.cmd playwright install chromium
```

Then start the static target in its own terminal:

```powershell
python -m http.server 4173 --bind 127.0.0.1 --directory lab/foundation-web
```

### Exact actions or commands

1. Read `lab/clients/playwright/first_workflow.ts` from imports through cleanup.
2. Predict the ordered resource requests using the Module 01 trace.
3. Start the headed workflow with `npm.cmd run playwright:first`.
4. Watch the browser search, then inspect
   `lab/telemetry/playwright-first-workflow.json`.
5. Compare resource families, result, and stored query with the manual baseline.
6. Execute `npm.cmd run typecheck` and explain why static type success is not a
   substitute for runtime assertions.

### Expected output

The terminal reports `Synthetic Widget - 5 available`, stored query `widget`,
and a saved event count. The JSON contains `target`, `result`, `storedQuery`, and
request/response events for the local document, assets, frame, worker, and
inventory. Exact event interleaving may vary; paired URLs and outcomes matter.

### Interpretation

The workflow proves that Playwright reproduced the local UI/search behavior and
captured its trace. It does not prove evasion or an authorization bypass. That
distinction is intentional: first learn the browser client correctly.

### Common failure modes

- `ERR_CONNECTION_REFUSED`: static server is absent or stopped
- browser executable missing: complete the pinned Chromium installation step
- changing the target/port and invalidating the fixed safety and expected output
- counting event order as stable across every browser version
- leaving a browser open after an exception; retain the script's cleanup path

### Cleanup

The script closes its Browser. Press Ctrl+C in the static-server terminal. Keep
the JSON as the required artifact.

## Why this matters offensively

An automated adversary begins as a faithful, explainable workflow. Only after
the normal action, state, trace, and cleanup are reliable can an operator vary a
signal or state binding and attribute a changed outcome to that experiment.

## Required artifact

Keep `lab/telemetry/playwright-first-workflow.json` and create
`artifacts/module-03/first-workflow-review.md` with object/line explanations,
manual comparison, observed versions, conclusion, and limitations.

## Pass gate

1. Why are listeners attached before `goto`?
2. What completion condition does the status Locator establish?
3. Why is the script headed by default?
4. What does the JSON artifact prove and not prove?
5. Why can typecheck pass while the workflow fails?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. Navigation begins resource requests immediately, so later listeners would miss early evidence.
2. The page rendered status text containing `Found 1` after the search action.
3. A beginner can observe and correlate actions; headless is introduced as a deliberate later population.
4. It proves one local workflow result, storage value, and observed browser events; it does not prove control evasion or server-side mutation.
5. Types validate program structure, not server availability, browser behavior, selectors, or runtime assertions.

</details>

## Next lesson

[Contexts and state](03-contexts-and-state.md) measures what a context preserves
and what a clean context removes.
