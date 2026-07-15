# Source-first rewrite status

Last updated: 2026-07-15  
Branch: `agent/source-first-rewrite`  
Remote state: **not pushed**

## Phase status

| Phase | Status | Evidence |
|---|---|---|
| 0 — Protect and audit | Complete | Baseline tests/build recorded; lab commands executed; old render archived; audit written |
| 1 — Sources, provenance, Module 00 | In progress | Next work |
| 2 — HTTP, browser, JavaScript, Playwright | Not started | — |
| 3 — Automated abuse | Not started | — |
| 4 — Control reconnaissance and evasion | Not started | — |
| 5 — Protocol identity | Not started | — |
| 6 — DDoS and resilience | Not started | — |
| 7 — Tooling, findings, interview | Not started | — |
| 8 — Integration and review | Not started | — |

## Baseline facts

- 14 Python tests passed.
- TypeScript typecheck passed.
- mypy and Ruff passed.
- Docker Compose configuration passed.
- Strict MkDocs build passed.
- Every existing local runner executed against the synthetic application.
- Docker Desktop was unavailable; application behavior was exercised by running
  the pinned FastAPI target directly on loopback.
- The current resilience comparison is not evidentially strong and is marked for
  rebuild.

## Next exact task

Build and validate `sources/sources.yaml`, write the source policy and AATE-loop
provenance, add the three new validators, configure the new `docs/` tree, and
rewrite Module 00 before drafting later modules.

## Completion rule

Do not push or deploy this branch. The rewrite is complete only when source,
lesson, internal-link, code, safety, and strict MkDocs checks pass and this file
records the final human-review order.
