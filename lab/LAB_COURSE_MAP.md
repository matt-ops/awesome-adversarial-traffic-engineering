# Complete lab-to-course map

Use the lesson **Next lesson** links for normal study. Use this page only to
locate the instruction, evidence, boundary, cleanup, and retest purpose for a
command. A command is never a substitute for its canonical lesson.

## Foundation setup and browser workflow

### `python -m lab.clients.safe_client --dry-run`

- **Canonical lesson:** `docs/modules/00-method/02-scope-and-rules.md`
- **Checkpoint:** Foundation
- **Prerequisite:** written synthetic engagement boundary
- **Offensive objective:** preflight the exact target and work envelope before an adversary client can run
- **Protected action or service effect:** none; this is a zero-traffic authorization/control check
- **Expected output:** JSON with the allowlisted loopback target, `dry_run: true`, and bounded duration, rate, concurrency, and totals
- **Interpretation:** the proposed local run fits executable guardrails; the output is not legal authorization or attack proof
- **Source basis:** `nist-sp-800-115`, `aate-local-lab`
- **Safety boundary:** validation completes before any request and accepts only the fixed loopback target
- **Expected evidence or output:** printed dry-run JSON showing the validated local target and envelope
- **Cleanup:** none; zero requests are emitted
- **Retest use:** rerun before every changed safe-client plan and compare the full envelope

### `python -m lab.clients.safe_client --target https://example.com --total 1`

- **Canonical lesson:** `docs/modules/00-method/02-scope-and-rules.md`
- **Checkpoint:** Foundation
- **Prerequisite:** successful safe-client dry run
- **Offensive objective:** prove an unapproved destination is rejected before contact
- **Protected action or service effect:** none; rejection is the required effect
- **Expected output:** JSON containing `rejected: true` and process exit status 2
- **Interpretation:** hostname validation blocked this example; it does not prove every out-of-scope representation is impossible
- **Source basis:** `nist-sp-800-115`, `aate-local-lab`
- **Safety boundary:** do not replace the URL with a real service; the command must not send traffic
- **Expected evidence or output:** a rejected-target error before any network request
- **Cleanup:** none; stop immediately if the target is accepted
- **Retest use:** mandatory negative test after any target-validation change

### `python -m http.server 4173 --bind 127.0.0.1 --directory lab/foundation-web`

- **Canonical lesson:** `docs/modules/01-http-edge/01-http-request-response.md`
- **Checkpoint:** Foundation
- **Prerequisite:** completed scope lesson and Python 3.12+
- **Offensive objective:** expose a minimal local workflow for manual HTTP and browser tracing
- **Protected action or service effect:** local search reads `inventory.json`; no protected mutation exists
- **Expected output:** loopback server logs local `GET` requests and the page reports one matching widget
- **Interpretation:** the trace teaches HTTP, DOM, storage, frame, and worker behavior; it is not a control bypass
- **Source basis:** `mdn-http-overview`, `chrome-devtools-network`, `aate-local-lab`
- **Safety boundary:** explicit `127.0.0.1` bind and fixed document root
- **Expected evidence or output:** an annotated request, manual Network trace, and browser-context observations
- **Cleanup:** press Ctrl+C and verify the page no longer refreshes
- **Retest use:** repeat the same manual workflow before comparing Playwright output

### `npm install`

- **Canonical lesson:** `docs/modules/03-playwright/02-first-browser.md`
- **Checkpoint:** Foundation
- **Prerequisite:** completed JavaScript and async lessons
- **Offensive objective:** install the exact browser-client toolchain used by the local adversary
- **Protected action or service effect:** none; pinned dependency installation only
- **Expected output:** npm resolves `package-lock.json` without dependency errors
- **Interpretation:** package success proves environment setup, not script behavior or target reachability
- **Source basis:** `microsoft-learn-playwright`, repository lockfile
- **Safety boundary:** no target traffic; review install errors rather than changing versions casually
- **Expected evidence or output:** the installed Node.js, npm, and resolved Playwright versions
- **Cleanup:** none; retain `package-lock.json`, and do not commit `node_modules`
- **Retest use:** rerun only when rebuilding the local dependency environment

### `npx playwright install chromium`

- **Canonical lesson:** `docs/modules/03-playwright/02-first-browser.md`
- **Checkpoint:** Foundation
- **Prerequisite:** npm dependencies installed
- **Offensive objective:** install the Chromium build paired with the pinned Playwright version
- **Protected action or service effect:** none; browser binary installation only
- **Expected output:** Playwright reports successful Chromium installation or an already-present matching build
- **Interpretation:** a browser binary exists; no workflow, state, or evasion claim follows
- **Source basis:** `microsoft-learn-playwright`, Playwright project documentation
- **Safety boundary:** no target traffic and no arbitrary browser extension installation
- **Expected evidence or output:** the installed Playwright and Chromium version record
- **Cleanup:** none; use Playwright's normal cache management if removal is later required
- **Retest use:** verify the recorded browser version before version-drift comparisons

### `npm run playwright:first`

- **Canonical lesson:** `docs/modules/03-playwright/02-first-browser.md`
- **Checkpoint:** Foundation
- **Prerequisite:** static server on 4173, pinned dependencies, and object-model lesson
- **Offensive objective:** reproduce the manual widget workflow with a headed automated browser
- **Protected action or service effect:** local search returns `Synthetic Widget - 5 available`; no authorization or evasion claim
- **Expected output:** terminal result and `lab/telemetry/playwright-first-workflow.json` with result, stored query, and local request/response events
- **Interpretation:** Playwright repeated one explainable workflow and captured evidence comparable to DevTools
- **Source basis:** `microsoft-learn-playwright`, `aate-local-lab`
- **Safety boundary:** target is a constant loopback URL; the script accepts no target argument
- **Expected evidence or output:** the generated first-workflow JSON and a manual-versus-automated comparison
- **Cleanup:** nested `finally` blocks close the BrowserContext and Browser; stop the static server separately
- **Retest use:** rerun unchanged after dependency/browser updates to establish drift in events or behavior

### `npm run typecheck`

- **Canonical lesson:** `docs/modules/03-playwright/02-first-browser.md`
- **Checkpoint:** Foundation
- **Prerequisite:** npm dependencies installed
- **Offensive objective:** reject type-inconsistent browser-client changes before execution
- **Protected action or service effect:** none; static analysis only
- **Expected output:** TypeScript exits 0 with no diagnostics
- **Interpretation:** types are consistent; selectors, runtime cleanup, and protected-action assertions still require execution
- **Source basis:** Playwright TypeScript declarations and repository `tsconfig.json`
- **Safety boundary:** no network traffic
- **Expected evidence or output:** the terminal typecheck result
- **Cleanup:** none
- **Retest use:** run after every TypeScript client edit and before a browser exercise

## Synthetic API and workflow attacks

### `docker compose -f lab/docker-compose.yml up --build -d`

- **Canonical lesson:** `docs/modules/04-automated-abuse/02-workflow-mapping.md`
- **Checkpoint:** Applied
- **Prerequisite:** Modules 00-03 and a successful non-Docker Playwright workflow
- **Offensive objective:** start the isolated edge/API target used for workflow, control, and resilience attacks
- **Protected action or service effect:** local services become healthy on loopback port 8080
- **Expected output:** Compose builds and starts `edge` and synthetic application containers
- **Interpretation:** the target is available; no vulnerability or bypass has yet been demonstrated
- **Source basis:** `aate-local-lab`, repository Compose configuration
- **Safety boundary:** published port binds to loopback and course services only
- **Expected evidence or output:** the built image configuration, version, and startup timestamp
- **Cleanup:** use the assigned Compose down command
- **Retest use:** rebuild after application/control remediation before repeating the same attack

### `curl.exe http://localhost:8080/health`

- **Bash or zsh equivalent:** `curl http://localhost:8080/health`
- **Canonical lesson:** `docs/modules/04-automated-abuse/02-workflow-mapping.md`
- **Checkpoint:** Applied
- **Prerequisite:** running local Compose stack
- **Offensive objective:** establish the pre-attack service-health baseline
- **Protected action or service effect:** health endpoint returns an OK service state
- **Expected output:** `{"status":"ok","service":"aate-local-app"}` with HTTP 200
- **Interpretation:** the service is reachable and healthy at this instant; business workflows still need separate baselines
- **Source basis:** `aate-local-lab`
- **Safety boundary:** one loopback request
- **Expected evidence or output:** a successful timestamped health response
- **Cleanup:** none
- **Retest use:** execute before pressure, after traffic stops, and after remediation

### `python -m lab.run recon`

- **Canonical lesson:** `docs/modules/04-automated-abuse/02-workflow-mapping.md`
- **Checkpoint:** Applied
- **Prerequisite:** HTTP/edge path knowledge and healthy local stack
- **Offensive objective:** map only the assigned local routes, workflows, controls, and immediate attack hypotheses
- **Protected action or service effect:** none; route/workflow inventory only
- **Expected output:** local surface map with ranked hypotheses and no adjacent-target discovery
- **Interpretation:** observations identify where to test; they are not vulnerability proof
- **Source basis:** `owasp-wstg-entry-points-v42`, `owasp-wstg-map-architecture-v42`, `aate-local-lab`
- **Safety boundary:** fixed loopback target and documented endpoints
- **Expected evidence or output:** an application, control, and resource path map
- **Cleanup:** reset is not required because recon does not mutate state
- **Retest use:** repeat after routing/control changes to confirm the attack surface actually changed

### `python -m lab.run credential`

- **Canonical lesson:** `docs/modules/04-automated-abuse/03-auth-and-rate-controls.md`
- **Checkpoint:** Applied
- **Prerequisite:** local recon map and synthetic credential data
- **Offensive objective:** reproduce a bounded login-abuse population and observe control/state decisions
- **Protected action or service effect:** synthetic login acceptance or rejection for five fixed attempts
- **Expected output:** five labeled outcomes plus a summary of accepted, rejected, and limited attempts
- **Interpretation:** the result characterizes this toy workflow and control; it does not authorize credential testing elsewhere
- **Source basis:** `owasp-automated-threats`, `portswigger-authentication-path`, `aate-local-lab`
- **Safety boundary:** fixed synthetic credentials, fixed loopback target, bounded attempts
- **Expected evidence or output:** the printed credential-attempt summary and blocked baseline
- **Cleanup:** call `/api/reset`
- **Retest use:** repeat the same five attempts after the authentication/rate-control change

### `python -m lab.run workflow`

- **Canonical lesson:** `docs/modules/04-automated-abuse/04-inventory-and-promotion-abuse.md`
- **Checkpoint:** Applied
- **Prerequisite:** workflow map and reset synthetic state
- **Offensive objective:** reproduce account, cart, promotion, challenge, and reservation transitions
- **Protected action or service effect:** synthetic inventory or promotion state changes only when the workflow permits
- **Expected output:** ordered state transitions with final synthetic inventory and control outcomes
- **Interpretation:** the sequence reveals business-state assumptions independently of browser transport
- **Source basis:** `owasp-automated-threats`, `portswigger-business-logic`, `aate-local-lab`
- **Safety boundary:** fixed local data and bounded requests
- **Expected evidence or output:** the printed workflow and state-machine observations
- **Cleanup:** call `/api/reset`
- **Retest use:** replay the identical transition sequence after binding/authorization remediation

### `npm run playwright:workflow-authorization`

- **Canonical lesson:** `docs/modules/04-automated-abuse/04-inventory-and-promotion-abuse.md`
- **Checkpoint:** Applied
- **Prerequisite:** mapped reservation workflow, Playwright setup, and local stack
- **Offensive objective:** prove caller-controlled identity can reserve inventory without required account/authentication state
- **Protected action or service effect:** fixed product inventory changes from 5 to 4
- **Expected output:** `lab/telemetry/workflow-authorization.json` with unauthenticated request, statuses, and before/after inventory
- **Interpretation:** this is an authorization/workflow flaw independent of browser transport; curl, Python, Burp, or Playwright can exercise it
- **Source basis:** `portswigger-business-logic`, `owasp-api-security-top-10`, `aate-local-lab`
- **Safety boundary:** fixed product and loopback target; one synthetic reservation
- **Expected evidence or output:** the generated workflow-authorization JSON and a finding outline
- **Cleanup:** call `/api/reset` and confirm inventory returns to 5
- **Retest use:** require the same request to fail while an authenticated intended reservation still succeeds

### `python -m lab.run ratelimit`

- **Canonical lesson:** `docs/modules/04-automated-abuse/03-auth-and-rate-controls.md`
- **Checkpoint:** Integrated
- **Prerequisite:** blocked fixed-key baseline and reset local state
- **Offensive objective:** test whether a caller-controlled session key defeats the toy expensive-route limit
- **Protected action or service effect:** more expensive reports are accepted than the fixed-key control permits
- **Expected output:** fixed key reaches 429 while rotated synthetic keys continue receiving 200
- **Interpretation:** the control trusts an attacker-controlled aggregation key; the result does not establish a network-identity bypass
- **Source basis:** `owasp-automated-threats`, `portswigger-authentication-path`, `aate-local-lab`
- **Safety boundary:** bounded calls, fixed loopback route, synthetic key values
- **Expected evidence or output:** the fixed-key versus rotated-key result comparison
- **Cleanup:** call `/api/reset`
- **Retest use:** repeat fixed and rotated populations after server-derived identity/workflow binding

### `python -m lab.analysis.analyze`

- **Canonical lesson:** `docs/modules/05-control-recon/01-signal-families.md`
- **Checkpoint:** Applied
- **Prerequisite:** signal-family lesson; no running target required
- **Offensive objective:** identify overtrusted toy features, collateral classifications, and useful experiment pivots
- **Protected action or service effect:** none; offline detector-support analysis
- **Expected output:** confusion matrix, per-population counts, and explicit limitations written to detector-analysis JSON
- **Interpretation:** metrics help select a brittle assumption or legitimate near-neighbor; detector construction is not the learner's principal outcome
- **Source basis:** `fp-inconsistent`, `aate-local-lab`
- **Safety boundary:** offline fixed fixture only
- **Expected evidence or output:** the generated `lab/telemetry/detector-analysis.json`
- **Cleanup:** none
- **Retest use:** compare the same fixture after a rule change to explain collateral and drift

### `npm run playwright:control-recon`

- **Canonical lesson:** `docs/modules/05-control-recon/05-blocked-baseline.md`
- **Checkpoint:** Integrated
- **Prerequisite:** manual and Python baselines, page/frame/worker model, healthy local stack
- **Offensive objective:** compare stock headed/headless populations, change one observable, repeat the protected action, and preserve residuals
- **Protected action or service effect:** synthetic protected report returns 200 only when the toy challenge decision issues an action token
- **Expected output:** `control-recon.json` with four trials: stock headed, stock headless, successful one-variable, and challenged frame-only cross-context mismatch
- **Interpretation:** one toy decision changes; the deliberately incoherent property change does not create a coherent or generally stealthy identity
- **Source basis:** `fpscanner-project`, `rebrowser-bot-detector`, `fp-inconsistent`, `aate-local-lab`
- **Safety boundary:** fixed loopback URL and four fixed browser trials
- **Expected evidence or output:** the generated control-recon JSON and trusted-signal comparison
- **Cleanup:** client closes contexts/browsers; call `/api/reset`
- **Retest use:** rerun unchanged after a control rule or browser-version change

### `python -m lab.run bypass`

- **Canonical lesson:** `docs/modules/06-browser-evasion/04-replay-and-temporal-consistency.md`
- **Checkpoint:** Integrated
- **Prerequisite:** blocked challenge baseline and token-binding hypothesis
- **Offensive objective:** test whether a synthetic challenge token can be replayed across sessions
- **Protected action or service effect:** second session creates the protected report
- **Expected output:** baseline 403, token issue, cross-session 200, and replay evidence
- **Interpretation:** the lab token is insufficiently bound; it does not prove a weakness in another token format or service
- **Source basis:** `fpscanner-project`, `aate-local-lab`, `aate-adversarial-control-loop`
- **Safety boundary:** fixed loopback endpoint and synthetic token/session identifiers
- **Expected evidence or output:** the replay request, response, and returned server session evidence
- **Cleanup:** call `/api/reset`
- **Retest use:** repeat the same cross-session replay after session/action/nonce/expiry/single-use binding

### `curl.exe -X POST http://localhost:8080/api/reset`

- **Bash or zsh equivalent:** `curl -X POST http://localhost:8080/api/reset`
- **Canonical lesson:** every stateful Applied-or-deeper lab page
- **Checkpoint:** Applied and later
- **Prerequisite:** running local stack
- **Offensive objective:** restore a known state so conditions remain comparable
- **Protected action or service effect:** synthetic users, inventory, counters, tokens, cache, and retry fixtures return to defaults
- **Expected output:** HTTP 200 reset confirmation
- **Interpretation:** the next experiment starts from the documented state; preserve reset failure as a confounder
- **Source basis:** `aate-local-lab`
- **Safety boundary:** one fixed loopback POST
- **Expected evidence or output:** the reset confirmation and timestamp
- **Cleanup:** none beyond confirming health
- **Retest use:** execute before every baseline/treatment pair and exact remediation retest

### `docker compose -f lab/docker-compose.yml down`

- **Canonical lesson:** every Docker-backed lab page
- **Checkpoint:** Applied and later
- **Prerequisite:** course Compose stack was started from this repository
- **Offensive objective:** terminate the isolated target after evidence capture
- **Protected action or service effect:** course containers and network stop
- **Expected output:** Compose reports course services and network removed/stopped
- **Interpretation:** local attack surface is no longer running; this is cleanup, not evidence deletion
- **Source basis:** repository Compose configuration, `aate-local-lab`
- **Safety boundary:** exact course Compose file only
- **Expected evidence or output:** the cleanup confirmation and timestamp
- **Cleanup:** this command is the cleanup action
- **Retest use:** start from a new build when validating application remediation

## Compatibility commands retained for regression

### `python -m lab.run evasion`

- **Canonical lesson:** `docs/modules/06-browser-evasion/02-one-variable-experiments.md`
- **Checkpoint:** Applied
- **Prerequisite:** blocked-baseline concept and running local stack
- **Offensive objective:** change one fixture property and observe the transparent toy rule
- **Protected action or service effect:** toy decision may change; primary protected-action proof comes from the Playwright control-recon client
- **Expected output:** compact before/after fixture decision JSON
- **Interpretation:** useful deterministic regression only; not a coherent identity or primary evasion lab
- **Source basis:** `aate-local-lab`
- **Safety boundary:** fixed loopback fixture and bounded requests
- **Expected evidence or output:** the compatibility JSON printed by the command
- **Cleanup:** call `/api/reset`
- **Retest use:** retain as a fast detector-rule regression after local changes

### `python -m lab.run resilience`

- **Canonical lesson:** `docs/modules/08-ddos-resilience/01-resource-exhaustion-model.md`
- **Checkpoint:** Foundation
- **Prerequisite:** healthy local stack and resource-chain model
- **Offensive objective:** compare small cheap and expensive request sets before k6
- **Protected action or service effect:** observe different local work/latency paths without attempting material degradation
- **Expected output:** bounded timing comparison with explicit client-noise limitation
- **Interpretation:** supports the resource model; k6 scenarios provide the primary controlled evidence
- **Source basis:** `aate-local-lab`
- **Safety boundary:** fixed count and loopback target
- **Expected evidence or output:** the compatibility timing output printed by the command
- **Cleanup:** call `/api/reset`
- **Retest use:** quick resource-path check after endpoint implementation changes

### `npm run playwright:foundation`

- **Canonical lesson:** `docs/modules/01-http-edge/01-http-request-response.md`
- **Checkpoint:** Foundation
- **Prerequisite:** Python, Node dependencies, and the pinned Playwright Chromium browser
- **Offensive objective:** deterministic local regression test of the Foundation inventory exercise
- **Protected action or service effect:** exact local search result; no protected action
- **Expected output:** HTTP, JSON fixture, accessible UI, result, URL, and cleanup checks pass
- **Interpretation:** proves the bundled exercise works locally; it does not prove production behavior
- **Source basis:** `microsoft-learn-playwright`, `aate-local-lab`
- **Safety boundary:** fixed loopback target
- **Expected evidence or output:** terminal pass or fail output; no separate learner file is required
- **Cleanup:** the test closes Chromium and the static server, including on failure
- **Retest use:** run after Foundation web application or lesson changes

## Protocol, resilience, and Python tooling

### `python -m lab.protocol.compare clienthello`

- **Canonical lesson:** `docs/modules/07-protocol-identity/01-tls-clienthello.md`
- **Checkpoint:** Integrated
- **Prerequisite:** TLS ClientHello field model
- **Offensive objective:** isolate how ALPN configuration changes generated ClientHello bytes without contacting a host
- **Protected action or service effect:** none; socket-free fixture generation
- **Expected output:** two TLS records with selected outer fields, byte counts, non-JA4 digest prefixes, a `bytes_differ` result, and the declared ALPN configuration change
- **Interpretation:** Python/OpenSSL configuration changes generated bytes; the helper does not parse ALPN, calculate JA4, capture browser TLS, or prove identity
- **Source basis:** `rfc-8446`, `ja4-project`
- **Safety boundary:** no socket is opened
- **Expected evidence or output:** the ClientHello comparison table and fixture hashes
- **Cleanup:** none
- **Retest use:** repeat after Python/OpenSSL changes to document protocol drift

### `python -m lab.protocol.compare http`

- **Canonical lesson:** `docs/modules/07-protocol-identity/04-proxies-and-connection-reuse.md`
- **Checkpoint:** Integrated
- **Prerequisite:** running local stack and observation-point model
- **Offensive objective:** record what the fixed Python HTTP helper and local edge/application actually send and receive
- **Protected action or service effect:** one harmless local observation request
- **Expected output:** server-visible HTTP version, selected headers, and source-address observation
- **Interpretation:** the plain-HTTP result describes only this helper/path; browser TLS, JA4, HTTP/2, HTTP/3, QUIC, and proxy-induced changes remain source-led theory or future approved work
- **Source basis:** `mdn-http-overview`, `owasp-wstg-map-architecture-v42`, `ja4-project`
- **Safety boundary:** one fixed loopback URL
- **Expected evidence or output:** a client, edge, and application observation-point matrix
- **Cleanup:** none
- **Retest use:** repeat with a declared local intermediary/configuration change

### `k6 run lab/load/bounded.js`

- **Canonical lesson:** `docs/modules/08-ddos-resilience/04-bounded-load-testing.md`
- **Checkpoint:** Integrated
- **Prerequisite:** Modules 00-08, dry-run evidence, healthy stack, selected `AATE_SCENARIO`
- **Offensive objective:** execute one of seven application-layer scenario contracts, including two explicitly observation-only cases
- **Protected action or service effect:** scenario-specific latency, fixture-state, retry, sequence, or immediate-health outcome
- **Expected output:** named behavior assertions, checks and thresholds, bounded request metrics, and teardown health `200` within 1,000 ms
- **Interpretation:** compare only the asserted local behavior inside the hard envelope; endpoint-cost and workflow-sequence observations are not mitigation tests, and no run is a capacity claim
- **Source basis:** `k6-thresholds`, `aws-builders-library-load-shedding`, `aate-local-lab`
- **Safety boundary:** loopback only, ≤15 seconds, ≤5 VUs, ≤10 effective requests/second, ≤100 worst-case requests, aborting thresholds
- **Expected evidence or output:** the scenario configuration and bounded k6 result
- **Cleanup:** teardown health check, `/api/reset`, then Compose down when finished
- **Retest use:** repeat the identical scenario, rate, duration, assertions, thresholds, and legitimate-neighbor check; a mitigation claim also requires a real changed control

### `Dry-run bounded load (platform commands below)`

- **Canonical lesson:** `docs/modules/08-ddos-resilience/04-bounded-load-testing.md`
- **Checkpoint:** Integrated
- **Prerequisite:** k6 installed and scenario selected
- **Offensive objective:** validate target, scenario, duration, rate, VU, and total ceilings before traffic
- **Protected action or service effect:** none; dry run must emit zero HTTP requests
- **Expected output:** JSON configuration with `dryRun: true`; one no-traffic iteration
- **Interpretation:** configuration is accepted by guards; no service behavior has been tested
- **Source basis:** `k6-thresholds`, `aate-local-lab`
- **Safety boundary:** dry-run branch returns before reset or scenario requests
- **Expected evidence or output:** the printed scenario configuration JSON
- **Cleanup:** none
- **Retest use:** mandatory before every changed scenario configuration

#### PowerShell

```powershell
$env:AATE_DRY_RUN = "1"
k6 run lab/load/bounded.js
```

#### Bash or zsh

```bash
AATE_DRY_RUN=1 k6 run lab/load/bounded.js
```

### `python -m lab.tooling.client telemetry`

- **Canonical lesson:** `docs/modules/09-tooling-code-review/01-python-telemetry.md`
- **Checkpoint:** Foundation
- **Prerequisite:** Python dictionaries, JSON, and `Counter` assignments
- **Offensive objective:** turn raw fixture events into reproducible population/label evidence
- **Protected action or service effect:** none; offline analysis
- **Expected output:** record count, population counts, label counts, and limitations
- **Interpretation:** counts describe the fixture; they do not identify a user or establish production prevalence
- **Source basis:** `python-standard-library`, `pytest-documentation`, `aate-local-lab`
- **Safety boundary:** offline fixed fixture
- **Expected evidence or output:** the generated telemetry summary JSON
- **Cleanup:** none
- **Retest use:** use the same fixture and assertions after parser/rule changes

### `python -m lab.tooling.client concurrent --total 6 --concurrency 2`

- **Canonical lesson:** `docs/modules/09-tooling-code-review/02-async-and-bounded-concurrency.md`
- **Checkpoint:** Applied
- **Prerequisite:** safe target validation, running local stack, and async lesson
- **Offensive objective:** generate a representative local request population with explicit total and in-flight bounds
- **Protected action or service effect:** six health actions complete while at most two are in flight
- **Expected output:** six statuses plus trace data showing the concurrency budget
- **Interpretation:** concurrency shapes timing but does not change total work; both limits must remain explicit
- **Source basis:** `python-standard-library`, `pytest-documentation`, `aate-local-lab`
- **Safety boundary:** fixed loopback route, total 6, concurrency 2, per-request timeout
- **Expected evidence or output:** the bounded-concurrency trace
- **Cleanup:** none; health is read-only
- **Retest use:** repeat the same work/concurrency pair after client or service changes

### `python -m lab.tooling.client retry --target "http://localhost:8080/api/reports/unstable?operation_id=lesson-09" --attempts 3`

- **Canonical lesson:** `docs/modules/09-tooling-code-review/03-retries-timeouts-and-jitter.md`
- **Checkpoint:** Applied
- **Prerequisite:** reset local stack and retry-budget lesson
- **Offensive objective:** measure deterministic retry amplification and stop after success
- **Protected action or service effect:** first attempt returns 503 and one retry returns 200 for the same operation
- **Expected output:** attempt trace with `503 -> 200`, bounded delay, and unused third attempt
- **Interpretation:** one logical action consumed two requests; unbounded retries could magnify overload
- **Source basis:** `aws-builders-library-timeouts-retries-jitter`, `python-standard-library`, `aate-local-lab`
- **Safety boundary:** exact loopback URL, ≤3 attempts, ≤2-second timeout, bounded jitter
- **Expected evidence or output:** the retry-budget trace
- **Cleanup:** call `/api/reset`
- **Retest use:** repeat after idempotency, retry, or overload-control remediation

## Repository validation commands

These commands validate the course but do not perform an attack:

| Command | Required result |
|---|---|
| `python scripts/validate_sources.py` | ledger schema, mandated sources, and lesson attribution pass |
| `python scripts/validate_lessons.py` | every canonical lesson satisfies the remediation teaching contract |
| `python scripts/validate_labs.py` | learner lab contracts, command map, and report template/validated sample pass |
| `python scripts/validate_load_scripts.py` | local-only target and all hard load guards pass |
| `python scripts/check_internal_links.py` | all local Markdown files and anchors resolve |
| `python -m unittest discover -s lab/tests -v` | Python application, safety, protocol, analysis, and tooling tests pass |
| `python -m mypy lab scripts` | strict Python type checking passes |
| `python -m ruff check lab scripts` | Python lint and security rules pass |
| `npm run typecheck` | TypeScript type checking passes |
| `docker compose -f lab/docker-compose.yml config --quiet` | Compose configuration parses without mutation |
| `mkdocs build --strict` | the same local public site builds without warnings |
