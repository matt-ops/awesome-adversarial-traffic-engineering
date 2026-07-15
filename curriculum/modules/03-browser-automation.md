# Module 3: Browser automation

## Why this matters

Browser automation creates representative client behavior and exposes browser-side evidence that raw HTTP clients cannot. The role requires understanding the object and event model, not merely copying a scraping script.

## Role outcomes

You can build safe local Playwright workflows, isolate state, collect browser events, use CDP for focused observation, compare populations, and distinguish framework artifacts from browser or task behavior.

## Level 1: Foundation, 24-hour checkpoint

### Knowledge outcome

Explain Browser, BrowserContext, Page, navigation, cookies, storage state, requests and responses, and headed versus headless execution. Know that a Context is an isolated session container and a Page is a tab-like document surface.

### Hands-on outcome

Install Playwright, launch Chromium, create one BrowserContext and Page, navigate only to the local lab, capture request and response events, complete a simple search, and save structured output.

### Interview outcome

Explain the object model, why Context isolation matters, what state persists, and why changing a user agent alone does not create a coherent browser identity.

### Required artifact

One working Playwright script against the local lab plus saved request/response output.

### Completion test

From a clean state, run the script, show a successful local navigation, identify Browser/Context/Page in the code, locate a response status, and prove the script rejects or lacks any external target input.

### Estimated time

4 focused hours.

### Required resources only

- [Playwright introduction](https://playwright.dev/docs/intro) — `[L1 Foundation]` `[Required]` installation and first test only
- [Playwright BrowserContext](https://playwright.dev/docs/api/class-browsercontext) — `[L1 Foundation]` `[Required]` overview and core methods only
- [Playwright network events](https://playwright.dev/docs/network) — `[L1 Foundation]` `[Required]` observation only

### Optional deeper resources

- [Playwright pages](https://playwright.dev/docs/pages) — `[L1 Foundation]` `[Recommended]`

## Level 2: Applied, 7-day checkpoint

### Knowledge outcome

Explain multiple contexts, fresh versus reused storage, frames, workers, service workers, CDP sessions, execution contexts, and Network and Runtime events.

### Hands-on outcome

Run multiple BrowserContexts, save and reuse storage state, observe frame and worker creation, and collect selected CDP Network and Runtime events for local manual-equivalent and automated workflows.

### Interview outcome

Compare Playwright API and CDP evidence and explain which observations belong to the browser, page, renderer context, network stack, or server.

### Required artifact

Structured event bundle covering contexts, storage, requests, responses, frames, workers, and selected CDP events with a short interpretation.

### Completion test

Demonstrate state isolation and reuse, map at least five events to their source layer, and explain two causes of missing or reordered events.

### Estimated time

4 additional focused hours.

### Required resources only

- [Playwright events](https://playwright.dev/docs/events) — `[L2 Applied]` `[Required]`
- [Playwright CDPSession](https://playwright.dev/docs/api/class-cdpsession) — `[L2 Applied]` `[Required]`
- [CDP Network domain](https://chromedevtools.github.io/devtools-protocol/tot/Network/) — `[L2 Applied]` `[Required]` selected events only

### Optional deeper resources

- [CDP Runtime domain](https://chromedevtools.github.io/devtools-protocol/tot/Runtime/) — `[L2 Applied]` `[Recommended]`

## Level 3: Integrated, 21-day checkpoint

### Knowledge outcome

Explain how client design, task flow, accessibility-like interaction, timing, state reuse, frames, workers, and error recovery affect server and sensor evidence.

### Hands-on outcome

Create at least four local client populations: manual browser, normal Playwright, fast scripted Playwright, and keyboard-only accessibility-like Playwright. Add one local rule-based browser-agent run and correlate browser and server telemetry.

### Interview outcome

Separate browser-framework artifacts, task-policy artifacts, environment configuration, and true workflow abuse; discuss how a detector can fail legitimate automation or accessibility tools.

### Required artifact

Client-population design, deterministic run logs, correlation table, and agent-versus-script behavior comparison.

### Completion test

Reproduce each population, explain which differences are causal versus incidental, and identify at least three accessibility or test-automation false-positive risks.

### Estimated time

6 additional focused hours.

### Required resources only

- [Playwright repository](https://github.com/microsoft/playwright) — `[L3 Integrated]` `[Required]` issues/design material relevant to the chosen behavior
- [AATE browser-process concept](../../docs/concepts/browser-process-model.md) — `[L3 Integrated]` `[Required]`

### Optional deeper resources

- [OpenWPM](https://github.com/openwpm/OpenWPM) — `[L3 Integrated]` `[Optional]` research architecture reference

## Level 4: Deep, 6-week checkpoint

### Knowledge outcome

Understand execution contexts, renderer processes, target attachment, runtime instrumentation, source maps, selected browser implementation details, and version drift well enough to investigate a narrow question.

### Hands-on outcome

Instrument the local sensor or browser runtime, trace one value from collection through transmission, compare contexts or versions, and use browser source only when necessary to resolve the question.

### Interview outcome

Teach the investigation method, defend what Playwright or CDP changed, and explain which result is implementation-specific or unstable.

### Required artifact

Runtime investigation note with reproduction, event timeline, source references, version details, alternatives, and limitations.

### Completion test

A second researcher can reproduce the observation on the pinned version and understands what would need retesting after a browser update.

### Estimated time

8–12 additional focused hours.

### Required resources only

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) — `[L4 Deep]` `[Required]` domains relevant to the question

### Optional deeper resources

- [Chromium source](https://source.chromium.org/chromium) — `[L4 Deep]` `[Optional]`
- [Chrome JavaScript debugging](https://developer.chrome.com/docs/devtools/javascript/) — `[L4 Deep]` `[Recommended]`

## Common misconceptions

- Headless versus headed is not a universal human-versus-bot boundary.
- BrowserContext isolation is substantial but not equivalent to a separate host or network stack.
- CDP access does not explain every server-side observation.
- A public detector score is not a controlled experiment.

## Production limitations

The local client set does not represent browser versions, devices, extensions, enterprise policies, assistive technology, mobile webviews, geographies, networks, or adversarial adaptation at production scale.

## Interview questions

1. Explain Browser, BrowserContext, Page, Frame, Worker, and CDPSession.
2. What evidence changes when storage state is reused?
3. How would you determine whether an artifact comes from Playwright, Chromium, or the task policy?

## Related lab components

- `lab/clients/playwright/`
- `lab/sensor/`
- `lab/agent/`
- `lab/telemetry/`

