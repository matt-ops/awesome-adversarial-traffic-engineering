# Attack ranges and supporting resources

The course teaches the concept, then assigns an exact external lab when a mature range provides better adversarial practice than the bundled toy target. Paid labs are valid primary assignments; a free or self-hosted alternative is named in the course whenever practical. This page is only a lookup table—do not work through everything.

## Free hosted labs

| Resource | Assigned offensive skill | Course depth |
|---|---|---|
| [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) | Exploit authentication, business-logic, API, cache, request-smuggling, and Web LLM flaws in assigned targets | Applied–Deep |
| [PortSwigger Authentication path](https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities) | Enumerate users and attack password/session controls | Applied |
| [PortSwigger Web LLM attacks](https://portswigger.net/web-security/learning-paths/llm-attacks) | Exploit tool-enabled LLM trust boundaries and prompt injection | Integrated |
| [SEED Labs TCP/IP Attack Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/TCP_Attacks/) | Reproduce TCP state attacks and SYN pressure in an isolated topology | Deep |
| [SEED Labs Firewall Exploration](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/) | Test packet-filter behavior and validate countermeasures | Deep |
| [Exercism Python](https://exercism.org/tracks/python/exercises) | Guided Python fundamentals and feedback | Foundation–Applied |

## Self-hosted targets and tools

| Resource | Assigned offensive skill | Course depth |
|---|---|---|
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | Attack intentionally vulnerable commerce workflows | Applied–Integrated |
| [OWASP crAPI](https://owasp.org/www-project-crapi/) | Exploit API authorization and business-logic assumptions | Applied–Integrated |
| [OWASP WebGoat](https://owasp.org/www-project-webgoat/) | Practice guided web exploitation with explanations | Applied |
| [OWASP Coraza](https://github.com/corazawaf/coraza) | Build a self-hosted WAF target and test normalization/evasion cases | Integrated |
| [ModSecurity CRS Docker](https://github.com/coreruleset/modsecurity-crs-docker) | Attack a containerized WAF/CRS deployment and inspect rule decisions | Integrated |
| [Toxiproxy](https://github.com/Shopify/toxiproxy) | Deterministic private proxy/network conditions | Integrated |
| [containerlab](https://containerlab.dev/manual/) | Isolated network topologies | Deep |
| [Scapy](https://scapy.readthedocs.io/en/stable/introduction.html) | Packet construction and capture inside an isolated topology | Deep |

## Browser and AI-agent labs

| Resource | Assigned offensive skill | Course depth |
|---|---|---|
| [Playwright](https://playwright.dev/docs/intro) | Build browser attackers that execute and record hostile workflows | Foundation–Integrated |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Build a model-driven browser attacker with constrained tools | Integrated |
| [BrowserGym](https://github.com/ServiceNow/BrowserGym) | Run reproducible adaptive web-agent attacks and preserve action traces | Integrated–Deep |
| [AgentDojo](https://github.com/ethz-spylab/agentdojo) | Attack and evaluate tool-using agents under prompt injection | Integrated–Deep |
| [Camoufox](https://camoufox.com/) | Test anti-fingerprinting changes against a controlled sensor | Integrated–Deep |
| [Rebrowser Patches](https://github.com/rebrowser/rebrowser-patches) | Test browser automation patches against a controlled detector | Integrated–Deep |
| [promptfoo red teaming](https://www.promptfoo.dev/docs/red-team/quickstart/) | Local/authorized AI attack and evaluation | Deep |
| [PyRIT](https://azure.github.io/PyRIT/) | Orchestrated AI red-team experiments | Deep |

## Paid or freemium ranges

| Resource | Assignments that match this course | Course depth |
|---|---|---|
| [Hack The Box Academy: Login Brute Forcing](https://academy.hackthebox.com/course/preview/login-brute-forcing) | Execute web-form credential attacks and complete the skills assessment | Applied |
| [Hack The Box Academy: Using Web Proxies](https://academy.hackthebox.com/course/preview/using-web-proxies/setting-up) | Intercept, modify, replay, and organize attack traffic | Applied |
| [Hack The Box AI Red Teamer path](https://academy.hackthebox.com/path/preview/ai-red-teamer) | Attack AI applications/systems and test evasion techniques | Integrated–Deep |
| [Hack The Box Senior Web Penetration Tester](https://academy.hackthebox.com/path/preview/senior-web-penetration-tester) | Chain advanced web and API attacks into assessments | Deep |
| [Hack The Box Pro Labs](https://www.hackthebox.com/hacker/pro-labs) | Conduct multi-system red-team operations in assigned ranges | Deep |
| [TryHackMe Web Application Pentesting](https://tryhackme.com/path/outline/webapppentesting) | Progress through guided web exploitation | Applied–Integrated |
| [PentesterLab exercises](https://pentesterlab.com/exercises/) | Exploit focused web vulnerabilities and explain the mechanism | Applied–Deep |

## Rule for every external lab

Use only the target assigned by the provider or your isolated self-hosted environment. Keep five notes: attack goal, technique, bypass evidence, remediation, and retest. A badge, flag, or completion percentage by itself is not the learning result.
