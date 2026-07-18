# JA4 and JA4H as pivots

<!-- source-ids: ja4-project, rfc-8446, aate-adversarial-control-loop -->

## Progress

- Module: 07 - Protocol identity
- Lesson: 2 of 5
- Depth: Applied
- Estimated time: 3 hours
- Prerequisites:
  - [TLS ClientHello](01-tls-clienthello.md)
  - Signal-family and residual-anomaly artifacts
- Required artifact: `artifacts/module-07/ja4-interpretation.md`
- Next lesson: HTTP/2

## Role outcome

Interpret JA4/JA4H components as implementation/behavior pivots and write a
cross-layer hypothesis without treating a fingerprint as identity proof.

> A network fingerprint is an analytical pivot, not proof of a specific user or browser.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [JA4+ project](https://github.com/FoxIO-LLC/ja4) | overview; JA4; JA4H; technical details; version considerations | Primary method documentation | Fingerprints change with implementations; licensing differs across JA4+ methods; fingerprints are not identity proof. |
| STANDARD | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | §4.1.2 | Grounds the TLS fields behind JA4 | Assigned only at Integrated depth; it does not define JA4. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | candidate signal, alternatives, action proof | Prevents identity overclaim | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Method | Input surface | Useful for | Not proof of |
|---|---|---|---|
| JA4 | normalized ClientHello characteristics | clustering/pivoting client stacks | person, account, intent |
| JA4H | HTTP request characteristics | clustering request implementations/behavior | same device across all intermediaries |
| Cross-layer comparison | browser claim + TLS + HTTP + state | finding contradictions/hypotheses | universal bot classification |

## Required external instruction

### JA4 project assignment

**Direct link:** [JA4+ network fingerprinting methods](https://github.com/FoxIO-LLC/ja4)  
**Exact section, chapter, or unit:** project overview; JA4 TLS fingerprint; JA4H HTTP fingerprint; relevant ClientHello/HTTP technical details; version/change considerations  
**Estimated time:** 90 minutes  
**What to focus on:** selected/normalized components, observation point, implementation drift, intermediaries, and project-stated use  
**What to skip:** other JA4+ methods, commercial tooling, installation, and rule feeds  
**Expected takeaway:** decode what a JA4/JA4H value summarizes and name at least five alternative explanations for a cluster.

## Course bridge

Fingerprinting compresses structured observations into a comparable value. That
supports grouping and investigation; shared software/configuration creates shared
values, while updates and intermediaries change them.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Use a fingerprint as a pivot into raw observations,
    versions, session/workflow evidence, and the protected action. Never write
    "fingerprint X is attacker Y" without independent attribution evidence.

## Worked example

A browser claims current Chrome/Windows, but the edge sees a JA4 associated in
the operator's own controlled baselines with Python/OpenSSL. Hypothesis: a
non-browser TLS client or terminating proxy produced the connection. Alternatives
include proxy, scanner, version mismatch, library reuse, and mislabeled baseline.

## Guided exercise

### Objective

Write a correct interpretation from a fictional cross-layer record.

### Setup

Use a synthetic record; do not query public reputation services.

### Exact actions or commands

1. List raw components summarized by JA4 and JA4H per project documentation.
2. Separate observed value, local baseline association, and inference.
3. Add observation point and termination path.
4. List five alternatives and required corroboration.
5. State a protected-action hypothesis and narrow conclusion.

### Expected output

The worksheet records the input fields, method/version, observation point,
resulting fingerprint or comparison key, and a sentence using "consistent with"
or "inconsistent with" the recorded baseline. It separately lists fields an
intermediary can transform and versions that constrain the observation.

### Interpretation

The fingerprint narrows a population and raises a falsifiable cross-layer
question: does this transport/HTTP behavior agree with the browser claim under
the same route and intermediary? It does not identify a person, prove a specific
browser binary, or replace repeating the protected action.

### Common failure modes

- Importing a reputation label as ground truth
- Ignoring TLS termination
- Calling a shared library fingerprint unique
- Omitting version/date

### Cleanup

No traffic generated. Keep fictional values.

## Why this matters offensively

Alternate clients and proxies may betray a browser claim at the edge. Red teams
must understand which component they changed and which server evidence remains.

## Required artifact

`artifacts/module-07/ja4-interpretation.md` with method fields, observation point,
fact/inference split, alternatives, corroboration, action, and limits.

## Pass gate

1. What does normalization enable?
2. Why is JA4 not a person identifier?
3. What can a TLS proxy replace?
4. Why retain raw fields?
5. What wording is appropriate for a local association?

## Answer key

<details><summary>Check your reasoning</summary>

1. Comparable grouping despite selected unstable/order properties.
2. Many clients share implementations/configurations and intermediaries/drift alter observations.
3. The observed client handshake downstream/upstream of termination.
4. To audit the fingerprint, explain changes, and avoid opaque labels.
5. "Consistent with the recorded versioned baseline," with alternatives.

</details>

## Next lesson

[HTTP/2](03-http2.md) adds streams, connection state, and multiplexing behavior
that request-header summaries alone miss.
