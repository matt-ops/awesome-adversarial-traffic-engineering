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
| 4 - Control reconnaissance and evasion | In progress | Next work |
| 5 - Protocol identity | Not started | - |
| 6 - DDoS and resilience | Not started | - |
| 7 - Tooling, findings, interview | Not started | - |
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

## Next exact task

Build the manual/headed/headless/HTTP-client control-recon populations, add
top-page/frame/worker sensor capture, replace score-only evasion with a protected
local action, and write Modules 05-06 from the fingerprinting research sources.

## Completion rule

Do not push or deploy this branch. The rewrite is complete only when source,
lesson, internal-link, code, safety, and strict MkDocs checks pass and this file
records the final human-review order.
