# Scope and Rules of Engagement

<!-- source-ids: nist-sp-800-115, aate-local-lab, aate-adversarial-control-loop -->

## Appendix guide

- Appendix: Red-team method and engagement practice
- Status: Optional
- Best time to review: before an informational or interview; before a
  provider-hosted assessment; before an organization-owned engagement; or
  before the integrated capstone
- Prior technical lessons required: None
- Return to the core path: [HTTP request and response](../01-http-edge/01-http-request-response.md)
- Appendix lesson: 2 of 3
- Estimated time: 90 minutes

## Role outcome

Translate owner permission into target, action, data, traffic, abort, evidence,
cleanup, and retest controls that can be checked before and during execution.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §6.5 and Appendix B | Defines assessment-plan and Rules of Engagement content | General testing guide; it does not define bot-control or DDoS red-team procedure. |
| LAB_SPECIFIC | [AATE local target policy](../../safety/local-target-policy.md) | Allowed hosts and rejected examples | Shows the repository's executable destination boundary | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | Steps 1 and 15 | Makes authorization and identical retest bookends of the method | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
owner permission
  -> written plan (who/what/when/how/data/contacts)
  -> executable controls (allowlist/caps/timeouts/abort)
  -> operator preflight (health/reset/evidence destination)
  -> monitored run (stop on threshold or owner request)
  -> cleanup and exact retest ownership
```

Permission without executable controls is easy to misapply. An allowlist without
written ownership is only a technical restriction, not authorization.

## Required external instruction

### NIST planning and Rules of Engagement

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)  
**Exact section, chapter, or unit:** §6.5 Assessment Plan Development and Appendix B Rules of Engagement  
**Estimated time:** 35 minutes  
**What to focus on:** scope, authorized and excluded systems, personnel, logistics, data handling, incident handling, and reporting  
**What to skip:** detailed technique sections and tool descriptions  
**Expected takeaway:** produce a plan another operator could execute without guessing whether a target, action, rate, data source, or stop condition is allowed.

## Course bridge

NIST's assessment plan identifies scope, required resources, roles,
limitations, logistics, and deliverables; Appendix B supplies example Rules of
Engagement fields.[^nist-plan] A URL discovered during mapping does not become
authorized merely because it appears related.

[^nist-plan]: NIST SP 800-115, §6.5 and Appendix B.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE separates three layers. **Authorization** is the
    owner's grant. **Scope** is the exact boundary written in the plan.
    **Guardrails** are controls that prevent or stop execution outside that
    boundary. All three must agree.

The bundled client uses an exact hostname allowlist and rejects lookalike hostnames,
private LAN addresses, public IPs, embedded credentials, and non-HTTP schemes.
Its load envelope caps duration, concurrency, rate, total requests, and expensive
requests. These controls do not authorize another target; they constrain only the
local exercise.

## Worked example

“Test our staging site” is not executable scope. A usable row is:

| Field | Value |
|---|---|
| Owner | Named service owner and approving security contact |
| Target | `http://localhost:8080/api/reports/protected` |
| Allowed action | One challenge solve and one cross-session replay |
| Excluded | Other ports, adjacent containers, public services, real accounts |
| Data | Fixed synthetic session IDs only |
| Traffic | Under repository hard caps; three protected requests |
| Abort | Unexpected redirect/host, health failure, non-synthetic data, owner stop |
| Evidence | Request IDs, statuses, response session, timestamps, versions |
| Cleanup | Reset synthetic state and stop the local service |
| Retest owner | Named operator repeats the exact replay after token binding fix |

## Optional exercise

### Objective

Prove that the repository's destination and traffic controls accept the intended
local plan and reject an unapproved public target before sending traffic.

### Setup

From the repository root, confirm Python 3.12 or newer is available. The command
imports the standard-library client, validates its default loopback URL, validates
the default envelope, prints the plan, and exits without a request because
`--dry-run` is set.

### Exact actions or commands

First display the safe plan:

```powershell
python -m lab.clients.safe_client --dry-run
```

Then test the negative boundary. This command should be rejected before network
activity because `example.com` is not allowlisted:

```powershell
python -m lab.clients.safe_client --target https://example.com --total 1
```

### Expected output

The dry run prints a JSON object containing `localhost`, `dry_run: true`, a
five-second duration, concurrency 1, rate 2, total 10, and zero expensive
requests. The negative test prints a JSON error with `rejected: true` and exits
with status 2.

### Interpretation

The first result proves only that the *plan* fits local guardrails. The second
proves the client rejects that hostname. Neither result grants authorization or
proves an attack outcome.

### Common failure modes

- `python` is not found: locate Python 3.12+ and rerun only the version command
- Module import fails: run from the repository root
- The public URL is accepted: stop; the safety control is broken
- Editing the allowlist to make a lesson pass: revert the edit and document the failure

### Cleanup

No traffic is sent by the dry run or rejected-target test. Preserve the two
outputs in your exercise notes and remove any accidental secrets or real target names.

## Why this matters offensively

Browser automation, replay, key rotation, and load tools can change destinations
or multiply traffic quickly. An operator should not rely on memory at execution
time. Preflight output, hard destination validation, attempt budgets, timeouts,
abort thresholds, and explicit cleanup turn written boundaries into observable
controls.

## Check your understanding

1. The safe client accepts `http://localhost:8080` because the address is allowlisted. Why does that technical check not replace written authorization from the service owner?
2. During reconnaissance, a response names a related hostname that is absent from the engagement plan. May the operator actively test the new hostname?
3. The phrase “test staging” is too vague to execute safely. Which fields in the worked scope row turn that phrase into an executable plan?
4. A request to the approved loopback target returns a redirect to an unlisted host. What should the client and operator do before any request follows the redirect?
5. The guided exercise prints a valid local dry-run and rejects `example.com` before network activity. What do those two results prove, and what remains unproved?

## Answer key

<details>
<summary>Show answers</summary>

- **1. An allowlist only restricts where the client can send traffic.** Authorization is the owner's explicit permission for a named target, action, time, and limit, so a reachable or allowlisted address can still be outside the approved engagement.

- **2. No active testing is allowed until the owner explicitly adds the hostname to scope.** Discovery creates a candidate for review; the response does not grant permission to contact or attack the related system.

- **3. The plan needs the exact target, allowed and excluded actions, timing, data, traffic limits, abort conditions, contacts, evidence, cleanup, reporting, and retest owner.** Those fields let both tools and people check the boundary before execution.

- **4. The client must stop before following the redirect, preserve the response, and revalidate the destination.** The operator should obtain an amended scope only if the owner wants the newly identified host tested.

- **5. The outputs prove that the configured local plan passes repository guardrails and that one public hostname is rejected before traffic.** They do not prove legal permission, application behavior, control effectiveness, or attack success.

</details>

## Continue

- Continue through the appendix with [Experimental method before attack
  execution](03-experimental-method.md) when you want more methodology depth.
- Return to [HTTP request and response](../01-http-edge/01-http-request-response.md)
  to begin the core technical path.
