# Protocol identity foundations lab

- Authorization boundary: fixed loopback raw TLS observation only
- Target: runtime-selected listener on `127.0.0.1`
- Objective: capture real ClientHello records from available local clients,
  parse declared fields, and preserve unsupported rows without treating a digest
  or field as identity
- Protected action: none; this measurement feeds later coherence work
- Baseline/change: compare actual Python/OpenSSL, installed curl, and Playwright Chromium capability rows
- Changed variable: actual client implementation and runtime version
- Hypothesis: available clients offer different ordered ClientHello fields at the same local observer
- Fixed variables: loopback observer, field parser, connection and time caps, and output schema
- Success: Python/OpenSSL parses; other clients parse or report an explicit unsupported reason; every digest rejects identity/JA4 claims
- Evidence: record and handshake versions, ciphers, extensions, groups,
  signatures, ALPN, SNI presence, byte count, runtime version, and non-JA4 digest
- Limitation: no packet capture, official JA4 calculation, HTTP/3, QUIC, real proxy chain, or commercial control
- Cleanup: observers and clients close on success or failure
- Remediation: not applicable; coherence findings later recommend the invariant/control change
- Retest: repeat at the same observer after a declared runtime version change

The raw observer starts and stops inside this command:

```powershell
python -m lab.protocol.compare clienthello
```

Expected output reports actual client/runtime versions, handshake record type
`22`, handshake type `1`, parsed vectors, byte counts, unsupported rows, and an
explicit warning that each digest is not JA4 and not identity proof.

## Executable boundary

This focused command supports real raw ClientHello observation only. The
[multi-client comparison](multi-client-protocol-comparison.md) adds real local
HTTP/2 settings and reuse. Official JA4/JA4H parity, HTTP/3/QUIC, proxy-induced
transport changes, and client identity remain unsupported.
