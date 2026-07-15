# Map the edge request path

<!-- source-ids: owasp-wstg-map-architecture-v42, mdn-http-overview, aate-adversarial-control-loop -->

> **Progress**  
> Module: 01 - HTTP and the edge  
> Lesson: 4 of 4  
> Depth: Applied  
> Estimated time: 100 minutes  
> Prerequisites: DevTools Network  
> Artifact: `artifacts/module-01/request-path.svg`  
> Next: Browser process model

## Role outcome

Draw the complete request path and identify where routing, caching, identity,
challenge, rate, application, and dependency decisions can occur.

## Prerequisites

- [Observe requests with DevTools](03-devtools-network.md)
- Your manual trace and workflow map

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| PROJECT_DOCUMENTATION | [OWASP WSTG: Map Application Architecture](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture) | Summary; objectives; How to Test | Establishes architecture and intermediary mapping |
| OFFICIAL_DOCUMENTATION | [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | Components of HTTP-based systems | Describes proxies and client/server components |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Step 3 | Specializes mapping around control and resource paths |

## Mental model

```text
browser
  -> resolver/network
  -> CDN or reverse proxy
       -> WAF / bot / challenge / rate decision
       -> cache lookup
  -> application route
       -> session/state store
       -> queue or worker
       -> database/dependency
  -> response and telemetry at every boundary
```

The visible URL is the start of a path, not the architecture.

## Required external instruction

### OWASP architecture assignment

**Direct link:** [Map Application Architecture](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture)  
**Exact assignment:** Summary; Test Objectives; How to Test  
**Estimated time:** 30 minutes  
**Focus on:** components, hosting relationships, intermediary behavior, trust boundaries, and evidence sources  
**Skip:** unrelated information-gathering tests and broad infrastructure scanning  
**Expected takeaway:** turn a URL and trace into a hypothesis-bearing component map without inventing hidden infrastructure.

## Course bridge

An intermediary can terminate connections, normalize headers, cache a response,
or make a control decision before application code runs. The application can
then apply authorization and business rules; dependencies determine cost and
state. OWASP treats architecture mapping as identification of components and
their relationships, not merely hostname collection.[^owasp-architecture]

[^owasp-architecture]: OWASP WSTG v4.2, "Map Application Architecture," Summary and How to Test.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Annotate every component with observable input,
    decision, output, telemetry, resource consumed, and evidence owner. That
    makes a later bypass or pressure hypothesis falsifiable.

## Worked example

| Component | Input | Decision/work | Evidence | Possible false inference |
|---|---|---|---|---|
| Browser cache | URL plus cache metadata | reuse or fetch | DevTools size/headers | no network row means no user action |
| Reverse proxy | connection and request | route/static cache/control | access log | header claim equals identity |
| Application | normalized request and state | workflow rule | app event/state record | `200` equals intended authorization |
| Database | query/update | durable state | row/audit record | latency proves database saturation |

In the Foundation target, Python's static server collapses proxy, application,
and file dependency into one process. The honest map shows this simplicity; it
does not draw a fictitious WAF. Later modules add the local edge and API.

## Guided exercise

### Objective

Build a current-state map and a later-test overlay without mixing observation
with hypothesis.

### Setup

Use your manual trace. You do not need to start Docker. Choose a diagram format
that exports to SVG.

### Actions

1. Draw the browser, loopback network, Python static server, files, iframe, and
   worker.
2. Label observed arrows with methods, paths, and evidence source.
3. Mark the process boundary and browser execution contexts.
4. On a separate dashed overlay, add generic edge control, application, state,
   and dependency components for later modules.
5. Label every dashed component `hypothesis/not present in Foundation target`.
6. Add observation points and the protected action each could help prove.

### Expected output

The solid map contains only verified Foundation components. The dashed overlay
shows where a cache, challenge, WAF, rate limiter, session store, and expensive
dependency could appear, each explicitly unverified.

### Interpretation

Separating observed architecture from a test hypothesis prevents recon notes
from becoming unsupported facts. The overlay becomes a question set for the
later Docker lab rather than a claim about it.

### Common failure modes

- Treating DNS, TLS, CDN, WAF, bot control, and application as one box
- Drawing a commercial control that was never observed
- Omitting browser cache or execution contexts
- Recording a header without recording which component generated it

### Cleanup

No service is required. Remove real hostnames or proprietary architecture from
the artifact before committing a public-safe version.

## Why this matters offensively

A bypass changes the inputs or state observed at a particular enforcement
point. A pressure test consumes a resource behind a path. A precise map tells
the operator where to collect baselines, where a control can be evaded, and what
server-side evidence can disprove an attractive but wrong hypothesis.

## Required artifact

Export `artifacts/module-01/request-path.svg` and keep its editable source. Every
node must state observed/hypothetical, input, decision/work, telemetry, resource,
and evidence owner.

## Pass gate

1. Why can the browser-visible URL underdescribe the request path?
2. What is the difference between a solid and dashed node in this exercise?
3. Where can connection-derived evidence be replaced or terminated?
4. Why should a dependency appear on an offensive path map?
5. What evidence separates an edge block from an application rejection?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. Intermediaries, routing, caches, controls, application services, and dependencies can sit behind one authority.
2. Solid means directly observed in the Foundation target; dashed is a later test hypothesis.
3. At a connection-terminating proxy or edge before a new downstream connection is created.
4. Its work and limits may determine the actual resource-exhaustion or protected-action impact.
5. Correlated edge and application telemetry showing whether the request reached the application.

</details>

## Next lesson

[Browser process model](../02-browser-javascript/01-browser-process-model.md)
explains where the document, scripts, frames, and workers in this map execute.
