# Synthetic finding: challenge token replays across sessions

> Synthetic educational finding against the bundled local target; not a production assessment.

## Summary

The protected report accepts a challenge token issued to a different synthetic session, allowing an attacker who captures one valid token to replay it for another session.

## Evidence

`python -m lab.run bypass` first requests the report without a token and receives `403`. It solves the local challenge as `solver-session`, captures the returned token, then supplies that token while requesting the report as `attacker-copy`. The protected action returns `200`, proving that the control does not bind the token to the requesting session.

## Impact

Inside this toy workflow, one solved token authorizes other synthetic sessions and can be reused. The experiment does not establish that any external or production system has the same weakness.

## Recommendation

Issue an unpredictable server-generated token bound to the authenticated session, protected action, nonce, and short expiry. Track one-time use server-side and reject a token when any binding differs.

## Retest

Repeat the exact cross-session replay. The solver session should receive `200` for the intended action once; `attacker-copy`, a second use, an expired token, a different action, and a modified token should each receive `403`.

## Limitations

The answer, token, sessions, target, and data are deliberately synthetic. No CAPTCHA service, customer account, external control, or production traffic was tested.
