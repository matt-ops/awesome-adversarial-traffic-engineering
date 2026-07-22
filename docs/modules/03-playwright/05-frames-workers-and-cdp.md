# Frames, workers, and CDP

<!-- source-ids: playwright-cdpsession, chrome-browser-process-model, aate-local-lab -->

## Progress

- Module: 03 - Playwright foundations
- Lesson: 5 of 5
- Depth: Applied
- Estimated time: 2 hours
- Prerequisites:
  - [Network events and evidence](04-network-events.md)
  - [Browser process model](../02-browser-javascript/01-browser-process-model.md)
  - Successful first local Playwright workflow
- Next lesson: Automated-abuse objectives

## Role outcome

Collect comparable top-page, iframe, and worker observations and explain when a
Chromium-only CDP session is appropriate and version-sensitive.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Playwright CDPSession](https://playwright.dev/docs/api/class-cdpsession) | Overview; attach/detach; send; event subscription | Defines the raw Chromium DevTools Protocol connection | Chromium-only and explicitly not a Foundation assignment. |
| OFFICIAL_DOCUMENTATION | [Chrome browser process model](https://developer.chrome.com/blog/inside-browser-part1/) | Browser architecture; process responsibilities | Explains why contexts and processes are distinct | Historical Chrome architecture article; implementation details evolve. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Top page, same-origin iframe, dedicated worker | Supplies controlled context outputs | Deliberately small and vulnerable; results do not generalize to production systems. |

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
**Exact section, chapter, or unit:** class overview; `detach`; `send`; event subscription examples  
**Estimated time:** 25 minutes  
**What to focus on:** raw protocol escape hatch, command/event pattern, and Chromium-only limitation  
**What to skip:** domain-specific CDP command catalogs and runtime modification  
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

### Exact actions or commands

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

## Check your understanding

1. The top page, iframe, and worker each expose a different global environment. Why can an API or instrumented value appear in the page but not the worker?
2. The page creates a short-lived worker during navigation. When must the worker event listener be registered to avoid missing that worker?
3. The exercise opens a CDPSession and sends `Browser.getVersion`. Why is that step limited to Chromium rather than portable across all Playwright browsers?
4. Page, frame, and worker all report `en-US` in one trial. What does the matching value prove, and what identity claim remains unsupported?
5. Why should the context matrix record both the browser version and the returned protocol version?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Each execution context has a different global interface and may be reached by different instrumentation.** Workers have a worker global and no document, so page-only APIs or changes may be unavailable there.

- **2. Register the listener or wait before navigation or any action that creates the worker.** A listener attached after the short-lived worker starts may never observe the creation event.

- **3. CDPSession exposes the Chromium DevTools Protocol, which is an engine-specific interface rather than a browser-neutral Playwright API.** High-level page, frame, and worker APIs are the portable choice when sufficient.

- **4. The match proves only that this property was consistent across the observed contexts in the recorded trial.** It does not prove a unique user, a genuine device, or control acceptance.

- **5. Browser behavior and CDP fields can change across versions.** Recording both versions lets a reviewer reproduce the environment, interpret drift, and avoid attributing a protocol change to the wrong cause.

</details>

## Next lesson

[Open Module 04](../04-automated-abuse/index.md) to shift from learning the
browser client to modeling the hostile workflow it will perform.
