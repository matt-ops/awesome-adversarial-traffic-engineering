# Adversarial Traffic Engineering Course

This is the entire course. You do not need to understand the repository.

This is a **red-team-first course**. You learn a defense well enough to identify its trust assumptions; then you attack those assumptions, complete the protected action, preserve bypass evidence, recommend a fix, and retest. Detector design and defensive telemetry support that mission. They are not the mission.

1. Read **Learn**.
2. Do **Lab**.
3. Answer **Self-assess**, then check the answers.
4. Click the next link.

Start with Foundation in Modules 0 through 8. That is the 24-hour minimum. If you continue, repeat the same modules at Applied, Integrated, then Deep depth. [CHECKPOINTS.md](CHECKPOINTS.md) only tells you when you may stop; it adds no work.

Every core lab uses this attack loop:

```text
name the target/control -> establish the blocked baseline -> state a bypass hypothesis
-> execute the attack -> prove the protected action succeeded or the mitigation failed
-> explain impact -> recommend a fix -> run the same test again
```

Observation alone is reconnaissance. A completed red-team lab includes an adversarial action and evidence of its outcome. Use only the bundled local target, your isolated self-hosted target, or the exact target a training provider assigns.

Before a lab, start the target once:

```bash
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
```

Expected response: `{"status":"ok","service":"aate-local-app"}`. When finished, run `docker compose -f lab/docker-compose.yml down`.

---

# Module 0: Safety and red-team engagement discipline

**Red-team outcome:** Define an authorization and containment envelope that lets you execute real attack techniques in a lab without crossing the target boundary.

<a id="module-0-foundation"></a>
## Foundation

### Learn

Authorization is permission from the system owner for a specific target, action, time, and data set. Owning an account or being able to reach a host is not authorization to security-test it.

Write scope as three lists:

- **In scope:** exact hosts, accounts, workflows, times, and techniques.
- **Out of scope:** connected systems and actions that must not be touched.
- **Stop conditions:** measurable events that end the test immediately.

A provider-assigned training machine can be in scope while the provider’s website, login portal, and adjacent machines remain out of scope.

Safety controls limit different dimensions:

- an allowlist prevents a wrong destination;
- a total-request cap bounds all work;
- rate and concurrency caps bound simultaneous pressure;
- timeouts prevent stuck operations;
- synthetic data excludes real users and secrets;
- an abort threshold stops a deteriorating service.

Make abort conditions numerical. “Stop if performance gets bad” is unusable. “Stop after two failed health checks, error rate over 5%, or p95 latency over 500 ms for 30 seconds” tells the operator exactly what to do.

Rate is not concurrency. A useful approximation is `concurrency = requests per second × average response seconds`. Five requests/second with two-second responses creates about ten in-flight requests.

Evidence should record authorization, target, time, command/version, caps, request or session IDs, result, limitations, and cleanup. A useful finding connects **condition → evidence → impact → remediation → retest**.

### Lab

Prove the bundled client’s allowlist works:

```bash
python -m lab.clients.safe_client --dry-run
python -m lab.clients.safe_client --target https://example.com --total 1
```

The first command prints the local target and caps without sending traffic. The second must print `"rejected": true`. Rejection is the successful result.

Write this seven-line plan in any notes app:

```text
Owner: me
Target: localhost:8080
Allowed: GET /health with the bundled client
Cap: 10 total requests at 2 requests/second
Abort: unexpected status or manual stop
Data: synthetic only
Cleanup: stop containers; retain no secrets
```

### Self-assess

1. Does owning an account authorize credential testing?
2. At 4 requests/second and 1.5 seconds per response, what is approximate concurrency?
3. What happens first when an abort threshold trips?
4. Name the five parts of a finding and validation chain.

<details><summary>Check your answers</summary>

1. No. The owner must authorize that target and action.
2. About six.
3. Stop traffic; diagnose and preserve evidence afterward.
4. Condition, evidence, impact, remediation, retest.

</details>

[Next: Module 1 Foundation](#module-1-foundation)

<a id="module-0-applied"></a>
## Applied

### Learn

An engagement plan converts permission into controls. It names the objective, owner, tester, targets, exclusions, techniques, synthetic data, time window, caps, health metrics, abort thresholds, stop authority, evidence handling, cleanup, and retest owner.

Preflight before traffic: resolve the target, compare it with the allowlist, confirm synthetic accounts, print a dry run, check health, and start below the maximum. If health crosses a threshold, stop first. Record when, why, and how the run stopped; do not continue for “one more sample.”

### Lab

Run a five-request engagement:

```bash
python -m lab.clients.safe_client --target http://localhost:8080/api/search?q=demo --rps 2 --total 5
```

Expect five JSON lines with `"ok": true` and `"status": 200`. Add actual start/stop time and result to your seven-line plan.

### Self-assess

1. Why print a dry run?
2. Why specify both a total cap and a rate cap?

<details><summary>Check your answers</summary>

1. To catch an incorrect target or unsafe envelope before execution.
2. They limit different things: all work versus work per unit time.

</details>

[Next: Module 1 Applied](#module-1-applied)

<a id="module-0-integrated"></a>
## Integrated

### Learn

An integrated runbook orders experiments so earlier state does not contaminate later evidence: health check, reset, baseline, adversarial populations, detection evaluation, resilience test, evidence export, cleanup. Keep a decision log with time, observation, decision, and reason.

Provider-hosted ranges add one rule: authorization ends at the assigned targets and the provider’s allowed techniques. It does not extend to adjacent infrastructure, and AATE’s local client must not be repointed at a provider.

### Lab

Write the nine-step order above. Beside each step name its command, expected result, abort condition, and cleanup. Walk through it without traffic. Fix every missing command or threshold before the capstone.

### Self-assess

1. Why can test order invalidate results?
2. What does a decision log contain that telemetry does not?

<details><summary>Check your answers</summary>

1. One test can change accounts, inventory, cache, or service health seen by the next.
2. The operator’s interpretation and reason for continuing, changing, or stopping.

</details>

[Next: Module 1 Integrated](#module-1-integrated)

<a id="module-0-deep"></a>
## Deep

### Learn

Production validation is staged: lab reproduction, approved offline analysis, shadow evaluation with no enforcement, an allowlisted canary, then broader use. Separate the lab result, the hypothesis that might transfer, and the production evidence needed. Every stage needs an owner, monitoring, rollback, and new approval.

### Lab

Choose one course finding and write those five stages, including the metric that advances the test and the metric that rolls it back. Read [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final), Sections 3.1–3.3, 5.1, and 5.2, then check that planning, execution, analysis, mitigation, and retest have owners.

### Self-assess

1. Does a lab bypass prove production is vulnerable?
2. Why run a shadow evaluation?

<details><summary>Check your answers</summary>

1. No. It creates a transfer hypothesis; production differs in controls, traffic, data, and scale.
2. To measure behavior and false positives without taking enforcement action.

</details>

[Next: Module 1 Deep](#module-1-deep)

---

---

# Module 1: Web request path and network fundamentals

**Red-team outcome:** Capture, mutate, proxy, and replay traffic while explaining which attacker-controlled values survive each intermediary.

<a id="module-1-foundation"></a>
## Foundation

### Learn

Follow a request through this logical path:

```text
Browser -> DNS -> CDN/edge -> WAF/bot control -> load balancer
        -> application -> database/cache/dependency -> response
```

**DNS** maps a hostname to an IP address. **TCP** provides a reliable byte stream and consumes connection state. **TLS** authenticates the server and encrypts traffic between TLS endpoints. A CDN that terminates TLS can inspect HTTP and usually makes a separate connection to the origin.

An HTTP request contains a method, path, headers, and optional body:

```http
GET /api/search?q=demo HTTP/1.1
Host: localhost:8080
Accept: application/json
```

The response contains a status, headers, and body. `2xx` means success, `3xx` redirect, `4xx` client or policy outcome, and `5xx` server failure.

A cookie is a value the browser returns on later requests. Session cookies usually carry an opaque identifier mapped to server-side state. `Secure` means HTTPS only, `HttpOnly` blocks ordinary JavaScript access, and `SameSite` constrains cross-site sending. Automation can replay cookies, so a cookie is not proof of a human.

A reverse proxy forwards requests, a CDN caches near users, a WAF applies HTTP policy, bot controls combine automation and workflow evidence, and a load balancer distributes work. Each may terminate connections, normalize headers, add IDs, cache, rate-limit, or block.

| Layer | Evidence | Resource that can fail |
|---|---|---|
| DNS | query rate, answer, TTL | resolver/authoritative capacity |
| TCP/TLS | connections, handshakes, bytes | sockets, CPU, bandwidth |
| Edge/WAF | requests, rule action, cache result | workers, inspection CPU |
| Application | route, status, latency, request ID | CPU, memory, tasks |
| Dependency | query latency, queue depth | pools, locks, storage I/O |

A request ID joins one exchange across layers. A session ID joins several requests in a workflow. Neither automatically identifies a person.

### Lab

```bash
curl.exe -i "http://localhost:8080/api/search?q=demo" -H "X-Request-ID: replay-foundation-1"
curl.exe -i "http://localhost:8080/api/search?q=kit" -H "X-Request-ID: replay-foundation-1"
curl.exe -i "http://localhost:8080/api/products/not-real" -H "X-Request-ID: attacker-controlled"
```

In the first two responses find status `200`, `content-type`, `x-request-id`, `x-aate-latency-ms`, and the JSON body. You replayed the request while mutating only the query and proved the client can supply a correlation header that the edge reflects. The third response should be `404`; a caller-controlled request ID does not authorize a nonexistent object.

Open `lab/edge/nginx.conf` and find `proxy_pass`. Draw the actual path:

```text
client -> 127.0.0.1:8080 Nginx -> app:8000 FastAPI -> in-memory state
```

Mark DNS and TLS as absent. Then add three attacker notes: the query and request-ID header are controllable, Nginx forwards the request, and the application decides what object exists. This is the minimum offensive primitive used by later proxy, WAF, cache, and replay attacks.

### Self-assess

1. Does DNS carry `/api/search`?
2. Can a CDN that terminates TLS inspect HTTP headers?
3. Why can equal request rates create unequal impact?
4. Request ID versus session ID: what does each correlate?

<details><summary>Check your answers</summary>

1. No; it resolves the hostname before HTTP.
2. Yes, at the termination point.
3. Endpoints perform different CPU, I/O, allocation, locking, or dependency work.
4. One exchange versus several exchanges in a workflow.

</details>

[Next: Module 2 Foundation](#module-2-foundation)

<a id="module-1-applied"></a>
## Applied

### Learn

`curl`, Python, and a browser can request the same URL but produce different evidence. Browsers manage cookies, redirects, JavaScript, caches, and connection reuse. Their TLS ClientHello advertises versions, algorithms, extensions, and **ALPN**, which selects an application protocol such as HTTP/1.1 or HTTP/2. A TLS fingerprint summarizes an implementation path; it is not an identity.

HTTP/2 multiplexes many streams over one connection. Therefore requests/connection, connections/second, and requests/second answer different questions.

An intercepting proxy allows capture, one-variable modification, and replay. Replay is useful because it isolates a variable, but stale tokens and changed server state can mislead you. Record preconditions and reset state.

### Lab

Complete PortSwigger’s [Intercepting HTTP traffic with Burp Proxy](https://portswigger.net/burp/documentation/desktop/getting-started/intercepting-http-traffic) tutorial. Use its target or localhost only.

Then run:

```bash
curl.exe -s -D - http://localhost:8080/health
python -m lab.clients.safe_client --target http://localhost:8080/health --total 1
npm run playwright:foundation
```

The last command creates `lab/telemetry/foundation-playwright.jsonl`. Compare what each client exposes. In Burp Repeater, replay `GET /api/search?q=demo`, change `demo` to `kit`, and verify only the synthetic kit remains.

### Self-assess

1. What does ALPN select?
2. Why does a proxy change some transport evidence but not necessarily workflow evidence?

<details><summary>Check your answers</summary>

1. The application protocol over the encrypted connection.
2. It creates a new upstream connection, while cookies, accounts, request order, and payload semantics can remain.

</details>

[Next: Module 2 Applied](#module-2-applied)

<a id="module-1-integrated"></a>
## Integrated

### Learn

Correlate `edge request ID -> application request ID -> session -> account/workflow -> dependency trace`. A rotating private proxy changes target-visible source IP and often TLS behavior; it does not automatically change browser properties, account state, or action sequence.

HTTP/3 carries HTTP over QUIC/UDP. The useful questions remain: what can each endpoint observe, what survives an intermediary, and which resource is exhausted?

### Lab

Create manual-browser, Playwright, Python, and Burp-replayed local populations. Give each the same adversarial goal: reserve one synthetic item using a caller-supplied identity that was never authenticated. Record whether the protected action succeeds, plus source address, headers, cookies/session behavior, connection evidence, and what the proxy changed. The expected weakness is invariant across clients: transport variation does not repair missing application authorization.

Then read [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113), Sections 2 and 5, and explain how multiplexing can defeat a control that mistakes connections/second for requests or attacker identities.

### Self-assess

1. Name evidence that may survive an IP-changing proxy.
2. Why is a protocol fingerprint not an identity?

<details><summary>Check your answers</summary>

1. Account/session state, cookies, request order, payload semantics, and some browser evidence.
2. Clients share implementations, versions and middleboxes change it, and some inputs can be modified.

</details>

[Next: Module 2 Integrated](#module-2-integrated)

<a id="module-1-deep"></a>
## Deep

### Learn

Deep protocol work separates standardized possibilities from one implementation’s behavior. Change one variable—version, proxy, reuse, or protocol—record configuration, repeat runs, and report both stable and non-replicating observations.

### Lab

Choose one attacker question: can proxying change a TLS/HTTP fingerprint without changing the hostile workflow, can HTTP/2 multiplexing evade a connection-count assumption, or can browser-version drift mimic an evasion? Capture a blocked or flagged baseline and at least five runs per changed condition. Use the matching reference: [HTTP/2 Sections 2 and 5](https://www.rfc-editor.org/rfc/rfc9113), [QUIC Sections 2 and 5](https://www.rfc-editor.org/rfc/rfc9000), [HTTP/3 Sections 2 and 3](https://www.rfc-editor.org/rfc/rfc9114), or [TLS 1.3 Sections 2 and 4](https://www.rfc-editor.org/rfc/rfc8446). Your conclusion must say whether the protected action still succeeded and whether the control decision changed.

### Self-assess

1. What makes the comparison reproducible?
2. Why report results that did not replicate?

<details><summary>Check your answers</summary>

1. Fixed variables, recorded versions/configuration, preserved captures, repetitions, and a defined comparison.
2. To prevent cherry-picking and bound the claim.

</details>

[Next: Module 2 Deep](#module-2-deep)

---

---

# Module 2: Automated abuse and threat modeling

**Red-team outcome:** Execute synthetic credential and business-workflow attacks, identify the control invariant, and vary identity, state, timing, or path to test a bypass hypothesis.

<a id="module-2-foundation"></a>
## Foundation

### Learn

Automated abuse uses legitimate-looking application functions to violate a business rule or consume a scarce resource.

| Abuse | Attacker goal | Typical workflow | Useful evidence | Likely control | False-positive risk |
|---|---|---|---|---|---|
| Credential stuffing | take over accounts | many known username/password pairs | failure/success sequence, account reuse, device/session changes | breached-password checks, MFA, risk-based friction | travelers and shared networks |
| Account creation | obtain many identities | repeated signup/verify/profile | identity graph, velocity, reused attributes | verification, quotas, graph controls | households and classrooms |
| Scraping | copy data | enumerate search/detail pages | coverage, sequence, pagination, bytes | quotas, caching, terms enforcement | search engines and accessibility tools |
| Scalping | win scarce purchase | monitor, add, checkout rapidly | timing, inventory focus, account/payment graph | fair queues, purchase limits | enthusiastic buyers |
| Denial of inventory | make stock unavailable | reserve without completing | reserve-to-purchase ratio, hold expiry | short holds, identity limits | abandoned carts |
| Promotion abuse | gain repeated discount | redeem across identities | promo/account/device/payment graph | global and per-entity policy | shared households |
| Application-layer DoS | exhaust expensive work | repeatedly call costly routes | route cost, concurrency, dependency pressure | cache, quota, admission control | flash crowds |

Do not threat-model “a bot” as one object. Write: **goal → workflow steps → state/identities → observable behavior → control → bypass hypothesis → false-positive risk**. Business state often detects abuse better than a single header because the attacker must still accomplish the workflow.

OWASP defines 21 canonical automated threats, including account creation, CAPTCHA defeat, credential cracking/stuffing, denial of inventory/service, fingerprinting, scalping, scraping, and token cracking. Open [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/) and use its identification chart. For Foundation, identify the OAT name and number for the local credential, account-creation, inventory, and DoS exercises; do not memorize all 21.

Credential terms matter:

- **brute force:** many candidate passwords against one account;
- **password spraying:** one or a few common passwords against many accounts;
- **credential stuffing:** reused username/password pairs obtained elsewhere.

Use only fixed synthetic credentials in this course.

### Lab

Run two local attack workflows:

```bash
python -m lab.run credential
python -m lab.run workflow
```

The credential attack must show five attempts, four failures, and one success: a synthetic spray-like pattern followed by successful reuse. The automated workflow creates an account, logs in, searches, reserves inventory, redeems a promotion, and passes a fixed local challenge. Treat the successful login, reservation, and redemption as adversary outcomes—not merely generated telemetry.

For each, write one row with goal, protected action, attack sequence, current control, bypass hypothesis, evidence, and false-positive risk. Example: `deny availability | reserve | enumerate → reserve → abandon | per-identity quantity | rotate synthetic identity | inventory falls without purchase | legitimate abandoned carts`.

### Self-assess

1. Stuffing versus spraying: what changes?
2. Why is high request rate not required for abuse?
3. Why is an inventory hold signal stronger than User-Agent alone?
4. Which control reduces promotion abuse across many accounts sharing one payment method?

<details><summary>Check your answers</summary>

1. Stuffing uses many distinct credential pairs; spraying tries a small password set across many accounts.
2. Low-rate actions can still violate a business invariant or accumulate impact.
3. It is tied to the attacker’s required business outcome; User-Agent is cheap to change and shared by legitimate users.
4. A graph/workflow policy that links account, payment, promotion, and redemption history.

</details>

[Next: Module 3 Foundation](#module-3-foundation)

<a id="module-2-applied"></a>
## Applied

### Learn

An abuse simulation needs representative state. A login test records account, session, outcome, timing, source/proxy, challenge state, and subsequent action. An account-creation test records reused attributes and downstream use. A scraper test measures coverage and business cost, not just request count.

A challenge introduces a branch: request → risk decision → challenge → solve/fail/abandon → protected action. Evaluate who receives the challenge, whether tokens bind to session/action/time, whether replay works, and how accessibility or privacy tools behave. The goal is to assess your own control—not outsource CAPTCHA solving against an unrelated site.

A proxy pool redistributes source-address evidence. In a private lab it is useful for testing whether controls rely only on IP. Account, device, cookie, token, payment, request sequence, and success patterns can still correlate the traffic.

### Lab

First complete the free [PortSwigger Authentication learning path](https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities) through the username-enumeration and password-based login sections. Use only PortSwigger’s assigned labs.

Then run `python -m lab.run credential`. Explain which pattern is spray-like and which is stuffing-like. Add a proposed rule that uses both account and session dimensions. It must allow the successful synthetic login and flag the repeated failed pattern.

If you have HTB Academy, complete [Login Brute Forcing](https://academy.hackthebox.com/course/preview/login-brute-forcing), the sections on basic HTTP authentication, web forms, and skills assessment. The PortSwigger assignment is the free path; HTB is an alternative lab, not an extra requirement.

### Self-assess

1. Why bind a challenge token to session and action?
2. What weakness does a private proxy-pool experiment test?
3. Why evaluate successful actions after failed logins?

<details><summary>Check your answers</summary>

1. To prevent a token solved elsewhere or earlier from authorizing a different protected action.
2. Overreliance on source IP as the identity or rate-limit key.
3. A single success after a broad failure pattern can represent account takeover and deserves more context than failures alone.

</details>

[Next: Module 3 Applied](#module-3-applied)

<a id="module-2-integrated"></a>
## Integrated

### Learn

AI-powered bots add a decision loop:

```text
observe page/API state -> choose a goal-relevant action -> execute tool
-> observe result -> adapt or stop
```

The model is only one layer. The browser/API tools, memory, credentials, proxy, challenge handling, policy, and stop conditions determine actual capability. Defenders can observe tool regularity, navigation choices, retries, semantic goals, account graphs, and cross-layer inconsistencies. Agent security also matters: untrusted page content may try to redirect the agent through prompt injection.

A good experiment compares a fixed script with an adaptive agent on the same goal. Measure completion rate, actions, retries, time, errors, challenge behavior, and detection score. Do not call a deterministic script “AI,” and do not infer human intent from a model label.

### Lab

`python -m lab.run workflow` is the fixed-policy attacker baseline. Its JSON lines are an observe/action trace. Change one lab condition—for example deplete `demo-1` first—and make the policy choose another available product after reading `/api/search` and `/api/products/{id}`. The adversarial goal is still to reserve inventory and redeem the promotion. Record why each action was selected, whether the protected action succeeded, and why the agent stopped.

For a genuine model-powered environment, choose one exact authorized assignment:

- [Playwright MCP](https://github.com/microsoft/playwright-mcp): restrict it to `localhost:8080`, give it the goal “reserve one synthetic item using an unregistered identity,” save its trace, and verify the `200` bypass; or
- [AgentDojo](https://github.com/ethz-spylab/agentdojo): run the documented quick start and one prompt-injection attack, then explain utility versus security success; or
- [PortSwigger Web LLM attacks](https://portswigger.net/web-security/learning-paths/llm-attacks): exploit the first three assigned labs and explain the trust-boundary failure in each.

The evidence to keep is the attacker goal, observation/action trace, protected-action outcome, safety policy, and one control signal the agent did or did not evade. Installing every framework is not required.

### Self-assess

1. What makes an agent different from a fixed script?
2. Name three non-model components that affect an AI bot’s capability.
3. What two outcomes does AgentDojo distinguish?

<details><summary>Check your answers</summary>

1. It selects or changes actions from observations rather than following only a fixed sequence.
2. Browser/API tools, memory, credentials, proxy, challenge integration, and stop policy are examples.
3. Completing the assigned utility task and resisting the security attack.

</details>

[Next: Module 3 Integrated](#module-3-integrated)

<a id="module-2-deep"></a>
## Deep

### Learn

Adaptive abuse changes pace, identity, path, and tool after feedback. Distributed low-rate campaigns defeat rules that look only for a burst from one IP. Account and workflow graphs join identities through shared attributes and actions; temporal analysis finds coordinated behavior that each individual event hides.

Evasion testing must ask what the attacker must preserve. Changing User-Agent is easy; maintaining consistent TLS, browser runtime, cookies, account history, payment graph, navigation timing, and successful business semantics is harder. A robust defense raises attacker cost across layers and measures harm to legitimate populations.

### Lab

Design three variants of one workflow: fixed direct client, private-proxy rotation, and adaptive browser agent. For each predict which signals change and which required business invariants remain. Then run the variants only in localhost, a self-hosted target, or the provider-assigned range.

If you do not already have a private multi-proxy topology, complete the proxychains and SOCKS sections plus skills assessment in [HTB Academy: Pivoting, Tunneling, and Port Forwarding](https://academy.hackthebox.com/course/preview/pivoting-tunneling-and-port-forwarding). Use only its assigned range. Your course note must separate route/source evidence that changed from account, browser, and workflow evidence that survived.

For deeper authorized practice, choose one:

- [HTB Senior Web Penetration Tester path](https://academy.hackthebox.com/path/preview/senior-web-penetration-tester): complete the authentication and web-service assessment modules relevant to your gap;
- [HTB AI Red Teamer path](https://academy.hackthebox.com/path/preview/ai-red-teamer): complete Introduction to Red Teaming AI, LLM Output Attacks, and Attacking AI Applications and Systems;
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics): complete the authentication, business-logic, API-testing, and Web LLM lab sets.

Visual CAPTCHA defeat is a Deep specialization, not a Foundation prerequisite. Complete [Infosec: Hacking CAPTCHA Systems](https://www.infosecinstitute.com/skills/courses/hacking-captcha-systems/) if that skill is relevant to your target controls. Build the assigned Selenium/neural-network solver and run it only against the course's supplied FoolMe target. Preserve solver accuracy, failure examples, end-to-end protected-action success, and one control improvement; do not test a third-party CAPTCHA service.

For every external lab, write the mechanism, evidence, remediation, and retest. A flag alone is not course completion.

### Self-assess

1. Why do low-rate distributed attacks evade per-IP burst limits?
2. What is an attacker invariant?
3. Why compare false positives by legitimate population?

<details><summary>Check your answers</summary>

1. Each source remains below the local threshold while aggregate workflow impact grows.
2. A behavior or state the attacker must preserve to achieve the goal.
3. Aggregate accuracy can hide disproportionate harm to accessibility tools, privacy users, shared networks, or unusual devices.

</details>

[Next: Module 3 Deep](#module-3-deep)

---

---

# Module 3: Browser automation

**Red-team outcome:** Build scripted and model-driven browser attackers that complete hostile workflows, preserve action traces, and vary browser identity or behavior for evasion tests.

<a id="module-3-foundation"></a>
## Foundation

### Learn

Playwright controls real browser engines. Its object model is simple:

- **Browser:** one running browser process controlled by Playwright.
- **BrowserContext:** an isolated profile with its own cookies, storage, permissions, locale, and cache.
- **Page:** a tab inside a context.
- **Locator:** a retrying way to find and act on an element.
- **Request/Response events:** network activity observed by the page.

One browser can contain several contexts, and each context can contain several pages. Use a fresh context when you need a clean identity. Reusing a context preserves state and can contaminate an experiment.

`page.goto()` navigates. `page.on("request", ...)` and `page.on("response", ...)` collect traffic. `context.storageState()` saves cookies and web storage for later reuse. Headless mode omits the visible window; headed mode shows it. Neither mode is inherently malicious or human, and modern differences extend beyond one `navigator.webdriver` value.

Reliable automation waits for meaningful state rather than sleeping an arbitrary number of seconds. Prefer locator assertions, response predicates, or `domcontentloaded`. Always set timeouts and close the context/browser in cleanup.

The bundled script does this:

```ts
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ locale: "en-US" });
const page = await context.newPage();
page.on("request", request => { /* save local request */ });
page.on("response", response => { /* save local status */ });
await page.goto("http://localhost:8080/api/search?q=demo");
await page.evaluate(() => fetch("/api/cart/reserve", { /* synthetic unauthenticated reservation */ }));
await context.close();
await browser.close();
```

### Lab

Install once, then run:

```bash
npm install
npx playwright install chromium
npm run playwright:foundation
```

Expected console text includes `Bypass confirmed` and names `lab/telemetry/foundation-playwright.jsonl`. Open that file. Find the browser request and response for `/api/cart/reserve`. The script supplied an identity that was never created or authenticated, yet inventory changed. That `200` is bypass evidence for missing authorization/state binding in the intentionally flawed local workflow.

Change `headless: true` to `headless: false`, run again, and watch the browser. Change it back after the comparison. The bypass should still succeed: execution mode changed, but the target still trusted the caller-supplied identity. Write one remediation—bind reservation to an authenticated server-side identity—and one retest that expects `401` or `403` for the same attack.

### Self-assess

1. BrowserContext versus Page: what state does each represent?
2. Why use a new context for a new experimental identity?
3. Why are fixed sleeps brittle?
4. Does headless automatically mean abusive?

<details><summary>Check your answers</summary>

1. A context is an isolated browser profile; a page is a tab in that profile.
2. It prevents cookies, storage, permissions, and cache from the earlier identity leaking into the new run.
3. They wait too long on fast runs and may be too short on slow runs; they do not test the actual condition.
4. No. Legitimate testing and accessibility tooling can be headless, while abuse can use headed browsers.

</details>

[Next: Module 4 Foundation](#module-4-foundation)

<a id="module-3-applied"></a>
## Applied

### Learn

Frames have their own documents and execution contexts. Workers run JavaScript away from the page; service workers can intercept network requests and cache responses. Browser automation that observes only the top-level page can miss all three.

The Chrome DevTools Protocol (CDP) exposes lower-level domains such as Network, Runtime, Target, and Performance. Playwright already uses browser protocols internally; a CDP session is useful when the high-level API does not expose an event. CDP is Chromium-specific, so do not make cross-browser claims from it.

Storage-state reuse is a controlled replay:

```ts
await context.storageState({ path: "lab/telemetry/state.json" });
const replay = await browser.newContext({ storageState: "lab/telemetry/state.json" });
```

Treat the state file like a credential even in a lab. Never commit real session tokens.

### Lab

Read the Playwright pages for [Browser contexts](https://playwright.dev/docs/browser-contexts), [Authentication/state reuse](https://playwright.dev/docs/auth), and [Network events](https://playwright.dev/docs/network). Perform these exact changes in a copy of the foundation script:

1. create two contexts with different locale values;
2. reserve one item from each using two identities that were never created or authenticated;
3. save storage state from the first context;
4. attach a CDP session with `context.newCDPSession(page)`;
5. enable `Network` and count `Network.requestWillBeSent` events;
6. close both contexts and the browser.

Expected result: both hostile populations complete the protected action, have separate browser state, and produce independently counted network events. Explain why locale is an attacker-controlled experimental variable, not proof of identity. The report must lead with the missing server-side authorization bypass; the browser differences are supporting evidence.

### Self-assess

1. When is CDP appropriate, and what portability cost does it have?
2. Why is storage-state replay security-sensitive?
3. Why observe frames and workers?

<details><summary>Check your answers</summary>

1. For Chromium detail missing from the high-level API; it does not generalize automatically to Firefox/WebKit.
2. It can contain authenticated cookies and tokens.
3. They can execute code, make requests, and hold state not visible in the top-level document.

</details>

[Next: Module 4 Applied](#module-4-applied)

<a id="module-3-integrated"></a>
## Integrated

### Learn

A browser bot includes automation, identity state, request path, decision logic, and recovery. A fixed script follows predetermined steps. A rule-based agent chooses from coded conditions. A model-powered agent selects actions from observations and a goal. Compare them by outcome and trace, not by marketing label.

Anti-detect tools modify observable browser properties or launch configuration. Some changes improve cross-layer consistency; others create new mismatches. A controlled red-team comparison changes only the browser build/patch set while keeping account, proxy, workflow, and timing policy fixed.

Browser-driving models can be attacked by page content. Treat page text as untrusted input, restrict tools and destinations, require confirmation for consequential actions, and log every observation/action pair.

### Lab

Run the fixed baseline:

```bash
python -m lab.run workflow
```

Then choose one agent assignment:

- [Playwright MCP](https://github.com/microsoft/playwright-mcp): follow “Getting started,” connect it to a model client, allow only `localhost:8080`, and ask it to find and reserve one synthetic product using an unregistered identity; or
- [BrowserGym](https://github.com/ServiceNow/BrowserGym): follow its installation and MiniWoB quick start, complete one assigned adversarial task, and save the action trace.

Compare fixed versus agent attacker: protected-action success, number of actions, retries, unexpected actions, control decision, and stop-policy compliance. Do not give the agent credentials or access to any non-lab target.

For an anti-detect comparison, use either [Camoufox](https://github.com/daijro/camoufox) or [Rebrowser Patches](https://github.com/rebrowser/rebrowser-patches) only against the local sensor you build in Module 4. Follow the project’s installation example exactly; collect the same signal set before and after; report corrected inconsistencies and new ones.

### Self-assess

1. What must remain fixed in an anti-detect comparison?
2. Why log an agent’s observations and actions?
3. What is the difference between a rule-based and model-powered agent?

<details><summary>Check your answers</summary>

1. Goal, account/state, network path, workflow, timing policy, and detector version.
2. To reproduce decisions, identify unsafe branches, and distinguish model choice from tool failure.
3. Rules choose from explicit coded conditions; a model maps observations and goals to actions more flexibly.

</details>

[Next: Module 4 Integrated](#module-4-integrated)

<a id="module-3-deep"></a>
## Deep

### Learn

Browser internals matter when a signal depends on process boundaries or implementation detail. The browser process manages tabs, permissions, and networking; renderer processes execute page content; workers may run separately. Site isolation and sandboxing affect which contexts share process state.

JavaScript properties have values and descriptors. A patch that changes a value but leaves a surprising getter, prototype, enumeration rule, error stack, or cross-frame result can create detectable inconsistency. Runtime instrumentation can also change timing and semantics. Source reading should answer a narrow question, not become unguided exploration.

### Lab

Choose one evasion question, such as “What must change beyond `navigator.webdriver` for the top page, iframe, and worker to agree?” Use [Chromium Code Search](https://source.chromium.org/chromium/chromium/src) to find the implementation and [Chrome DevTools Protocol Runtime](https://chromedevtools.github.io/devtools-protocol/tot/Runtime/) to observe contexts. Record the exact revision, file/function, blocked baseline, patch or launch change, control decision, and whether the automated protected action still succeeds.

If the question is anti-fingerprinting rather than Chromium internals, use [Camoufox’s implementation documentation](https://camoufox.com/) and compare the documented patch to observed descriptors in top page, iframe, and worker contexts.

### Self-assess

1. Why is changing a property value sometimes insufficient?
2. What makes source exploration useful rather than open-ended?

<details><summary>Check your answers</summary>

1. Descriptors, prototypes, error behavior, timing, or cross-context values can remain inconsistent.
2. A narrow hypothesis, exact revision, named implementation location, and experiment that can falsify the claim.

</details>

[Next: Module 4 Deep](#module-4-deep)

---

---

# Module 4: Browser signals and bot detection

**Red-team outcome:** Reconnoiter a bot detector's decision boundary, change the smallest useful signal set, and prove the automated workflow is allowed after evasion.

<a id="module-4-foundation"></a>
## Foundation

### Learn

Bot detection is inference under uncertainty. As a red teamer, you need this model to discover the control's inputs, threshold, and blind spots. Signals describe observations; they do not prove who or what is behind a request.

Signal families include:

- **network/transport:** source, connection reuse, TLS/ALPN, HTTP behavior;
- **HTTP:** headers, order, cookies, cache and redirect behavior;
- **browser runtime:** APIs, property descriptors, canvas/WebGL/audio, permissions;
- **behavior:** timing, navigation, input, retries, coverage;
- **identity/workflow:** account, token, payment, reserve/purchase ratio, challenge result;
- **history/graph:** prior sessions and shared attributes.

Cross-layer consistency asks whether claims agree. A Windows User-Agent paired with a Linux platform value is suspicious, but virtual machines, compatibility modes, privacy tools, and instrumentation can create legitimate mismatches.

Request-level evidence describes one exchange. Session-level evidence describes sequence, state, and outcomes. Workflow evidence connects the actions required to achieve a goal. Combine them because each has different failure modes.

Detection outcomes:

| | Actual abuse | Actual legitimate |
|---|---:|---:|
| Predicted abuse | true positive (TP) | false positive (FP) |
| Predicted legitimate | false negative (FN) | true negative (TN) |

`precision = TP / (TP + FP)` asks how often alerts are correct. `recall = TP / (TP + FN)` asks how much abuse is found. `false-positive rate = FP / (FP + TN)` asks what fraction of legitimate events are flagged. A threshold trades recall against false positives.

An explainable score adds named reasons. It is easier to test, appeal, and remediate than a magic opaque label.

### Lab

Run:

```bash
python -m lab.analysis.analyze
python -m lab.run evasion
```

The analyzer is reconnaissance. Expected fixture result is `tp: 4`, `fp: 0`, `tn: 6`, `fn: 0`, with precision and recall `1.0`. That is deliberately perfect because the ten records were written for the rules. It proves deterministic code, not production quality.

The evasion command is the attack. Its baseline combines `webdriver=true` with missing browser headers and receives `challenge`. It changes only webdriver exposure; the score falls below the threshold and the same protected-workflow event receives `allow`. Open `lab/detectors/rules.py`, locate both weights, and write the exact failed invariant: the control assumes the automation property remains present.

### Self-assess

1. If TP=80 and FP=20, what is precision?
2. If TP=80 and FN=40, what is recall?
3. Why is one automation property not enough?
4. Why are perfect fixture metrics weak evidence?
5. What proves the Foundation evasion succeeded?

<details><summary>Check your answers</summary>

1. `80 / 100 = 0.80`.
2. `80 / 120 ≈ 0.67`.
3. Legitimate automation can expose it and malicious automation can modify it; it says little about workflow intent.
4. The sample is tiny, synthetic, non-diverse, and designed around the known rules.
5. The same workflow event changed one attacker-controlled signal and moved from `challenge` to `allow`.

</details>

[Next: Module 5 Foundation](#module-5-foundation)

<a id="module-4-applied"></a>
## Applied

### Learn

Build a detector from a hypothesis, not a list of weird values. Example: “An abusive expensive-endpoint session combines missing browser headers, sub-100 ms repetition, and three or more expensive calls.” Each feature maps to a mechanism, the threshold is explicit, and legitimate counterexamples can be tested.

Evaluate by population. Manual users, Playwright tests, accessibility-like automation, privacy browsers, corporate proxies, and abusive scripts can have different error rates. Overall accuracy can hide harm to a small group.

An evasion test changes one signal and asks whether the attacker still succeeds. If clearing `webdriver` drops the score below threshold, the result demonstrates rule fragility. It does not prove all bots bypass the system.

### Lab

Make a temporary copy of `lab/fixtures/requests.jsonl` outside the repository. Perform two controlled changes:

1. Change `e09` to `webdriver:false` and rerun the analyzer on the copy.
2. Change legitimate `e05` to `inter_arrival_ms:50` and remove `accept_language`, then rerun.

Record which reasons, decisions, FP/FN counts, precision, and recall changed. Restore nothing because you edited only a temporary copy. Then propose one workflow feature that would make the first evasion harder, such as account success after broad failures or abnormal reserve-to-purchase ratio.

### Self-assess

1. What does a one-variable evasion test establish?
2. Why report metrics by population?
3. What is a feature’s mechanism?

<details><summary>Check your answers</summary>

1. How sensitive this specific detector/fixture is to that variable under controlled conditions.
2. To expose disproportionate false positives and false negatives hidden by aggregate metrics.
3. The causal or operational reason the observation is associated with the abuse workflow.

</details>

[Next: Module 5 Applied](#module-5-applied)

<a id="module-4-integrated"></a>
## Integrated

### Learn

A layered detector separates collection, feature computation, scoring, action, and feedback. Collection should minimize data and document retention. Scoring can combine request, session, workflow, and service-impact features. Action may be observe, rate-limit, challenge, delay, or block. Feedback includes appeals, confirmed abuse, drift, and post-action behavior.

Replay resistance asks whether a captured valid value still works in another session, action, or time. Temporal consistency asks whether a session evolves plausibly across requests. Agentic bots may vary superficial timing while still exposing goal-directed retries and tool constraints.

Feature ablation removes one feature or family and repeats evaluation. If performance barely changes, the feature may add cost without value. If one feature dominates, it may be a brittle single point.

### Lab

First self-host [FingerprintJS BotD](https://github.com/fingerprintjs/BotD) by following its official local/npm quick start. Do not test an anti-detect tool against a public demo. Establish ordinary-browser and normal-Playwright baselines against your local copy and preserve the BotD result plus the browser/driver versions.

Then compare six authorized attacker populations: manual replay, normal Playwright, Python script, replay through Burp/ZAP, one anti-detect browser, and one model- or rule-driven agent. Give each the same protected-workflow goal and use the same toy-detector and BotD versions. For each record completion, score/reasons, action count, latency, challenge result, BotD result, and whether the hostile business outcome succeeded.

Your offensive objective is to find the least costly population or mutation that changes `challenge` to `allow` without breaking the workflow. Then remove each rule family in turn from a temporary copy of the detector and rerun the fixed fixture. Report the change in bypass rate, TP, FP, precision, recall, and population effect. The conclusion must name the successful evasion, one brittle feature, and one workflow feature that would force the attacker to pay more.

### Self-assess

1. Why separate score from enforcement action?
2. What does feature ablation reveal?
3. What makes a token replay-resistant?

<details><summary>Check your answers</summary>

1. The same risk evidence can support different proportional actions and allows shadow evaluation.
2. Each feature’s incremental value, redundancy, and dominance.
3. Binding it to the intended session, action, audience, nonce, and short validity window, with server-side replay tracking where needed.

</details>

[Next: Module 5 Integrated](#module-5-integrated)

<a id="module-4-deep"></a>
## Deep

### Learn

Signals drift when browsers, devices, networks, privacy controls, and attacker tools change. Monitor missing-value rate, feature distribution, score distribution, action rate, confirmed outcomes, and population-specific false positives by version and time.

Fingerprinting creates privacy risk when data can link a person across contexts. Minimize collection, avoid raw high-entropy values when aggregates suffice, set retention, control access, and provide governance. Accessibility technologies and enterprise instrumentation can create automation-like behavior; include them in test populations before enforcement.

Calibration asks whether a score of 0.8 corresponds to about 80% confirmed abuse in comparable traffic. A ranker can separate cases while still being poorly calibrated. Production thresholds must reflect response cost and customer harm, not only model metrics.

### Lab

Choose an anti-detect or browser-patch hypothesis and attempt the same automated protected action across at least two browser versions or patch configurations. Start with a challenged baseline. Build a table with patch/version, cross-context consistency, score, action, workflow success, and new anomaly. A successful Deep result either proves a repeatable bypass or falsifies the evasion hypothesis with preserved evidence.

Add one legitimate privacy/accessibility near-neighbor so you can show whether the proposed remediation would block non-adversarial automation. For every collected feature record purpose, granularity, retention, access, deletion, and a safer alternative.

For a deeper authorized AI detector exercise, use [promptfoo’s red-team quick start](https://www.promptfoo.dev/docs/red-team/quickstart/) or [PyRIT’s documentation](https://azure.github.io/PyRIT/). Run only against a local or provider-assigned model endpoint. Record attack category, observed behavior, detector/judge limitation, and remediation.

### Self-assess

1. Name two drift indicators.
2. Why can a well-ranked score be poorly calibrated?
3. What privacy question should every feature answer?

<details><summary>Check your answers</summary>

1. Missing-value rate, feature/score distribution, action rate, outcome rate, or population error changes.
2. Ranking order does not guarantee the numeric score matches outcome probability.
3. Why it is needed, how little can be collected, who can access it, how long it remains, and how it is deleted.

</details>

[Next: Module 5 Deep](#module-5-deep)

---

---

# Module 5: Edge controls and DDoS resilience

**Red-team outcome:** Bypass challenge and WAF assumptions, identify the resource a mitigation protects, and pressure-test that control with bounded adversarial traffic.

<a id="module-5-foundation"></a>
## Foundation

### Learn

Denial of service is resource exhaustion that prevents acceptable service. Classify the constrained resource, not just the packet type.

- **Layer 3:** network-layer capacity or processing, measured with bits/packets and routing state.
- **Layer 4:** transport connection/state pressure, measured with new connections, concurrent connections, handshakes, and packets.
- **Layer 7:** application work, measured with requests, concurrency, latency, errors, queues, CPU, memory, and dependency use.

Key units:

- `bps`: bits per second, useful for link capacity;
- `pps`: packets per second, useful when per-packet work is the limit;
- `rps`: application requests per second;
- connections/second: new connection setup rate;
- concurrent connections/requests: work alive at once.

Two equal-RPS routes can have radically different cost. A cached health check may do almost nothing; a report route may hash data, query a database, allocate memory, and wait on dependencies. Measure latency, errors, saturation, and recovery alongside traffic.

Controls act at different points:

- caching avoids repeated origin work;
- rate limits bound a chosen key and time window;
- concurrency limits bound in-flight work;
- challenges add attacker cost before protected work;
- queues smooth bursts but can increase latency and memory;
- load shedding rejects low-priority work to preserve critical paths;
- timeouts/circuit breakers prevent dependency failures from spreading;
- origin shielding restricts direct origin access.

Per-IP limiting is incomplete because users share IPs and attackers distribute traffic. Combine source with account, session, token, workflow, and cost.

### Lab

Run:

```bash
python -m lab.run bypass
python -m lab.run resilience
```

The first command establishes a `403` baseline, solves the local challenge as one synthetic session, captures the returned token, then replays it as a different session to reach the protected report. The final `200` proves the toy control failed to bind the token to session, action, expiry, or one-time use.

The second command applies bounded resource pressure: five cheap and five expensive requests, one at a time. Compare median latency and the printed ratio. The correct claim is only “this local route costs more under this implementation,” not a production capacity estimate.

Write a finding with the replay condition, protected action, evidence, impact, server-side binding remediation, and retest. Then write a safe pressure-test plan with target, 10-request cap, one-at-a-time concurrency, expected statuses, health check, abort on any failure, and cleanup.

### Self-assess

1. A small request triggers a costly database query. Which layer describes the exhausted work?
2. When is pps more useful than bps?
3. Why can a queue make an outage worse?
4. Why is per-IP limiting incomplete?
5. What made the challenge-token result a bypass rather than an observation?

<details><summary>Check your answers</summary>

1. Layer 7/application and its database dependency.
2. When per-packet processing rather than link volume is the bottleneck.
3. An unbounded queue consumes memory and increases latency until work is useless.
4. Shared networks group legitimate users, while distributed attackers spread across addresses.
5. A token issued to one session authorized a protected action for another session after the no-token baseline was denied.

</details>

[Next: Module 6 Foundation](#module-6-foundation)

<a id="module-5-applied"></a>
## Applied

### Learn

Red-team a control by stating its invariant and testing nearby cases. For a rate limit, vary key, window, concurrency, endpoint cost, account, session, and proxy. For a WAF, vary encoding and request representation only in an authorized lab and verify whether normalization is consistent. For a challenge, test issuance, binding, expiry, replay, failure, accessibility, and protected-action enforcement.

A flash crowd and attack can share high volume. Intent is rarely directly observable. Compare workflow distribution, cacheability, account history, conversion, errors, retries, geographic/network diversity, and response to controls. Mitigations should preserve critical legitimate flows even when classification is uncertain.

### Lab

Repeat the local challenge attack and add a rate-limit bypass:

```bash
python -m lab.run bypass
python -m lab.run ratelimit
```

Build a challenge matrix for missing token, invalid token, valid token in the solver session, and replay in a second session. Then inspect the rate-limit output: one session receives `200, 200, 429`, while three attacker-chosen session IDs receive `200, 200, 200`. Explain why trusting one caller-controlled key makes the limit bypassable.

Propose a random challenge token bound to session, action, expiry, and single use, plus a rate policy that aggregates authenticated identity, workflow, endpoint cost, and source risk. State the expected status for every retest row.

Then complete PortSwigger’s [Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning) explanation plus its first lab. The provider’s assigned lab is the only target. Explain how disagreement between cache and origin parsing creates risk.

### Self-assess

1. What dimensions should a rate-limit bypass assessment vary?
2. Why does a successful challenge response need server-side binding?
3. Name one flash-crowd feature that can resemble attack traffic.

<details><summary>Check your answers</summary>

1. Key, window, route cost, concurrency, identity/session, source/proxy, and distributed aggregation.
2. Otherwise a solved token may be replayed for another session, action, or time.
3. High RPS, high concurrency, retries, concentrated popular objects, or geographic spikes.

</details>

[Next: Module 6 Applied](#module-6-applied)

<a id="module-5-integrated"></a>
## Integrated

### Learn

An end-to-end resilience experiment has a baseline, controlled workload, service-health measures, mitigation change, recovery period, and identical retest. Separate traffic metrics from service metrics. A mitigation that lowers RPS by failing every customer is not success.

Workflow-aware controls protect a scarce action—login success, reservation, checkout, report generation—across IP changes. Cost-aware admission can charge expensive operations more than cached reads. Backpressure tells upstream callers to slow or fail quickly when downstream capacity is gone.

### Lab

Self-host [OWASP Coraza](https://github.com/corazawaf/coraza) or [OWASP ModSecurity CRS Docker](https://github.com/coreruleset/modsecurity-crs-docker) in a private Compose network in front of an intentionally vulnerable local target such as [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/). Follow the chosen project’s Docker quick start exactly.

Before improvising parser mutations, complete PortSwigger’s [HTTP request smuggling](https://portswigger.net/web-security/request-smuggling) learning material and assigned labs through “bypassing front-end security controls.” Those deliberately vulnerable labs supply the parser-diversity target the repository does not. Then run three provider- or self-hosted cases: obvious blocked request, one representation/normalization variation from that assignment, and a legitimate near-neighbor. Record WAF action, origin result, protected action, false positive, and rule/log evidence. Do not test a public WAF.

For the local app, begin with `python -m lab.run ratelimit` and preserve the successful key-rotation bypass. Implement a replacement locally—at the application or private reverse proxy—that charges the expensive action across session rotation while allowing the cheap health route. Run the identical attack again. The Integrated lab is incomplete until the original rotated attack is blocked or throttled and the legitimate near-neighbor still succeeds.

### Self-assess

1. Why measure service health as well as traffic?
2. What does workflow-aware aggregation retain when source IP rotates?
3. What is backpressure?

<details><summary>Check your answers</summary>

1. Traffic reduction can still harm users; the objective is acceptable service.
2. Account/session/action state and progress toward the protected business outcome.
3. A mechanism that prevents upstream work from overwhelming a saturated downstream resource, often by limiting, delaying, or failing quickly.

</details>

[Next: Module 6 Integrated](#module-6-integrated)

<a id="module-5-deep"></a>
## Deep

### Learn

Packet floods target link or per-packet processing. SYN-style pressure targets connection setup/state. Reflection sends requests with a victim’s spoofed address so responders send replies to the victim. Amplification uses a small request that produces a larger response. These mechanics are important for defense, but spoofing and amplification must stay inside a physically or virtually isolated, non-routable topology with no shared network access.

Protocol pressure can also occur at higher layers: HTTP/2 streams, rapid resets, expensive decompression, or dependency fan-out. The same method applies: name the resource, create the smallest reproducer, cap it below lab capacity, measure, mitigate, and retest.

### Lab

Use one structured isolated lab; do not improvise on a routed network. Complete [SEED Packet Sniffing and Spoofing](https://seedsecuritylabs.org/Labs_20.04/Networking/Sniffing_Spoofing/) for packet construction/source spoofing, [SEED TCP/IP Attack Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/TCP_Attacks/) for SYN-state mechanics, and [SEED Firewall Exploration](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/) for mitigation/retest. Use the provided VM/container topology and its exact instructions.

For an isolated lab that also covers SYN/FIN/RST floods, Smurf-style amplification, and Slowloris mechanics, use Lab 8 in the [University of South Carolina Cybersecurity Lab Series](https://research.cec.sc.edu/cyberinfra/cybertraining). Run it only in its supplied isolated range. If that range is routed, recreate its lab hosts in the `internal: true` containerlab topology below, prove there is no default route, and then follow the lab procedure there.

If you build your own topology, use [containerlab](https://containerlab.dev/manual/) plus Docker `internal: true` networks and [Scapy’s official introduction](https://scapy.readthedocs.io/en/stable/introduction.html). Before generating a packet, prove the namespace has no default route, capture traffic at every interface, cap total packets, and verify cleanup. Do not bridge it to Wi-Fi, Ethernet, a VPN, cloud VPC, or the Internet.

Report packet/connection rate, state table or queue behavior, loss/errors, service latency, recovery time, control effect, and proof of isolation. The required skill is controlled offensive reproduction plus defensive validation—not traffic volume.

### Self-assess

1. Reflection versus amplification: what is the distinction?
2. Why prove no default route before packet generation?
3. What makes a Deep DDoS lab complete?

<details><summary>Check your answers</summary>

1. Reflection redirects a responder’s reply using spoofed source identity; amplification makes the reply larger than the request. They often occur together but are different properties.
2. To demonstrate generated traffic cannot escape the isolated topology.
3. Named resource, bounded reproducer, telemetry, abort condition, mitigation, retest, recovery measurement, and isolation evidence.

</details>

[Next: Module 6 Deep](#module-6-deep)


---

---

# Module 6: Practical Python and secure code review

**Red-team outcome:** Build bounded offensive clients, automate attack variations, and review code for trust, parsing, retry, concurrency, and resource-exhaustion weaknesses.

<a id="module-6-foundation"></a>
## Foundation

### Learn

Python reads top to bottom. Values have types: strings (`"GET"`), integers (`200`), floats (`12.5`), booleans (`True`), and `None`. The main containers are:

```python
paths = ["/login", "/search"]                 # list: ordered values
event = {"path": "/login", "status": 401}   # dict: key -> value
sessions = {"s1", "s2"}                      # set: unique values
```

A loop processes each item; an `if` chooses a branch; a function names reusable behavior:

```python
def is_failed_login(event: dict[str, object]) -> bool:
    return event.get("path") == "/login" and event.get("status") == 401

failures = 0
for event in events:
    if is_failed_login(event):
        failures += 1
```

JSONL stores one JSON object per line. It is convenient for event streams because a program can parse one line at a time:

```python
import json
from pathlib import Path

events = []
for line in Path("lab/fixtures/requests.jsonl").read_text().splitlines():
    events.append(json.loads(line))
```

Use `Counter` to group and count:

```python
from collections import Counter

by_population = Counter(event["population"] for event in events)
print(by_population)
```

Sessionization groups events by a stable session key and usually sorts them by time. Without a session ID, analysts sometimes use a timeout gap, but that is an inference and can merge people behind a shared address or split one person across addresses.

Secure network code needs:

- an allowlisted destination;
- connect/read timeout;
- bounded total attempts;
- bounded retries with backoff;
- bounded concurrency;
- response-size limit;
- redirect policy;
- error handling and cleanup.

Common review bugs:

```python
while True:                         # unbounded retry
    send()

requests.get(url)                   # no timeout; arbitrary target

asyncio.gather(*(call(x) for x in huge_input))  # unbounded concurrency

query = "SELECT * FROM users WHERE name='" + name + "'"  # injection
```

Fix them with explicit limits, validation, semaphores/worker pools, parameterized queries, and tests for rejection paths.

### Lab

Run three attacker workflows, then the tests:

```bash
python -m lab.run credential
python -m lab.run evasion
python -m lab.run bypass
python -m unittest discover -s lab/tests -v
```

Open `lab/run.py`. Find the fixed target, request builder, timeout, baseline check, one-variable detector evasion, challenge-token capture, cross-session replay, and failure handling. For each, mark whether it generates the attack, constrains it, or preserves evidence.

Open `lab/clients/safe_client.py`. Find the URL validator, timeout, fixed response read limit, total-request cap, and disabled redirect following. These are engagement safeguards around offensive tooling; write down one failure each prevents.

Finally write this five-line program yourself:

```python
from lab.detectors.rules import score_event
event = {"webdriver": True, "accept_language": "", "sec_fetch_site": ""}
print(score_event(event))
event["webdriver"] = False
print(score_event(event))
```

Expected decisions: `challenge`, then `allow`. You wrote an attack mutation in Python and reproduced the bypass without editing the detector.

### Self-assess

1. List versus set: when would you use each?
2. Why can sessionization by IP be wrong?
3. What does a timeout bound?
4. What is wrong with `asyncio.gather` over an unbounded input?
5. How do parameterized queries prevent injection?

<details><summary>Check your answers</summary>

1. A list preserves ordered values and duplicates; a set gives uniqueness and fast membership checks.
2. Many users can share an IP and one user can change IPs.
3. How long an operation may wait; it does not by itself limit retries or concurrency.
4. It can create enormous simultaneous work and exhaust memory, sockets, or the target.
5. The database receives code and data separately, so input is not parsed as query syntax.

</details>

[Next: Module 7 Foundation](#module-7-foundation)


If the Python syntax above is unfamiliar, complete the official [Python Tutorial Sections 3–5](https://docs.python.org/3/tutorial/index.html) before Applied. Those sections cover control flow, functions, and data structures; you do not need the entire tutorial first.

<a id="module-6-applied"></a>
## Applied

### Learn

Type hints describe intended values and let a checker find mismatches before runtime. Tests prove selected examples and failure paths. Neither replaces input validation.

Asynchronous code lets one task make progress while another waits on I/O. It does not make CPU work free. Bound it with a semaphore:

```python
semaphore = asyncio.Semaphore(5)

async def bounded_call(item: str) -> Result:
    async with semaphore:
        return await call(item, timeout=2.0)
```

Retries should be limited, delayed, and selective. Retry a transient timeout or `503`; do not automatically retry an invalid credential or every `4xx`. Add jitter so many clients do not retry in lockstep. A retry budget limits the additional load retries can create.

Review data flow from source to sink: external input → parsing/validation → state → sensitive operation. Also review resource lifecycle: open → use → close; acquire semaphore → release; create task → await/cancel; log → minimize secrets.

### Lab

Extend a copy of the safe client into a bounded attack runner with a five-worker thread or async pool, a two-second timeout, at most two retries for `503`, and a maximum of 20 total attempts. Add a mutation function that rotates the local `session_id` and use it to reproduce `python -m lab.run ratelimit`. Keep the target validator unchanged. Add tests that reject a public URL, reject concurrency 6, stop at the attempt budget, and do not retry `401`.

Run type and style checks if the development dependencies are installed:

```bash
python -m mypy lab scripts
python -m ruff check lab scripts
```

For guided practice, complete [Exercism Python: Lasagna, Ghost Gobble Arcade Game, and Inventory Management](https://exercism.org/tracks/python/exercises) plus the official [Python asyncio queues example](https://docs.python.org/3/library/asyncio-queue.html#examples). These assignments cover functions, conditionals, collections, and bounded producer/consumer work.

### Self-assess

1. Why not retry `401` automatically?
2. What does a semaphore bound?
3. Why test rejection paths?

<details><summary>Check your answers</summary>

1. The credential or authorization is invalid; retrying adds load and can trigger lockout without changing the cause.
2. The number of tasks inside a protected concurrent section.
3. Safety and validation controls are useful only if malformed or out-of-scope inputs actually fail closed.

</details>

[Next: Module 7 Applied](#module-7-applied)

<a id="module-6-integrated"></a>
## Integrated

### Learn

An engagement tool is a pipeline: generate a population, execute a bounded workflow, record structured events, score, aggregate metrics, and render a report. Give every record a schema version, run ID, population, session, request ID, monotonic sequence, timestamp, action, result, and error. Never log passwords or real session tokens.

Reproducibility requires deterministic fixtures where possible, recorded random seeds, dependency versions, configuration, and a command that recreates the result. A tool should distinguish operational failure from security outcome; “browser crashed” is not “defense blocked the bot.”

### Lab

Modify `lab/run.py workflow` in a branch or temporary copy so each JSON line includes one run ID, attacker-population label, and monotonically increasing sequence. Save output as JSONL. Add at least two mutations—session-key rotation and one bot-signal change—and report protected-action completion, control action, and median actions by population. The parser must reject a missing run ID.

Add a proxy label and agent-decision field even if the value is `none` or `fixed-policy`. This prevents later analysis from guessing how traffic was produced.

### Self-assess

1. Why separate tool error from defense action?
2. What fields make a workflow trace joinable?
3. Why record dependency versions?

<details><summary>Check your answers</summary>

1. They have different causes and remediation; combining them inflates apparent control effectiveness.
2. Run, population, session, request/trace, sequence, time, action, and result identifiers.
3. Browser and library changes can alter traffic and behavior; a second person needs the same environment to reproduce it.

</details>

[Next: Module 7 Integrated](#module-7-integrated)

<a id="module-6-deep"></a>
## Deep

### Learn

Large logs should stream rather than load entirely into memory. Iterate line by line, aggregate only required state, and write incremental output. Measure peak memory and throughput before choosing parallelism. More concurrency can reduce throughput when locks, disk, CPU, or the target saturate.

A reusable CLI needs clear subcommands, safe defaults, configuration precedence, structured errors, exit codes, dry run, progress, and an output schema. Security tools should make the safe action easier than the unsafe action.

### Lab

Generate a synthetic JSONL attack corpus at least 100 times larger than the fixture by repeating records with new IDs and controlled signal mutations. Implement a streaming scorer that reports which mutations move `challenge` to `allow` without storing all records. Measure elapsed time and peak memory, and preserve the generator seed and command.

Package the offensive tool as a CLI with `plan`, `run-local`, `replay`, and `report` subcommands. `plan` must print the resolved target, mutations, caps, and output without traffic; `run-local` must reject non-loopback destinations; `replay` must require a captured local fixture; `report` must distinguish bypass, blocked attack, and tool failure. Add tests for malformed input, missing fields, arbitrary targets, attempt-budget exhaustion, and interrupted writes.

If you need a mature exploit-development range rather than another repository exercise, use the source-guided scripting and reporting work in [OffSec WEB-300](https://help.offsec.com/hc/en-us/articles/360046868971-WEB-300-Advanced-Web-Attacks-and-Exploitation-FAQ) or the relevant modules in the [HTB Senior Web Penetration Tester path](https://academy.hackthebox.com/path/preview/senior-web-penetration-tester). This is an alternative assignment, not extra work.

### Self-assess

1. When is loading the whole file acceptable?
2. Why can more concurrency reduce performance?
3. What should a safe dry run show?

<details><summary>Check your answers</summary>

1. When the bounded input comfortably fits memory and simplicity is more valuable than streaming complexity.
2. It can increase contention, context switching, queueing, memory, and downstream saturation.
3. Resolved target, actions, caps, exclusions, configuration source, and output location without executing traffic.

</details>

[Next: Module 7 Deep](#module-7-deep)

---

---

# Module 7: Experimental method, detection analysis, and reporting

**Red-team outcome:** Convert an attack into a falsifiable experiment, defensible bypass finding, actionable remediation, and identical retest.

<a id="module-7-foundation"></a>
## Foundation

### Learn

An experiment turns an opinion into a falsifiable comparison.

- **Question:** what do you want to know?
- **Hypothesis:** what result do you predict and why?
- **Independent variable:** the one factor you change.
- **Dependent measure:** what you observe.
- **Controls:** what stays fixed.
- **Baseline:** comparison without the tested change.
- **Alternative explanations:** other reasons for the result.
- **Limitation:** where the evidence does not transfer.

Example:

```text
Question: Does endpoint cost change service latency at equal request count?
Hypothesis: The bounded expensive route has higher median latency because it performs more CPU work.
Change: route (/health versus /api/reports/expensive?work=100)
Fixed: five sequential requests, same client, same host, same run
Measure: elapsed milliseconds
Limitation: local sequential timing does not estimate production capacity
```

Detection metrics need counts and a labeled ground truth. If labels are synthetic, say so. Service experiments need traffic and health metrics. A chart without units, population, time window, and sample count is not interpretable.

A finding is concise:

```text
Title and severity rationale
Condition
Evidence and reproduction
Impact
Affected scope
Recommendation
Retest and success criterion
Limitations
```

Severity comes from plausible impact and exploit conditions, not the cleverness of the technique.

### Lab

Run:

```bash
python -m lab.run evasion
python -m lab.run bypass
```

Write one six-sentence finding:

1. condition observed;
2. exact reproduction command and cap;
3. measured evidence;
4. plausible impact without exaggeration;
5. specific remediation;
6. retest and limitation.

Choose one bypass and make its blocked baseline, attack change, protected action, and successful result explicit. Compare yours with `lab/reports/synthetic-finding.md`. Correct any sentence that claims production behavior from the local fixture.

### Self-assess

1. What makes a hypothesis falsifiable?
2. Why hold other variables fixed?
3. What makes a retest pass condition useful?
4. Why is a perfect synthetic detector not “critical severity” evidence?

<details><summary>Check your answers</summary>

1. A possible observation could show it is wrong.
2. To attribute a difference to the chosen change rather than a confounder.
3. It names the repeated method and measurable result that demonstrates remediation.
4. Severity describes security impact; the detector result is tiny, designed, and non-production.

</details>

[Next: Module 8 Foundation](#module-8-foundation)

<a id="module-7-applied"></a>
## Applied

### Learn

Before execution, write a test matrix with population, variable, expected result, sample count, and abort condition. Afterward, preserve raw data separately from derived tables. Analysis code should recreate tables from raw evidence.

Alternative explanations are not disclaimers; they drive follow-up tests. If Playwright scored higher, possible causes include webdriver, headers, timing, platform mismatch, or workflow—not “automation” as an indivisible cause. Change one factor at a time.

Recommendations should map to the failed invariant. “Add a WAF” is vague. “Bind the challenge result to session, protected action, nonce, and five-minute expiry; reject reuse; monitor legitimate failure by population” is testable.

### Lab

Use the Module 4 temporary-fixture experiment. Before rerunning, write the hypothesis and expected confusion-matrix change. Run it, save raw fixture and JSON output, then make a table showing baseline versus changed condition. Write one alternative explanation and a follow-up experiment.

Give a five-minute briefing in this order: objective, method/safety, result, impact, limitation, recommendation, retest. Record it once. If any section exceeds one minute, shorten it.

### Self-assess

1. Why keep raw and derived data separate?
2. What makes a recommendation measurable?
3. What should a useful alternative explanation produce?

<details><summary>Check your answers</summary>

1. So analysis can be checked and rerun without silently altering evidence.
2. A named mechanism, owner/action, metric, threshold, and retest.
3. A competing hypothesis and an experiment that distinguishes it from the original explanation.

</details>

[Next: Module 8 Applied](#module-8-applied)

<a id="module-7-integrated"></a>
## Integrated

### Learn

The capstone connects the complete work cycle:

```text
authorization -> target reconnaissance -> attack hypothesis -> exploit/bypass
-> evidence and service impact -> finding -> remediation -> retest -> briefing
```

The report must make evidence easy to audit. Put scope and executive result first, method and findings next, raw commands/configuration in an appendix, and link every claim to a run/table/request ID. Report failed experiments and tool errors; they are part of reproducibility.

### Lab

Run one local capstone whose objective is to complete a protected workflow while evading or bypassing its control. Use the six populations from Module 4, the credential/workflow scenario from Module 2, and the challenge/resource experiments from Module 5. Produce:

1. one-page scope/runbook;
2. threat map;
3. population/test matrix;
4. raw JSONL and version/config record;
5. attack success, control action, and service-impact tables by population;
6. two findings with remediation and retest;
7. one-page executive summary;
8. five-minute briefing.

One finding must prove a bypass that completed the protected action; the other may be a second bypass, false positive, observability gap, or reliability weakness. Re-run the exact attack locally after implementing or simulating the recommended change.

### Self-assess

1. Can another person trace every conclusion to raw evidence?
2. Did the report distinguish defense action from tool failure?
3. Did every production implication remain a hypothesis?

<details><summary>Check your answers</summary>

All three must be yes. If not, add stable IDs/commands, separate outcome categories, or narrow the claim before continuing.

</details>

[Next: Module 8 Integrated](#module-8-integrated)

<a id="module-7-deep"></a>
## Deep

### Learn

Original research begins with a narrow unanswered question and a method that could disprove your explanation. Version and environment are variables. Reproduction by someone else is stronger evidence than more screenshots from the author.

For mature detection research, compare feature families, rule overlap, cost, drift, and population harm. Confidence should reflect evidence quality. “Observed in 10/10 controlled runs” is more honest than “always.”

### Lab

Choose one original evasion, replay, normalization, workflow-abuse, or bounded resource-pressure question from Modules 1–5. Preregister the hypothesis, variables, sample count, analysis, and stop condition before collecting data. Run a blocked baseline, at least two attack conditions, and one legitimate near-neighbor. Ask another person to reproduce from your instructions, or repeat in a clean environment.

Publish a portfolio version with synthetic data only: abstract, threat model, ethics/scope, method, results, alternative explanations, limitations, remediation, retest, and reproduction commands. Remove tokens, provider target details, and anything prohibited by an external range.

### Self-assess

1. What distinguishes original research from a product demo?
2. Why preregister the analysis?
3. What is a calibrated claim?

<details><summary>Check your answers</summary>

1. A falsifiable question, controlled comparison, evidence, limitations, and a result not assumed in advance.
2. To reduce changing the method after seeing results and cherry-picking favorable measures.
3. A conclusion whose confidence and scope match the quantity and quality of evidence.

</details>

[Next: Module 8 Deep](#module-8-deep)

---

---

# Module 8: Interview communication and role translation

**Red-team outcome:** Explain an attack plan and bypass evidence clearly enough that another engineer can reproduce the weakness, judge impact, implement a fix, and run the retest.

<a id="module-8-foundation"></a>
## Foundation

### Learn

An interview answer should make your reasoning visible. Use this technical structure:

```text
objective -> assumptions -> design/mechanism -> tradeoffs -> measurement
-> failure modes -> remediation/retest
```

Do not list tool names. Translate prior experience into role mechanisms. Incident response becomes hypothesis formation and evidence triage. Detection engineering becomes feature design and false-positive measurement. Network engineering becomes request-path and exhausted-resource reasoning. Application security becomes workflow abuse and remediation.

A 90-second role narrative has four parts:

1. current security identity and strongest evidence;
2. why bots/DDoS/red teaming is the logical next problem;
3. one course experiment that proves hands-on movement;
4. what value you can deliver while deepening the specialty.

Behavioral answers use Situation, Task, Action, Result, and Lesson. Spend most time on your actions and decisions. State metrics and what you would change.

A five-minute bot-control red-team plan should cover the protected action, request path, control assumptions, attack populations, fingerprint/identity/timing mutations, success evidence, safety, and retest. A DDoS test answer begins with the exhausted resource and service objective, then the smallest bounded reproducer, telemetry, abort conditions, mitigation, and identical retest.

### Lab

Write and say aloud:

- your 90-second narrative;
- one behavioral story about ambiguity;
- one about a security or reliability improvement;
- one about disagreement or a failed approach;
- a five-minute bot-control attack and bypass plan.

Record the answers on your phone. Listen once. Remove unexplained acronyms, unsupported “always/never” claims, and any section that hides your decision behind “we.”

### Self-assess

1. Can the listener identify your objective, decision, evidence, and result?
2. Did the technical answer include the attack path, bypass criterion, false positives, and measurement?
3. Did each behavioral story say what you personally did?
4. Can you explain the lab’s limitations without undermining its learning value?

<details><summary>Check your answers</summary>

All four should be yes. A good limitation sounds like: “The fixture proves the scoring and measurement workflow, not production accuracy; I would validate in shadow mode on representative populations.”

</details>

[Foundation checkpoint: stop or continue](CHECKPOINTS.md#foundation-about-24-focused-hours)

<a id="module-8-applied"></a>
## Applied

### Learn

Expect follow-ups that remove your first assumption: What if IP is shared? What if JavaScript is disabled? What if the detector is evaded? What if the traffic is a flash crowd? What if the dependency, not the edge, is saturated? Strong answers update the model instead of defending the first design at all costs.

For code, state input, output, constraints, data structure, complexity, failure handling, and tests before typing. For system design, start with objective and scale, draw the request path, name state and trust boundaries, then cover measurement and degradation.

### Lab

Prepare six behavioral stories with no duplicated primary example. Run two 45-minute mocks:

1. bot/automated-abuse attack plan, evasion strategy, and bypass evidence;
2. bounded DDoS/resource-exhaustion attack plan, mitigation test, and retest.

After each answer, ask the reviewer to challenge one assumption. Revise the answer to incorporate the new constraint. Score 0–2 on structure, correctness, evidence, tradeoffs, and clarity. Repeat any answer below 7/10.

Use these practice questions:

- Design red-team coverage for a bot detection platform.
- How would you test fingerprint evasion safely?
- Diagnose high latency at unchanged RPS.
- Compare per-IP and workflow-aware rate limits.
- Design an AI browser attacker, then explain how you would test its evasion and constrain its tools.
- Review a client with no timeout and unbounded retries.

### Self-assess

1. What should happen when a follow-up invalidates an assumption?
2. What comes before choosing a data structure in a coding answer?

<details><summary>Check your answers</summary>

1. State the changed assumption, update the design, and explain the new tradeoff.
2. Clarify input, output, constraints, and failure cases.

</details>

[Applied checkpoint: stop or continue](CHECKPOINTS.md#applied-about-7-days)

<a id="module-8-integrated"></a>
## Integrated

### Learn

A full loop tests several modes: coding/review, technical depth, system design, behavioral judgment, and portfolio communication. Reusing the same polished speech in every session is weaker than selecting evidence that answers the specific question.

Use a claim-evidence-limitation pattern. “I built X” is a claim; the command, trace, metric, finding, and retest are evidence; local scale and synthetic populations are limitations. This pattern is credible because it neither undersells nor exaggerates.

### Lab

Run five sessions on separate days if possible:

1. Python offensive tooling and exploit-oriented code review;
2. browser-bot evasion technical deep dive;
3. WAF bypass and bounded DDoS/edge attack design;
4. three behavioral stories with skeptical follow-up;
5. capstone briefing and questions.

Use the same 0–2 rubric. For every score below 2, write one corrective action and repeat that section. The loop is complete when no category is below 1 and the average is at least 1.5; this is only a self-assessment marker.

### Self-assess

1. Can every major claim point to course evidence?
2. Can you defend one failed experiment or changed conclusion?
3. Can you adapt a design when scale, privacy, or customer-impact assumptions change?

<details><summary>Check your answers</summary>

All three should be yes. If an answer relies only on memorized terminology, return to the matching experiment.

</details>

[Integrated checkpoint: stop or continue](CHECKPOINTS.md#integrated-about-21-days)

<a id="module-8-deep"></a>
## Deep

### Learn

Senior communication teaches the model, defends tradeoffs, and identifies what remains unknown. A 90-day proposal should not promise a rewrite. It should begin with people, architecture, telemetry, current incidents, false-positive populations, and safe reproduction; then choose one measured improvement.

### Lab

Teach one 20-minute lesson from this course without reading the text. Include a demonstration and answer skeptical questions. Then run two more full mock loops with different reviewers or question order.

Write a first-90-day plan:

- Days 1–30: learn owners, architecture, controls, incidents, data governance, and safe test process.
- Days 31–60: reproduce one priority weakness, establish baseline/false positives, and propose a bounded remediation.
- Days 61–90: validate in shadow/canary mode, retest, document, and select the next research question.

Tie each phase to a deliverable and measure. Avoid promising production access or high-volume testing before authorization and system understanding.

### Self-assess

1. Can another learner follow your explanation and reproduce the demo?
2. Does the 90-day plan learn before changing production?
3. Does every proposed improvement have a measure and retest?

<details><summary>Check your answers</summary>

All three should be yes. If teaching reveals a gap, return to that module’s Learn and Lab sections; that is the purpose of the exercise.

</details>

[Deep checkpoint: course complete](CHECKPOINTS.md#deep-about-6-weeks)

---

# You are done

There is no repository ceremony. If you completed a section’s lesson, lab, and self-assessment honestly, continue or stop at a checkpoint. Use [RESOURCES.md](RESOURCES.md) only when a module assigns it or when you want another authorized lab.
