# Attack ranges and supporting resources

The course assigns resources at the exact point they are needed. Paid labs are valid primary assignments; a free or self-hosted alternative is named whenever practical. This page is only a lookup table—do not work through it separately and do not choose a path here.

## From-zero prerequisites

These are the instructional routes used by the Foundation sections. “Required” means complete the linked sections and examples unless you can already pass that module’s explicit readiness gate.

| Resource | Exact assignment | Use |
|---|---|---|
| [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | Sections 3.1–3.3 for planning and Rules of Engagement; Sections 5.1–5.2 for analysis and reporting | Required in Modules 0 and 7 |
| [Cloudflare DNS](https://www.cloudflare.com/learning/dns/what-is-dns/), [TCP/IP](https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/), and [TLS](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/) primers | Draw the endpoints and state what each completed exchange proves | Required free route in Module 1 |
| [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) and [HTTP messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages) | Work through the client/proxy/request/response/message examples and annotate one exchange | Required free route in Module 1 |
| [HTB Introduction to Networking](https://academy.hackthebox.com/course/preview/introduction-to-networking) and [Web Requests](https://academy.hackthebox.com/course/preview/web-requests) | Networking Models through TCP/UDP Connections, then the complete Web Requests module and exercises | Guided route in Module 1 |
| [OWASP Automated Threats](https://owasp.org/www-project-automated-threats-to-web-applications/) | Identification chart and handbook entries for credential, account, scraping, scalping, inventory, and DoS abuse | Required in Module 2 |
| [MDN JavaScript Fundamentals](https://developer.mozilla.org/en-US/curriculum/core/javascript-fundamentals/) | Units 6.1–6.13, including DOM, events, async JavaScript, fetch, and JSON, when JavaScript is new | Required from-zero route in Module 3 |
| [Playwright introduction](https://playwright.dev/docs/intro), [writing tests](https://playwright.dev/docs/writing-tests), [locators](https://playwright.dev/docs/locators), and [network](https://playwright.dev/docs/network) | Run each first working example before the repository browser lab | Required in Module 3 |
| [Google classification metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall) | Threshold/confusion-matrix lesson plus precision/recall lesson and exercises | Required in Module 4 |
| [Cloudflare application-layer DDoS](https://www.cloudflare.com/learning/ddos/application-layer-ddos-attack/) and [Google SRE Handling Overload](https://sre.google/sre-book/handling-overload/) | Map resources and units, then read the assigned QPS, customer-limit, and throttling sections | Required in Module 5 |
| [Official Python Tutorial](https://docs.python.org/3/tutorial/) | Chapters/sections 3, 4.1–4.9, 5.1–5.5, 7.2, and 8.3 | Required free route in Module 6 |
| [HTB Introduction to Python 3](https://academy.hackthebox.com/course/preview/introduction-to-python-3) | Complete module and exercises | Guided route in Module 6 |

## Free hosted labs

| Resource | Assigned offensive skill | Course stage |
|---|---|---|
| [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | Build rules of engagement, evidence gates, mitigation, and retest ownership | Foundation–Deep |
| [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/) | Classify account, credential, scraping, scalping, CAPTCHA, inventory, token, and DoS abuse with the canonical OAT identifiers | Foundation–Deep |
| [OWASP Bot Management and Anti-Automation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html) | Connect threat hypotheses, layered signals, proportional response, privacy, and adversarial evaluation | Foundation–Deep |
| [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/latest/) | Apply a complete web-assessment methodology when the course teaches only the traffic-abuse slice | Applied–Deep |
| [OWASP WSTG: Information Gathering](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/) | Identify attack surface, entry points, execution paths, technologies, and application architecture | Foundation–Integrated |
| [OWASP WSTG: Reporting Structure](https://owasp.org/www-project-web-security-testing-guide/latest/5-Reporting/01-Reporting_Structure) | Turn reproducible evidence into technical findings, remediation, and retest guidance | Foundation–Deep |
| [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) | Exploit authentication, business-logic, API, cache, request-smuggling, and Web LLM flaws in assigned targets | Applied–Deep |
| [PortSwigger API testing: API recon](https://portswigger.net/web-security/api-testing#api-recon) | Discover API documentation, endpoints, methods, parameters, content types, authentication, and rate-limit behavior | Applied |
| [PortSwigger Authentication path](https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities) | Enumerate users and attack password/session controls | Applied |
| [PortSwigger HTTP request smuggling](https://portswigger.net/web-security/request-smuggling) | Exploit proxy parsing disagreements and bypass front-end controls in deliberately vulnerable targets | Integrated–Deep |
| [PortSwigger Web LLM attacks](https://portswigger.net/web-security/learning-paths/llm-attacks) | Exploit tool-enabled LLM trust boundaries and prompt injection | Integrated |
| [SEED Labs TCP/IP Attack Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/TCP_Attacks/) | Reproduce TCP state attacks and SYN pressure in an isolated topology | Deep |
| [SEED Packet Sniffing and Spoofing Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/Sniffing_Spoofing/) | Construct, spoof, sniff, and inspect packets in the supplied isolated topology | Deep |
| [SEED Labs Firewall Exploration](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/) | Test packet-filter behavior and validate countermeasures | Deep |
| [University of South Carolina Cybersecurity Lab Series](https://research.cec.sc.edu/cyberinfra/cybertraining) | Use Lab 8 for isolated SYN/FIN/RST, Smurf, and Slowloris attack/mitigation practice | Deep |
| [Exercism Python](https://exercism.org/tracks/python/exercises) | Guided Python fundamentals and feedback | Foundation–Applied |
| [Official Nmap Network Scanning guide](https://nmap.org/book/toc.html) | Perform scoped host discovery, port scanning, and service/version enumeration in a private topology | Deep |
| [Google SRE: Handling Overload](https://sre.google/sre-book/handling-overload/) | Model request cost, quotas, criticality, retry budgets, and graceful rejection before resilience tests | Foundation–Deep |
| [Google SRE: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) | Explain queue growth, retry amplification, dependency failure, load shedding, and recovery | Deep |
| [Python asyncio queues](https://docs.python.org/3/library/asyncio-queue.html#examples) | Implement bounded work queues and reason about producer/consumer cleanup | Applied–Deep |
| [Python asyncio semaphores](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore) | Bound concurrent work inside an asynchronous offensive client | Applied–Deep |

## Self-hosted targets and tools

| Resource | Assigned offensive skill | Course stage |
|---|---|---|
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | Attack intentionally vulnerable commerce workflows | Applied–Integrated |
| [OWASP crAPI](https://owasp.org/www-project-crapi/) | Exploit API authorization and business-logic assumptions | Applied–Integrated |
| [OWASP WebGoat](https://owasp.org/www-project-webgoat/) | Practice guided web exploitation with explanations | Applied |
| [OWASP Coraza](https://github.com/corazawaf/coraza) | Build a self-hosted WAF target and test normalization/evasion cases | Integrated |
| [ModSecurity CRS Docker](https://github.com/coreruleset/modsecurity-crs-docker) | Attack a containerized WAF/CRS deployment and inspect rule decisions | Integrated |
| [CRS Paranoia Levels](https://coreruleset.org/docs/2-how-crs-works/2-2-paranoia_levels/) | Distinguish enabled rule sets from anomaly thresholds before WAF-evasion testing | Integrated |
| [WAFW00F](https://github.com/EnableSecurity/wafw00f) | Fingerprint a WAF in a self-hosted or provider-authorized range, then corroborate the guess with controlled response and audit-log evidence | Integrated |
| [FingerprintJS BotD](https://github.com/fingerprintjs/BotD) | Self-host a real open-source browser bot sensor for controlled Playwright and anti-detect comparisons | Integrated–Deep |
| [Toxiproxy](https://github.com/Shopify/toxiproxy) | Deterministic private proxy/network conditions | Integrated |
| [containerlab](https://containerlab.dev/manual/) | Isolated network topologies | Deep |
| [Scapy](https://scapy.readthedocs.io/en/stable/introduction.html) | Packet construction and capture inside an isolated topology | Deep |

## Browser and AI-agent labs

| Resource | Assigned offensive skill | Course stage |
|---|---|---|
| [Playwright](https://playwright.dev/docs/intro) | Build browser attackers that execute and record hostile workflows | Foundation–Integrated |
| [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) | Join browser actions, DOM state, console, and network evidence when diagnosing an attack run | Foundation–Applied |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Build a model-driven browser attacker with constrained tools | Integrated |
| [BrowserGym](https://github.com/ServiceNow/BrowserGym) | Run reproducible adaptive web-agent attacks and preserve action traces | Integrated–Deep |
| [AgentDojo](https://github.com/ethz-spylab/agentdojo) | Attack and evaluate tool-using agents under prompt injection | Integrated–Deep |
| [Camoufox](https://camoufox.com/) | Test anti-fingerprinting changes against a controlled sensor | Integrated–Deep |
| [Rebrowser Patches](https://github.com/rebrowser/rebrowser-patches) | Test browser automation patches against a controlled detector | Integrated–Deep |
| [promptfoo red teaming](https://www.promptfoo.dev/docs/red-team/quickstart/) | Local/authorized AI attack and evaluation | Deep |
| [PyRIT](https://azure.github.io/PyRIT/) | Orchestrated AI red-team experiments | Deep |

## Paid or freemium ranges

| Resource | Assignments that match this course | Course stage |
|---|---|---|
| [Hack The Box Academy: Login Brute Forcing](https://academy.hackthebox.com/course/preview/login-brute-forcing) | Execute web-form credential attacks and complete the skills assessment | Applied |
| [Hack The Box Academy: Using Web Proxies](https://academy.hackthebox.com/course/preview/using-web-proxies/setting-up) | Intercept, modify, replay, and organize attack traffic | Applied |
| [Hack The Box Academy: Information Gathering — Web Edition](https://academy.hackthebox.com/course/preview/information-gathering---web-edition) | Practice passive and active web recon, DNS enumeration, crawling, archive analysis, and technology fingerprinting | Integrated |
| [Hack The Box Academy: Network Enumeration with Nmap](https://academy.hackthebox.com/course/preview/network-enumeration-with-nmap) | Discover hosts, ports, services, and versions and preserve results in the assigned range | Deep |
| [Hack The Box Academy: Footprinting](https://academy.hackthebox.com/course/preview/footprinting) | Extend recon across common enterprise services with a provider skills assessment | Deep optional |
| [Hack The Box Academy: Pivoting, Tunneling, and Port Forwarding](https://academy.hackthebox.com/course/preview/pivoting-tunneling-and-port-forwarding) | Practice proxychains, SOCKS, tunnels, and route changes in the provider-assigned range | Deep |
| [Hack The Box AI Red Teamer path](https://academy.hackthebox.com/path/preview/ai-red-teamer) | Attack AI applications/systems and test evasion techniques | Integrated–Deep |
| [Hack The Box Senior Web Penetration Tester](https://academy.hackthebox.com/path/preview/senior-web-penetration-tester) | Chain advanced web and API attacks into assessments | Deep |
| [Hack The Box Pro Labs](https://www.hackthebox.com/hacker/pro-labs) | Conduct multi-system red-team operations in assigned ranges | Deep |
| [TryHackMe Web Application Pentesting](https://tryhackme.com/path/outline/webapppentesting) | Progress through guided web exploitation | Applied–Integrated |
| [PentesterLab exercises](https://pentesterlab.com/exercises/) | Exploit focused web vulnerabilities and explain the mechanism | Applied–Deep |
| [OffSec WEB-300](https://help.offsec.com/hc/en-us/articles/360046868971-WEB-300-Advanced-Web-Attacks-and-Exploitation-FAQ) | Develop exploit scripts from source-guided analysis and chain advanced web attacks in a private lab | Deep |
| [Infosec: Hacking CAPTCHA Systems](https://www.infosecinstitute.com/skills/courses/hacking-captcha-systems/) | Build a Selenium/neural-network CAPTCHA solver and test it against the course-supplied FoolMe target | Deep |

## Coverage fallback

No course objective disappears because the repository cannot safely or realistically reproduce it. Use this map when a module routes you away from the bundled lab:

| Skill the role requires | Repository limit | Required route |
|---|---|---|
| Full attack-surface reconnaissance before exploitation | Local OpenAPI discovery teaches the lifecycle but represents only one small application | Use OWASP WSTG Information Gathering plus a self-hosted target for the free route, or HTB Information Gathering — Web Edition and Network Enumeration with Nmap in their assigned ranges |
| Full automated-abuse taxonomy, including CAPTCHA defeat and token cracking | The local app demonstrates selected synthetic workflows, not every OAT | Read the OWASP Automated Threats page; use the local challenge-replay lab for token binding, provider-assigned authentication/business-logic labs, and Infosec's Hacking CAPTCHA Systems for visual CAPTCHA solving |
| Credential attacks | No stolen, leaked, or customer credentials | Use fixed local credentials, PortSwigger Authentication labs, or HTB Login Brute Forcing with provider-supplied data |
| Proxy chains and source/path variation | No public proxy network or third-party routing | Use HTB Pivoting/Tunneling in its assigned range, or a private self-hosted proxy topology |
| Browser fingerprint and anti-detect evasion | The bundled detector is deliberately transparent and small | Self-host BotD, then compare ordinary Playwright with Camoufox or Rebrowser while keeping the target and workflow fixed |
| Front-end/WAF parsing bypass | The bundled Nginx target does not emulate the full parser diversity of production edges | Use PortSwigger request-smuggling labs plus a private Coraza or ModSecurity CRS deployment |
| Packet spoofing, SYN pressure, reflection/amplification mechanics, and slow application DoS | The normal local stack forbids raw/routable floods | Use the supplied SEED topology and University of South Carolina Lab 8 exactly as written; never bridge the range to another network |
| Advanced exploit development and multi-stage web attacks | A simple course cannot reproduce a mature private range | Use HTB Senior Web Penetration Tester, HTB Pro Labs, PentesterLab, or OffSec WEB-300 |
| AI-powered attacker behavior | The bundled fixed workflow is not a general model | Use Playwright MCP locally, BrowserGym/AgentDojo, PortSwigger Web LLM labs, or the HTB AI Red Teamer path |

## Rule for every external lab

Use only the target assigned by the provider or your isolated self-hosted environment. A link is a learning assignment, not permission to test the provider’s ordinary website or any unrelated system. Keep six notes: recon evidence, attack goal, technique, bypass evidence, remediation, and retest. A badge, flag, or completion percentage by itself is not the learning result.
