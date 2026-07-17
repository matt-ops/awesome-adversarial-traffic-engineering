# Safety and authorization

Learn offensive techniques only in an environment where the owner explicitly authorizes them.

## Allowed environments

- The bundled AATE lab on `localhost`
- A self-hosted target on an isolated private network you control
- The exact target assigned by a training provider, under that provider’s rules
- An organization-owned test environment covered by a separate written authorization

Authorization is specific. Access to one assigned machine does not authorize adjacent hosts, the provider’s website, or the public Internet.

Passive recon can reveal candidate assets without contacting them; discovery does not place them in scope. Active recon—including crawling, service/port scanning, content discovery, parameter discovery, and control fingerprinting—sends traffic and requires explicit target, technique, rate, and time authorization.

## Allowed course work

Inside an allowed environment, the course includes passive research, bounded active reconnaissance, request capture/replay, synthetic credential attacks, account/workflow abuse, browser automation, private proxy comparisons, challenge testing, fingerprint-evasion comparisons, WAF/bot-control testing, AI-agent experiments, and bounded resilience testing.

Deep packet, spoofing, reflection, amplification, and connection-state exercises require a non-routable isolated topology with no bridge to Wi-Fi, Ethernet, VPN, cloud VPC, or the Internet. Prove isolation before generating traffic.

## Never do this

- Test an unrelated public or production service
- Use real stolen/leaked credentials or customer data
- Send denial-of-service traffic over a routed or shared network
- Operate malware, botnets, persistence, or public attack infrastructure
- Use public proxies without authorization
- Escape a provider’s assigned range or bypass its safeguards
- Disable target allowlists, hard caps, timeouts, abort conditions, or cleanup
- Present a synthetic detector or lab result as production proof

## Bundled lab limits

The included client accepts only local targets and enforces:

- exact fixed origins: `http://localhost:8080`, `http://127.0.0.1:8080`,
  `http://app:8000`, and `http://edge:8080`
- rejection of every redirect, including local-to-local redirects
- 15 seconds maximum duration
- a monotonic wall-clock deadline; no request starts after it expires
- a two-second maximum per-request timeout, reduced to the remaining duration
  budget when that is smaller
- 5 maximum concurrency
- 10 requests/second maximum rate
- 100 maximum total requests
- 20 maximum expensive requests

The broader `validate_local_url()` helper accepts arbitrary valid ports only for
controlled local development and in-process tests. The executable course client
uses the stricter fixed-origin policy, and neither exposes a flag that disables
redirect or destination validation.

Course exercises usually use much less. A run that consumes its deadline records
`duration_budget_exceeded`; it does not silently start another request. Stop
immediately on an unexpected status, failed health check, breached limit, or
owner request.

## Before every run

Write down: owner, target, allowed passive sources, allowed active discovery, allowed attack, data, request/rate/concurrency cap, abort condition, expected result, and cleanup. Keep newly discovered adjacent assets out of scope until the owner adds them. Run the smallest useful test first. Preserve evidence without secrets. Reset state and stop services when finished.
