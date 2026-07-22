# Challenge systems and protected-action enforcement lab

- Authorization boundary: bundled synthetic loopback application only
- Target: `http://localhost:8080`
- Objective: map challenge trigger through protected-action enforcement, then
  compare cross-session and repeat-use proof behavior
- Protected action: `GET /api/reports/protected` completes one bounded synthetic report
- Baseline: Session B receives `403` without accepted proof
- Hypothesis: Session A's proof is transferable to Session B and remains reusable
- Changed variable: presence of the same captured synthetic proof in Session B
- Fixed variables: target, endpoint, `work=10`, Session A/Session B names,
  answer, request order, reset state, and evidence fields
- Success: protected endpoint returns `200` with `session-b` on first and second presentation
- Evidence: HTTP response sequence plus browser document/script/network/storage/callback trace
- Limitation: fixed answer and bearer token; no visual widget, iframe, expiry,
  second challenge-gated action, risk engine, or external provider
- Cleanup: call `/api/reset`, close browsers, and stop the course Compose stack
- Remediation: bind unpredictable proof to session, action, origin, nonce,
  expiry, and atomic one-use consumption at every protected server path
- Retest: reject both Session B presentations while allowing Session A once before expiry

The initial executable endpoints are `POST /api/challenge` and
`GET /api/reports/protected`.

## Start and reset

Use the [local API lifecycle](local-api.md), confirm `/health`, and reset state.
The page and both runners use constants for the loopback target; no command
accepts an external target argument.

## HTTP lifecycle

```powershell
python -m lab.run bypass
```

Expected sequence:

| Phase | Expected status | Protected evidence |
|---|---:|---|
| Session B blocked baseline | 403 | `synthetic challenge required` |
| Session A synthetic solve | 200 | proof response names `session-a` |
| Session B first presentation | 200 | protected response names `session-b` |
| Session B identical second presentation | 200 | protected response again names `session-b` |

The final output names the absent session, action, origin, nonce, expiry, and
one-use properties, then states the negative and legitimate-positive retest.

## Browser trace

```powershell
npm run playwright:challenge-flow
```

The fixed Playwright client opens two isolated BrowserContexts. It traces the
challenge-triggering request, `/challenge-lab` document, `/challenge-lab.js`,
API traffic, cookie/local/session-storage key names, form callback, proof
production, protected verification point, and final action. The trace states
that the fixture contains no visual CAPTCHA widget or iframe; it does not invent
commercial branding or a proprietary protocol.

The generated JSON is optional diagnostic evidence ignored by Git. The learner
does not have to preserve or submit an artifact to complete the lesson.

## Deterministic economics and customer impact

```powershell
python -m lab.analysis.challenge_metrics
```

The small synthetic fixture compares a manual legitimate user, a composite
legitimate automation/accessibility-like near-neighbor, a stock automated
attacker, and an adapted/replaying attacker. It calculates challenge issuance,
solve/bypass, protected completion, abandonment, added latency, repeat challenge,
attacker time/cost, legitimate false positives, near-neighbor impact, and
stopped-versus-displaced outcomes.

The composite row is a test proxy, not evidence about actual disabled people,
privacy-tool users, or production test automation. Interpret the exact fixture
only: the stock client is mostly stopped, while adapted replay is cheap and some
abuse moves to another workflow.

## Exact remediation retest

After a future remediated fixture exists, repeat the same reset and request order:

1. Session B without proof remains `403`.
2. Session A produces proof for the exact protected report.
3. Session B's first transfer receives `403`.
4. Session B's repeated transfer receives `403`.
5. Session A's intended request succeeds once before expiry.
6. Session A's identical second use receives `403`.

Cross-action and expired-use experiments are planned, not executable in the
current fixture. Add them only after a distinct protected action and controllable
clock exist.
