# Local Multi-client Protocol Comparison

<!-- source-ids: rfc-8446, rfc-9113, playwright-network, curl-http2-capabilities, node-http2, ja4-project, aate-local-lab, aate-adversarial-control-loop -->
<!-- source-ledger-consistency: strict -->

## Progress

- Module: 07 - Protocol identity
- Lesson: 5 of 6
- Depth: Deep
- Estimated time: 4 hours
- Prerequisites:
  - [Proxies and connection reuse](04-proxies-and-connection-reuse.md)
  - TLS ClientHello fields, HTTP/2 streams, and observation-point limits
- Next lesson: HTTP/3 and QUIC

## Role outcome

Capture real ClientHello fields from multiple installed local clients, compare
real local HTTP/2 settings and connection reuse, and report every unsupported or
unexposed dimension without turning a fingerprint into identity proof.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| STANDARD | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | 4.1.2 ClientHello and 4.2 extensions | Defines parsed TLS structure, versions, cipher suites, and extensions | Does not define JA4 or associate fields with a person. |
| STANDARD | [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) | 3.4 preface; 5 streams; 6.5 SETTINGS; 9.1 connections | Defines connection settings, streams, and reuse semantics | Does not define a universal client fingerprint. |
| OFFICIAL_DOCUMENTATION | [Playwright Network](https://playwright.dev/docs/network) | introduction and network events | Supports browser request execution and observable request boundaries | Playwright does not expose every TLS or HTTP/2 wire field to page code. |
| OFFICIAL_DOCUMENTATION | [curl manual](https://curl.se/docs/manpage.html) | `--http2`, `--version`, `--noproxy`, timeouts | Supports runtime capability checks and bounded proxy-free execution | The installed build can omit HTTP/2 or fail before a TLS handshake. |
| OFFICIAL_DOCUMENTATION | [Node.js HTTP/2](https://nodejs.org/api/http2.html) | secure server, session `remoteSettings`, ALPN, and stream event | Supplies the local HTTP/2 observer's genuinely exposed fields | Decoded header names are available; wire-level header ordering is not claimed. |
| PROJECT_DOCUMENTATION | [JA4 project](https://github.com/FoxIO-LLC/ja4) | JA4 TLS method, technical details, ordering Q&A, and licensing | Explains input concepts and current licensing boundary | This lab does not implement official JA4, GREASE normalization, sorting rules, or test vectors. |
| LAB_SPECIFIC | [Multi-client protocol lab](../../labs/integrated/multi-client-protocol-comparison.md) | caps, clients, output table, certificate lifecycle, and tests | Supplies the executable fixed-loopback comparison | Runtime-specific observations change with installed versions. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | observations, alternatives, protected effect, limitations, retest | Keeps protocol fields as analytical pivots | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

```text
local client
  -> Observer A reads one raw TLS ClientHello record, then closes
  -> Observer B terminates ephemeral local TLS and exposes HTTP/2 session data

ClientHello fields -> implementation comparison pivot
HTTP/2 settings    -> one connection's peer parameters
session/account    -> separate application identity and authorization state
```

Observer A records only parsed record/ClientHello versions, cipher-suite IDs in
order, extension IDs in order, supported groups, signature algorithms, ALPN
offers, SNI presence, and total bytes. Its digest is deterministic over those
fields and is labeled `not JA4; not identity proof`.

Observer B records negotiated ALPN, peer settings exposed by Node, stream count,
two-request reuse on one connection, and the set of decoded request-header names.
It explicitly does not claim HTTP/2 header ordering.

## Required external instruction

### TLS structure assignment

**Direct link:** [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446)
**Exact section, chapter, or unit:** 4.1.2 ClientHello and 4.2 Extensions
**What to focus on:** record versus handshake legacy versions, cipher-suite vector, and typed extension vector
**What to skip:** the complete TLS state machine, certificate validation internals, and cryptographic proofs
**Estimated time:** 35 minutes
**Expected takeaway:** identify each field the raw observer can parse without claiming that one field identifies a browser or user.

### HTTP/2 settings and reuse assignment

**Direct link:** [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113)
**Exact section, chapter, or unit:** 3.4 Connection Preface, 5 Streams, 6.5 SETTINGS, and 9.1 Connection Management
**What to focus on:** settings belong to an endpoint on a connection, request exchanges use streams, and connections can persist
**What to skip:** complete frame error tables, prioritization history, and server push details
**Estimated time:** 40 minutes
**Expected takeaway:** explain why two streams can prove connection reuse but cannot establish an account identity.

### Client capability assignment

**Direct link:** [curl manual](https://curl.se/docs/manpage.html)
**Exact section, chapter, or unit:** `--http2`, `--version`, `--noproxy`, `--connect-timeout`, and `--max-time`
**What to focus on:** build-time HTTP/2 reporting, explicit proxy bypass, and bounded failure behavior
**What to skip:** unrelated transfer protocols and public example destinations
**Estimated time:** 20 minutes
**Expected takeaway:** report `unsupported` when the local curl feature list omits HTTP2 instead of accepting an HTTP/1.1 fallback.

### Runtime and JA4 boundary assignment

**Direct link:** [Node.js HTTP/2 API](https://nodejs.org/api/http2.html)
**Exact section, chapter, or unit:** secure-server example, `Http2Session.remoteSettings`, `alpnProtocol`, and the stream event
**What to focus on:** exactly which session, setting, and stream data the observer runtime exposes
**What to skip:** compatibility APIs and cleartext HTTP/2
**Estimated time:** 25 minutes
**Expected takeaway:** distinguish a genuine runtime observation from a field the course would need another capture layer to support.

## Course bridge

Earlier lessons described TLS, JA4 input concepts, HTTP/2, and intermediary
effects. This exercise replaces a conceptual-only stop with real local
measurements. An intermediary could still replace the downstream ClientHello,
and one client can change its fields across versions, so the result stays tied
to runtime, observation point, and date.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** A client tag is a grouping label, not verified identity.
    A fingerprint is an analytical pivot, not identity proof. Bind protected
    actions to server-side session, principal, workflow, and authorization state.

## Worked example

In the dated verified development run on 2026-07-22, Python 3.12.13/OpenSSL
3.5.5 offered no ALPN in Observer A, while Playwright Chromium 149.0.7827.55
offered `h2,http/1.1`. Observer B negotiated `h2` for Chromium and Node
v24.12.0/OpenSSL 3.5.4. Chromium sent `initialWindowSize=6291456` and
`headerTableSize=65536`; Node sent `65535` and `4096`. Both used streams `1` and
`3` on one connection.

The installed curl 8.21.0/Windows Schannel client produced a raw ClientHello for
Observer A: 429 bytes, ALPN `http/1.1`, and no SNI. Its build did not advertise
HTTP2 support, so its Observer B result was `unsupported`. These are dated
workstation observations, not universal expected values; each learner's command
output is the source of truth.

## Guided exercise

### Objective

Run both fixed-loopback observers, compare installed clients, and separate
observed fields from unsupported capabilities and identity claims.

### Setup

- Required working directory: repository root
- Preflight: Python 3.12, project dependencies, Node 22+, curl, and repository-pinned Playwright Chromium
- Exact targets: ephemeral listeners bound only to `127.0.0.1`
- Whole-command wall budget: 45 seconds, enforced from command start
- Per-observer caps: four connections per observer; 4-second raw-connection window; 30-second HTTP/2 observer window
- HTTP/2 stream cap: eight streams at Observer B
- Per-client timeout: 15 seconds, always reduced to the remaining whole-command budget
- Proxy behavior: proxy environment is removed and clients receive explicit loopback bypass
- Browser-page enforcement: every navigation target is prevalidated; Playwright aborts and reports non-loopback page requests
- Certificate behavior: an ephemeral key and certificate are generated in the OS temporary directory

### Exact actions or commands

PowerShell:

```powershell
python --version
node --version
curl.exe --version
npm run typecheck
python -m lab.protocol.compare automated
```

Bash or zsh:

```bash
python3 --version
node --version
curl --version
npm run typecheck
python3 -m lab.protocol.compare automated
```

The command starts Observer A for Python/OpenSSL, installed curl, and Playwright
Chromium; starts Observer B; runs Node HTTP/2 and Playwright Chromium; runs
`curl --http2` only when `curl --version` reports HTTP2; prints a comparison
table; stops children; and removes temporary key material.

### Expected output

The first table contains client, runtime version, parsed ClientHello fields,
extension order, ALPN offers, negotiated protocol, HTTP/2 remote settings, reuse,
missing fields, and limitations. Python/OpenSSL and Playwright should yield real
ClientHello fields when installed. Node and Playwright should negotiate `h2`
and use two streams on one connection. Missing browser or curl capabilities
must print `unsupported` without turning the entire comparison into a false pass.

The safety record says configured targets are loopback only, lists the observed
non-loopback page-request violations (normally `[]`), states that proxy
environment inheritance is false, and labels packet-level external traffic
`not measured`. Browser flags reduce background networking, but they are not a
packet-capture guarantee. Any reported non-loopback page request makes the
command fail.

### Interpretation

Differences are evidence about the exact runtime and observation point. They are
not stable browser identities: versions change, GREASE values appear, a proxy
can originate another ClientHello, and HTTP/2 settings describe a connection.
Compare genuinely parsed values and preserve missing fields instead of filling
them from documentation or another tool.

### Common failure modes

- Calling the local digest JA4 without the current algorithm, license review, GREASE rules, sorting rules, and passing vectors
- Allowing an inherited proxy or redirect to change the destination
- Treating decoded HTTP/2 header-name sets as captured wire ordering
- Treating a client tag, connection, or settings vector as a verified account
- Describing the four-connection cap as command-wide instead of per observer
- Reporting an empty Playwright violation list as packet-level proof of zero external connections

### Troubleshooting

- **curl is missing:** install curl for the operating system and rerun the
  explicit `curl.exe --version` or `curl --version` preflight.
- **curl lacks HTTP2:** keep its ClientHello result when observed, but record its
  HTTP/2 row as `unsupported`; do not infer support from another machine.
- **Playwright Chromium is missing:** install the repository-pinned browser and
  its platform dependencies, then rerun the command.
- **Node or `npx` is missing:** install Node 22+ with npm; Observer B cannot start
  without it.
- **Timeout:** read the timeout error, confirm the 45/30/15/4-second layers, and
  investigate the delayed local dependency rather than increasing the global cap.
- **Unsupported client:** retain its runtime and reason; do not substitute a
  different implementation's fields.
- **Cleanup failure:** stop any remaining `http2_observer.ts` process, remove the
  named `aate-protocol-` temporary directory, and treat the run as failed.

### Cleanup

Every handled failure path closes observers, browser contexts, sessions, child
standard streams, and listeners. The parent requests graceful child shutdown,
then terminates and kills within the remaining deadline when necessary. The
temporary certificate directory is removed even for malformed ready output,
client exceptions, output parse failures, or the global timeout. Forced
operating-system termination can bypass application cleanup; follow the cleanup-
failure guidance and never place certificate, key, or telemetry in the repository.

## Why this matters offensively

Protocol coherence can expose a claimed browser whose transport behavior comes
from another runtime, but it can also create false confidence. Real measurement,
version labels, and observation-point limits keep that hypothesis testable.

## Check your understanding

1. Which ClientHello fields does Observer A genuinely parse, and what two claims are prohibited for its digest?
2. Why do two HTTP/2 streams on one connection establish reuse but not an account identity?
3. What result must the command print when the installed curl build lacks HTTP2 support?
4. How can an intermediary make the origin-visible ClientHello differ from the downstream browser's ClientHello?
5. Which protocol capabilities remain explicitly unsupported after this exercise?

## Answer key

<details>
<summary>Show answers</summary>

- **1. It parses record and ClientHello legacy versions, cipher-suite and extension order, supported groups, signature algorithms, ALPN, SNI presence, and bytes.** The digest is not JA4 and is not identity proof.

- **2. Streams `1` and `3` on one session show that the client reused that transport connection for two request exchanges.** HTTP/2 settings and connection lifetime do not authenticate a person, account, or application principal.

- **3. Print `unsupported` with the observed curl runtime and the missing HTTP2 feature.** Silent HTTP/1.1 fallback would fabricate an HTTP/2 comparison and hide a real local capability boundary.

- **4. A forward or terminating proxy can create its own upstream TLS connection and ClientHello.** The origin then observes the intermediary's implementation while the browser-to-proxy handshake exists at another observation point.

- **5. Production JA4 parity, a universal browser fingerprint, HTTP/3 or QUIC capture, a real proxy-chain comparison, commercial-control conclusions, and HTTP/2 header ordering remain unsupported.** A manual Chrome comparison is optional and must be labeled absent unless actually executed.

</details>

## Next lesson

[HTTP/3 and QUIC](05-http3-quic.md) explains the transport concepts that remain
source-led because this lab deliberately does not capture QUIC.
