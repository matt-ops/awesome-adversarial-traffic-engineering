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
- Hard caps: four connections per observer, eight HTTP/2 streams, 45-second whole command
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

The Playwright client prevalidates navigation URLs and routes every page request.
Only `127.0.0.1`, `localhost`, and `::1` are permitted; a non-loopback page
request is aborted, returned to the Python parent, and fails the comparison.
Browser flags reduce background networking. The output does not claim packet-
level capture: it reports loopback-only configured targets, observed page-
request violations, proxy inheritance, and `packet-level external traffic: not
measured`.

## Expected table

| Client | ClientHello | HTTP/2 | Reuse | Honest missing result |
|---|---|---|---|---|
| Python/OpenSSL | parsed ciphers, extensions, groups, signatures, ALPN, SNI, bytes | not assigned | not assigned | HTTP/2 settings missing |
| installed curl | parsed if its TLS backend sends a complete hello | only when `Features:` includes HTTP2 | two URLs on one connection when supported | otherwise `unsupported` |
| Playwright Chromium | parsed real browser hello | negotiated `h2` and remote settings | streams `1` and `3` on one connection | HTTP/2 header order missing |
| Node HTTP/2 | not captured by Observer A | negotiated `h2` and remote settings | streams `1` and `3` on one connection | ClientHello fields missing |
| manual Chrome/Chromium | optional | optional | optional | `unsupported` until actually launched |

The digest beside each parsed ClientHello is labeled `not JA4; not identity proof`.
The exact field values and versions can change when Python, OpenSSL,
curl, Chromium, Playwright, or Node changes.

## Focused checks

```powershell
python -m lab.protocol.compare clienthello
python -m lab.protocol.compare http2
python -m unittest lab.tests.test_protocol -v
```

Tests cover generated ClientHello parsing, malformed and truncated records,
connection caps, loopback rejection, certificate cleanup, Python/OpenSSL
capture, the local HTTP/2 observer, unsupported-client rows, non-JA4 labels,
global-deadline exit behavior, non-loopback page-request failure, malformed
ready output, client exceptions, output parse failure, terminate/kill
escalation, and temporary-key cleanup.

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

Successful and failed paths close children and remove temporary certificate
material. No packet capture, administrator privilege, production JA4, HTTP/3,
QUIC, external fingerprint site, real proxy chain, or commercial control is
used. An empty page-request violation list is scoped Playwright evidence, not
proof that the browser process made zero packet-level external connections.
