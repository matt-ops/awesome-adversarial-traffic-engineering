# Scope and Rules of Engagement

<!-- source-ids: nist-sp-800-115, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 00 — Method and authorization
- Lesson: 2 of 3
- Depth: Foundation
- Estimated time: 90 minutes
- Prerequisites:
  - [The authorized red-team role](01-red-team-role.md)
  - A terminal capable of running Python 3.12 or newer
- Required artifact: `artifacts/module-00/engagement-plan.md`
- Next lesson: Experimental method

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

## Guided exercise

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
outputs in the artifact and remove any accidental secrets or real target names.

## Why this matters offensively

Browser automation, replay, key rotation, and load tools can change destinations
or multiply traffic quickly. An operator should not rely on memory at execution
time. Preflight output, hard destination validation, attempt budgets, timeouts,
abort thresholds, and explicit cleanup turn written boundaries into observable
controls.

## Required artifact

`artifacts/module-00/engagement-plan.md` containing:

```text
owner and authorization reference
exact targets and exclusions
allowed passive and active discovery
allowed adversary objectives and protected actions
synthetic data and evidence handling
rate/concurrency/duration/attempt ceilings
health and abort conditions
contacts and incident handling
cleanup and state reset
report and exact-retest owner
dry-run output
rejected-target output
```

## Pass gate

1. Why is an allowlist not the same as authorization?
2. Does discovering a related hostname place it in scope?
3. Which fields make “test staging” executable?
4. What must happen when a local request redirects to an unlisted host?
5. What do the dry-run and rejection outputs prove—and not prove?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. An allowlist is a technical restriction; authorization is the owner's grant.
   A client can be technically capable of reaching a target that no owner approved.
2. No. Discovery supplies a candidate. The owner must explicitly add it before
   active contact or attack.
3. Exact target, allowed/excluded actions, timing, data, traffic limits, stop
   conditions, contacts, evidence, cleanup, reporting, and retest ownership.
4. Stop before following it, preserve the response, revalidate the destination,
   and obtain an amended scope if the owner wants it tested.
5. They prove the local plan passes guardrails and one public hostname is
   rejected. They do not prove legal permission, target behavior, or attack success.

</details>

## Next lesson

[Design a falsifiable experiment](03-experimental-method.md) so an authorized
run can support a causal, limited conclusion.
