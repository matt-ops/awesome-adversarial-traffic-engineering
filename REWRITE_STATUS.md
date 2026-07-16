# Source-first rewrite status

Last updated: 2026-07-15  
Branch: `agent/source-first-rewrite`  
Remote state: **not pushed**

## Phase status

| Phase | Status | Evidence |
|---|---|---|
| 0 - Protect and audit | Complete | Baseline tests/build recorded; lab commands executed; old render archived; audit written |
| 1 - Sources, provenance, Module 00 | Complete | 47-entry ledger; three lessons; source/lesson/link validation and strict build pass |
| 2 - HTTP, browser, JavaScript, Playwright | Complete | 13 new lessons; zero-Docker static site and headed-first Playwright workflow tested |
| 3 - Automated abuse | Complete | Five lessons; exact OWASP/PortSwigger assignments; local runners and renamed authorization proof tested |
| 4 - Control reconnaissance and evasion | Complete | Ten lessons; three-context enforced local control; stock baselines, action proof, replay, research limits |
| 5 - Protocol identity | Complete | Five lessons; generated ClientHello comparison; fixed-loopback HTTP observation; protocol identity bounded as a pivot rather than identity proof |
| 6 - DDoS and resilience | Complete | Five lessons; seven bounded k6 scenarios; hard target, duration, VU, rate, total-request, threshold, abort, dry-run, and recovery controls |
| 7 - Tooling, findings, interview | In progress | Next work |
| 8 - Integration and review | Not started | - |

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
- Source validation resolves all 47 IDs, lesson and internal-link validation
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

## Next exact task

Write Modules 09-10 from the selected Python, secure-code-review, finding,
briefing, and interview sources. Every lesson must end in a runnable artifact or
an exact external assignment, not a topic prompt.

## Completion rule

Do not push or deploy this branch. The rewrite is complete only when source,
lesson, internal-link, code, safety, and strict MkDocs checks pass and this file
records the final human-review order.
