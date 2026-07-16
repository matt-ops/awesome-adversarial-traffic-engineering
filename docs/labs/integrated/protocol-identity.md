# Protocol-identity lab

- Authorization boundary: in-memory TLS fixture generation and fixed loopback API
- Target: in-memory `ssl.MemoryBIO` and `http://localhost:8080`
- Objective: observe how client configuration changes protocol bytes and compare
  HTTP fields without treating a fingerprint as identity
- Protected action: none; this is a measurement lab feeding later coherence work
- Baseline/change: Python default ClientHello versus ALPN `h2,http/1.1`
- Changed variable: configured ALPN offer for the generated comparison
- Hypothesis: adding ALPN changes generated ClientHello bytes while outer record/handshake types remain valid
- Fixed variables: Python/OpenSSL runtime, process, TLS context construction, parser, and output schema
- Success: both records parse; digests/length differ; output rejects identity/JA4 claims
- Evidence: outer TLS record/handshake fields, byte count, non-JA4 digest prefix,
  HTTP version, and server-visible request fields
- Limitation: Python/OpenSSL process fixture; no packet capture and no JA4 parser
- Cleanup: helper closes its HTTP connection and opens no TLS socket
- Remediation: not applicable; coherence findings later recommend the invariant/control change
- Retest: repeat with the same runtime, then explicitly version any changed runtime comparison

The in-memory comparison needs no running service:

```powershell
python -m lab.protocol.compare clienthello
```

With the synthetic API healthy, fixed-loopback HTTP observation uses:

```powershell
python -m lab.protocol.compare http
```

Expected ClientHello output reports handshake record type `22`, handshake type
`1`, legacy versions, lengths, different digest prefixes, and an explicit warning
that the digest is not JA4. Local HTTP normally reports HTTP/1.1 through the
current development path; record the observed value rather than assuming it.
