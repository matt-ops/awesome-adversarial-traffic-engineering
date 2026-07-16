# Source-first rewrite status

Last updated: 2026-07-15  
Branch: `agent/source-first-rewrite`  
Remote state: **not pushed**

## Phase status

| Phase | Status | Evidence |
|---|---|---|
| 0 - Protect and audit | Complete | Baseline tests/build recorded; lab commands executed; old render archived; audit written |
| 1 - Sources, provenance, Module 00 | Complete | Validated ledger (48 entries after final additions); three lessons; source/lesson/link validation and strict build pass |
| 2 - HTTP, browser, JavaScript, Playwright | Complete | 13 new lessons; zero-Docker static site and headed-first Playwright workflow tested |
| 3 - Automated abuse | Complete | Five lessons; exact OWASP/PortSwigger assignments; local runners and renamed authorization proof tested |
| 4 - Control reconnaissance and evasion | Complete | Ten lessons; three-context enforced local control; stock baselines, action proof, replay, research limits |
| 5 - Protocol identity | Complete | Five lessons; generated ClientHello comparison; fixed-loopback HTTP observation; protocol identity bounded as a pivot rather than identity proof |
| 6 - DDoS and resilience | Complete | Five lessons; seven bounded k6 scenarios; hard target, duration, VU, rate, total-request, threshold, abort, dry-run, and recovery controls |
| 7 - Tooling, findings, interview | Complete | Nine lessons; executable telemetry, bounded concurrency/retry tooling, four code-review cases, finding/retest/briefing/narrative/mock artifacts |
| 8 - Integration and review | Complete | Four cumulative checkpoint views; four-depth module indexes; lab/command matrix; progress, electives, coverage and quality audits; full suite and strict build pass |

## Verified facts

- The old baseline had 14 passing Python tests, a passing TypeScript check,
  mypy, Ruff, Docker Compose configuration, and strict MkDocs build.
- Docker Desktop was unavailable; the pinned FastAPI target was exercised
  directly on loopback, and every existing runner was inventoried.
- The monolithic `COURSE.md` and obsolete validator were removed after their
  source and rendered output were archived.
- Module 00 and Modules 01-03 now contain 16 template-compliant lessons total.
- The Foundation static application returned `200` on loopback.
- The first Playwright workflow ran headless for automated verification, found
  the synthetic widget, retained `widget` in local storage, and captured twelve
  local request/response events. The learner command remains headed by default.
- Source validation resolves all 48 IDs, lesson and internal-link validation
  pass, TypeScript passes, and the Phase 2 site builds in strict mode.
- Module 04 adds five lessons with exact provider assignments. Local recon,
  credential, workflow, authorization, and rate-limit runners executed against
  the loopback API. The authorization artifact proves inventory changed 5 -> 4
  without authentication and explicitly states that this is not browser evasion.
- Modules 05-06 add ten lessons grounded in FPScanner, Rebrowser,
  FP-Inconsistent, and Gummy Browsers. The local control test passes: stock
  headed/headless populations are challenged; one top-page change is allowed;
  the protected report returns `200`; one-use replay returns `403`. Verification
  mode records that its requested headed trial actually launched headless.
- Module 07 adds five lessons grounded in the TLS, HTTP/2, HTTP/3, and JA4
  sources. The local helper generates and parses ClientHello records without a
  network socket, demonstrates ALPN-dependent byte changes, and keeps its digest
  explicitly separate from JA4 and identity claims. Fixed-loopback HTTP
  observation records what a server can actually see.
- Module 08 adds five lessons and a bounded k6 exercise. All seven scenarios ran
  successfully against the local fixture with 100% checks in the verification
  envelope. The script rejects non-loopback targets and excessive duration,
  VUs, request rate, and worst-case total requests; dry-run sends no traffic;
  thresholds abort; teardown checks recovery.
- The Phase 6 suite has 19 passing Python tests, passing mypy, Ruff, TypeScript,
  source, lesson, internal-link, load-safety, and strict MkDocs checks.
- Modules 09-10 add nine lessons and three lab guides. The standard-library
  tooling parses fixture telemetry, validates bounded concurrency before task
  creation, records a two-attempt 503 -> 200 retry trace, and rejects a fourth
  attempt. Four synthetic code-review cases connect attacker input to a
  protected effect and exact remediation test.
- The Module 10 sequence produces a finding, remediation invariant, exact
  negative/positive retest, five-minute briefing, public-safe role narrative,
  and full mock repair loop. It does not convert local lab work into production
  experience claims or include personal/employer-specific artifacts.
- Phase 7 validation resolves 48 ledger entries and 50 lesson source blocks;
  22 Python tests, mypy, Ruff, TypeScript, lesson/source/link validation, and a
  strict MkDocs build pass.
- Phase 8 exposes Foundation, Applied, Integrated, and Deep sections in all 11
  module indexes. Four checkpoint pages link to those sections without copying
  lesson instruction. A plain progress page, 11-page lab contract set, complete
  command map, curated electives, and capability/restriction-gap audit are present.
- The Integrated portfolio now explicitly assigns six Python exercises, ten
  code reviews, five threat models, five system designs, a six-to-eight-page
  report, and executive summary. The Deep package explicitly assigns original,
  drift, runtime, protocol, privacy/accessibility, coherence, remediation,
  portfolio, mock, and first-90-day research work.
- Final local validation passes: 48 sources, 50 lessons, 11 module indexes, 11
  lab pages, 102 checked Markdown files, 22 Python tests, strict mypy, Ruff,
  TypeScript, Compose configuration, load-safety validation, and strict MkDocs.
  The external-link sweep checked 78 URLs; five provider/doc responses were
  classified as transient warnings (HTTP 403, 429, or 502), not malformed or
  conclusively broken links.

## Known limitations

- The local control and API are deliberately transparent/small; they do not
  represent a commercial control, production diversity, or production scale.
- The protocol helper generates ClientHello bytes in memory and observes local
  HTTP. It is not a packet capture or JA4 implementation.
- The normal lab covers bounded application-layer pressure, not L3/L4 floods,
  spoofing, reflection, or attack infrastructure. Exact isolated external routes
  are listed in the electives and coverage audit.
- Real WAF parser chains, AI-powered browser agents, visual CAPTCHA solvers,
  broad recon, and multi-system operations use exact mature external routes
  rather than shallow repository simulations.
- External pages and version-sensitive browser projects can change. The ledger
  records verification date and lessons require runtime/project versions.
- Docker Desktop was unavailable during the original audit. Compose
  configuration passes, and application behavior was exercised directly on
  fixed loopback with the same pinned FastAPI code.

## Recommended human-review order

1. `README.md`, `docs/start-here.md`, and `docs/path.md` for the one-path experience.
2. Modules 00-03 plus the static and first-Playwright labs for from-zero browser readiness.
3. Modules 04-06 plus workflow/control labs for offensive lifecycle and impact proof.
4. Modules 07-09 plus protocol, bounded-load, Python, and code-review artifacts.
5. Module 10 plus the finding, retest, briefing, narrative, and mock outputs.
6. Checkpoints, portfolio drills, progress, electives, and `COVERAGE_AUDIT.md`.
7. Safety pages, `lab/LAB_COURSE_MAP.md`, validators, CI, and this status record.

## Completion rule

Do not push or deploy this branch. The rewrite is complete only when source,
lesson, internal-link, code, safety, and strict MkDocs checks pass and this file
records the final human-review order. Those local conditions are now satisfied;
remote review/push remains a separate user-authorized action.
