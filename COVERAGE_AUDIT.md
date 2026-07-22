# Capability and restriction-gap audit

This audit prevents a capability from disappearing because the repository is too
small to reproduce it or direct instruction would be inappropriate outside a
purpose-built range. “External by design” means the course provides an exact
free/paid route instead of a shallow paragraph or empty assignment.

## Core role coverage

| Capability | Direct instruction | Demonstration/evidence | Status |
|---|---|---|---|
| Authorized offensive method and attack lifecycle | [Optional red-team method appendix](docs/modules/00-method/index.md) plus concise experiment frames inside relevant technical lessons | executable target rejection, local safety boundaries, and complete optional experiment plan | Optional depth; minimum technical method remains core and self-contained |
| HTTP, sessions, workflows, edge path | [Module 01](docs/modules/01-http-edge/index.md) | DevTools trace and request-path diagram | Core complete |
| Browser processes, DOM, Web APIs, JavaScript async | [Module 02](docs/modules/02-browser-javascript/index.md) | static page/frame/worker/fetch exercises | Core complete |
| Browser automation and evidence | [Module 03](docs/modules/03-playwright/index.md) | headed local workflow and network trace | Core complete |
| Automated abuse taxonomy and protected workflows | [Module 04](docs/modules/04-automated-abuse/index.md) | credential, inventory, promotion, rate-key, and provider assignments | Core complete |
| Immediate recon for a specific attack/control | [workflow mapping](docs/modules/04-automated-abuse/02-workflow-mapping.md) and [Module 05](docs/modules/05-control-recon/index.md) | route inventory, population matrix, blocked baseline, ranked hypothesis | Core complete |
| Bot-control signal reconnaissance | [Module 05](docs/modules/05-control-recon/index.md) | manual/headed/headless/HTTP plus top/frame/worker evidence | Core complete |
| Browser-control evasion and bypass proof | [Module 06](docs/modules/06-browser-evasion/index.md) | one-variable, coherence, replay, protected `200`, residual anomalies | Core complete within local target limits |
| Protocol identity foundations and source-led TLS/HTTP/2/HTTP/3 reasoning | [Module 07](docs/modules/07-protocol-identity/index.md) | Python/OpenSSL ClientHello fixtures and loopback plain-HTTP observer; advanced protocols remain evidence plans | Executable foundations complete; no browser TLS, JA4, HTTP/2 settings, HTTP/3, or QUIC capture claim |
| Application-layer resource/control assumptions | [Module 08](docs/modules/08-ddos-resilience/index.md) | seven hard-bounded k6 scenario contracts with named assertions; endpoint/workflow cases are observations | Core local L7 instruction; no endpoint/workflow mitigation or production-capacity claim |
| Python attack tooling, telemetry, concurrency, retries | [Module 09](docs/modules/09-tooling-code-review/index.md) | executed telemetry, concurrency, retry trace, and tests | Core complete |
| Security code review | [secure code review](docs/modules/09-tooling-code-review/04-secure-code-review.md) | four input-to-effect reviews and regression designs | Core complete |
| Findings, remediation, retest, briefing, collaboration | [Module 10](docs/modules/10-findings-interview/index.md) | finding, acceptance matrix, briefing, narrative, full mock | Core complete |

## Capabilities routed to mature external instruction

| Capability not realistically reproduced by the normal lab | Exact route | Why it is not silently omitted |
|---|---|---|
| Broad web recon before exploitation | [OWASP WSTG free route or HTB paid route](docs/references/electives.md#broader-web-reconnaissance) | Core teaches immediate attack-specific recon; elective adds DNS/subdomain/archive/technology scope |
| Real WAF/parser bypass | [PortSwigger plus self-hosted Coraza/CRS](docs/references/electives.md#waf-and-proxy-parsing-bypass) | Mature parser chains, rules, and audit evidence replace an unrealistic toy claim |
| Credential attacks using realistic provider fixtures | [PortSwigger or HTB](docs/references/electives.md#credential-attacks-at-realistic-scale) | No stolen, leaked, or customer credentials enter the repository |
| Commercial-like second browser control target | [BotD or Rebrowser](docs/references/electives.md#browser-anti-fingerprinting-research-target) | Transfer is tested against a pinned self-hosted implementation with explicit limitations |
| AI-powered browser attacker | [Playwright MCP or BrowserGym](docs/references/electives.md#ai-powered-browser-adversaries) | The learner first masters deterministic Playwright, then measures model planning/action traces |
| Visual CAPTCHA solver development | [provider-supplied paid course](docs/references/electives.md#captcha-solver-development) | Core teaches challenge workflow, binding, and replay; ML solver work uses supplied targets/data |
| Raw L3/L4 pressure, spoofing, TCP state | [SEED isolated labs](docs/references/electives.md#l3l4-pressure-spoofing-and-tcp-state-attacks) | Purpose-built non-routable topology replaces raw tooling in the ordinary repo |
| Proxy routing, pivoting, multi-system operations | [HTB assigned range](docs/references/electives.md#proxy-paths-and-multi-system-operations) | General red-team routing is available after the specialized core without derailing it |
| Advanced exploit development | [HTB or WEB-300](docs/references/electives.md#advanced-web-exploit-development) | Mature provider ranges replace an implausibly small local multi-stage environment |

## Explicit exclusions, not curriculum holes

- Malware, persistence, credential theft, botnet operation, and attack hosting are
  not required to learn this specialized authorized traffic-testing role.
- Universal stealth, “all bots” coverage, identity proof from a fingerprint, and
  production expertise from a toy lab are claims the course deliberately rejects.
- A provider link is not authorization to test the provider's ordinary website.

## Final gap rule

Before release, every row must have one of three outcomes: full source-backed
instruction plus a self-contained exercise; an exact mature external assignment; or an explicit
out-of-role exclusion. No row may end in “research it,” a generic paragraph, or a
tool list without a readiness point and expected evidence.
