# Workflow-authorization lab

- Authorization boundary: local synthetic API only
- Target: `http://localhost:8080`
- Objective: reserve one unit without an authenticated account
- Protected action: `POST /api/cart/reserve`
- Baseline: inventory `demo-1` has five units after reset
- Hypothesis: caller-supplied JSON `identity` is not bound to authentication
- Changed variable: authentication is omitted
- Fixed variables: product, quantity, reset state, target, client, evidence schema
- Success: response accepts the reservation and product state changes 5 -> 4
- Evidence: `lab/telemetry/workflow-authorization.json`
- Limitation: intentionally vulnerable synthetic code; browser variation is irrelevant
- Cleanup: reset the API and close the Browser
- Remediation: derive identity from authenticated server state and authorize the action
- Retest: repeat the same unauthenticated request and verify rejection plus inventory 5

With the local API healthy, execute:

```powershell
npm run playwright:workflow-authorization
```

The terminal names the protected state change and artifact. The script is
headless because browser operation was already learned in Module 03; this lesson
tests application authorization, not browser evasion.
