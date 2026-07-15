# HTTP request and response

<!-- source-ids: mdn-http-overview, aate-local-lab, aate-adversarial-control-loop -->

> **Progress**  
> Module: 01 - HTTP and the edge  
> Lesson: 1 of 4  
> Depth: Foundation  
> Estimated time: 90 minutes  
> Prerequisites: Module 00  
> Artifact: `artifacts/module-01/request-anatomy.md`  
> Next: Sessions and workflows

## Role outcome

Trace a browser action into a concrete HTTP request and response, naming what
each component can and cannot prove about the caller.

## Prerequisites

- [Module 00](../00-method/index.md), especially protected-action proof
- A browser and the Python runtime already present on the course workstation

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MDN: An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | Components; basic aspects; stateless but not sessionless; connections; flow; messages | Defines the protocol model and separates messages from connections and state |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Synthetic target and local-only policy | Identifies the deliberately small target used below |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Evidence and protected-action steps | Separates protocol observations from offensive proof |

## Mental model

```text
browser action
  -> URL resolution
  -> request line + headers + optional body
  -> connection carrying HTTP
  -> server/intermediary processing
  -> status + response headers + optional body
  -> browser updates state and renders or executes the result
```

An HTTP message is evidence of a request, not proof of a human, a unique device,
or a complete business workflow.

## Required external instruction

### MDN assignment

**Direct link:** [An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)  
**Exact assignment:** Components of HTTP-based systems; Basic aspects of HTTP; HTTP is stateless, but not sessionless; HTTP and connections; HTTP flow; HTTP Messages  
**Estimated time:** 35 minutes  
**Focus on:** client, proxy, server, method, target, headers, body, status, connection, and how cookies add continuity above a stateless exchange  
**Skip:** stop before APIs based on HTTP  
**Expected takeaway:** narrate a complete HTTP exchange and explain why a connection, request, session, and user are different units.

## Course bridge

The request target says *what resource or action is requested*. The method says
the requested operation's protocol semantics. Headers carry metadata such as
representation preferences, origin context, cookies, and client claims. A body
can carry application input. The response status summarizes the server's HTTP
outcome; response headers describe handling and state changes; the body carries
the representation or error detail.[^mdn-messages]

HTTP is stateless at the message layer: request two does not inherit meaning
from request one merely because it came later. Applications build continuity
with cookies, bearer tokens, server-side records, URLs, or other state.[^mdn-state]

[^mdn-messages]: MDN, "An overview of HTTP," sections "HTTP flow" and "HTTP Messages."
[^mdn-state]: MDN, "HTTP is stateless, but not sessionless."

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** For offensive work, record separately the bytes or
    fields sent, the connection that carried them, the state they referenced,
    the control decision, and the protected-action result. Conflating them hides
    which assumption actually failed.

## Worked example

```http
GET /inventory.json HTTP/1.1
Host: 127.0.0.1:4173
Accept: */*
Referer: http://127.0.0.1:4173/

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 196

[{"name":"Synthetic Widget","stock":5}]
```

`GET` and `/inventory.json` identify the operation and target. `Host` selects
the authority. `Accept` is a preference, not a guarantee. `Referer` is context
supplied by the client and can be absent or altered. `200` means this exchange
succeeded at HTTP level; only the JSON and application behavior tell us whether
a business action occurred. Here the request reads inventory and changes none.

## Guided exercise

### Objective

Start the zero-Docker site, cause one request, and annotate both messages.

### Setup

The server exposes only files under `lab/foundation-web` on loopback. The command
creates no account and contacts no external target.

```powershell
python -m http.server 4173 --bind 127.0.0.1 --directory lab/foundation-web
```

The module starts a basic static-file server. Port `4173` is local; `--bind`
prevents listening on other interfaces; `--directory` limits the document root.

### Actions

1. Keep the terminal open and visit `http://127.0.0.1:4173`.
2. Search for `widget` and observe the result.
3. In a second terminal request `http://127.0.0.1:4173/inventory.json` with the
   browser or `curl.exe`.
4. Record the method, target, request headers you can observe, status, response
   headers, media type, and body purpose.
5. Mark every client-controlled claim and every server-generated fact.

### Expected output

The page shows `Found 1 item` and `Synthetic Widget - 5 available`. The direct
inventory request returns a JSON array and an HTTP `200` response.

### Interpretation

The two requests share a host and may share a connection, yet each is a separate
HTTP exchange. The JSON response proves the static server returned a file. It
does not prove identity, intent, authorization, or inventory mutation.

### Common failure modes

- Opening the HTML file directly creates a `file:` origin; use the loopback URL.
- A busy port means another process owns `4173`; stop it before retrying.
- Treating every header as server-verified; many are caller claims.
- Calling the search a protected action even though it only reads static data.

### Cleanup

Press Ctrl+C in the server terminal. Confirm that refreshing the page now fails.

## Why this matters offensively

Bot, WAF, rate, and workflow controls consume features derived from messages,
connections, and state. An operator must know which layer produced a feature
before changing it and must repeat the actual protected action afterward.

## Required artifact

Create `artifacts/module-01/request-anatomy.md` with the raw exchange, an
annotation for every line, and a three-column table: client-controlled claim,
server observation, conclusion that is *not* justified.

## Pass gate

1. What is the difference between a request target and a `Host` header?
2. Why does HTTP statelessness not prevent login sessions?
3. What does a `200` response prove in the worked example?
4. Which part of the exchange expresses representation preference?
5. Why is a request header not automatically an identity fact?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. The target selects the path or resource within the authority; `Host` selects the authority serving it.
2. Applications layer state over exchanges with cookies, tokens, URLs, and server-side records.
3. It proves the server completed that HTTP exchange successfully and returned a representation, not that a protected business action occurred.
4. `Accept` expresses what response media types the client prefers.
5. The client constructs most request headers, so the server must corroborate a claim with other state or observations.

</details>

## Next lesson

[Sessions and workflows](02-sessions-and-workflows.md) connects otherwise
independent messages into the stateful action an adversary is trying to reproduce.
