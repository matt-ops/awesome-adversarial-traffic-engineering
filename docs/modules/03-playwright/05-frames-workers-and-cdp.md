# Frames, workers, and CDP

<!-- source-ids: playwright-cdpsession, chrome-browser-process-model, aate-local-lab -->

> **Progress**  
> Module: 03 - Playwright foundations  
> Lesson: 5 of 5  
> Depth: Applied  
> Estimated time: 2 hours  
> Prerequisites: Network events and browser process model  
> Artifact: `artifacts/module-03/context-observations.json`  
> Next: Automated-abuse objectives

## Role outcome

Collect comparable top-page, iframe, and worker observations and explain when a
Chromium-only CDP session is appropriate and version-sensitive.

## Prerequisites

- [Network events and evidence](04-network-events.md)
- [Browser process model](../02-browser-javascript/01-browser-process-model.md)
- Successful first local Playwright workflow

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Playwright CDPSession](https://playwright.dev/docs/api/class-cdpsession) | Overview; attach/detach; send; event subscription | Defines the raw Chromium DevTools Protocol connection |
| OFFICIAL_DOCUMENTATION | [Chrome browser process model](https://developer.chrome.com/blog/inside-browser-part1/) | Browser architecture; process responsibilities | Explains why contexts and processes are distinct |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Top page, same-origin iframe, dedicated worker | Supplies controlled context outputs |

## Mental model

| Surface | Global/document | Playwright access | Portability |
|---|---|---|---|
| Top Page | `Window` + `document` | `page.evaluate` | browser-agnostic API |
| Iframe | another `Window` + document | `frame.evaluate` / frame locator | browser-agnostic API |
| Worker | Worker global, no document | `worker.evaluate` | browser-agnostic API |
| CDP target/session | raw Chromium protocol domains | `newCDPSession`, `send`, events | Chromium-only, protocol/version-sensitive |

## Required external instruction

### CDPSession assignment

**Direct link:** [Playwright CDPSession](https://playwright.dev/docs/api/class-cdpsession)  
**Exact assignment:** class overview; `detach`; `send`; event subscription examples  
**Estimated time:** 25 minutes  
**Focus on:** raw protocol escape hatch, command/event pattern, and Chromium-only limitation  
**Skip:** domain-specific CDP command catalogs and runtime modification  
**Expected takeaway:** justify CDP only when the cross-browser Playwright API lacks the required observation.

## Course bridge

Frames and workers are distinct execution contexts even when delivered from one
origin. Playwright exposes high-level evaluation APIs for each. CDPSession sends
raw Chrome DevTools Protocol commands and receives protocol events; Playwright
documents it as Chromium-only.[^cdp]

[^cdp]: Playwright API, "CDPSession," overview and methods.

!!! info "Version-sensitive observation"
    CDP domains, fields, target attachment, and browser behavior can change with
    Chromium. Record browser and Playwright versions and avoid making CDP the
    default when a supported Playwright API answers the question.

## Worked example

```typescript
const pageValue = await page.evaluate(() => navigator.language);
const frameValue = await page.frames()[1].evaluate(() => navigator.language);
const worker = await page.waitForEvent("worker");
const workerValue = await worker.evaluate(() => navigator.language);
```

Each callback executes inside a different browser context and returns one
serializable value to Node. Matching values show consistency for this property
in this trial; they do not prove a unique or authentic identity.

## Guided exercise

### Objective

Capture a context matrix and one read-only CDP observation.

### Setup

Start the static server. Create a fixed-target learner script based on the first
workflow. Register the worker listener before navigation so creation is not
missed.

### Actions

1. Record `navigator.language` and `navigator.platform` from top page and frame.
2. Record language and `hardwareConcurrency` from the dedicated worker.
3. Record browser and Playwright versions.
4. Create a CDPSession for the Page, send `Browser.getVersion`, save the returned
   product/protocol fields, then detach.
5. Serialize raw observations plus context, timestamp, version, and errors.
6. State why `Browser.getVersion` was educational but not necessary for the
   high-level context values.

### Expected output

The page and frame return language/platform; the worker returns language and a
numeric concurrency value. CDP returns Chromium product and protocol version
metadata. Values depend on the local environment and must not be hard-coded as a
universal expectation.

### Interpretation

This is a collection pattern, not an evasion. Later modules establish a manual,
headed, headless, and HTTP-client population before forming a controlled
hypothesis about a trusted signal.

### Common failure modes

- Registering `waitForEvent("worker")` after the worker already started
- Assuming frame index without verifying its URL
- Using CDP for a value already available through Playwright
- Claiming matching values prove authenticity
- Failing to detach or close resources

### Cleanup

Detach the CDPSession, close contexts and Browser, stop the server, and retain
only local synthetic observations.

## Why this matters offensively

Cross-context collection exposes incomplete modifications and distinguishes
browser-exposed identity from Node/client and protocol behavior. CDP enables
deeper approved observation, but its version sensitivity becomes part of the
finding's limitations and retest plan.

## Required artifact

`artifacts/module-03/context-observations.json` with environment, top/frame/worker
values, CDP version response, errors, conclusion, and prohibited inferences.

## Pass gate

1. Why might page and worker globals differ?
2. What must happen before a short-lived worker starts?
3. Is CDPSession cross-browser?
4. What does matching language across contexts prove?
5. Why record browser and protocol versions?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. They are different execution contexts with different global interfaces and instrumentation reach.
2. The worker event listener/wait must be registered early enough to observe creation.
3. No; Playwright documents CDPSession as Chromium-only.
4. Only that this property was consistent across the observed contexts in this trial.
5. CDP and observable browser behavior drift, so results and retests require the exact environment.

</details>

## Next lesson

[Open Module 04](../04-automated-abuse/index.md) to shift from learning the
browser client to modeling the hostile workflow it will perform.
