# HTTP request and response

<!-- source-ids: mdn-http-overview, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 01 - HTTP and the edge
- Lesson: 1 of 4
- Depth: Foundation
- Estimated time: 90 minutes
- Prerequisites:
  - [Module 00](../00-method/index.md), especially protected-action proof
  - A browser and the Python runtime already present on the course workstation
- Required artifact: `artifacts/module-01/request-anatomy.md`
- Next lesson: Sessions and workflows

## Role outcome

Trace a browser action into a concrete HTTP request and response, naming what
each component can and cannot prove about the caller.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MDN: An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | Components; basic aspects; stateless but not sessionless; connections; flow; messages | Defines the protocol model and separates messages from connections and state | Stop before APIs based on HTTP; it is a browser-platform overview, not an attack guide. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | Synthetic target and local-only policy | Identifies the deliberately small target used below | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Evidence and protected-action steps | Separates protocol observations from offensive proof | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

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
**Exact section, chapter, or unit:** Components of HTTP-based systems; Basic aspects of HTTP; HTTP is stateless, but not sessionless; HTTP and connections; HTTP flow; HTTP Messages  
**Estimated time:** 35 minutes  
**What to focus on:** client, proxy, server, method, target, headers, body, status, connection, and how cookies add continuity above a stateless exchange  
**What to skip:** stop before APIs based on HTTP  
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

Open a terminal in the root of the cloned repository. The server command below
uses a repository-relative path, so confirm the working directory before
starting it.

#### PowerShell preflight

```powershell
Test-Path .\lab\foundation-web\index.html
```

Expected output:

```text
True
```

`True` means the terminal is in the correct repository directory. `False` means
you must change into the cloned repository directory before continuing. Do not
start the server until this command returns `True`.

#### Bash or zsh preflight

```bash
test -f ./lab/foundation-web/index.html && echo "Found" || echo "Not found"
```

Expected output:

```text
Found
```

`Found` means the terminal is in the correct repository directory. `Not found`
means you must change into the cloned repository directory before continuing.
Do not start the server until this command prints `Found`.

The server exposes only files under `lab/foundation-web` on loopback. It creates
no account and contacts no external target.

#### PowerShell server command

```powershell
python -m http.server 4173 `
  --bind 127.0.0.1 `
  --directory ".\lab\foundation-web"
```

#### Bash or zsh server command

```bash
python3 -m http.server 4173 \
  --bind 127.0.0.1 \
  --directory "./lab/foundation-web"
```

- `4173` is the local listening port.
- `--bind 127.0.0.1` restricts the server to the loopback interface.
- `--directory` selects the bundled Foundation web application as the document
  root.

Expected terminal output should resemble:

```text
Serving HTTP on 127.0.0.1 port 4173 ...
```

Leave this terminal open while completing the exercise.

### Exact actions or commands

#### Use the search form

1. Visit `http://127.0.0.1:4173/`.
2. Confirm that the page displays the heading `Local inventory search`.
3. Find the input field labeled **Product name** and type:

   ```text
   widget
   ```

4. Click the button labeled **Search**.
5. Observe the search result displayed below the form:

   ```text
   Found 1 matching product(s).
   Synthetic Widget — 5 available
   ```

!!! warning "Search term, not URL path"
    Do not navigate to `http://127.0.0.1:4173/widget`.
    `widget` is a search term entered into the **Product name** field. It is not
    a URL path or file name. A request to `/widget` returns `404` because this
    static lab contains no `/widget` route or file.

#### What happens technically

1. The browser initially requests `/` and loads the HTML application.
2. The page loads its JavaScript and supporting files.
3. When you click **Search**, the page's JavaScript requests:

   ```text
   /inventory.json
   ```

4. The browser receives the JSON inventory data.
5. The JavaScript filters the inventory for entries matching `widget`.
6. The JavaScript updates the DOM with the matching result.
7. The browser does not request `/widget`.

Based on the bundled application, the local-server log should include these
requests. The exact order of the supporting-resource requests may vary:

```text
GET / HTTP/1.1
GET /styles.css HTTP/1.1
GET /app.js HTTP/1.1
GET /frame.html HTTP/1.1
GET /worker.js HTTP/1.1
GET /inventory.json HTTP/1.1
```

#### Inspect the inventory response directly

Open a second terminal in the repository root while the server remains running.

PowerShell:

```powershell
curl.exe -i http://127.0.0.1:4173/inventory.json
```

Bash or zsh:

```bash
curl -i http://127.0.0.1:4173/inventory.json
```

This request retrieves the raw inventory JSON directly without using the search
form. Record:

- HTTP method
- Request target
- Observable request headers
- Response status
- Response headers
- Media type
- Purpose of the response body

Then mark every client-controlled claim and every server-generated fact.

### Expected output

The form shows `Found 1 matching product(s).` and
`Synthetic Widget — 5 available`. The direct inventory request returns a valid
JSON array with an HTTP `200` response and a JSON media type.

### Interpretation

The two requests share a host and may share a connection, yet each is a separate
HTTP exchange. The JSON response proves the static server returned a file. It
does not prove identity, intent, authorization, or inventory mutation.

### Common failure modes

- Starting the server before the repository-root preflight passes can select the
  wrong document root and make `/` or `/inventory.json` return `404`.
- Putting `widget` in the address bar requests the nonexistent `/widget` path;
  enter it in the **Product name** field instead.

!!! tip "Troubleshooting the Foundation server and search"
    - **Homepage returns 404.** The server was likely started from the wrong
      working directory, so the relative `lab/foundation-web` path resolved
      somewhere outside the repository. Check with PowerShell:
      `Test-Path .\lab\foundation-web\index.html`. For Bash or zsh, use
      `test -f ./lab/foundation-web/index.html && echo "Found" || echo "Not found"`.
      Do not continue until the first command returns `True` or the second
      prints `Found`.
    - **`/widget` returns 404.** This is expected. `widget` is a search term
      entered into the **Product name** field; it is not a route. Return to
      `http://127.0.0.1:4173/`, type `widget` into **Product name**, and click
      **Search**.
    - **`/inventory.json` returns 404.** Verify the fixture with PowerShell:
      `Test-Path .\lab\foundation-web\inventory.json`. For Bash or zsh, use
      `test -f ./lab/foundation-web/inventory.json && echo "Found" || echo "Not found"`.
      Also confirm that the server was started with the correct `--directory`.
    - **Port 4173 is already in use.** If the previous server terminal is open,
      return to it and press `Ctrl+C`. To identify the owner in PowerShell, use
      `Get-NetTCPConnection -LocalPort 4173 -State Listen | Select-Object -ExpandProperty OwningProcess`.
      In Bash or zsh, use `lsof -nP -iTCP:4173 -sTCP:LISTEN`. Stop the previous
      local server before retrying. Do not switch ports; later commands expect
      `4173`.
    - **Browser still displays an old error page.** Confirm that the current
      server terminal shows successful requests, reload the page, use a hard
      refresh if necessary, and verify that the URL is exactly
      `http://127.0.0.1:4173/`.
    - Opening the HTML file directly creates a `file:` origin; always use the
      loopback URL. Also remember that many request headers are caller claims
      and that this read-only search is not a protected action.

### Cleanup

Return to the terminal running the static server and press `Ctrl+C`. This stops
the local HTTP server. Confirm that refreshing the page now fails.

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
