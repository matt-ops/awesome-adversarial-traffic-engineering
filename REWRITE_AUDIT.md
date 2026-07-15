# Source-first rewrite audit

Audit date: 2026-07-15  
Branch: `agent/source-first-rewrite`  
Baseline commit: `02cfce3`  
Remote policy: local work and local commits only; no push or deployment before
human review.

## Repository and history

The repository began with a broad curriculum, concept pages, templates,
interview material, validators, and a progress tracker. Commit `0461762`
collapsed that structure into a small public site centered on one monolithic
`COURSE.md`. Later commits added red-team framing, reconnaissance, external
coverage, and a linear nine-module sequence. The current rewrite preserves the
working technical slice while replacing that monolithic instructional layer.

The pre-rewrite learner surface had five navigation entries:

1. Start — `README.md`
2. Course — `COURSE.md`
3. Extra labs — `RESOURCES.md`
4. Local lab — `lab/README.md`
5. Safety — `SAFETY.md`

The former source and its strict MkDocs render are preserved in
`archive/v1-course/`. The archive will not be added to course navigation.

## Baseline validation

| Check | Baseline result |
|---|---|
| `scripts/validate_course.py` | PASS |
| Python unit tests | PASS, 14 tests |
| TypeScript `npm run typecheck` | PASS |
| mypy | PASS, 19 source files |
| Ruff | PASS |
| Docker Compose configuration | PASS; Docker warned that its user config was unreadable in the sandbox |
| MkDocs strict build | PASS |
| Live/public page fetch | Previously deployed v1 was reachable; local rendered copy archived |

Docker Desktop was not running during the audit, so Compose could not start
containers. To test application behavior rather than skip it, the same FastAPI
application was started on `127.0.0.1:8080` with the pinned development
dependencies. The temporary process was stopped after the command audit.

## Lab command inventory

| Command | Current references | Observed result | Rewrite disposition |
|---|---|---|---|
| `python -m lab.clients.safe_client --dry-run` | Module 0; local lab page | Prints local target and enforced duration, concurrency, rate, total, and expensive-request caps | Preserve and teach after authorization terminology |
| `python -m lab.run recon` | course introduction; Modules 0–2; local lab page | Inventories OpenAPI routes, sends five bounded probes, emits four hypotheses | Preserve; move behind HTTP/DevTools prerequisites and align with the AATE loop |
| `python -m lab.run credential` | Modules 2, 6; local lab page | Five fixed synthetic attempts; four failures, one success | Preserve in automated-abuse module with exact OWASP/PortSwigger preparation |
| `python -m lab.run workflow` | Modules 2–3; local lab page | Completes seven-step account, login, product, reservation, promotion, and challenge workflow | Preserve as fixed-policy baseline; add protected-action and state worksheet |
| `python -m lab.run evasion` | Modules 4, 6–7; local lab page | Changes only `webdriver`; toy score changes from challenge to allow | Retain only as the deliberately limited first experiment; it currently does not send the protected action and must not be presented as coherent evasion |
| `python -m lab.run bypass` | Modules 0, 5, 6–7; local lab page | Baseline `403`; cross-session token replay returns `200` | Preserve as the strongest current end-to-end bypass exercise |
| `python -m lab.run ratelimit` | Modules 5–6; local lab page | Fixed key returns `200, 200, 429`; rotated caller-controlled keys return `200, 200, 200` | Preserve; add workflow-aware replacement and identical retest |
| `python -m lab.run resilience` | Modules 5; local lab page | Runs five cheap and five expensive calls, but observed median ratio was only `1.01` in this environment | Rebuild; client latency currently swamps the intended cost evidence |
| `python -m lab.analysis.analyze` | Module 4; local lab page | Deterministic 4 TP, 0 FP, 6 TN, 0 FN on a ten-record fixture | Preserve as a transparent target-analysis exercise, not the learner's identity |
| `npm run playwright:foundation` | Modules 1 and 3; local lab page | Saves six local request/response events and proves the unauthenticated reservation | Move the authorization finding to automated abuse; replace Foundation with a non-Docker static-app workflow |

## Safety assets to preserve

- Exact local hostname allowlist in `lab/safety.py`
- Hard duration, concurrency, request-rate, total-request, and
  expensive-request ceilings
- Compose port bound to `127.0.0.1`
- Compose `internal: true` network
- Fixed synthetic identities and credentials
- Bounded FastAPI inputs and bounded CPU work
- Challenge replay and rate-key weaknesses clearly marked as intentional
- Unit tests that reject public/private/arbitrary targets
- Generated telemetry excluded from Git

## Instructional defects confirmed

1. The landing page displays Docker commands before browser and HTTP
   prerequisites.
2. `COURSE.md` is one page of more than 2,500 lines.
3. Foundation assignments mix mutually exclusive routes instead of naming one
   primary source and one optional alternate.
4. The browser Foundation exercise is an application authorization flaw, not a
   browser-evasion lesson.
5. The one-property detector bypass changes a score but does not execute the
   protected action.
6. The resilience runner lacks useful server/resource evidence in this
   environment.
7. Source type, assigned section, version sensitivity, and synthesis provenance
   are not represented consistently.
8. Broad Nmap, pivoting, generic AI red-team, CAPTCHA-development, and advanced
   exploitation material distract from the core sequence.
9. Many commands lack a complete explanation/output/interpretation/failure/
   cleanup frame.
10. Experimental method appears throughout the old course but is not a
    first-class prerequisite before the earliest attacks.

## Browser/navigation capture

The strict pre-rewrite rendering is archived as `archive/v1-course/index.html`
and `archive/v1-course/COURSE.html`. The in-app browser connection failed during
capture because its runtime could not initialize; the archived strict render is
the required rendered copy and preserves the exact navigation and content.

## Rewrite decisions

- Replace the monolith with the specification's `docs/` lesson tree.
- Keep one canonical path. Checkpoint pages will only link to canonical lessons.
- Use exact, source-first assignments and short role-specific bridges.
- Restore useful historical templates only where they support a required
  artifact.
- Introduce the non-Docker Playwright exercise before Compose.
- Teach control reconnaissance before evasion and resource modeling before
  load generation.
- Preserve local-only controls and make cleanup/abort behavior visible in every
  lab.

