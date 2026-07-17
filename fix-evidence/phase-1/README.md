# Phase 1 fix evidence

This directory contains the complete local evidence for the targeted safety
repair. It does not contain Phase 2 work, a push, or a deployment.

## Starting point

- Branch: `fix/audit-remediation`
- Commit: `e33b9751f67030b2a1da9e4ffd7b4f83bbda0b3d`
- The repository was already dirty. `starting-state.txt` records branch, commit,
  full short status, and diff stat before Phase 1 files were created.

## Evidence index

| File | Command/result |
|---|---|
| `starting-state.txt` | Starting Git branch, commit, status, and diff stat; all exit 0 |
| `preflight-tests.txt` | Initial 20-test boundary preflight; exit 1 on unsupported-scheme redirect |
| `post-fix-preflight-tests.txt` | Corrected 20-test boundary preflight; exit 0 |
| `quality-preflight.txt` | `python -m ruff/mypy` unavailable in target-style install; exits 1 preserved |
| `quality-binary-preflight.txt` | Ruff exit 0; initial MyPy exit 1 on test class attributes |
| `tool-setup.txt` | Pinned pytest and PyYAML temporary-tool installs; exit 0 |
| `acceptance-attempt-1-summary.txt` | First full gate: source validator exit 1 for missing PyYAML; other commands exit 0 |
| `validate-sources-attempt-1.txt` | Complete missing-PyYAML failure transcript |
| `acceptance-summary.txt` | Final ten-command gate; every exit 0 |
| `pytest.txt` | 38-dot pytest run; exit 0 |
| `unittest.txt` | 38 verbose tests; exit 0 |
| `ruff.txt` | `ruff check .`; exit 0 |
| `mypy.txt` | repository Makefile equivalent `mypy lab scripts`; exit 0 |
| `validate-sources.txt` | 48 ledger entries / 50 lessons; exit 0 |
| `validate-lessons.txt` | 50 lessons / 11 indexes / Foundation gates; exit 0 |
| `validate-labs.txt` | lab contracts, 29 command records, sample finding; exit 0 |
| `validate-load-scripts.txt` | bounded-load structural validator; exit 0 |
| `internal-links.txt` | 103 Markdown files; exit 0 |
| `mkdocs-build.txt` | strict rendered build; exit 0 |
| `scope-review.txt` | Phase 1 diff/status scope and scoped whitespace check; exits 0 |
| `global-diff-check.txt` | informational whole dirty-tree check; exit 2 on pre-existing Markdown whitespace |
| `precommit-check.txt` | staged names/status and all-files staged check; exit 2 only because verbatim evidence retains emitted whitespace |

Every command transcript records the displayed command, UTC start/end,
stdout, stderr, and exit status. The acceptance mappings use the pinned tools
already installed under `C:\tmp`: a bundled Python 3.12 runtime, executable
Ruff/MyPy entry points, and the MkDocs 1.6.1 environment. The source commands
remain the same commands declared by the repository; only the executable path
is made explicit.

`git diff --cached --check` is intentionally not presented as passing: raw
evidence files contain exact output lines with trailing spaces. The scoped check
over Phase 1 implementation and documentation files is the relevant code-quality
check and returned exit 0. Reformatting transcripts would violate the evidence
requirement.

## Safety proof

The verbose test transcript names each required redirect case. Every redirect
test first contacts only a loopback in-process HTTP server. A `SafetyError` is
raised on the first 3xx response, so no redirect destination is resolved or
contacted. The slow-response test uses that same local server and proves the
network timeout is bounded by the monotonic deadline. Deterministic clock tests
prove timeout calculation and refusal to start a later request.

The dependency downloads recorded in `tool-setup.txt` were test-tool setup, not
safe-client or lab target traffic. The final acceptance run itself made no
external lab/client request and no meaningful load.
