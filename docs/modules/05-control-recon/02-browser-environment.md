# Browser-environment observations

<!-- source-ids: fpscanner-project, rebrowser-bot-detector, aate-local-lab -->

## Progress

- Module: 05 - Control reconnaissance
- Lesson: 2 of 6
- Depth: Foundation
- Estimated time: 2 hours
- Prerequisites:
  - [Five signal families](01-signal-families.md)
  - Chrome DevTools Console and Module 02 context model
- Next lesson: Cross-context consistency

## Role outcome

Collect a versioned manual browser-environment baseline and explain the source,
meaning, attacker influence, and limit of each observation.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PROJECT_DOCUMENTATION | [FPScanner](https://github.com/antoinevastel/fpscanner) | Features; What It Detects | Provides categories for a concrete control target | Observations are valid only for the recorded code and browser versions. |
| PROJECT_DOCUMENTATION | [Rebrowser detector](https://github.com/rebrowser/rebrowser-bot-detector) | navigatorWebdriver; viewport; main-world tests | Provides version-sensitive automation examples | Version-sensitive artifact catalog with strong project claims; not a model of every commercial control. |
| LAB_SPECIFIC | [Control-recon lab](../../labs/integrated/control-recon.md) | Manual baseline target | Supplies the local collection page | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

| Observation | Where read | What it reflects | Limit |
|---|---|---|---|
| UA/platform/language | Navigator in a realm | browser/OS/locale claims | changeable and compatibility-shaped |
| timezone | Intl API | configured time-zone behavior | travel/VM/privacy tools vary |
| viewport/screen | Window/Screen | page viewport and reported display | headless, zoom, RDP, mobile vary |
| webdriver | Navigator | standardized automation exposure | one property, not identity |
| graphics/API output | Web APIs | stack/device/software interaction | privacy defenses and drift affect it |

## Required external instruction

### FPScanner browser-surface assignment

**Direct link:** [FPScanner](https://github.com/antoinevastel/fpscanner)  
**Exact section, chapter, or unit:** Features and What It Detects  
**Estimated time:** 20 minutes  
**What to focus on:** each browser-exposed surface, where it is collected, and the project's stated constraint  
**What to skip:** installation and bypass code  
**Expected takeaway:** write a collection-location and limitation row for each selected browser observation.

### Rebrowser environment-test assignment

**Direct link:** [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector)  
**Exact section, chapter, or unit:** navigatorWebdriver; viewport; mainWorldExecution  
**Estimated time:** 20 minutes  
**What to focus on:** the exact property or execution behavior, context, and version sensitivity of each test  
**What to skip:** bypass packages and tests outside the three assigned entries  
**Expected takeaway:** explain why the three observations can support a hypothesis but cannot uniquely identify automation or a person.

## Course bridge

Browser properties are outputs of standards, implementation, configuration,
environment, and sometimes privacy/accessibility software. The collection point
matters: a main-world value may differ from an isolated world, frame, or worker.

!!! info "Version-sensitive observation"
    Record browser version, platform, launch mode, locale, timezone, viewport,
    extensions/privacy settings, and collection time. A value without environment
    metadata is not a reproducible baseline.

## Worked example

```javascript
({
  userAgent: navigator.userAgent,
  platform: navigator.platform,
  language: navigator.language,
  webdriver: navigator.webdriver,
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  viewport: [innerWidth, innerHeight],
  screen: [screen.width, screen.height]
})
```

This reads one top-page realm. It performs no evasion and says nothing about TLS,
session history, behavior, or server enforcement.

## Guided exercise

### Objective

Capture the normal manual population before any automation trial.

### Setup

Open `http://localhost:8080/control-lab` manually in Chrome after local health
passes. Open DevTools Console and record the exact browser version.

### Exact actions or commands

1. Evaluate the worked object and save its JSON-compatible values.
2. Record page URL, time, version, extensions/privacy mode, and whether DevTools
   was open.
3. Inspect the same-origin frame with the Console context picker.
4. Record what cannot be collected manually from the worker with this snippet.
5. Add HTTP request headers from Network and keep them separate from JS values.

### Expected output

A top-page and frame record plus request headers, with no control decision yet.
Exact values are environment-dependent; the schema and provenance are fixed.

### Interpretation

This is the legitimate reference population. Differences in later automation
are observations to explain, not automatic detection reasons.

### Common failure modes

- Copying an expected fingerprint instead of recording the workstation
- Mixing request headers into JavaScript properties
- Calling a missing worker value proof of equality
- Omitting browser version or privacy settings

### Cleanup

Close DevTools and retain only public-safe local values.

## Why this matters offensively

An operator cannot claim automation differs from normal without a normal
baseline. Precise provenance also exposes when a later result is browser drift,
configuration, or collection error instead of a control response.

## Check your understanding

1. The worked Console object records a timezone. Which browser API expression supplies the reported timezone value?
2. Why does the exercise store HTTP request headers separately from values read through `navigator`, `screen`, and `Intl`?
3. The manual browser reports `navigator.webdriver` as false. Why does that single value not prove a human is using the browser?
4. Why should the baseline record privacy, extension, accessibility, and DevTools conditions along with browser version?
5. The learner collects top-page, frame, and request observations without changing a signal or attempting a protected action. Why is the record a baseline rather than a bypass?

## Answer key

<details>
<summary>Show answers</summary>

- **1. `Intl.DateTimeFormat().resolvedOptions().timeZone` supplies the timezone value.** The record should include the collection context because browser configuration can affect what the API reports.

- **2. Headers and JavaScript values arise at different layers and collection points, so they may vary or contradict each other.** Keeping provenance separate prevents the matrix from treating unlike observations as one fact.

- **3. The value is one browser-exposed property that software can influence.** A human, automation framework, or modified environment may report the same value, so identity and intent remain unproved.

- **4. Those legitimate conditions can change, reduce, or expose observable values.** Recording them makes the baseline reproducible and helps distinguish control drift from normal user variation and accessibility needs.

- **5. No treatment or control response is being compared, and no protected server action is attempted.** The observations define the normal reference population for later controlled experiments.

</details>

## Next lesson

[Cross-context consistency](03-cross-context-consistency.md) compares page,
frame, and worker observations rather than assuming the top page is complete.
