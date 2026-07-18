# Electives after the core path

These are not a menu for beginners. Each elective names when it becomes useful,
one required route, and at most one alternate. Use only the provider-assigned
target or an isolated environment you own.

## Broader web reconnaissance

**Begin after:** Module 04 Applied, when you can map request, workflow, state, and protected action.

**Relevant checkpoint:** Applied or later.

**Why elective:** the core teaches immediate control-specific recon. Broad DNS,
subdomain, archive, and technology discovery supports a wider assessment but
would interrupt the bot/control attack chain.

- **Required free route:** [OWASP WSTG Information Gathering](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/) — complete Conduct Search Engine Discovery Reconnaissance, Fingerprint Web Server, Review Webserver Metafiles, Enumerate Applications, Identify Application Entry Points, and Map Application Architecture against a self-hosted target.
- **Paid alternate:** [HTB Academy Information Gathering - Web Edition](https://academy.hackthebox.com/course/preview/information-gathering---web-edition) — complete all sections and the provider skills assessment; preserve the surface map, not only the completion mark.

## WAF and proxy parsing bypass

**Begin after:** Modules 01, 04, 05, and 07 Integrated.

**Relevant checkpoint:** Integrated or later.

**Why elective:** realistic WAF bypass needs a deliberately vulnerable parser
chain and rule telemetry; the bundled edge does not reproduce production parser diversity.

- **Required free route:** [PortSwigger HTTP request smuggling](https://portswigger.net/web-security/request-smuggling) — complete the introductory mechanism, finding CL.TE/TE.CL, confirming the issue, and the assigned Academy labs in provider targets.
- **Self-hosted alternate:** [Coraza](https://github.com/corazawaf/coraza) with [OWASP Core Rule Set](https://coreruleset.org/docs/) — deploy only in an isolated topology; record rule/paranoia level, normalization path, blocked baseline, one parser hypothesis, protected effect, residual anomalies, remediation, and exact retest.

## Credential attacks at realistic scale

**Begin after:** Module 04 authentication and rate controls.

**Relevant checkpoint:** Applied or later.

**Why elective:** the repository uses fixed synthetic credentials and cannot
legitimately reproduce leaked-account data or external login pressure.

- **Required free route:** [PortSwigger Authentication vulnerabilities](https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities) — complete the exact sections and broken brute-force-protection lab assigned by Module 04.
- **Paid alternate:** [HTB Academy Login Brute Forcing](https://academy.hackthebox.com/course/preview/login-brute-forcing) — complete the provider module and skills assessment using only supplied accounts/targets.

## Browser anti-fingerprinting research target

**Begin after:** Modules 05-06 Deep.

**Relevant checkpoint:** Deep.

**Why elective:** the bundled control is transparent and intentionally small. A
second implementation tests whether the method transfers without implying that
either target represents all commercial controls.

- **Required self-hosted route:** [FingerprintJS BotD](https://github.com/fingerprintjs/BotD) — self-host a pinned release; compare manual, stock headed/headless, and one declared coherent profile while holding workflow/version fixed.
- **Alternate research tool:** [Rebrowser Bot Detector](https://github.com/rebrowser/rebrowser-bot-detector) — pin commit/browser/framework versions and repeat the same population matrix; report residual tests and version sensitivity.

## AI-powered browser adversaries

**Begin after:** Modules 03-06 Integrated.

**Relevant checkpoint:** Integrated or later.

**Why elective:** the core builds a deterministic browser attacker first. A model
adds planning variability and tool-use risk; it should not hide weak browser foundations.

- **Required local route:** [Playwright MCP](https://github.com/microsoft/playwright-mcp) — expose only the self-hosted course target and a constrained action set; compare model plan, actual Playwright trace, protected effect, failed actions, and replayability with the deterministic workflow.
- **Research alternate:** [BrowserGym](https://github.com/ServiceNow/BrowserGym) — run one supplied benchmark/task locally and preserve action/observation traces. General prompt-injection frameworks such as AgentDojo remain outside this browser-traffic course.

## CAPTCHA solver development

**Begin after:** Module 06 Deep and only when the authorized role explicitly requires visual-challenge research.

**Relevant checkpoint:** Deep.

**Why elective:** challenge-token binding and replay belong in the core. Training
or operating a visual solver adds ML/data/tooling prerequisites and is not needed
to learn the control-evasion method.

- **Paid route:** [Infosec Hacking CAPTCHA Systems](https://www.infosecinstitute.com/skills/courses/hacking-captcha-systems/) — use only its supplied target/data and retain model/version, success metric, false solves, boundary, and limitations.

## L3/L4 pressure, spoofing, and TCP-state attacks

**Begin after:** Module 08 Deep plus isolated-network administration experience.

**Relevant checkpoint:** Deep, after the core application-layer resilience work.

**Why elective:** the normal repository intentionally contains no raw flood,
spoofing, reflection, or attack-infrastructure tooling. Those mechanisms require
a purpose-built topology that cannot reach another network.

- **Required isolated route:** [SEED TCP/IP Attack Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/TCP_Attacks/) — use the supplied topology and complete its TCP-state experiments and countermeasure analysis.
- **Alternate isolated route:** [SEED Packet Sniffing and Spoofing Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/Sniffing_Spoofing/) — complete only inside the supplied VM/container topology; never bridge it to a routable network.

## Proxy paths and multi-system operations

**Begin after:** the complete Integrated checkpoint.

**Relevant checkpoint:** Integrated or later.

**Why elective:** tunneling, pivoting, and multi-system exploitation are general
red-team skills but not prerequisites for browser-control and bounded traffic testing.

- **Required paid route:** [HTB Academy Pivoting, Tunneling, and Port Forwarding](https://academy.hackthebox.com/course/preview/pivoting-tunneling-and-port-forwarding) — use only assigned routes and preserve the before/after observation-point map.
- **Advanced alternate:** [HTB Pro Labs](https://www.hackthebox.com/hacker/pro-labs) — choose a provider range only after completing its prerequisites; document the attack chain and evidence, not just flags.

## Advanced web exploit development

**Begin after:** the Deep checkpoint.

**Relevant checkpoint:** Deep, as post-core specialization.

**Why elective:** broad exploit chains are valuable red-team practice but exceed
the specialized traffic-control path.

- **Required paid route:** [HTB Senior Web Penetration Tester path](https://academy.hackthebox.com/path/preview/senior-web-penetration-tester) — complete its ordered modules and provider assessments.
- **Alternate:** [OffSec WEB-300](https://help.offsec.com/hc/en-us/articles/360046868971-WEB-300-Advanced-Web-Attacks-and-Exploitation-FAQ) — use when source-guided exploit development is the next role gap.

For every elective, retain: authorization, recon evidence, objective, attack
path, protected effect, raw evidence, limitations, remediation invariant, and exact retest.
