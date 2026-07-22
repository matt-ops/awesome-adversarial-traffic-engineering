# Sessions and workflows

<!-- source-ids: mdn-http-overview, owasp-wstg-entry-points-v42, aate-adversarial-control-loop -->

## Progress

- Module: 01 - HTTP and the edge
- Lesson: 2 of 4
- Depth: Foundation
- Estimated time: 90 minutes
- Prerequisites:
  - [HTTP request and response](01-http-request-response.md)
  - Be able to identify an HTTP method, target, headers, status, and body
- Next lesson: DevTools Network

## Role outcome

Separate request, connection, session, workflow, and adversary objective while
mapping the state required for a protected action.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | Stateless but not sessionless; connections | Grounds message, connection, and session distinctions | Stop before APIs based on HTTP; it is a browser-platform overview, not an attack guide. |
| PROJECT_DOCUMENTATION | [OWASP WSTG: Identify Application Entry Points](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/06-Identify_Application_Entry_Points) | Summary; objectives; How to Test; Requests; Responses | Provides a repeatable way to enumerate inputs and multi-step state | Version 4.2 is intentionally pinned; examples are general web testing guidance. |
| COURSE_SYNTHESIS | [AATE adversarial-control loop](../../methodology/adversarial-control-loop.md) | Steps 2-6 | Connects workflow mapping to legitimate and blocked baselines | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Unit | Example | Lifetime | Offensive question |
|---|---|---|---|
| Request | `POST /cart/add` | One exchange | Which inputs and claims reach the action? |
| Connection | TCP/TLS channel | Multiple exchanges possible | Which transport observations are reused? |
| Session | Cookie plus server record | Across requests/connections | What state binds actions to a caller? |
| Workflow | browse -> cart -> challenge -> reserve | Ordered state transitions | Which prerequisite can be skipped, replayed, or raced? |
| Objective | reserve unavailable inventory | Entire emulation | Did the hostile outcome occur? |

## Required external instruction

### OWASP entry-point assignment

**Direct link:** [Identify Application Entry Points](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/06-Identify_Application_Entry_Points)  
**Exact section, chapter, or unit:** Summary; Test Objectives; How to Test; Requests; Responses  
**Estimated time:** 35 minutes  
**What to focus on:** parameters, methods, headers, cookies, response clues, and ordering of multi-step actions  
**What to skip:** unrelated WSTG tests linked from the page  
**Expected takeaway:** build an entry-point inventory that preserves where input originates and which state precedes an action.

## Course bridge

A session is an application convention, not an HTTP primitive. A cookie may
carry an opaque session identifier while the authoritative record lives on the
server. A bearer token may carry signed claims. Local storage may hold state the
browser later copies into a request. None is equivalent to the TCP connection.

OWASP recommends observing requests and responses to enumerate parameters,
methods, headers, cookies, and state transitions.[^wstg-entry] That inventory is
the raw material for a workflow graph: nodes are meaningful states; directed
edges are actions that transition between them.

[^wstg-entry]: OWASP WSTG v4.2, "Identify Application Entry Points," How to Test, Requests, and Responses.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** A workflow bypass hypothesis names a missing or weak
    binding. Examples include a token not bound to its issuing session, a limit
    keyed to a caller-controlled value, or an action that checks inventory but
    not reservation authorization. The protected action, not a status label,
    decides success.

## Worked example

```text
anonymous --GET /item/7--> item viewed
item viewed --POST /challenge/start--> challenge issued to session A
challenged --POST /challenge/solve--> session A approved
approved --POST /reserve item=7--> reservation created
```

A replay experiment does not begin by changing random headers. It asks whether
the approval edge is bound to session A. Establish that session B receives a
block. Then present A's approval proof from B and repeat exactly `POST /reserve`.
Only a reservation record for B proves the objective.

## Guided exercise

### Objective

Model the static search as a workflow and identify why it is not yet an
authorization test.

### Setup

Start the loopback static server as explained in the prior lesson and open
`http://127.0.0.1:4173/`. The browser stores the last query in `localStorage`.

### Exact actions or commands

1. In the **Product name** field, enter `widget`, click **Search**, and confirm
   that `Found 1 matching product(s).` and `Synthetic Widget — 5 available`
   appear below the form.
2. Reload and inspect the **Product name** field.
3. Use the browser menu item **New private window** or **New Incognito window**,
   open `http://127.0.0.1:4173/`, and confirm that **Product name** is empty.
4. Draw states for page loaded, query entered, inventory fetched, result shown,
   and query stored.
5. For every transition record the request, browser-only state, and server state.
6. Add a hypothetical protected `reserve` transition and list the authorization
   fact a server would need to verify.

### Expected output

The normal profile remembers `widget`; the separate private context begins with
empty storage. Both can fetch the same public JSON. The server has no per-user
session and creates no reservation.

### Interpretation

Local storage separates browser contexts but is not server authorization. A
client can change it. The exercise makes browser state visible before Module 03
automates it and before Module 04 introduces an actual workflow flaw.

### Common failure modes

- Calling local storage a server session
- Treating an empty private profile as a different network identity
- Omitting failure transitions such as inventory fetch error
- Inferring a reservation from a displayed search result

### Cleanup

Close the private window, clear the site's local storage, and stop the server.

## Why this matters offensively

Real abuse is usually a chain. Mapping the chain reveals controls attached to
the wrong transition, proofs that can be replayed, and limits scoped to a weak
identity. It also identifies the exact state evidence needed for a finding.

## Check your understanding

1. The normal browser window remembers `widget` after a reload, while a new private window starts with an empty Product name field. What browser state caused the difference, and does the difference prove either window is logged in?
2. The static page fetches `inventory.json` and displays `Synthetic Widget`. Did the server create a reservation, and what did the server actually provide?
3. A hypothetical `POST /reserve` request contains `identity: "alice"` in its JSON body, but there is no authenticated session. Why is that client-supplied identity not enough to authorize the reservation?
4. Session B is normally blocked from reserving an item. You reuse Session A's approval token in Session B and repeat the same reserve request. What server-side result would prove that the replay succeeded?
5. If `GET /inventory.json` fails, why should the workflow map include that failure path?

## Answer key

<details>
<summary>Show answers</summary>

- **1. `localStorage` caused the difference, and the stored value does not prove a login.** Each browser context has separate local storage that browser JavaScript can change, while a login requires a server-validated session record.

- **2. No reservation was created.** The server returned a public JSON file, and JavaScript in the browser filtered those inventory records and displayed the matching product without changing server-side inventory.

- **3. The JSON value is only a claim made by the client.** The server must identify the caller from a validated authenticated session and then check whether that caller may reserve the requested product and quantity.

- **4. A server-side reservation attributed to Session B would prove the replay succeeded.** A changed status message, browser storage value, or detector score is insufficient unless the protected reservation action actually occurs.

- **5. The failure path shows where the search workflow can stop and records the error response the learner should expect.** Including failures prevents the workflow map from describing only the successful path.

</details>

## Next lesson

[DevTools Network](03-devtools-network.md) turns the workflow diagram into a
trace of initiators, messages, timing, and browser-visible state.
