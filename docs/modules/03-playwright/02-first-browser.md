# First local Playwright workflow

<!-- source-ids: microsoft-learn-playwright, aate-local-lab -->

> **Progress**  
> Module: 03 - Playwright foundations  
> Lesson: 2 of 5  
> Depth: Foundation  
> Estimated time: 3 hours  
> Prerequisites: Playwright object model  
> Artifact: `lab/telemetry/playwright-first-workflow.json`  
> Next: Contexts and state

## Role outcome

Execute, explain, and verify a headed Playwright workflow against a loopback
application without Docker.

## Prerequisites

- [Playwright object model](01-object-model.md)
- Complete JavaScript/async prerequisites from Module 02
- Node 22 or later and npm; use `node --version` and `npm --version` to verify

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Microsoft Learn: Build with Playwright](https://learn.microsoft.com/en-us/training/modules/build-with-playwright/) | All eight units | Provides guided beginner setup, first test, debugging, and completion check |
| LAB_SPECIFIC | [First Playwright workflow](../../labs/foundation/first-playwright.md) | Entire commented source described there | Supplies a tested, fixed-target local workflow |

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
**Exact assignment:** Complete all eight units in order, including its knowledge check  
**Estimated time:** 75 minutes  
**Focus on:** test lifecycle, locators, assertions, execution, debugging, and cleanup; translate concepts to the AATE script rather than copying its public target  
**Skip:** linked follow-on modules and cloud/browser-grid material  
**Expected takeaway:** explain every object and asynchronous step in `first_workflow.ts` before executing it.

## Course bridge

The AATE script imports Playwright's `chromium` launcher plus `Request` and
`Response` TypeScript types. Node's `fs/promises` functions create a directory
and write the evidence file asynchronously. The target is a constant loopback
URL; the script does not accept arbitrary targets.

Listeners are attached before navigation, or early events would be lost. The
script waits for a specific status, reads the first result and local storage,
writes the raw local event list, then closes its resources.

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

### Actions

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
