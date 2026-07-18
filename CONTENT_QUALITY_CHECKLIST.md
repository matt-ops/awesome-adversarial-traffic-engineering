# Content quality and acceptance checklist

This checklist implements Sections 16, 17, and 19 of the authoritative rewrite
specification. Automated checks support review; they do not replace reading the lessons.

## Instructional integrity

- [x] Method precedes attacks; HTTP, browser, DOM, JavaScript, and Playwright precede Docker.
- [x] Every lesson has one typed source block and exact external assignment fields.
- [x] Every lesson has a worked example, guided exercise, expected output,
  interpretation, failure modes, cleanup, artifact, pass gate, explained answer key, and next link.
- [x] Every Foundation lesson contains an authoritative assignment and a diagram or comparison table.
- [x] All eleven module indexes expose Foundation, Applied, Integrated, and Deep sections.
- [x] Course synthesis, lab-specific behavior, vendor/research limits, and version-sensitive observations are labeled.
- [x] The fifteen-step method has step-by-step provenance.
- [x] The monolithic course page is removed from navigation and from the public release tree.
- [x] No core lesson asks the learner to locate their own resource.
- [x] No code block longer than 20 lines appears without being split into a taught outcome.

## Offensive alignment

- [x] Learner objective is adversary emulation and protected-action/service-effect proof.
- [x] Detection content is framed as control reconnaissance and trusted-signal analysis.
- [x] Workflow authorization is taught as an application abuse finding, not browser evasion.
- [x] Browser evasion requires a blocked baseline and progresses through one-variable,
  coherence, replay/temporal, protocol, and drift work.
- [x] Score/fingerprint changes are distinguished from protected impact and identity proof.
- [x] Residual anomalies, legitimate near-neighbors, alternate explanations, and limitations are required.
- [x] Remediation invariants and exact same-attack retests are required.

## Lab and command quality

- [x] Every learner lab states authorization, target, objective, protected action,
  baseline, hypothesis, variables, success, evidence, limitations, cleanup, remediation, and retest.
- [x] `lab/LAB_COURSE_MAP.md` maps every active or preserved compatibility command.
- [x] First browser lab uses a static loopback target without Docker.
- [x] Local API and state weaknesses remain synthetic and explicitly limited.
- [x] Target allowlisting and traffic envelopes execute before repeated work.
- [x] k6 scripts enforce local target, duration, VU, effective-rate, worst-case-total,
  threshold, abort, dry-run, and recovery controls.
- [x] Expected output and cleanup appear beside the assigning command or linked lab contract.

## Learner usability

- [x] Landing page has one primary action: Start the path.
- [x] README reduces use to start, complete, and follow Next.
- [x] Progress is a plain copyable table; no account or platform is required.
- [x] Checkpoints are cumulative views linking module depth sections, not duplicate lessons.
- [x] Foundation checkpoint makes the minimum informational-readiness claim and rejects expertise claims.
- [x] Resources are labeled Required, Required provider lab, Alternate, or Elective.
- [x] Broad recon, WAF/parser bypass, AI agents, CAPTCHA solvers, raw L3/L4,
  pivoting, and advanced exploitation have readiness-labeled external routes.

## Final automated evidence

- [x] Source ledger validator passes.
- [x] Lesson and module-depth validator passes.
- [x] Lab-contract validator passes.
- [x] Internal-link validator passes.
- [x] External-link pass distinguishes permanent/malformed failures from transient warnings.
- [x] Load-script safety validator passes.
- [x] Python unit tests pass.
- [x] Fast JavaScript/TypeScript unit tests pass without launching a browser.
- [x] ESLint and Prettier checks pass.
- [x] Markdown lint passes with explicit course-format exceptions.
- [x] mypy and Ruff pass.
- [x] TypeScript type check passes.
- [x] Docker Compose configuration parses.
- [x] All seven k6 scenarios and dry-run evidence remain recorded as passing.
- [x] MkDocs strict build passes.
- [x] `PUBLISH_CHECKLIST.md` records release gates, known review boundaries, and the human-review order.

## Restriction-gap result

`COVERAGE_AUDIT.md` requires each target capability to end in full course
instruction, an exact mature external assignment, or an explicit out-of-role
exclusion. No capability may end in a generic paragraph, tool list, or learner-led search.
