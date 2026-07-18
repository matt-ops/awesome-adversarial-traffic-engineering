# Workflow and API mapping

<!-- source-ids: portswigger-api-testing-path, owasp-wstg-entry-points-v42, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 04 - Automated abuse and workflow attacks
- Lesson: 2 of 5
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [Automated-abuse objectives](01-abuse-objectives.md)
  - Module 01 request/workflow/path artifacts
  - Docker Desktop or compatible Docker Engine for the integrated local lab
- Required artifact: `artifacts/module-04/local-api-map.md`
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

Docker Compose builds one FastAPI application behind a loopback-only Nginx edge.
`-f` selects its course file; `up --build -d` builds images and starts them in the
background. The health request verifies the route before any exercise.

```powershell
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
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

## Required artifact

`artifacts/module-04/local-api-map.md` with endpoint inventory, workflow graph,
error/control boundaries, four hypotheses, required proof, and observed versus
documented labels.

## Pass gate

1. Why is an OpenAPI security declaration not enforcement proof?
2. What does the invalid-product `404` contribute to the map?
3. Why does recon end in hypotheses rather than findings?
4. Which observation suggests the reservation authorization test?
5. What limits the local recon scope?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. Documentation expresses intended metadata; runtime code/state decides enforcement.
2. It locates object validation and records a controlled error boundary.
3. Observations have not yet been tested through the protected actions and authoritative state.
4. The reserve schema accepts caller-supplied `identity` and declares no security requirement.
5. Fixed loopback base URL, hard-coded relative paths, five bounded probes, and synthetic state.

</details>

## Next lesson

[Authentication and rate controls](03-auth-and-rate-controls.md) tests two
specific assumptions discovered in the map using synthetic and provider data.
