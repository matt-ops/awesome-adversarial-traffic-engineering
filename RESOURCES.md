# Attack ranges and supporting resources

The course teaches the concept, then assigns an exact external lab when a mature range provides better adversarial practice than the bundled toy target. Paid labs are valid primary assignments; a free or self-hosted alternative is named in the course whenever practical. This page is only a lookup table—do not work through everything.

## Free hosted labs

| Resource | Assigned offensive skill | Course depth |
|---|---|---|
| [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/) | Classify account, credential, scraping, scalping, CAPTCHA, inventory, token, and DoS abuse with the canonical OAT identifiers | Foundation–Deep |
| [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/latest/) | Apply a complete web-assessment methodology when the course teaches only the traffic-abuse slice | Applied–Deep |
| [OWASP WSTG: Information Gathering](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/) | Identify attack surface, entry points, execution paths, technologies, and application architecture | Foundation–Integrated |
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

## Self-hosted targets and tools

| Resource | Assigned offensive skill | Course depth |
|---|---|---|
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | Attack intentionally vulnerable commerce workflows | Applied–Integrated |
| [OWASP crAPI](https://owasp.org/www-project-crapi/) | Exploit API authorization and business-logic assumptions | Applied–Integrated |
| [OWASP WebGoat](https://owasp.org/www-project-webgoat/) | Practice guided web exploitation with explanations | Applied |
| [OWASP Coraza](https://github.com/corazawaf/coraza) | Build a self-hosted WAF target and test normalization/evasion cases | Integrated |
| [ModSecurity CRS Docker](https://github.com/coreruleset/modsecurity-crs-docker) | Attack a containerized WAF/CRS deployment and inspect rule decisions | Integrated |
| [FingerprintJS BotD](https://github.com/fingerprintjs/BotD) | Self-host a real open-source browser bot sensor for controlled Playwright and anti-detect comparisons | Integrated–Deep |
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
