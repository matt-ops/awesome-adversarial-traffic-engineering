# Learning experience rewrite report

## Scope and rewrite counts

| Measure | Count |
| --- | ---: |
| Canonical lessons reviewed | 50 |
| `Required artifact` sections removed | 50 |
| Progress-record artifact fields removed | 50 |
| Artifact-based lesson prerequisites rewritten | 15 |
| Checkpoint artifact lists removed | 4 |
| Knowledge-check questions rewritten | 246 |
| Answer keys reformatted | 50 |
| Vague scenario questions corrected in the required Sessions and Workflows repair | 5 |
| `required_artifacts` manifest keys removed, including checkpoint entries | 54 |
| Lab-map command records changed from artifact paths to expected output | 29 |

All 50 pass gates are now learner-facing `Check your understanding` sections.
Each lesson has three to five questions, followed by one collapsed answer key
whose numbered bullet count matches the question count. The final corpus contains
246 rewritten questions; the former corpus contained 259 questions.

The Sessions and Workflows rewrite explicitly distinguishes browser storage from
login state, treats the public inventory JSON response as a read rather than a
reservation, rejects a client-supplied identity as proof without an authenticated
session, defines the cross-session approval-token replay proof, and includes the
inventory failure path in the workflow map.

## Estimate review

No lesson estimate changed. Removing the filing requirement did not remove the
natural exercise work, expected result, code, trace, diagram, report, or note that
teaches the lesson. The duration audit therefore found no material change to the
work represented by any lesson estimate.

| Checkpoint | Before | After |
| --- | ---: | ---: |
| 24 focused hours | 1,300 min (21.67 h) | 1,300 min (21.67 h) |
| 7 days cumulative | 2,235 min (37.25 h) | 2,235 min (37.25 h) |
| 21 days cumulative | 4,275 min (71.25 h) | 4,275 min (71.25 h) |
| 6 weeks cumulative | 7,195 min (119.92 h) | 7,195 min (119.92 h) |

The checkpoint closures, prerequisite graph, source references, and lesson depth
distribution are unchanged.

## Validation

The complete required validation suite passed:

| Command | Result |
| --- | --- |
| `python scripts/validate_sources.py` | PASS: 48 sources, 50 lessons, 31 mandated source IDs |
| `python scripts/validate_lessons.py` | PASS: 50 lessons, 11 module indexes, 12 Foundation release pages |
| `python scripts/validate_assessments.py` | PASS: 50 assessments, 246 questions, 0 human-review warnings |
| `python scripts/validate_labs.py` | PASS: 11 lab pages, 29 mapped commands, synchronized maps |
| `python scripts/validate_load_scripts.py` | PASS: one bounded-load script safety configuration |
| `python scripts/validate_curriculum.py` | PASS: manifest structure, graph, depths, and checkpoint closures |
| `python scripts/check_internal_links.py` | PASS: 101 Markdown files checked |
| `python -m pytest lab/tests -q` | PASS: 45 tests |
| `ruff check .` | PASS |
| `mypy .` | PASS: 37 source files |
| `npm test` | PASS: 6 tests |
| `npm run lint` | PASS |
| `npm run format:check` | PASS |
| `npm run typecheck` | PASS |
| `npm run markdown:lint` | PASS |
| `npm run playwright:foundation` | PASS: local page and inventory endpoint returned 200 with expected content |
| `mkdocs build --strict` | PASS |
| `python scripts/scan_public_tree.py` | PASS |

`git diff --check` also passed, and a repository-wide legacy-language scan found
no published `Required artifact`, `Pass gate`, artifact-submission, artifact-path,
or `required_artifacts` requirement outside the validators that intentionally
reject those strings.

## Rendered-page review

The local strict MkDocs build was reviewed in the in-app browser at desktop size.
The review covered Start Here, Progress, all four checkpoint pages, a Foundation
lesson from every module that defines one, and the required special pages. Module
06 has no Foundation-depth lesson, so its earliest available lesson was inspected:

- The authorized red-team role
- Sessions and workflows
- Browser process model
- First local Playwright workflow
- Automated-abuse objectives
- Five signal families
- Form an evasion hypothesis
- One-variable evasion experiment
- TLS ClientHello
- HTTP/2 connections and streams
- Resource-exhaustion model
- Bounded application-layer load testing
- Python telemetry as evidence
- Secure code review through an adversary's path
- Finding and evidence
- Full mock loop

All 22 reviewed pages loaded with navigation and headings, no horizontal overflow,
no 404 state, no legacy requirement wording, and no raw answer-list Markdown. Each
reviewed lesson had one answer disclosure collapsed by default, with four or five
matching numbered answer bullets. The Progress page rendered 50 lesson checkboxes.

Progress, Sessions and Workflows, and the six-week checkpoint were also reviewed
at a 390 by 844 mobile viewport. All three exposed the mobile menu, remained free
of horizontal overflow, and preserved readable content. The Sessions answer key
was expanded on mobile to verify the disclosure and answer bullets visually. The
browser console contained no errors.

## Remaining limitations

- The local Foundation browser smoke test validates the repository's synthetic lab;
  it does not make claims about an external or production system.
- The vague-language validator is a warning heuristic. It complements, but cannot
  replace, the completed lesson-by-lesson human wording review.
- Markdown requires a small MkDocs hook to mark the source-exact answer disclosures
  as Markdown-capable during rendering; lesson source still uses the required exact
  `<details>` and `<summary>Show answers</summary>` structure.

No new modules, sources, labs, attack techniques, or safety behavior were added.
The separate workflow-map artifact patch was not performed.
