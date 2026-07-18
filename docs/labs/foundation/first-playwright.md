# First Playwright workflow

The source is `lab/clients/playwright/first_workflow.ts`. It launches Chromium,
creates one clean context and Page, attaches local request/response listeners,
searches the Foundation static site, asserts the rendered result, records local
storage, writes JSON evidence, and closes its resources.

## Boundary and objective

- Authorization boundary: the fixed repository-owned loopback application
- Target: `http://127.0.0.1:4173`
- Objective: reproduce and explain the normal workflow
- Protected action: none; this is the automation baseline
- Baseline: the manual DevTools trace from Module 01
- Hypothesis: stock headed Playwright reproduces the same local result and state
- Changed variable: manual operation becomes stock headed Playwright
- Fixed variables: target, query, inventory, context defaults, page, frame, worker, and evidence schema
- Success: exact result and storage value plus paired local events
- Evidence: `lab/telemetry/playwright-first-workflow.json`
- Limitation: a normal workflow does not prove evasion or authorization impact
- Remediation: not applicable; failures are corrected in the client/fixture
- Retest: reset storage and repeat the identical query and artifact fields

## Execute and expected output

With the static server already active, this command starts the headed learner
workflow:

```powershell
npm run playwright:first
```

The browser visibly searches for `widget`. The terminal prints the synthetic
result, stored query, and number of local events. Event interleaving may differ
slightly by browser version.

## Cleanup, limitation, and retest

The script closes the Browser; stop the static server with Ctrl+C. This proves a
reproducible local browser workflow, not evasion or authorization failure. Retest
by repeating the same query and comparing the same artifact fields.
