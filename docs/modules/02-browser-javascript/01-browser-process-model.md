# Browser process model

<!-- source-ids: chrome-browser-process-model, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 02 - Browser and JavaScript foundations
- Lesson: 1 of 4
- Depth: Foundation
- Estimated time: 80 minutes
- Prerequisites:
  - [Module 01](../01-http-edge/index.md)
  - Be able to explain the request path and read a manual Network trace
- Next lesson: DOM and Web APIs

## Role outcome

Locate browser UI, network coordination, rendering, frames, and workers in a
process/thread model without treating "the browser" as one execution context.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Chrome: Inside look at a modern web browser, Part 1](https://developer.chrome.com/blog/inside-browser-part1/) | Process and Thread; Browser architecture; Which process controls what? | Establishes the multiprocess architecture and responsibilities | Historical Chrome architecture article; implementation details evolve. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Foundation page, iframe, and worker | Supplies visible execution contexts for inspection | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Candidate signals and residual evidence | Connects context boundaries to controlled observation | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Concept | Boundary | Typical responsibility | Offensive consequence |
|---|---|---|---|
| Process | OS-isolated program instance | browser coordination, renderer, GPU, utility work | a change in one process/context may not reach another |
| Thread | execution sequence inside a process | main-thread tasks or supporting work | blocking changes timing and responsiveness |
| Browser process | browser-wide coordinator | UI, navigation coordination, storage/network mediation | owns lifecycle beyond one page script |
| Renderer process | site content execution/rendering | parse, DOM, style, layout, page JavaScript | top page and frames may be isolated by site/process policy |
| Worker | background JS context | computation/network without a document DOM | page-world patches do not automatically alter worker globals |

## Required external instruction

### Chrome architecture assignment

**Direct link:** [Inside look at a modern web browser, Part 1](https://developer.chrome.com/blog/inside-browser-part1/)  
**Exact section, chapter, or unit:** Execute program on Process and Thread; Browser architecture; Which process controls what?  
**Estimated time:** 30 minutes  
**What to focus on:** process isolation, browser/renderer responsibilities, multiple renderer processes, and why architecture varies by browser/environment  
**What to skip:** deep process-optimization discussion after the assigned sections  
**Expected takeaway:** draw the major browser processes and state which objects and observations belong to content execution versus browser-wide coordination.

## Course bridge

A process has its own memory boundary; threads share their process memory while
executing different task sequences. Chrome uses multiple processes and assigns
browser-wide responsibilities separately from renderer work.[^chrome-process]
The exact number of processes is not fixed: site isolation, platform, browser
version, and resource policy influence placement.

[^chrome-process]: Chrome Developers, "Inside look at modern web browser (part 1)," Browser architecture and Which process controls what?

!!! info "Source-backed fact"
    Page JavaScript does not execute in the browser UI process. Content executes
    in renderer-related contexts, while the browser coordinates navigation and
    other browser-wide facilities.[^chrome-process]

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Treat every realm or execution context as a possible
    independent observation point. A property altered in the top page may retain
    its original value in an iframe or worker, producing a coherence failure.

## Worked example

The Foundation site creates three content contexts:

```text
top document: index.html + app.js -> DOM, localStorage, fetch
child frame:  frame.html          -> its own Window and navigator access
worker:       worker.js           -> WorkerGlobalScope; no document DOM
```

They share an origin in this lab, but they are not the same JavaScript global
object. Same origin permits important interactions; it does not collapse them
into one realm or guarantee identical instrumentation.

## Guided exercise

### Objective

Observe process/context boundaries and map them to the resources from Module 01.

### Setup

Start the Foundation static server and visit `http://127.0.0.1:4173/`. Open
Chrome's built-in Task Manager from **More tools > Task manager**, then select
the **Sources** panel in DevTools. Exact process rows vary by version.

### Exact actions or commands

1. With `http://127.0.0.1:4173/` loaded, note the browser, tab/renderer, GPU, and
   utility rows shown in Task Manager.
2. In DevTools Sources, locate the top page, `frame.html`, and `worker.js`.
3. Select each available JavaScript context in the Console context picker.
4. Evaluate `globalThis.constructor.name` in the page/frame and
   `self.constructor.name` in the worker if its console is available.
5. Add each resource and global object to your Module 01 path map.

### Expected output

The page and frame expose a `Window` global; the worker exposes a worker global
scope rather than `Window` and has no `document`. Task Manager shows multiple
browser-related processes, though labels and counts can differ.

### Interpretation

Context is the stable lesson; process count is a version-sensitive observation.
Record both browser version and what you actually saw instead of asserting that
every frame always owns a separate OS process.

### Common failure modes

- Using process, thread, realm, frame, and tab as synonyms
- Expecting a worker to expose `document`
- Treating one Task Manager snapshot as a universal Chrome architecture
- Assuming same origin means same global object

### Cleanup

Close DevTools and Task Manager, then stop the static server.

## Why this matters offensively

Control code can collect signals in multiple execution contexts. An evasion that
changes only the easiest page-visible property can leave contradictory evidence
in frames, workers, protocols, or browser-managed behavior. Architecture is the
reason cross-context validation matters.

## Check your understanding

1. The browser's task manager shows a renderer process with several execution threads. How does the renderer process's memory boundary differ from the threads inside that process?
2. The Foundation page runs page JavaScript and renders HTML. Which broad browser process normally performs that work, subject to site-isolation policy?
3. Why should a process map record the browser version and observed process allocation instead of assuming one fixed process count?
4. A top-page modification changes `navigator.language`, but the worker still reports the original value. What does that cross-context difference reveal about the modification?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A process has its own memory and resource boundary, while threads are execution sequences that share resources inside that process.** The distinction explains why some browser components are isolated more strongly than others.

- **2. A renderer process normally handles page rendering and page JavaScript.** The exact allocation can vary because browser architecture, origins, platform, resource policy, and site isolation influence renderer placement.

- **3. Browser version, platform, site isolation, origins, and resource policy can all change process allocation.** Recording the observed environment keeps the map evidence-based and makes a later comparison reproducible.

- **4. The modification reached the top-page context but not the worker context.** The unchanged worker value is a residual inconsistency that another collection point could observe, although it does not prove a control uses that signal.

</details>

## Next lesson

[DOM and Web APIs](02-dom-and-web-apis.md) explains the object model and browser
facilities exposed inside these content contexts.
