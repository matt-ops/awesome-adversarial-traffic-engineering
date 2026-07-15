# Browser contexts and storage state

<!-- source-ids: playwright-browser-contexts, playwright-auth, aate-local-lab -->

> **Progress**  
> Module: 03 - Playwright foundations  
> Lesson: 3 of 5  
> Depth: Foundation  
> Estimated time: 110 minutes  
> Prerequisites: First local Playwright workflow  
> Artifact: `artifacts/module-03/context-state.md`  
> Next: Network events

## Role outcome

Create clean and state-restored browser populations and state precisely which
cookies, origins, and storage values were carried between trials.

## Prerequisites

- [First local Playwright workflow](02-first-browser.md)
- Browser/BrowserContext/Page lifecycle

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Playwright Isolation](https://playwright.dev/docs/browser-contexts) | Isolation; two ways of test isolation; multiple contexts | Defines clean context behavior and multi-user patterns |
| OFFICIAL_DOCUMENTATION | [Playwright Authentication](https://playwright.dev/docs/auth) | Core concepts; storage state; session storage limitation | Defines persistent authentication/state reuse and its limits |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | `aate-last-query` local storage | Provides harmless state to measure |

## Mental model

| Trial | Context | Initial state | Expected query |
|---|---|---|---|
| A1 | A | empty | empty, then `widget` after action |
| A2 | second Page in A | shared A state | `widget` |
| B1 | new context B | empty | empty |
| C1 | new context from saved A state | restored cookies/local storage | `widget` |

Storage-state reuse is an experimental change. It must not be hidden inside test
setup.

## Required external instruction

### Context isolation assignment

**Direct link:** [Playwright Isolation](https://playwright.dev/docs/browser-contexts)  
**Exact assignment:** What is test isolation?; Two ways of test isolation; How Playwright achieves isolation; Multiple contexts in a single test  
**Estimated time:** 30 minutes  
**Focus on:** clean-slate reproducibility and deliberate multi-context workflows  
**Skip:** framework-specific fixture customization beyond the examples  
**Expected takeaway:** design trials that either share or isolate state intentionally.

### Storage-state assignment

**Direct link:** [Playwright Authentication](https://playwright.dev/docs/auth)  
**Exact assignment:** Core concepts; storage state reuse; session storage limitation  
**Estimated time:** 30 minutes  
**Focus on:** what the state file can contain, secret handling, and what it omits  
**Skip:** provider-specific login recipes and parallel account pools  
**Expected takeaway:** describe exactly what was restored and protect real authentication state from source control.

## Course bridge

Playwright contexts isolate cookies and origin storage, supporting reproducible
clean-state tests.[^pw-context] Storage state can serialize reusable cookies and
local storage, but the file may contain credentials capable of impersonation and
must not be committed when it represents a real account.[^pw-auth]

[^pw-context]: Playwright, "Isolation," How Playwright achieves test isolation.
[^pw-auth]: Playwright, "Authentication," Introduction and Core concepts.

!!! warning "Safety boundary"
    Use only synthetic local state in course artifacts. Keep real storage-state
    files outside the repository and follow the provider's authorization rules.

## Worked example

```typescript
const first = await browser.newContext();
// ... set localStorage through the local workflow ...
await first.storageState({ path: "artifacts/local-state.json" });
const clean = await browser.newContext();
const restored = await browser.newContext({ storageState: "artifacts/local-state.json" });
```

`clean` should not inherit `first`. `restored` deliberately begins from the
serialized state. The state file is the changed variable and must appear in the
experiment record.

## Guided exercise

### Objective

Demonstrate shared, isolated, and restored local storage with three contexts.

### Setup

Copy the fixed-target first workflow to an ignored learner workspace or a new
artifact script. Keep the target `127.0.0.1:4173`. Start the static server.

### Actions

1. In context A complete the `widget` search and save storage state.
2. Open a second Page in A and record the initial input value.
3. Create clean context B, open the page, and record the initial value.
4. Create context C from A's saved state and record the initial value.
5. Close A, B, C, and the Browser in a `finally` path.
6. Inspect the synthetic state file and identify cookies and origin/localStorage
   sections without adding any real secrets.

### Expected output

The second Page in A and restored context C begin with `widget`; clean context B
begins empty. The state file contains origin-scoped local storage and no real
authentication credential.

### Interpretation

Pages do not define the state boundary; contexts do. Restoring state can model
an approved session, but it is not evidence that the server accepts a protected
action until that action is repeated.

### Common failure modes

- Creating two Pages instead of two contexts for isolation
- Saving state before the query is stored
- Committing a real authentication state file
- Assuming session storage is automatically included
- Omitting cleanup after an assertion fails

### Cleanup

Close all contexts/Browser, stop the server, and delete the temporary state file
after recording its synthetic structure.

## Why this matters offensively

Replay, challenge, authentication, and workflow experiments depend on state
bindings. Context discipline tells whether success came from a changed signal,
carried approval state, or an accidentally reused session.

## Required artifact

`artifacts/module-03/context-state.md` with the trial matrix, creation code,
observed values, state-file schema, secret-handling rule, and conclusion.

## Pass gate

1. Which state boundary separates contexts A and B?
2. Why does a second Page in A see A's local storage?
3. What is the changed variable for restored context C?
4. Why are real storage-state files sensitive?
5. Does restored local storage prove a server-side authorization bypass?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. Each BrowserContext has isolated cookie and origin storage state.
2. Pages in the same context share that context's origin-scoped state.
3. C is initialized from A's serialized storage-state artifact.
4. They may contain cookies/tokens that permit account impersonation.
5. No; the protected server action and authoritative state must still be tested.

</details>

## Next lesson

[Network events](04-network-events.md) captures the HTTP evidence produced by
each deliberately controlled context.
