# Workflow and API mapping

<!-- source-ids: portswigger-api-testing-path, owasp-wstg-entry-points-v42, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 04 - Automated abuse and workflow attacks
- Lesson: 2 of 5
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [Automated-abuse objectives](01-abuse-objectives.md)
  - Be able to map HTTP requests, workflows, and the request path from Module 01
  - Docker Desktop or compatible Docker Engine for the integrated local lab
- Next lesson: Authentication and rate controls

## Role outcome

Inventory API endpoints, methods, inputs, state, and error boundaries, then turn
observations into bounded attack hypotheses tied to one protected action.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [PortSwigger API testing path](https://portswigger.net/web-security/learning-paths/api-testing) | API recon through supported content types | Provides an ordered provider-safe API discovery method | Use only provider-assigned targets; this is not permission to scan PortSwigger infrastructure. |
| PROJECT_DOCUMENTATION | [OWASP entry points](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/06-Identify_Application_Entry_Points) | Requests and Responses | Preserves parameters, state, and errors | Version 4.2 is intentionally pinned; examples are general web testing guidance. |
| LAB_SPECIFIC | [Integrated local app guide](../../labs/applied/local-api.md) | Docker topology and recon runner | Defines the fixed synthetic target | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Steps 2-8 | Converts mapping observations into testable hypotheses | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Map layer | Record | Example hypothesis clue |
|---|---|---|
| Documentation | path, method, schema, security declaration | reserve has no documented security requirement |
| Normal workflow | order, state, successful response | login returns token but reserve may not consume it |
| Error boundary | invalid object/state/method/content type | differences reveal validation location |
| Control boundary | challenge/rate response and key | caller supplies the value used for limiting |
| Authoritative state | product, reservation, promotion, account | action can be proved independently of UI |

## Required external instruction

### PortSwigger API assignment

**Direct link:** [API testing learning path](https://portswigger.net/web-security/learning-paths/api-testing)  
**Exact section, chapter, or unit:** API recon; API documentation; Discovering API documentation; Using machine-readable documentation; Identifying API endpoints; Interacting with endpoints; Identifying supported methods; Identifying supported content types  
**Estimated time:** 80 minutes  
**What to focus on:** provider-assigned targets, documentation as a hypothesis source, method/content-type boundaries, and recording evidence  
**What to skip:** complete no additional labs or API topics unless the path explicitly embeds them in these sections  
**Expected takeaway:** inventory an API without broad scanning and explain how documentation and observed behavior differ.

## Course bridge

Machine-readable documentation describes an intended interface: paths, methods,
parameters, body schemas, responses, and sometimes security requirements. It is
not proof that enforcement matches the declaration. PortSwigger teaches using
documentation and bounded interaction to identify endpoints and supported
methods/content types.[^ps-api]

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE turns each mapping observation into a candidate
    binding or control hypothesis, then withholds a finding until the same
    protected action and authoritative state test that hypothesis.

[^ps-api]: PortSwigger Web Security Academy, "API testing" learning path, assigned API recon sections.

!!! warning "Safety boundary"
    The local runner is fixed to `localhost:8080`. PortSwigger exercises use only
    the unique lab host issued by the Academy. Documentation discovery never
    grants permission to test adjacent infrastructure.

## Worked example

```json
{
  "path": "/api/cart/reserve",
  "method": "POST",
  "inputs": ["identity", "product_id", "quantity"],
  "security_required": false,
  "hypothesis": "the API accepts a caller identity without authenticated binding",
  "proof": "inventory decreases for an identity that never logged in"
}
```

The OpenAPI observation supports the hypothesis but does not prove it. Execution
must establish initial inventory, omit authentication, perform the reservation,
and query final inventory.

## Guided exercise

### Objective

Start the prerequisite-gated local API, inventory it, and produce four attack
hypotheses without exceeding the fixed probes.

### Setup

From the repository root, Docker Compose builds one FastAPI application behind
a loopback-only Nginx edge. The commands use the repository-relative
`lab/docker-compose.yml` path. `-f` selects that course file; `up --build -d`
builds images and starts them in the background. The health request verifies the
route before any exercise.

#### PowerShell

```powershell
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
```

#### Bash or zsh

```bash
docker compose -f lab/docker-compose.yml up --build -d
curl http://localhost:8080/health
```

Expected health JSON is `{"status":"ok","service":"aate-local-app"}`.

### Exact actions or commands

1. Read the `/openapi.json` route list in a browser before using the runner.
2. Execute `python -m lab.run recon` once.
3. For each route record method, input location, security declaration, response
   classes, workflow state, and likely evidence owner.
4. Preserve the five bounded probes and four printed hypotheses.
5. Mark every hypothesis as unproven and specify its next exact protected action.

### Expected output

The runner prints one surface inventory, then `200` health/search, `404` invalid
product, `403` unchallenged report, `200` first limited report, and four hypotheses
for workflow authorization, challenge replay, rate key, and resource cost.

### Interpretation

Recon is setup for a specific attack, not a repeated question in every module.
It ends with a map and hypotheses; later lessons execute the named tests.

### Common failure modes

- Treating OpenAPI `security` as observed enforcement
- Expanding to broad port/host scanning unrelated to the workflow
- Starting attacks before recording normal/error baselines
- Omitting server state from a hypothesis
- Using `0.0.0.0` or a non-loopback target

### Cleanup

Keep the app for the next lessons or stop it with
`docker compose -f lab/docker-compose.yml down`.

## Why this matters offensively

Real adversaries learn the reachable state machine before optimizing a bypass.
Precise reconnaissance exposes missing bindings and weak keys while keeping the
engagement reproducible, bounded, and tied to an outcome.

## Check your understanding

1. The OpenAPI entry for `POST /api/cart/reserve` declares no security requirement. Why is that documentation observation a hypothesis clue rather than proof of missing enforcement?
2. The bounded recon sends an invalid product and receives `404`. What workflow boundary does that response add to the API map?
3. The recon output lists four possible weaknesses but has not executed their protected actions. Why must those entries remain hypotheses instead of findings?
4. The reserve schema accepts `identity`, `product_id`, and `quantity` from the JSON body. Which observation suggests testing whether caller-supplied identity is bound to an authenticated session?
5. Which target and probe limits keep the guided reconnaissance within its documented local scope?

## Answer key

<details>
<summary>Show answers</summary>

- **1. OpenAPI describes the interface and intended security metadata, but runtime code and application state decide enforcement.** The operator must attempt the protected reservation and verify the inventory record returned by the server before concluding that authorization is missing.

- **2. The `404` records where the application rejects an unknown product and how that error appears.** The map now includes an object-validation failure path instead of only successful requests.

- **3. A finding needs executed evidence that connects the suspected weakness to a protected server-side result.** Reconnaissance only identifies promising observations, so each hypothesis must name the next exact action and proof.

- **4. The caller can provide an identity while the operation declares no security requirement.** That combination suggests testing whether the server trusts the body value without deriving the caller from authenticated server-side session state.

- **5. The runner is fixed to the loopback base URL, hard-coded relative paths, five bounded probes, and synthetic application state.** Those controls prevent the exercise from expanding into public or unlisted targets.

</details>

## Next lesson

[Authentication and rate controls](03-auth-and-rate-controls.md) tests two
specific assumptions discovered in the map using synthetic and provider data.
