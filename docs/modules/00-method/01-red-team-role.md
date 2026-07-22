# The authorized red-team role

<!-- source-ids: nist-sp-800-115, mitre-adversary-emulation-plans, aate-adversarial-control-loop -->

## Progress

- Module: 00 — Method and authorization
- Lesson: 1 of 3
- Depth: Foundation
- Estimated time: 75 minutes
- Prerequisites:
  - [Start here](../../start-here.md)
  - Ability to read a request/response example; no browser automation required
- Next lesson: Scope and Rules of Engagement

## Role outcome

Define an adversary objective and protected action, then distinguish offensive
proof from vulnerability discovery, control observation, and detection design.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | §5.2 and §5.2.1 | Establishes planning, discovery, attack, and reporting phases | General testing guide; it does not define bot-control or DDoS red-team procedure. |
| STANDARD | [MITRE Adversary Emulation Plans](https://attack.mitre.org/resources/adversary-emulation-plans/) | Complete page | Supports modeling behavior and chained actions rather than a tool list | Examples focus on enterprise adversaries, not automated-abuse controls. |
| COURSE_SYNTHESIS | [AATE method provenance](../../methodology/provenance.md) | AATE specialization | Connects those sources to protected-action proof and exact retest | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Activity | Question answered | Insufficient stopping point | Offensive completion |
|---|---|---|---|
| Vulnerability discovery | Is an assumption or weakness present? | A suspicious parameter exists | Reproduce the resulting hostile outcome |
| Control reconnaissance | What appears to influence a decision? | A signal or score changed | Repeat the protected action under the changed condition |
| Detection analysis | How does a rule classify samples? | Precision/recall or a challenge decision | Show the overtrusted assumption and operational consequence |
| Red-team engagement | Can representative adversary behavior defeat the objective? | A tool ran or a request returned | Preserve action, state/health effect, impact, limits, remediation, and retest |

## Required external instruction

### NIST penetration-test phases

**Direct link:** [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)  
**Exact section, chapter, or unit:** §5.2 Penetration Testing and §5.2.1 Penetration Testing Phases  
**Estimated time:** 25 minutes  
**What to focus on:** Planning, Discovery, Attack, Reporting, and the feedback between attack validation and additional discovery  
**What to skip:** technique catalogs outside §5.2  
**Expected takeaway:** explain why discovering a weakness, validating its effect, and reporting its evidence belong to one bounded engagement.

### MITRE behavior-chain assignment

**Direct link:** [MITRE Adversary Emulation Plans](https://attack.mitre.org/resources/adversary-emulation-plans/)  
**Exact section, chapter, or unit:** complete short page through Emulation Plan Documents  
**Estimated time:** 15 minutes  
**What to focus on:** the distinction between reproducing adversary behavior and copying one tool, command, or indicator  
**What to skip:** linked emulation-plan documents and unrelated APT material  
**Expected takeaway:** turn an objective into a short chain of representative actions whose result can be observed and evaluated.

## Course bridge

NIST describes penetration testing through Planning, Discovery, Attack, and
Reporting.[^nist-phases] Discovery can identify a weakness; the Attack phase
attempts to validate it, and Reporting communicates the evidence and mitigation.
MITRE's emulation material likewise emphasizes behavior and chained actions over
detecting one indicator or product.[^mitre-behavior]

[^nist-phases]: NIST SP 800-115, §5.2.1.
[^mitre-behavior]: MITRE ATT&CK, “Adversary Emulation Plans,” complete page.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** AATE names the observable hostile result the
    **protected action**. A browser score, WAF label, rate-limit counter, or TLS
    fingerprint is evidence about a control; it is not the objective. The
    operator repeats the protected action and verifies server-side state or a
    service-health effect.

For bot controls, the objective could be “reserve one unit without the required
account state.” For resilience, it could be “cause the expensive workflow to
breach its p95 objective while the cheap route remains healthy.” Both are
falsifiable. “Bypass bot detection” is not yet falsifiable because it lacks a
specific action, control response, and proof.

## Worked example

Suppose `/api/reports/protected` returns `403` until a browser solves a challenge.
The operator captures a token from session A and presents it from session B.

| Observation | Meaning |
|---|---|
| Session B without token returns `403` | Blocked baseline exists |
| Session A receives a token | Challenge flow works for one controlled session |
| Session B with A's token returns `200` | The protected action succeeded under replay |
| Server response names session B | Stronger evidence than a client-side score |
| Token is fixed in a toy lab | Limitation; not evidence about an external service |

The finding is not “the token looked reusable.” It is “a token issued in one
session authorized the protected action in another session.”

## Guided exercise

### Objective

Turn three vague security statements into adversary objectives with protected
actions and observable proof.

### Setup

Use a temporary note, document, or sheet. No software or target is needed.

### Exact actions or commands

For each statement below, write four fields: adversary objective, protected
action, proof, and an observation that would *not* be sufficient.

1. “Test the bot detector.”
2. “Check the rate limit.”
3. “Evaluate DDoS protection.”

Then add one behavior chain of three to five actions for each objective. A chain
might map state, establish a blocked baseline, change a key, repeat the action,
and query the resulting state.

### Expected output

A correct row for the rate-limit statement resembles:

```text
Objective: obtain three accepted expensive reports during one evaluation window.
Protected action: GET /api/reports/limited returns an accepted report.
Proof: fixed identity is throttled; three controlled identities each receive 200;
       server telemetry shows all actions belong to one hostile workflow.
Insufficient: the client used three IP-like strings or a counter reset.
```

### Interpretation

If the proof does not require a server-side state or service effect, the row is
still control observation. Tighten the objective until success and failure can be
decided from preserved evidence.

### Common failure modes

- Naming a tool (“use Playwright”) instead of behavior
- Treating “not challenged” as proof that the hostile action succeeded
- Omitting a legitimate baseline or a blocked adversary baseline
- Claiming impact beyond the test target

### Cleanup

No target was contacted. If you keep the exercise result, remove any real
organization or customer names before sharing or committing it.

!!! tip "Optional: keep this for later"
    Save the comparison if you want to reuse it during interview practice.
    Saving it is not required to continue.

## Why this matters offensively

An operator who cannot name the protected action will optimize whatever signal
is easiest to observe. That creates impressive-looking detector screenshots and
weak findings. A precise objective keeps reconnaissance, evasion, pressure,
evidence, remediation, and retest aligned to the outcome the control exists to
prevent.

## Check your understanding

1. The worked example shows Session B receiving `200` after reusing Session A's challenge token. Which observation is the protected-action proof, and which observations are only control signals?
2. A detector score changes after a browser property is modified, but `/api/reports/protected` still returns `403`. Why has the operator not proved a bypass?
3. NIST's Discovery phase identifies a possible weakness in challenge-token binding. Which NIST phase attempts to validate the weakness through the protected action?
4. MITRE's behavior-focused approach is applied to a challenge replay. Why should the emulation plan describe the chained actions instead of naming only Playwright or curl?
5. For the exercise statement “Check the rate limit,” what server-side result would turn the statement into a testable adversary objective?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The `200` response for Session B's protected request, backed by server evidence naming Session B, is the protected-action proof.** Token issuance and detector or challenge changes describe control behavior, but do not by themselves show that the protected action succeeded.

- **2. The operator has changed a control observation, not completed the hostile action.** Because the protected endpoint still returns `403`, the original objective remains blocked even if an intermediate score looks more favorable.

- **3. NIST's Attack phase attempts to validate the discovered weakness.** In this example, validation means replaying the token through the protected endpoint and checking the server-side outcome, followed by reporting the evidence and limits.

- **4. A behavior chain records what the adversary does and what each step accomplishes, so another operator can reproduce the objective with a different tool.** Naming only Playwright or curl describes implementation, not the sequence under test.

- **5. The objective needs a measurable accepted action, such as obtaining three expensive reports during one evaluation window when the intended limit allows fewer.** Statuses and server-side report results make success or failure decidable.

</details>

## Next lesson

[Define scope and Rules of Engagement](02-scope-and-rules.md) so the objective is
bounded by executable authorization rather than intent alone.
