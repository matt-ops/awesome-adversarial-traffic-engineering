# Phase 3 claim alignment

## Protocol identity foundations

Executable support is limited to:

- Python/OpenSSL ClientHello byte generation in memory;
- declared ALPN configuration change with uncontrolled per-handshake variation;
- selected outer TLS record/handshake fields;
- raw byte count, SHA-256 fixture digest, and `bytes_differ` comparison; and
- one fixed-loopback plain-HTTP metadata observation.

The executable lab does not parse ALPN values from the bytes, report changed
byte offsets, compare Chrome with Playwright TLS, calculate JA4/JA4H, capture
HTTP/2 settings, exercise HTTP/3/QUIC, or measure proxy-induced transport
changes. Those remain source-led instruction/evidence plans.

## Exercise packaging

The counted six Python, ten code-review, five threat-model, and five
system-design assignments are named portfolio drills. They reuse shared lessons,
code, tests, and answer guidance. They are not represented as independent
packages containing their own README, starter, learner task, expected artifact,
tests/grading criteria, solution, and explanation.

The existing four-case synthetic code-review lab remains a guided shared lab;
Phase 3 does not create or claim four independent exercise packages.

## Reporting

The supported capability is a **report template and validated sample** at
`lab/reports/synthetic-finding.md`. Learners write/adapt their report from
evidence. No report-generation command, Make/npm target, fixture-to-Markdown
generator, or deterministic generated-output claim exists.
