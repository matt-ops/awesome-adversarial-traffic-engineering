# Collection and confidence

<!-- source-ids: first-cti-source-evaluation, oasis-stix-21, aate-local-lab -->
<!-- source-ledger-consistency: strict -->

## Appendix guide

- Appendix: Traffic and Bot Threat Intelligence
- Status: Optional
- Best time to review: after workflow mapping or before an intelligence-informed emulation plan
- Prior technical lessons required: None
- Return to the core path: [HTTP request and response](../../modules/01-http-edge/01-http-request-response.md)
- Appendix lesson: 1 of 3
- Estimated time: 90 minutes

## Role outcome

Normalize synthetic traffic observations, grade source reliability separately
from information reliability, preserve uncertainty, and refuse actor attribution
when infrastructure or user-agent observations have plausible alternatives.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Source Evaluation and Information Reliability](https://www.first.org/global/sigs/cti/curriculum/source-evaluation) | Source reliability A-F and information reliability 1-6 | Separates source history from the reliability of one reported item | Ordinal judgment aids consistency; it does not calculate truth or attribution. |
| STANDARD | [STIX Version 2.1 Errata 01](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html) | 3.2 Common Properties (confidence); 4.7 Indicator; 4.14 Observed Data; 5.1 Relationship; 5.2 Sighting; Appendix A: Confidence Scales | Supplies typed objects and an interoperable confidence property | STIX defines representation; it does not validate the truth of supplied data. |
| LAB_SPECIFIC | [Synthetic intelligence exercise](../../labs/course-map.md) | `python -m lab.analysis.traffic_intelligence` fixture and command record | Provides deterministic, non-network evidence | Fabricated data cannot describe a real campaign, actor, product, or control. |

## Mental model

| Field | Question | Example |
|---|---|---|
| Incident | What bounded event triggered analysis? | a synthetic protected checkout completed after proof transfer |
| Observation | What was directly collected? | request sequence and returned protected result |
| Indicator | Which reviewable pattern may find related behavior? | proof changes session before checkout |
| Inference | What explanation is drawn from observations? | proof may be weakly bound |
| Hypothesis | Which falsifiable claim selects the next test? | session binding will reject transfer after remediation |
| Confirmed fact | Which claim has direct, repeatable supporting evidence? | the recorded local response named Session B |
| Source reliability | Has this source historically collected what it claims? | `A`: directly instrumented deterministic fixture |
| Information reliability | Is this particular assertion corroborated and internally coherent? | `2`: probably true with independent fields |
| Course confidence | How strongly does the analysis support the bounded conclusion? | `high`, with rubric inputs and contradictions listed |
| Attribution | Who conducted the behavior? | `unknown`; shared relay and UA are insufficient |

## Required external instruction

### FIRST source-evaluation assignment

**Direct link:** [Source Evaluation and Information Reliability](https://www.first.org/global/sigs/cti/curriculum/source-evaluation)
**Exact section, chapter, or unit:** Source reliability and Information reliability
**Estimated time:** 20 minutes
**What to focus on:** rating source history independently from the reliability of one reported item
**What to skip:** organizational adoption and unrelated curriculum units
**Expected takeaway:** justify one letter-number pair without converting it into a probability or actor claim.

### STIX observation assignment

**Direct link:** [STIX Version 2.1 Errata 01](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
**Exact section, chapter, or unit:** 3.2 Common Properties, specifically the confidence property; 4.7 Indicator; 4.14 Observed Data; 5.1 Relationship; 5.2 Sighting; and Appendix A: Confidence Scales
**Estimated time:** 25 minutes
**What to focus on:** observed facts, analytical patterns, relationships, sightings, timestamps, and confidence
**What to skip:** object types not used by the fixture and implementation bindings
**Expected takeaway:** Observed Data is raw observed information; an Indicator is an analytical detection pattern; a Sighting asserts that something was seen; and a Relationship links STIX objects. None validates the truth of supplied data.

## Course bridge

An observed header, network label, or challenge outcome is evidence about a
bounded event. It does not name an actor. Normalization preserves the original
value, collection point, time, source, and missing fields before analysis groups
events. Confidence must travel with contradictions and plausible alternatives.

Start with an intelligence requirement: name the protected workflow, decision
the analysis must support, populations, time window, required evidence, and
confidence threshold. Corroboration should join independent observations rather
than duplicate one collector's claim. Current evidence and historical reporting
remain separate because a past client artifact can drift even when the source
was reliable. The FIRST letter rates source history; its number rates this item,
so an `A` source never makes every reported fact true.

The command applies one categorical course rubric everywhere:

- **High:** at least two independently collected current direct observations,
  source ratings `A` or `B`, information ratings `1` or `2`, complete protected-
  workflow continuity, and no unresolved material contradiction.
- **Moderate:** independent current support and workflow continuity remain, but
  a direct-observation gap, weaker rating, missing supporting dimension,
  historical dependency, or bounded alternative remains.
- **Low:** support is single-source, entirely inferred or historical, materially
  contradictory, weakly rated, or missing workflow/action continuity.

These categories are course synthesis, not probabilities. The FIRST letter-
number pair remains separate. The exercise does not emit a numeric STIX
confidence value; Appendix A is reviewed only to understand interoperability
mappings that other systems may require.

## Worked example

Observation `obs-005` uses a shared relay, a common user agent, and an incomplete
workflow. The correct normalized record retains those facts and labels the
behavior ambiguous. Assigning a campaign name would discard the strongest fact:
several legitimate and automated populations could share the same observations.

## Optional exercise

### Objective

Generate a deterministic normalized evidence table and explain why the ambiguous
event does not support actor attribution.

### Setup

Use Python 3.12+ from the repository root. The fixture contains only synthetic
events and documentation-only hostnames.

- Required working directory: repository root
- Preflight: confirm Python 3.12+ and `lab/fixtures/traffic_intelligence_events.json`
- Exact target: the tracked synthetic fixture; the command opens no socket
- Failure guidance: stop on a missing field, invalid rating, unexpected file write, or attempted connection

### Exact actions or commands

```bash
python -m lab.analysis.traffic_intelligence
```

Read the normalized evidence and source-evaluation sections. Confirm the command
does not accept a target URL or make a network request.

### Expected output

Six normalized observations retain collection time, workflow sequence,
challenge and protected-action results, source reliability, information
reliability, and missing values. `obs-005` remains ambiguous, while the output
explicitly says shared infrastructure and user-agent strings do not identify an actor.

### Interpretation

The exercise succeeds when another analyst can distinguish collected fact from
inference and can see why each confidence judgment has limits. A cleanly
normalized record improves later clustering, but it does not make attribution
stronger than the original evidence.

### Common failure modes

- Combining source reliability, information reliability, and course confidence into one unexplained score
- Treating a shared relay or common user agent as actor identity
- Dropping missing fields or ambiguous observations before clustering

### Cleanup

The command writes nothing and opens no connection. No cleanup is required.

## Why this matters offensively

Traffic-control testing often produces abundant but weak observations. An
operator who preserves uncertainty can design a discriminating next test instead
of overfitting defenses to one stale header, relay, or client label.

## Check your understanding

1. Why must FIRST source reliability and information reliability remain separate ratings?
2. Why is an observed user-agent value not automatically a STIX Indicator or an actor attribution?
3. Which facts make `obs-005` unsuitable for a confident campaign assignment?
4. What must a normalized traffic observation preserve before behavioral clustering?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Source reliability describes the source's collection history, while information reliability evaluates one specific assertion.** A dependable source can report an uncertain item, and an unfamiliar source can provide a well-corroborated observation.

- **2. An observed user agent is a collected value, while an Indicator is an analytical pattern intended to detect activity.** Neither object alone proves which person or group produced the traffic.

- **3. The event uses shared infrastructure, a common client claim, and an incomplete workflow sequence with plausible legitimate alternatives.** Those contradictions support an ambiguous label and a next collection step, not attribution.

- **4. Preserve time, collection point, original values, source, workflow sequence, challenge and protected-action outcomes, version labels, missing fields, and provenance.** Those fields let another analyst test the grouping without silently inventing evidence.

</details>

## Continue

- Continue with [Behavioral clustering and indicator lifecycle](02-behavioral-clustering-and-indicator-lifecycle.md).
- Return to [HTTP request and response](../../modules/01-http-edge/01-http-request-response.md) for the core path.
