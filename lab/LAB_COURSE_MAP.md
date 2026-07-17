# Lab-to-course map

This is the maintenance index. Learners should follow lesson **Next** links.
Every command below has an assigned lesson, prerequisite, expected result,
source basis, boundary, and artifact.

## Foundation and browser commands

| Command | Lesson / depth | Prerequisite | Objective and expected output | Source basis | Safety boundary | Artifact |
|---|---|---|---|---|---|---|
| `python -m lab.clients.safe_client --dry-run` | Module 00 scope / Applied | authorized-role lesson | Print target/envelope and send zero traffic | Python stdlib; local-lab specification | allowlisted target plus hard envelope | boundary output |
| `python -m lab.clients.safe_client --target https://example.com --total 1` | Module 00 scope / Applied | dry run | Reject target before traffic | local-target policy | rejection is mandatory | rejected-target evidence |
| `python -m http.server 4173 --bind 127.0.0.1 --directory lab/foundation-web` | Module 01 request/response / Foundation | Python installed | Serve static page; browser receives local `200` | MDN HTTP and messages | explicit loopback bind | request worksheet |
| `npm install` | Module 03 first browser / Foundation | Modules 01-02 | Install pinned browser-client dependencies | Playwright installation docs | package installation only | lockfile-resolved environment |
| `npx.cmd playwright install chromium` | Module 03 first browser / Foundation | npm dependencies | Install Chromium used by Playwright | Playwright installation docs | no target traffic | installed browser version note |
| `npm run playwright:first` | Module 03 first browser / Foundation | static server on 4173 | Complete headed widget flow and save local network events | Playwright object/network docs | script target fixed to loopback | `playwright-first-workflow.json` |
| `npm run typecheck` | Module 03 and repository validation | npm dependencies | TypeScript exits successfully with no errors | TypeScript/Playwright types | no traffic | validation log |

## Synthetic API and attack commands

| Command | Lesson / depth | Prerequisite | Objective and expected output | Source basis | Safety boundary | Artifact |
|---|---|---|---|---|---|---|
| `docker compose -f lab/docker-compose.yml up --build -d` | Module 04 workflow mapping / Applied | Modules 00-03 | Start local edge/API | Docker Compose file; local-lab specification | published port is localhost 8080 | lab version/config |
| `curl.exe http://localhost:8080/health` | Module 04 workflow mapping / Applied | local stack | Return `{"status":"ok","service":"aate-local-app"}` | local-lab specification | one loopback request | health baseline |
| `python -m lab.run recon` | Module 04 workflow mapping / Foundation | local stack and HTTP model | Inventory local routes and emit ranked immediate attack hypotheses | OWASP WSTG architecture/API recon | runner fixed to loopback | surface/workflow map |
| `python -m lab.run credential` | Module 04 auth/rate / Applied | recon | Record five bounded synthetic login outcomes | OWASP auth/automated-threat sources | fixed credentials and loopback | credential evidence |
| `python -m lab.run workflow` | Module 04 inventory/promotion / Applied | recon and state model | Execute synthetic account/cart/promotion/challenge workflow | OWASP automated threats | fixed local data | workflow evidence |
| `npm run playwright:workflow-authorization` | Module 04 inventory/promotion / Applied | Playwright plus local stack | Prove unauthenticated inventory change `5 -> 4` | PortSwigger/OWASP authorization sources | loopback and fixed product | workflow-authorization JSON |
| `python -m lab.run ratelimit` | Module 04 auth/rate / Integrated | local stack reset | Show caller-controlled key rotation defeats toy per-session limit | OWASP automated threats | bounded calls, loopback | rate-key comparison |
| `python -m lab.analysis.analyze` | Module 05 signal families / Foundation | fixture only | Print confusion matrix, populations, and explicit limitations | classification-metric sources | offline fixture, no traffic | detector-analysis JSON |
| `npm run playwright:control-recon` | Modules 05-06 / Integrated | blocked baseline lessons and local stack | Compare stock populations; prove one-variable local action and replay result | FPScanner/Rebrowser/consistency research | loopback; fixed experiments | control-recon JSON |
| `python -m lab.run bypass` | Module 06 replay / Integrated | blocked baseline | Show `403`, issue synthetic token, replay across session, receive protected `200` | local-lab specification | loopback and fixed token fixture | replay evidence |
| `curl.exe -X POST http://localhost:8080/api/reset` | every stateful API lab | local stack | Restore synthetic users, inventory, counters, tokens, cache, and retries | local-lab specification | one loopback request | reset timestamp |
| `docker compose -f lab/docker-compose.yml down` | every Docker-backed lab | local stack | Stop/remove course containers and network | Compose file | course stack only | cleanup record |

## Preserved compatibility helpers

These tested commands remain for regression/history but are not the primary
learner exercise. Their replacements produce stronger evidence.

| Command | Lesson / depth | Prerequisite | Objective and expected output | Source basis | Safety boundary | Artifact |
|---|---|---|---|---|---|---|
| `python -m lab.run evasion` | Module 06 one-variable / Foundation | local stack and blocked-baseline concept | Change one fixture property and show toy decision change | local-lab specification | loopback; one request population | compatibility JSON output; primary artifact comes from `playwright:control-recon` |
| `python -m lab.run resilience` | Module 08 resource model / Foundation | local stack | Compare bounded cheap/expensive calls; output timings may be dominated by client noise | local-lab specification | loopback and fixed small count | compatibility timing output; primary evidence comes from bounded k6 scenarios |
| `npm run playwright:foundation` | Module 03 first browser / Foundation | static server on 4173 | Alias of `playwright:first`; runs the same headed local workflow | Playwright docs | fixed loopback target | same first-workflow artifact |

## Protocol, resilience, and tooling commands

| Command | Lesson / depth | Prerequisite | Objective and expected output | Source basis | Safety boundary | Artifact |
|---|---|---|---|---|---|---|
| `python -m lab.protocol.compare clienthello` | Module 07 TLS / Foundation | TLS lesson | Generate two socket-free Python/OpenSSL ClientHello records; report selected outer fields, byte counts, non-JA4 digests, `bytes_differ`, and the declared ALPN configuration change without claiming parsed ALPN/offsets/browser TLS | RFC 8446 | no socket opened | ClientHello comparison |
| `python -m lab.protocol.compare http` | Module 07 intermediaries / Integrated | local stack | Record the fixed Python helper's plain-HTTP version, headers, and address; do not claim browser TLS, JA4, HTTP/2, HTTP/3, QUIC, or proxy-change evidence | MDN HTTP; OWASP architecture | fixed loopback URL | observation-point map |
| `k6 run lab/load/bounded.js` | Module 08 bounded load / Integrated | Modules 00-08 and local stack | Run one of seven scenario contracts with named assertions; endpoint-cost/workflow-sequence cases are observations, not mitigation tests | k6 threshold docs; load-shedding source | local target, <=15 s, <=5 VUs, <=10 req/s, <=100 worst-case requests, aborts | scenario result |
| `$env:AATE_DRY_RUN='1'; k6 run lab/load/bounded.js` | Module 08 bounded load / Integrated | k6 installed | Print validated configuration; network I/O remains zero | k6 docs; local specification | dry run is traffic-free | safety configuration |
| `python -m lab.tooling.client telemetry` | Module 09 telemetry / Foundation | fixture only | Print record/population/label counts and limitations | Python `json`/`Counter` | offline fixture | telemetry summary |
| `python -m lab.tooling.client concurrent --total 6 --concurrency 2` | Module 09 concurrency / Applied | local stack | Return six health results within two in-flight permits | Python `asyncio` | local validation and envelope precede tasks | concurrency trace |
| `python -m lab.tooling.client retry --target "http://localhost:8080/api/reports/unstable?operation_id=lesson-09" --attempts 3` | Module 09 retries / Applied | reset local stack | Record deterministic `503 -> 200` with one delayed retry | timeout/retry/jitter source | local URL, <=3 attempts, <=2 s timeout | retry budget |

For k6 scenario selection, use the environment values documented in
`docs/labs/deep/bounded-load.md`; the same hard validation runs for every scenario.

## Validation commands

| Command | Expected result | Traffic |
|---|---|---|
| `python scripts/validate_sources.py` | all source IDs/types/assignments resolve | none |
| `python scripts/validate_lessons.py` | every lesson meets the teaching template | none |
| `python scripts/check_internal_links.py` | all local pages and anchors resolve | none |
| `python scripts/check_internal_links.py --external` | malformed/permanent links fail; transient remote failures warn | HEAD requests to cited public resources |
| `python scripts/validate_load_scripts.py` | every load script contains all hard controls, truthful names, and outcome assertions | none |
| `python -m unittest discover -s lab/tests -v` | all Python lab tests pass | in-process fixture only |
| `python -m mypy lab scripts` | strict type check passes | none |
| `python -m ruff check lab scripts` | lint/security rules pass | none |
| `npm run typecheck` | TypeScript type check passes | none |
| `docker compose -f lab/docker-compose.yml config --quiet` | Compose configuration parses | none |
| `mkdocs build --strict` | public site builds without warnings | none |
