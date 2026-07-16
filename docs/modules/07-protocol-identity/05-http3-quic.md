# HTTP/3 and QUIC

<!-- source-ids: rfc-9114, rfc-9000, aate-adversarial-control-loop -->

> **Progress**  
> Module: 07 - Protocol identity  
> Lesson: 5 of 5  
> Depth: Deep  
> Estimated time: 3 hours  
> Prerequisites: Proxies and connection reuse  
> Artifact: `artifacts/module-07/http3-quic.md`  
> Next: DDoS resource model

## Role outcome

Explain HTTP/3 mapping to QUIC streams and why connection identifiers, migration,
and encrypted transport change—but do not eliminate—identity questions.

## Prerequisites

- [Proxies and connection reuse](04-proxies-and-connection-reuse.md)
- HTTP/2 stream model

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| STANDARD | [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) | §2 and §3 | Defines HTTP/3 mapping and connection setup |
| STANDARD | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000) | §2 and §5 | Defines QUIC streams and connection IDs |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | cross-layer implications and limits | Connects standards to offensive hypotheses |

## Mental model

| Layer | Unit | Identity caution |
|---|---|---|
| HTTP/3 | request streams plus control/QPACK streams | request behavior is not IP identity |
| QUIC | encrypted packets, streams, connection IDs | CID supports routing/migration, not person identity |
| UDP path | address/port tuples can change | migration complicates IP-only grouping |
| application | session/account/workflow | still requires server binding/proof |

## Required external instruction

### HTTP/3 and QUIC assignment

**Direct link:** [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) and [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000)  
**Exact assignment:** RFC 9114 §§2-3; RFC 9000 §§2 and 5  
**Estimated time:** 90 minutes  
**Focus on:** HTTP/3 streams, QUIC connection setup, stream types, connection IDs, migration/routing purpose, and scope  
**Skip:** packet protection, congestion control, QPACK internals, recovery, and full RFC reading  
**Expected takeaway:** diagram request/session/connection/address units without equating a CID or address to a user.

## Course bridge

HTTP/3 maps HTTP semantics onto QUIC streams.[^h3] QUIC connection IDs let
endpoints and intermediaries associate packets with a connection despite address
changes, subject to protocol rules.[^quic]

[^h3]: RFC 9114 §§2-3.
[^quic]: RFC 9000 §5.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Treat transport continuity, network location, browser
    claim, session, and adversary workflow as separate correlated dimensions.

## Worked example

A mobile client's network address changes while QUIC continues through connection
migration. An IP-only control might split legitimate continuity; a CID-only claim
still does not authorize an account action. Server session/workflow proof remains.

## Guided exercise

### Objective

Build a protocol-layer comparison and a provider-lab plan without sending QUIC traffic.

### Setup

Use the RFC assignments and your HTTP/2 map. The local lab does not claim HTTP/3 support.

### Actions

1. Map HTTP/2 connection/streams against HTTP/3/QUIC.
2. Add address tuple, connection ID, TLS, application session, and workflow.
3. Model one legitimate migration and one adversarial rotation hypothesis.
4. State evidence needed from an approved HTTP/3 provider/test environment.
5. List false-positive and intermediary alternatives.

### Expected output

A standards-grounded diagram and future authorized experiment plan, clearly
labeled as unexecuted rather than fabricated evidence.

### Interpretation

Deep protocol understanding shapes better hypotheses; unsupported local tooling
is replaced by exact RFC instruction and an evidence plan.

### Common failure modes

- Calling QUIC connection ID a stable device ID
- Treating UDP as sessionless application behavior
- Inventing HTTP/3 support in the local stack
- Requiring entire RFCs

### Cleanup

No traffic or service changes.

## Why this matters offensively

Modern browser traffic may use transport continuity and multiplexing that naive
IP/request controls misunderstand. A red teamer must separate those units before testing.

## Required artifact

`artifacts/module-07/http3-quic.md` with layer comparison, migration scenarios,
control hypotheses, evidence plan, false positives, and limits.

## Pass gate

1. What carries HTTP/3 requests?
2. Why do QUIC connection IDs exist?
3. Are CIDs person identifiers?
4. What state remains above QUIC?
5. What is the local HTTP/3 evidence status?

## Answer key

<details><summary>Check your reasoning</summary>

1. QUIC streams, with separate control-related streams.
2. To associate/rout packets for a connection, including address changes.
3. No; they are transport identifiers with defined lifecycle/privacy behavior.
4. Application sessions, accounts, authorization, and workflows.
5. None executed; the lesson supplies standards instruction and a future authorized plan.

</details>

## Next lesson

[Open Module 08](../08-ddos-resilience/index.md) to model how traffic dimensions
consume resources and how bounded tests prove service effects.
