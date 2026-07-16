# Control-reconnaissance and one-variable lab

- Authorization boundary: local synthetic API only
- Target: `http://localhost:8080`
- Objective: map three browser contexts and a transparent control, establish
  stock baselines, change one property, and prove one protected action
- Protected action: create one synthetic report through `/api/control/protected`
- Baseline: stock headed and headless Playwright are challenged
- Hypothesis: the toy control overrelies on top-page `navigator.webdriver`
- Changed variable: top-page value only, after document load
- Fixed variables: target, workflow, locale, timezone, viewport/screen, frame,
  worker, request path, and action
- Success: decision changes to allow and protected action returns `200`
- Evidence: `lab/telemetry/control-recon.json`
- Limitation: transparent toy rules; one property is not a coherent identity
- Cleanup: endpoint tokens are reset and browsers close
- Remediation: never rely on one property; combine server-enforced workflow and
  replay controls with governed, tested signals
- Retest: repeat identical stock and changed trials after the rule change

With the local API healthy, the HTTP-only comparison uses the bounded client:

```powershell
python -m lab.clients.safe_client --target http://localhost:8080/control-lab --duration 1 --rps 1 --total 1
```

The browser populations and local action use:

```powershell
npm.cmd run playwright:control-recon
```

The learner command launches a visible headed population, then headless and
one-variable populations. Automated verification may set `AATE_HEADLESS=1`; the
artifact records actual and requested launch modes so that forced verification
cannot be mislabeled as a genuine headed observation.

