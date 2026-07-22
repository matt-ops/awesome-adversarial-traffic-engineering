# HTTP/3 and QUIC

<!-- source-ids: rfc-9114, rfc-9000, aate-adversarial-control-loop -->

## Progress

- Module: 07 - Protocol identity
- Lesson: 5 of 5
- Depth: Deep
- Estimated time: 3 hours
- Prerequisites:
  - [Proxies and connection reuse](04-proxies-and-connection-reuse.md)
  - HTTP/2 stream model
- Next lesson: DDoS resource model

## Role outcome

Explain HTTP/3 mapping to QUIC streams and why connection identifiers, migration,
and encrypted transport change—but do not eliminate—identity questions.

> A network fingerprint is an analytical pivot, not proof of a specific user or browser.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) | §2 and §3 | Defines HTTP/3 mapping and connection setup | Deep assignment only; does not teach QUIC transport in full. |
| STANDARD | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000) | §2 and §5 | Defines QUIC streams and connection IDs | Deep assignment only; packet-level experimentation remains isolated and bounded. |
| COURSE_SYNTHESIS | [AATE loop](../../methodology/adversarial-control-loop.md) | cross-layer implications and limits | Connects standards to offensive hypotheses | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Layer | Unit | Identity caution |
|---|---|---|
| HTTP/3 | request streams plus control/QPACK streams | request behavior is not IP identity |
| QUIC | encrypted packets, streams, connection IDs | CID supports routing/migration, not person identity |
| UDP path | address/port tuples can change | migration complicates IP-only grouping |
| application | session/account/workflow | still requires server binding/proof |

## Required external instruction

### HTTP/3 assignment

**Direct link:** [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114)  
**Exact section, chapter, or unit:** Sections 2 and 3  
**Estimated time:** 45 minutes  
**What to focus on:** HTTP semantics over QUIC, request streams, control streams, and connection setup  
**What to skip:** QPACK internals, error-code catalogs, and the remainder of the RFC  
**Expected takeaway:** map one HTTP request and response to their HTTP/3 stream without treating that stream as a user identity.

### QUIC identity assignment

**Direct link:** [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000)  
**Exact section, chapter, or unit:** Sections 2 and 5  
**Estimated time:** 45 minutes  
**What to focus on:** stream types, connection IDs, and the routing and migration purpose of connection IDs  
**What to skip:** packet protection, congestion control, recovery, and the remainder of the RFC  
**Expected takeaway:** diagram request, stream, connection, connection-ID, and address units without equating any of them to a person.

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

### Exact actions or commands

1. Map HTTP/2 connection/streams against HTTP/3/QUIC.
2. Add address tuple, connection ID, TLS, application session, and workflow.
3. Model one legitimate migration and one adversarial rotation hypothesis.
4. State evidence needed from an approved HTTP/3 provider/test environment.
5. List false-positive and intermediary alternatives.

### Expected output

A standards-grounded diagram distinguishes QUIC connections/streams from HTTP/3
control and request streams, then names handshake, ALPN, connection-ID, stream,
header, and intermediary observations for a future local experiment. Every
result field is marked `planned`; no packet or fingerprint evidence is invented.

### Interpretation

The plan identifies which layer could create a browser/protocol contradiction
and what an observation point can actually see. Because the repository does not
ship a validated HTTP/3 target, exact RFC instruction and an executable evidence
contract are more honest than claiming a local result that was never measured.

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

## Check your understanding

1. HTTP/3 maps requests and responses onto which QUIC transport objects?
2. A QUIC connection continues after a client's network address changes. Why do QUIC connection IDs help that association survive migration?
3. Why must a control avoid treating a QUIC connection ID as a permanent person or account identifier?
4. Which application identity and authorization state still exists above QUIC even when transport connection behavior changes?
5. The lesson creates a future authorized capture plan but runs no local HTTP/3 capture. What evidence status should the learner report?

## Answer key

<details>
<summary>Show answers</summary>

- **1. HTTP/3 carries request and response data on QUIC streams, with separate control-related streams for protocol state.** QUIC replaces the TCP transport used by earlier HTTP versions.

- **2. Connection IDs let endpoints and network devices associate packets with the same QUIC connection even when address and port information changes.** Their lifecycle also includes privacy and rotation considerations.

- **3. A connection ID identifies transport state for a limited lifecycle, not a human or application account.** Rotation, migration, multiple connections, and shared systems prevent a permanent one-to-one identity claim.

- **4. Application sessions, accounts, permissions, workflow prerequisites, and protected-action decisions remain above QUIC.** Transport observations can inform analysis but cannot replace server-side authentication and authorization.

- **5. Report that no HTTP/3 execution evidence was collected.** The lesson provides standards-based instruction and a bounded future plan, not a completed local capture or production claim.

</details>

## Next lesson

[Open Module 08](../08-ddos-resilience/index.md) to model how traffic dimensions
consume resources and how bounded tests prove service effects.
