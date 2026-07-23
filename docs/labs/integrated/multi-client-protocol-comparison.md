# Local multi-client ClientHello and HTTP/2 comparison lab

- Authorization boundary: fixed loopback only
- Required working directory: repository root
- Target: runtime-selected ports on `127.0.0.1`
- Objective: compare real available local ClientHello and HTTP/2 observations at fixed loopback observers
- Protected action: none; two HTTP/2 requests prove stream reuse, not authorization or identity
- Baseline: Python/OpenSSL raw ClientHello and Node HTTP/2 session at recorded runtime versions
- Hypothesis: installed implementations expose different ordered TLS fields and HTTP/2 peer settings
- Changed variable: actual client implementation and runtime version
- Fixed variables: observers, loopback target, parser, paths, caps, output schema, and proxy bypass
- Success: real supported rows are observed, missing capabilities are explicit, reuse uses streams `1` and `3`, and cleanup passes
- Evidence: runtime versions, ClientHello fields, ALPN, settings, streams, header-name sets, and unsupported reasons
- Limitation: observer-specific values are not universal fingerprints, production JA4, or identity proof
- Remediation: controls should bind authorization to server-side session and action invariants, not one protocol digest
- Retest: repeat at the same observer after one declared client/runtime change and compare the same fields
- Observer A: reads one bounded TLS ClientHello record and closes
- Observer B: ephemeral-certificate local TLS HTTP/2 server
- Clients: Python/OpenSSL, installed curl, Playwright Chromium, and Node HTTP/2
- Optional client: manually launched local Chrome or Chromium, not automated
- Hard caps: one connection per raw client observer, four HTTP/2 connections, eight HTTP/2 streams, 45-second whole command
- Smaller bounds: 4-second raw observer, 30-second HTTP/2 observer, and 15-second per client
- Output: standard output only; saving diagnostics is optional and ignored

## Preflight

PowerShell:

```powershell
python --version
node --version
curl.exe --version
npm run typecheck
```

Bash or zsh:

```bash
python3 --version
node --version
curl --version
npm run typecheck
```

If the installed curl version output lacks `HTTP2` on its `Features:` line, its
HTTP/2 row must be `unsupported`. That does not erase an independently observed
raw ClientHello.

## Fully automated command

PowerShell:

```powershell
python -m lab.protocol.compare automated
```

Bash or zsh:

```bash
python3 -m lab.protocol.compare automated
```

The Python parent removes proxy variables, validates every target, starts only
loopback listeners, generates the self-signed certificate and key under the OS
temporary directory, invokes supported clients, stops the Node observer through
its private standard input, and deletes the temporary directory. The 45-second
deadline begins at command start; each socket, queue, client, child process, and
shutdown wait receives only the remaining budget.

The Playwright client installs routing before navigation and allows only the
exact loopback origin and assigned paths. Every other HTTP(S) request is aborted.
Attempted external URLs are reduced to credential-free, query-free origins; the
Python parent aggregates `external_request_attempt_count`,
`blocked_external_origins`, and `allowed_loopback_request_count` and fails on
any external attempt. Browser flags reduce background networking. The output
does not claim packet-level capture: it reports proxy inheritance and
`packet-level external traffic: not measured`.

## Expected table

| Client | ClientHello | HTTP/2 | Reuse | Honest missing result |
|---|---|---|---|---|
| Python/OpenSSL | parsed handshake type, ciphers, extensions, groups, signatures, ALPN, SNI, bytes | not assigned | not assigned | HTTP/2 settings missing |
| installed curl | parsed if its TLS backend sends a complete hello | only when `Features:` includes HTTP2 | two URLs on one connection when supported | otherwise `unsupported` |
| Playwright Chromium | parsed real browser hello | negotiated `h2` and remote settings | streams `1` and `3` on one connection | HTTP/2 header order missing |
| Node HTTP/2 | not captured by Observer A | negotiated `h2` and remote settings | streams `1` and `3` on one connection | ClientHello fields missing |
| manual Chrome/Chromium | optional | optional | optional | `unsupported` until actually launched |

The digest beside each parsed ClientHello is labeled `not JA4; not identity proof`.
The exact field values and versions can change when Python, OpenSSL,
curl, Chromium, Playwright, or Node changes.

On the reviewed Windows workstation on 2026-07-23, curl 8.21.0 with Schannel
produced a 429-byte ClientHello with handshake type `1`, ALPN `http/1.1`, and no
SNI. That installed build did not advertise HTTP2, so its HTTP/2 result remained
explicitly `unsupported`. The 9.469-second automated run measured zero external
HTTP(S) request attempts, no blocked external origins, and three allowed
loopback requests across the two Playwright modes. Other curl builds and TLS
backends may differ.

## Focused checks

PowerShell:

```powershell
python -m lab.protocol.compare clienthello
python -m lab.protocol.compare http2
python -m unittest lab.tests.test_protocol -v
```

Bash or zsh:

```bash
python3 -m lab.protocol.compare clienthello
python3 -m lab.protocol.compare http2
python3 -m unittest lab.tests.test_protocol -v
```

Tests cover generated ClientHello parsing including handshake type, malformed
and truncated records, raw connection caps, loopback rejection, POSIX private-
key mode, certificate cleanup, Python/OpenSSL capture, the local HTTP/2
observer, parent failure on an HTTP/2 cap result, unsupported-client rows, non-
JA4 labels, whole-command deadline exit and child cleanup, exact browser-route
classification, external-request failure, final measured safety aggregation,
malformed ready output, client exceptions, output parse failure, and
terminate/kill escalation.

## Failure guidance

- `ClientHello observer timed out`: the client did not connect; record it as unsupported.
- `truncated TLS record`: the local TLS backend connected but sent no complete record.
- curl missing: install it, rerun the shell-specific version command, and do not infer the executable name.
- curl present without HTTP2: retain any raw ClientHello, but mark only its HTTP/2 row `unsupported`.
- Playwright browser missing: install the repository-pinned Chromium and platform dependencies, then repeat.
- Node or `npx` missing: install Node 22+ with npm before starting Observer B.
- HTTP/2 observer did not become ready: inspect Node/typecheck output; do not substitute HTTP/1.1.
- `Protocol comparison timeout`: a dependency exhausted the 45-second global budget; the command exits nonzero.
- Unsupported client: retain the runtime and reason rather than copying another client's values.
- `cap-exceeded`: stop and inspect the client; the command must exit nonzero.
- Cleanup failure: stop the named local observer, remove its `aate-protocol-` temporary directory, and fail the run.

## Cleanup and limitations

Successful and tested handled failure paths close children and remove temporary
certificate material. The private key is explicitly mode `0600` on POSIX. No
packet capture, administrator privilege, production JA4, HTTP/3,
QUIC, external fingerprint site, real proxy chain, or commercial control is
used. A measured zero external-request attempt count is scoped Playwright
routing evidence, not proof that the browser process made zero packet-level
external connections.
