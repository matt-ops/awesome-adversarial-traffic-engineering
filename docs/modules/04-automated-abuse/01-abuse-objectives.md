# Automated-abuse objectives

<!-- source-ids: owasp-automated-threats, aate-adversarial-control-loop -->

## Progress

- Module: 04 - Automated abuse and workflow attacks
- Lesson: 1 of 5
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [Module 03](../03-playwright/index.md) and the knowledge and exercise behavior from earlier modules
  - Ability to distinguish a request, session, workflow, and objective
- Next lesson: Workflow and API mapping

## Role outcome

Classify an automated business-abuse objective and define its protected action,
preconditions, state transition, proof, and legitimate near-neighbor.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [OWASP Automated Threats](https://owasp.org/www-project-automated-threats-to-web-applications/) | Project introduction plus seven exact OAT entries below | Supplies a business-abuse taxonomy, not an attack procedure | The project is a taxonomy and handbook, not an execution methodology. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Objective, protected action, mapping, baseline, proof | Converts taxonomy categories into falsifiable emulation objectives | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| OAT category | Adversary objective | Protected action/effect | Important distinction |
|---|---|---|---|
| Credential Stuffing | validate reused credential pairs | successful login to a synthetic/provider account | known pairs, not password guessing |
| Account Creation | create identities for later misuse | account record accepted | creation is preparation; later misuse is separate |
| Scraping | collect accessible data for use elsewhere | response set extracted | access may be public; harm depends on use/scale |
| Scalping | acquire scarce goods unfairly | purchase/reservation completed | attacker obtains the good |
| Denial of Inventory | hold scarce stock without purchase | availability removed/held | attacker does not complete acquisition |
| CAPTCHA Defeat | satisfy or bypass an anti-automation test | gated step accepted | challenge passage is not the final business objective |
| Denial of Service | impair service availability | resource/health objective breached | service capacity, not item availability |

## Required external instruction

### OWASP automated-threat assignment

**Direct link:** [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/)  
**Exact section, chapter, or unit:** project introduction; for each named entry read only Summary Defining Characteristics, Description, and Other Names and Examples  
**Estimated time:** 75 minutes  
**What to focus on:** the object or capability abused, whether the attacker acquires value, what state/effect proves success, and adjacent categories that must not be conflated  
**What to skip:** diagrams, cross-reference catalogs, symptoms, countermeasure catalogs, and every OAT not named here  
**Expected takeaway:** classify seven scenarios and defend the classification from workflow outcome rather than tool, traffic volume, or detector label.

Assigned entry links: [OAT-008 Credential Stuffing](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-008_Credential_Stuffing), [OAT-019 Account Creation](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-019_Account_Creation), [OAT-011 Scraping](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-011_Scraping), [OAT-005 Scalping](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-005_Scalping), [OAT-021 Denial of Inventory](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-021_Denial_of_Inventory), [OAT-009 CAPTCHA Defeat](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-009_CAPTCHA_Defeat), and [OAT-015 Denial of Service](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-015_Denial_of_Service).

## Course bridge

OWASP defines automated threats around misuse of normal web-application
functionality. For example, Credential Stuffing tests previously obtained pairs,
whereas Denial of Inventory holds limited stock without buying it.[^oat]

[^oat]: OWASP Automated Threats, OAT-008 and OAT-021, assigned sections.

The taxonomy answers *what abuse pattern is occurring*. It does not supply an
engagement scope, safe execution procedure, evidence standard, or bypass method.
Those come from the AATE method and the provider/local lab rules.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Define `objective -> workflow -> protected action ->
    authoritative proof`. A challenge, bot score, or rate-limit response is an
    intermediate control unless the engagement objective is explicitly to test
    that control in isolation.

## Worked example

```text
Scenario: script holds five reservation slots and never checks out.
Category: OAT-021 Denial of Inventory.
Protected action: reservation records reduce available slots.
Proof: server inventory 5 -> 0, reservation owner/state, and no purchase records.
Not enough: five POST requests, five UI messages, or a changed bot score.
Near-neighbor: a fast completed purchase is closer to Scalping.
```

The tool could be curl, Python, or Playwright; classification does not change
because the business outcome does not change.

## Guided exercise

### Objective

Produce a seven-row abuse threat map with testable outcomes.

### Setup

Use the table format shown in this lesson. No target or credential list is
needed; use fictional scenarios and synthetic identities.

### Exact actions or commands

1. Add one scenario for each assigned OAT entry.
2. State adversary objective, prerequisites, action chain, protected action,
   server-side proof, intermediate controls, and legitimate near-neighbor.
3. Add one misclassification and explain why it is wrong.
4. Mark the authorization source: local repository or named provider target.
5. For DoS, defer executable traffic details to Module 08 and define only the
   resource/health effect.

### Expected output

Every row names a business or service outcome. CAPTCHA passage leads to another
action; inventory denial distinguishes holds from purchases; credential stuffing
uses synthetic known pairs rather than guessed passwords.

### Interpretation

If a row's proof is a client message, request count, or detector score, revise it
until authoritative state or a service effect decides success.

### Common failure modes

- Classifying by tool ("Playwright bot") instead of outcome
- Calling password guessing credential stuffing
- Calling item unavailability and service unavailability the same denial
- Treating challenge passage as account takeover
- Using real leaked data; the course uses only synthetic/provider data

### Cleanup

No target was contacted. Remove employer, customer, or real account details from
the public-safe exercise result.

## Why this matters offensively

The abuse objective determines reconnaissance, client capabilities, fixed
variables, evidence, impact, and retest. A vague "bot test" encourages random
signal changes; a precise inventory or login outcome yields an emulation plan.

## Check your understanding

1. An operator tests a fixed list of previously obtained synthetic username/password pairs. Why is that Credential Stuffing rather than password guessing?
2. One script completes purchases while another holds reservations and never checks out. Which business outcome separates Scalping from Denial of Inventory?
3. A script passes a CAPTCHA but never performs the gated reservation. Why is CAPTCHA passage only an intermediate outcome in that workflow?
4. The exercise maps automated collection of publicly accessible catalog data. Can the activity still fit a scraping-abuse objective, and what must be analyzed before claiming harm?
5. Five reservation holds reduce inventory from 5 to 0 without purchases. Which evidence makes that Denial of Inventory rather than service-level Denial of Service?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Credential Stuffing tests known username/password pairs that came from an earlier source, while guessing generates candidate passwords.** The lesson uses only fixed synthetic pairs and does not obtain or test external credentials.

- **2. Scalping ends with the adversary acquiring the scarce product or service.** Denial of Inventory removes availability through holds or reservations without completing the acquisition, so purchase records distinguish the outcomes.

- **3. Passing the CAPTCHA only opens a later workflow edge.** The protected business objective remains unproved until the reservation, purchase, login, or other gated action actually succeeds.

- **4. Yes, automated collection of public content can fit a scraping scenario.** The operator must still analyze authorization, collection scale, later use, protected outcome, and demonstrated impact rather than assuming public access makes every use harmless.

- **5. Inventory records showing five held units and no completed purchases prove an inventory-state effect.** A Denial-of-Service claim instead requires resource and health evidence showing impaired service capacity or availability.

</details>

## Next lesson

[Workflow and API mapping](02-workflow-mapping.md) converts one selected abuse
objective into entry points, state transitions, and bounded hypotheses.
