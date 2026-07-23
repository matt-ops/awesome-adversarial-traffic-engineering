# TLS ClientHello

<!-- source-ids: rfc-8446, ja4-project, aate-local-lab -->

## Progress

- Module: 07 - Protocol identity
- Lesson: 1 of 6
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [Network events and evidence](../03-playwright/04-network-events.md)
  - [Five signal families](../05-control-recon/01-signal-families.md)
  - Basic TLS purpose; no packet-crafting experience required
- Next lesson: JA4 and JA4H

## Role outcome

Explain the ClientHello's role, identify its major offered parameters, and show
why client configuration/version changes a fingerprintable handshake.

> A network fingerprint is an analytical pivot, not proof of a specific user or browser.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | §4.1 and §4.1.2 | Defines handshake messages and ClientHello fields | Assigned only at Integrated depth; it does not define JA4. |
| PROJECT_DOCUMENTATION | [JA4 project](https://github.com/FoxIO-LLC/ja4) | overview; JA4 TLS summary | Connects field patterns to a practical fingerprint | Fingerprints change with implementations; licensing differs across JA4+ methods; fingerprints are not identity proof. |
| LAB_SPECIFIC | [Protocol identity foundations lab](../../labs/integrated/protocol-identity.md) | real loopback ClientHello observer | Supplies bounded inspectable records and parsed offered fields | Runtime availability varies; it does not calculate official JA4 or generalize to production systems. |

## Mental model

```text
client -> ClientHello: legacy fields, random, session, cipher suites,
                       compression, extensions (versions, groups, ALPN...)
server -> ServerHello: selected parameters
... encrypted handshake -> application data
```

## Required external instruction

### TLS assignment

**Direct link:** [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446)  
**Exact section, chapter, or unit:** §4.1 Cryptographic Negotiation and §4.1.2 Client Hello  
**Estimated time:** 70 minutes  
**What to focus on:** offered versus selected values, legacy compatibility fields, extensions, random/session fields, and retry behavior  
**What to skip:** cryptographic derivations, certificate processing, and all other sections  
**Expected takeaway:** annotate a ClientHello structure and explain which fields reflect implementation/configuration rather than a verified person.

## Course bridge

TLS 1.3 begins negotiation with ClientHello and ServerHello; the client offers
capabilities while the server selects acceptable parameters.[^tls]

[^tls]: RFC 8446 §§4.1 and 4.1.2.

Random, session, ordering, extension, cipher, group, signature, version, and ALPN
behavior creates observable structure. An intermediary terminating TLS produces
its own downstream handshake, so observation point matters.

## Worked example

The observer accepts a bounded loopback connection and reads one TLS record.
Python/OpenSSL supplies a real baseline; installed curl and Playwright Chromium
attempt the same observer. A client that cannot send a complete record is labeled
unsupported rather than replaced with invented data.

## Guided exercise

### Objective

Capture and annotate real local ClientHello records from available clients.

### Setup

From the repository root, read `lab/protocol/compare.py`. It binds only
`127.0.0.1`, caps connections and time, and parses declared ClientHello vectors.

### Exact actions or commands

1. Execute `python -m lab.protocol.compare clienthello`.
2. Verify record type 22 and handshake type 1 for every observed row.
3. Explain record versus ClientHello legacy versions.
4. Compare ordered ciphers, extensions, groups, signatures, ALPN, SNI, bytes, and versions.
5. Preserve unsupported rows and list prohibited conclusions.

### Expected output

The output contains a valid Python/OpenSSL ClientHello and attempted installed
curl and Playwright Chromium observations. The command creates a separate
identically configured ephemeral loopback listener for each client, keeping the
observation point and parser fixed. Each observed row includes record type,
handshake type `1`, parsed vectors, byte count, runtime version, and a digest
labeled `not JA4; not identity proof`; missing clients have explicit reasons.

### Interpretation

Differences describe actual installed client implementations at this observer.
An official fingerprint method applies specified selection, ordering, and
normalization; the local digest does not. Even a stable field set cannot
attribute a unique browser, device, account, or person.

### Common failure modes

- Calling the SHA prefix JA4
- Treating legacy version field as negotiated version
- Hiding an unsupported client or version-dependent failure
- Inferring browser identity from Python/OpenSSL bytes

### Cleanup

The observer and clients close automatically; no certificate is created in this focused mode.

## Why this matters offensively

A browser environment claim can conflict with the TLS stack seen at the edge.
Understanding the handshake reveals which layer a proxy or alternate client changes.

## Check your understanding

1. During a TLS handshake, which peer offers cipher suites and extensions in ClientHello, and which peer selects compatible parameters?
2. A ClientHello advertises `h2` and `http/1.1` through ALPN. What is ALPN negotiating?
3. Two captures from the same fixed client have different raw bytes because random and session fields changed. Why does that difference not prove a stable implementation change?
4. An edge proxy terminates the client TLS connection and opens a new TLS connection to the application. Which peer produces the downstream ClientHello?
5. The helper prints a digest prefix over a raw fixture. Why must the learner avoid calling that digest JA4?

## Answer key

<details>
<summary>Show answers</summary>

- **1. The client offers supported parameters in ClientHello, and the server selects a compatible set.** The observed offer can describe implementation and configuration behavior but does not identify one person.

- **2. ALPN negotiates the application protocol carried over TLS, such as HTTP/2 or HTTP/1.1.** The advertised list and server selection are part of the versioned handshake evidence.

- **3. Ephemeral values such as random and session fields can change on every handshake.** A stable comparison must normalize or interpret those fields before attributing the raw-byte difference to client implementation.

- **4. The terminating edge proxy acts as the TLS client for the downstream connection and produces the new ClientHello.** The application no longer observes the original client's handshake directly.

- **5. The helper computes an explicitly defined raw-fixture digest prefix, not the JA4 normalization and component format.** Using the JA4 name would overstate what the local calculation implements.

</details>

## Next lesson

[JA4 and JA4H](02-ja4-and-ja4h.md) examines a documented fingerprint method and
its correct use as a versioned pivot.
