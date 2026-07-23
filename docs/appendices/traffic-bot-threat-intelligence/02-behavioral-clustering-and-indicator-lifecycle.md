# Behavioral clustering and indicator lifecycle

<!-- source-ids: oasis-stix-21, owasp-automated-threats, misp-warning-lists, aate-local-lab -->
<!-- source-ledger-consistency: strict -->

## Appendix guide

- Appendix: Traffic and Bot Threat Intelligence
- Status: Optional
- Best time to review: after collection and confidence or before control-regression design
- Prior technical lessons required: None
- Return to the core path: [HTTP request and response](../../modules/01-http-edge/01-http-request-response.md)
- Appendix lesson: 2 of 3
- Estimated time: 120 minutes

## Role outcome

Cluster synthetic events by stable workflow behavior, document supporting and
contradicting evidence, and manage indicator freshness, version drift, false-
positive warnings, promotion, and retirement without assuming actor identity.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [STIX Version 2.1 Errata 01](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html) | 3.2 Common Properties; 4.7 Indicator; 5.1 Relationship; 5.2 Sighting | Supports lifecycle-aware indicator records and relationships | A valid STIX object can still encode poor analysis. |
| PROJECT_DOCUMENTATION | [OWASP Automated Threats](https://owasp.org/www-project-automated-threats-to-web-applications/) | Threat-event descriptions and mappings | Supplies behavior-oriented abuse categories | Taxonomy does not establish that one observed cluster belongs to a real actor. |
| PROJECT_DOCUMENTATION | [MISP Warning Lists](https://github.com/MISP/misp-warninglists) | README purpose, usage, categories, and known false-positive examples | Supports known-benign/shared-context warnings | A warning is contextual review input, not an automatic allow decision. |
| LAB_SPECIFIC | [Synthetic intelligence exercise](../../labs/course-map.md) | Version, sequence, relay, and outcome fields in the fixture command record | Provides deterministic cluster evidence and contradictions | Small fabricated fixture cannot estimate prevalence or production error rates. |

## Mental model

| Lifecycle state | Entry condition | Required review | Exit condition |
|---|---|---|---|
| Candidate | One bounded behavior pattern | Alternatives, shared context, missing fields | corroborate or discard |
| Active | Repeatable discriminating behavior | freshness, client version, warning-list context | update, expire, or retire |
| Degraded | Version drift or rising near-neighbor overlap | rerun exact regression populations | repair pattern or retire |
| Retired | No longer discriminating or supportable | preserve reason and dates | never silently reactivate |

Cluster across the protected workflow, request sequence, account/session
behavior, browser and JavaScript observations, HTTP and TLS observations,
network/proxy category, timing, target selection, infrastructure reuse,
challenge behavior, and final protected-action result. Treat behavioral
indicators as sequences, infrastructure indicators as shared pivots,
implementation artifacts as version-bound observations, and brittle atomic
indicators as cheap values such as one header.

## Required external instruction

### STIX indicator-lifecycle assignment

**Direct link:** [STIX Version 2.1 Errata 01](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
**Exact section, chapter, or unit:** 3.2 Common Properties; 4.7 Indicator; 5.1 Relationship; and 5.2 Sighting
**Estimated time:** 30 minutes
**What to focus on:** confidence, validity windows, sightings, relationships, and revocation as explicit lifecycle data
**What to skip:** cyber-observable object catalog not present in the fixture
**Expected takeaway:** define when a candidate indicator becomes active, degrades, expires, or is retired.

### OWASP behavior-taxonomy assignment

**Direct link:** [OWASP Automated Threats](https://owasp.org/www-project-automated-threats-to-web-applications/)
**Exact section, chapter, or unit:** Project overview and threat-event descriptions relevant to login and checkout automation
**Estimated time:** 25 minutes
**What to focus on:** sequences and objectives that remain meaningful when one header or client version changes
**What to skip:** using taxonomy labels as proof of a specific campaign
**Expected takeaway:** name a behavioral cluster by its workflow and effect rather than an assumed actor.

### MISP warning-context assignment

**Direct link:** [MISP Warning Lists](https://github.com/MISP/misp-warninglists)
**Exact section, chapter, or unit:** README purpose and usage, warning-list categories, and known false-positive examples
**Estimated time:** 15 minutes
**What to focus on:** shared, public, or otherwise context-sensitive values that can create false-positive matches
**What to skip:** installing or operating a MISP instance
**Expected takeaway:** add a warning and analyst review step instead of treating shared infrastructure as malicious identity.

## Course bridge

The executable grouping never reads a fixture-supplied answer. It first
normalizes every method/path request into an ordered sequence family. A proposed
group then requires at least two current events with the same protected workflow
and normalized request sequence plus recorded session, challenge, and protected-
action continuity. Timing, network/proxy category, and browser/protocol
availability are supporting dimensions. Missing values and divergent dimensions
remain visible; infrastructure is never a membership key.

A group record exposes its ID, member event IDs, matched and missing dimensions,
contradictions, alternatives, current support, historical-only support, the
categorical confidence result, and its attribution limitation. An ambiguous
record exposes candidate behavior families, insufficient or contradictory
dimensions, and alternative explanations.

Split a campaign hypothesis when behavior, target, or protected result diverges
beyond the stated alternatives. Merge hypotheses only when corroborated shared
behavior is stronger than infrastructure coincidence. Neither operation permits
attribution beyond the evidence, and this appendix does not teach geopolitical analysis.

## Worked example

The fixture's checkout sequence retains challenge replay and protected result as
strong behavior evidence. The historical fixture Chromium 132 string is stale
relative to fixture-current Playwright Chromium 149, so it becomes a degraded
version artifact, not the cluster definition. These fixture labels are not
claims about a universally current browser. `shared-relay.example` receives a
shared-context warning and cannot create membership or attribution.

## Optional exercise

### Objective

Produce two deterministic behavior clusters and an indicator lifecycle table
that explicitly handles ambiguity, version drift, and shared infrastructure.

### Setup

Use the repository fixture and the same local Python command as the first lesson.
No service, credential, or external collection source is required.

- Required working directory: repository root
- Preflight: confirm Python 3.12+ and the tracked fixture
- Exact target: `lab/fixtures/traffic_intelligence_events.json`; no network target
- Failure guidance: stop if ordering changes between identical runs or ambiguity disappears

### Exact actions or commands

```bash
python -m lab.analysis.traffic_intelligence
```

Compare each group's matched and missing dimensions, current and historical
support, contradictions, alternatives, confidence, and indicator validity
fields. Identify the stale browser artifact and warning-list match.

### Expected output

The evidence-derived output names `checkout-sequence-with-challenge-replay` and
`multi-account-login-sequence`, lists their actual members and matched
dimensions, and keeps cross-workflow `obs-005` ambiguous. The historical fixture
Chromium 132 artifact is degraded by version drift, and the shared relay is
marked insufficient for membership or attribution. The selected checkout group
has **high** confidence under the single rubric; the login group is
**moderate** because one record is inferred and carries weaker ratings.

### Interpretation

The clusters are useful because their names and evidence describe behavior that
can be emulated and retested. They remain hypotheses with bounded confidence;
retiring a stale artifact protects legitimate near-neighbors and prevents a
version string from becoming a permanent identity rule.

### Common failure modes

- Clustering only by IP-like value, user agent, or one stale version string
- Hiding observations that contradict the preferred cluster
- Treating a warning-list match as an automatic malicious or benign verdict

### Cleanup

The analysis is read-only and deterministic. No generated evidence must be committed.

## Why this matters offensively

An adversary can change cheap artifacts faster than a defender updates rules.
Behavioral and lifecycle discipline reveals which observations remain expensive
to imitate and which controls will drift into false positives or easy evasion.

## Check your understanding

1. Why is an ordered workflow sequence usually a stronger cluster feature than one user-agent string?
2. What should happen when an indicator's browser-version artifact no longer matches the current observed version?
3. How should a shared-relay warning affect analysis of a possible automated-abuse cluster?
4. Which evidence must accompany a named behavior cluster so another analyst can challenge the cluster?

## Answer key

<details>
<summary>Show answers</summary>

- **1. A sequence combines several stateful actions and outcomes, while a user-agent string is cheap to copy and changes with releases.** The sequence can therefore remain discriminating after one volatile claim drifts.

- **2. Mark the artifact degraded, rerun the exact regression populations, and either update or retire it with recorded dates and reasons.** Silently retaining it would increase stale matches and unsupported conclusions.

- **3. Treat the relay as contextual evidence that increases false-positive risk and requires analyst review.** Shared infrastructure cannot identify an actor and should not override contradictory workflow or protected-result evidence.

- **4. Publish supporting observations, contradictions, alternatives, missing fields, collection points, confidence, freshness, version labels, protected outcomes, and the next discriminating observation.** That record makes the cluster testable instead of accepted merely by assertion.

</details>

## Continue

- Continue with [Intelligence to emulation and regression](03-intelligence-to-emulation-and-regression.md).
- Return to [HTTP request and response](../../modules/01-http-edge/01-http-request-response.md) for the core path.
