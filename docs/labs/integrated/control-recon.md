# Control-reconnaissance and one-variable lab

- Authorization boundary: local synthetic API only
- Target: `http://localhost:8080`
- Objective: map three browser contexts and a transparent control, establish
  stock baselines, change one property, prove one protected action, then add a
  frame-only contradiction and show the control decision changes again
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
- Retest: repeat identical stock, changed, and cross-context trials after the rule change

With the local API healthy, the HTTP-only comparison uses the bounded client:

```powershell
python -m lab.clients.safe_client --target http://localhost:8080/control-lab --duration 1 --rps 1 --total 1
```

The browser populations and local action use:

```powershell
npm run playwright:control-recon
```

The learner command launches four fixed trials: stock headed, stock headless,
one-variable, and `cross-context-mismatch`. The third changes only the loaded
top page's `navigator.webdriver` value and proves the protected action. The
fourth begins from that condition, changes only the sensor frame's language to
`fr-FR`, and should be challenged for `cross_context_language_mismatch` without
attempting the protected action.

Automated verification may set `AATE_HEADLESS=1`; the JSON output records actual
and requested launch modes so that forced verification cannot be mislabeled as
a genuine headed observation.

Expected output in `control-recon.json`:

| Population | Expected decision | Protected-action result | Interpretation |
|---|---|---|---|
| `stock-headed` | challenge | not attempted | stock automation baseline |
| `stock-headless` | challenge | not attempted | headless baseline under the same transparent rule |
| `one-variable` | allow | first action 200; token reuse 403 | one toy assumption changed; identity remains incoherent |
| `cross-context-mismatch` | challenge | not attempted | frame-only contradiction remains visible to cross-context collection |
