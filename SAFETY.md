# Safety policy

AATE exists to study adversarial traffic without exposing third parties or users to risk.

## Non-negotiable boundaries

- Run clients and generated traffic only against `localhost`, `127.0.0.1`, `::1`, or repository-approved Docker Compose service names.
- Use synthetic accounts, inventory, promotions, sessions, and telemetry.
- Keep the hard-coded duration, concurrency, rate, and total-request ceilings enabled.
- Define monitoring, abort thresholds, an owner, and recovery validation before a bounded load run.
- Stop immediately if the target is ambiguous, telemetry is unavailable, or unexpected impact appears.

The repository does not include an override for remote targeting. It does not include proxy rotation, CAPTCHA solving, credential material, production targets, raw packet floods, spoofing, reflection, amplification, malware, or a universal stealth browser.

## Engagement test

Before running an experiment, be able to answer:

1. Who authorized it?
2. Which exact local components are in scope?
3. What objective and hypothesis justify the traffic?
4. What are the hard caps and abort conditions?
5. Who watches service health and how is recovery verified?
6. What evidence is retained, sanitized, and deleted?
7. What remediation and retest would make the result useful?

A test that creates uncontrolled impact is a failed engagement, regardless of whether it demonstrates a technical condition.

Report safety defects through [SECURITY.md](SECURITY.md).

