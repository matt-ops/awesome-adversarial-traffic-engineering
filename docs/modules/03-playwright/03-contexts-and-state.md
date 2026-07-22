# Browser contexts and storage state

<!-- source-ids: playwright-browser-contexts, playwright-auth, aate-local-lab -->

## Progress

- Module: 03 - Playwright foundations
- Lesson: 3 of 5
- Depth: Foundation
- Estimated time: 110 minutes
- Prerequisites:
  - [First local Playwright workflow](02-first-browser.md)
  - Browser/BrowserContext/Page lifecycle
- Next lesson: Network events

## Role outcome

Create clean and state-restored browser populations and state precisely which
cookies, origins, and storage values were carried between trials.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Playwright Isolation](https://playwright.dev/docs/browser-contexts) | Isolation; two ways of test isolation; multiple contexts | Defines clean context behavior and multi-user patterns | Examples follow the current Playwright test API and can change by version. |
| OFFICIAL_DOCUMENTATION | [Playwright Authentication](https://playwright.dev/docs/auth) | Core concepts; storage state; session storage limitation | Defines persistent authentication/state reuse and its limits | Test-suite examples require offensive reinterpretation and careful secret handling. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | `aate-last-query` local storage | Provides harmless state to measure | Deliberately small and vulnerable; results do not generalize to production systems. |

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
**Exact section, chapter, or unit:** What is test isolation?; Two ways of test isolation; How Playwright achieves isolation; Multiple contexts in a single test  
**Estimated time:** 30 minutes  
**What to focus on:** clean-slate reproducibility and deliberate multi-context workflows  
**What to skip:** framework-specific fixture customization beyond the examples  
**Expected takeaway:** design trials that either share or isolate state intentionally.

### Storage-state assignment

**Direct link:** [Playwright Authentication](https://playwright.dev/docs/auth)  
**Exact section, chapter, or unit:** Core concepts; storage state reuse; session storage limitation  
**Estimated time:** 30 minutes  
**What to focus on:** what the state file can contain, secret handling, and what it omits  
**What to skip:** provider-specific login recipes and parallel account pools  
**Expected takeaway:** describe exactly what was restored and protect real authentication state from source control.

## Course bridge

Playwright contexts isolate cookies and origin storage, supporting reproducible
clean-state tests.[^pw-context] Storage state can serialize reusable cookies and
local storage, but the file may contain credentials capable of impersonation and
must not be committed when it represents a real account.[^pw-auth]

[^pw-context]: Playwright, "Isolation," How Playwright achieves test isolation.
[^pw-auth]: Playwright, "Authentication," Introduction and Core concepts.

!!! warning "Safety boundary"
    Use only synthetic local state in course exercises. Keep real storage-state
    files outside the repository and follow the provider's authorization rules.

## Worked example

```typescript
const first = await browser.newContext();
// ... set localStorage through the local workflow ...
await first.storageState({ path: "local-state.json" });
const clean = await browser.newContext();
const restored = await browser.newContext({ storageState: "local-state.json" });
```

`clean` should not inherit `first`. `restored` deliberately begins from the
serialized state. The state file is the changed variable and must appear in the
experiment record.

## Guided exercise

### Objective

Demonstrate shared, isolated, and restored local storage with three contexts.

### Setup

Copy the fixed-target first workflow to a temporary script in a working
directory of your choice. Keep the target `127.0.0.1:4173`. Start the static server.

### Exact actions or commands

1. In context A, fill the field labeled **Product name** with `widget`, click the
   button labeled **Search**, verify `Found 1 matching product(s).`, and save
   storage state.
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

## Check your understanding

1. Contexts A and B are created from the same Browser, but only context A performs a `widget` search. Which Playwright boundary keeps B's cookies and local storage separate?
2. A second Page opens inside context A and reads `widget` from local storage. Why does the second Page see A's stored value?
3. Context C is created from A's serialized storage state. What is the declared changed condition when C is compared with a fresh context?
4. Why must a storage-state file from a real account be treated as sensitive even though the course uses only synthetic local state?
5. Context C restores the `widget` local-storage value. Why does that restored browser value not prove a server-side authorization bypass?

## Answer key

<details>
<summary>Show answers</summary>

- **1. BrowserContext is the isolation boundary.** Contexts A and B have separate cookies and origin storage even though the same Browser process owns both contexts.

- **2. Pages inside one BrowserContext share that context's origin-scoped storage.** Opening another Page changes the document instance, not the containing cookie and storage boundary.

- **3. Context C starts with A's serialized cookies and origin storage instead of empty state.** The target, browser version, and workflow should remain fixed so restored state is the meaningful difference.

- **4. Real storage state may contain cookies or tokens that allow account impersonation.** Such files should not enter course outputs, logs, or version control even when the serialization format looks harmless.

- **5. `localStorage` is browser-controlled state and can be restored without any server approval.** A bypass claim still requires repeating a protected server action and verifying authoritative server-side state.

</details>

## Next lesson

[Network events](04-network-events.md) captures the HTTP evidence produced by
each deliberately controlled context.
