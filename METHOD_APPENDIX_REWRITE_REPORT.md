# Method appendix curriculum-order correction report

## Summary

The required technical path now begins with Module 01 and [HTTP request and
response](docs/modules/01-http-edge/01-http-request-response.md). The former
Module 00 content remains at its published URLs as the optional **Red-team
method and engagement practice** appendix. Modules 01 through 10 were not
renumbered.

This was a curriculum-order correction, not a course rewrite. Existing
source-first instruction, beginner explanations, self-contained exercises,
`Check your understanding` sections, bullet-list answer keys, and the absence
of mandatory per-lesson artifacts were preserved.

## Files changed

- Curriculum metadata and validation:
  `curriculum/manifest.yaml`, `scripts/validate_curriculum.py`,
  `scripts/validate_lessons.py`, and `sources/sources.yaml`
- Entry path and public summaries: `README.md`, `docs/index.md`,
  `docs/start-here.md`, `docs/path.md`, `docs/progress.md`, and
  `COVERAGE_AUDIT.md`
- Navigation: `mkdocs.yml`
- Appendix pages: `docs/modules/00-method/index.md` and its three lesson pages
- Technical indexes and lessons: Module 01 index and first lesson, Module 05,
  Module 06, Module 08, and Module 10 indexes, Python telemetry, and the final
  mock-loop lesson
- Checkpoints: all four pages under `docs/checkpoints/`
- Lab maps and entry text: `lab/LAB_COURSE_MAP.md`, its synchronized public
  copy, and `lab/README.md`
- This report

## Former Module 00 pages reclassified

| Stable public path | New classification | Estimate |
|---|---|---:|
| `docs/modules/00-method/01-red-team-role.md` | Optional appendix lesson: The authorized red-team role | 75 minutes |
| `docs/modules/00-method/02-scope-and-rules.md` | Optional appendix lesson: Scope and Rules of Engagement | 90 minutes |
| `docs/modules/00-method/03-experimental-method.md` | Optional appendix lesson: Experimental method before attack execution | 100 minutes |

The appendix total is **265 minutes (4.42 hours)** and is excluded from core
lesson counts, depth counts, prerequisites, and checkpoint time. Each appendix
lesson retains its source basis, full instruction, worked example, optional
exercise, check for understanding, bullet answer key, and a return link to the
core HTTP start.

The appendix index also links the existing methodology provenance,
authorization and safety background, AATE adversarial-control loop, and
experiment-design references. No methodology page or former lesson was deleted.

## Core prerequisite references removed

| Core lesson or command | Removed dependency | Replacement |
|---|---|---|
| `m01-l01` - HTTP request and response | `m00-l03` | No prior course lesson; this is the root core lesson |
| `m08-l01` - Resource-exhaustion model | `m00-l02` | Keeps the real technical prerequisite `m01-l02` |
| `m09-l01` - Python telemetry as evidence | `m00-l03` | No prior lesson; the offline JSONL fixture and assigned Python material are self-contained |
| HTTP page progress box | Visible Module 00 prerequisite | Browser, then Python only when the local server command is reached |
| Python telemetry progress box | Visible Experimental method prerequisite | Local fixture plus the assigned Python/JSON instruction |
| Static-site command map | Completed scope lesson | Python 3.12+; no earlier course lesson |
| Compose startup command map | Modules 00-03 | Modules 01-03 |
| Bounded k6 command map | Modules 00-08 | Modules 01-08 |

All former `m00-l01`, `m00-l02`, and `m00-l03` rows were removed from every
checkpoint closure table. The two safe-client demonstrations remain available
inside the optional scope appendix and are labeled as optional, not Foundation
requirements.

## Core pages made self-contained

- Control Reconnaissance defines its baseline, changed variable, fixed
  variables, protected-action success condition, alternative explanation, and
  exact retest on the module index.
- Browser Evasion defines the same experiment frame for one-property and
  coherent-set treatments without requiring formal appendix study.
- DDoS and Resilience defines the bounded comparison, fixed caps, success and
  abort boundary, alternatives, recovery, cleanup, and identical retest. Its
  external-assessment callout recommends the optional scope appendix without
  gating the local course.
- Findings and Interview defines observation/evidence, the affected baseline,
  changed input or invariant, authoritative success condition, competing
  explanation, limitation, and exact retest. The optional appendix is
  recommended for interview-method review only.

No generic methodology lesson was inserted into the required sequence.

## New core first lesson and navigation

- `m01-l01` is first in the canonical `lessons` list and has
  `prerequisites: []`.
- Start Here links directly to HTTP request and response.
- The canonical module table begins at 01.
- The primary navigation begins with Start Here, Path and Checkpoints, HTTP and
  Edge, Browser and JavaScript, and Playwright.
- Former method pages and methodology references appear near the bottom under
  Optional Appendices.
- Safety remains its own visible top-level navigation section.

## Checkpoint closure times before and after

| Checkpoint | Before direct | Before closure | After direct | After closure | Closure change |
|---|---:|---:|---:|---:|---:|
| 24 focused hours | 1 lesson / 180 min | 12 lessons / 1,300 min (21.67 h) | 2 lessons / 285 min | 11 lessons / 1,250 min (20.83 h) | -50 min |
| 7 days | 3 lessons / 540 min | 18 lessons / 2,235 min (37.25 h) | 4 lessons / 645 min | 15 lessons / 1,970 min (32.83 h) | -265 min |
| 21 days | 6 lessons / 960 min | 31 lessons / 4,275 min (71.25 h) | 7 lessons / 1,065 min | 28 lessons / 4,010 min (66.83 h) | -265 min |
| 6 weeks | 10 lessons / 1,800 min | 47 lessons / 7,195 min (119.92 h) | 11 lessons / 1,905 min | 44 lessons / 6,930 min (115.50 h) | -265 min |

Optional appendix study is not included in any checkpoint time.

## Foundation technical rebalance

The old 24-hour endpoint selected the first local Playwright workflow
(`m03-l02`). The new endpoint also selects network events and evidence
(`m03-l04`), whose prerequisite closure adds:

- Browser contexts and storage state (`m03-l03`): 110 minutes
- Network events and evidence (`m03-l04`): 105 minutes

Those 215 directly relevant technical minutes replace most of the 265 minutes
moved out of the Foundation closure. The resulting 1,250-minute closure remains
inside the declared 20-to-24-hour range without estimate padding or appendix
membership.

## Validator changes

`scripts/validate_curriculum.py` now:

- validates 47 core lessons and three appendix lessons separately;
- requires the core list and prerequisite graph to start at `m01-l01`;
- requires `m01-l01` to have no prerequisite;
- rejects core prerequisites or checkpoints that reference appendix IDs;
- excludes appendix estimates and lessons from core depth and closure totals;
- validates appendix paths, source IDs, title/estimate agreement, index
  membership, and return links to the HTTP start; and
- prints separate core and optional-appendix summaries.

`scripts/validate_lessons.py` excludes `docs/modules/00-method/` from the core
module contract and applies a separate appendix contract. It retains full
source, instruction, worked-example, optional-exercise, assessment, and
bullet-answer checks without requiring core depth, checkpoint, prerequisite, or
mandatory Next-lesson semantics.

## Lab-map changes and retained safety

The private and public lab maps remain byte-for-byte synchronized. Local
commands no longer require former Module 00 work. Where formal engagement
planning is useful, the maps label the red-team method appendix as optional
review.

No executable safety control changed. Runnable pages and command records retain
their destination restrictions, hard caps, expected output, failure guidance,
cleanup, and retest guidance. Code-level loopback validation, redirect
rejection, timeouts, traffic ceilings, abort thresholds, and bounded retries
were not modified. Start Here displays a prominent safety boundary, and Safety
remains a top-level section.

## Stale-reference search

The tracked-tree searches for `Module 00`, `module-00`, `m00-l`, `method ->
HTTP`, `Begin with the authorized red-team role`, `Method and authorization`,
`required before HTTP`, and the four specified dependency phrases returned no
current match after the correction.

Matches for the stable directory name `00-method` were classified as expected:

- optional appendix metadata and links;
- the two optional safe-client command-map records;
- validator constants identifying the appendix directory; and
- optional recommendations from DDoS or interview review.

No core prerequisite or checkpoint uses that directory or an appendix lesson.
Source-ledger references formerly named `module-00` now use
`appendix-red-team-method`.

## Validation results

| Validation | Result |
|---|---|
| `python scripts/validate_sources.py` | Pass: 48 sources, 50 attributed lessons |
| `python scripts/validate_lessons.py` | Pass: 47 core lessons, 10 core indexes, 3 appendix lessons |
| `python scripts/validate_assessments.py` | Pass: 246 questions and sequential bullet answers |
| `python scripts/validate_labs.py` | Pass: 11 lab pages, 29 synchronized command records |
| `python scripts/validate_load_scripts.py` | Pass |
| `python scripts/validate_curriculum.py` | Pass: root, appendix exclusion, graph, depth, and all closure gates |
| `python scripts/check_internal_links.py` | Pass: 101 Markdown files checked |
| `python -m pytest lab/tests -q` | Pass: 45 tests |
| `ruff check .` | Pass |
| `mypy .` | Pass: 37 source files |
| `npm test` | Pass: 6 tests |
| `npm run lint` | Pass |
| `npm run format:check` | Pass |
| `npm run typecheck` | Pass |
| `npm run markdown:lint` | Pass before this report; rerun in the final pass |
| `npm run playwright:foundation` | Pass with the bundled Python path supplied through `AATE_PYTHON` |
| `mkdocs build --strict` | Pass |
| `python scripts/scan_public_tree.py` | Pass: 184 tracked paths after staging; no secret, privacy, or employer markers |

The first Foundation smoke invocation could not resolve a `python` executable
from `PATH`; the documented `AATE_PYTHON` override was set to the bundled Python
runtime and the required smoke test then passed.

## Rendered-page review

The strict build was served only on `127.0.0.1` for visual inspection. The
following rendered pages were reviewed:

1. Course home
2. Start Here
3. Canonical Path
4. 24-hour checkpoint
5. HTTP and Edge index
6. HTTP request and response
7. Browser and JavaScript index
8. First local Playwright workflow
9. Control Reconnaissance index
10. Browser Evasion index
11. DDoS and Resilience index
12. Findings and Interview index
13. Optional appendix index
14. Authorized red-team role appendix
15. Scope and Rules of Engagement appendix
16. Experimental method appendix
17. Safety

The desktop Material layout rendered without clipping or broken structure.
Representative screenshots confirmed the prominent Start Here safety callout
and the structured optional appendix guide. DOM inspection confirmed HTTP as the
first required lesson, Optional Appendices and Safety as separate navigation
sections, the revised 24-hour timing and technical selections, visible optional
status on every appendix lesson, and core-return links on every appendix page.

## Known limitations

- Visual and runnable review used only the bundled loopback targets. No public,
  provider-hosted, organization-owned, or production service was contacted.
- The repository keeps the `docs/modules/00-method/` directory name solely to
  preserve published URLs; learner-facing titles no longer classify it as a
  required numbered module.
- Appendix methodology references are navigation resources rather than
  canonical core lessons and therefore do not receive depth or checkpoint
  metadata.
