# Adversarial Traffic Engineering Course

This is the entire course. You do not need to understand the repository.

This is a **red-team-first course**. You learn a defense well enough to identify its trust assumptions; then you attack those assumptions, complete the protected action, preserve bypass evidence, recommend a fix, and retest. Detector design and defensive telemetry support that mission. They are not the mission.

1. Read **Learn**.
2. Do **Lab**.
3. Answer **Self-assess**, then check the answers.
4. Click the next link.

Complete the course in the order presented. Finish Foundation, Applied, Integrated, and Deep in Module 0 before starting Module 1; then repeat that pattern through Module 8. Every stage assumes that you can still perform the earlier work. There is no schedule or alternate path.

Every core lab uses this attack loop:

```text
authorize and define the objective -> passive reconnaissance -> bounded active mapping
-> map the workflow, controls, and exhausted resources -> establish the blocked baseline
-> state a bypass hypothesis -> execute the attack -> prove the protected action succeeded
or the mitigation failed -> explain impact -> recommend a fix -> run the same test again
```

Reconnaissance is the setup for the attack, not a substitute for it. **Passive recon** uses existing information without sending requests to the target. **Active recon** interacts with the target to discover hosts, services, routes, parameters, workflows, controls, and response behavior. Active recon is testing and must be explicitly authorized, bounded, and logged.

## Recon before attack

Each attack lab tells you what must be discovered before that attack makes sense. Preserve only four things: the authorized target and objective, the observed attack surface/workflow/control, the blocked baseline, and the first bypass hypothesis supported by those observations. Label evidence `documented`, `observed`, or `inferred`; do not fill gaps with guesses. If recon reveals a new host or service, it is a scope question, not automatic permission.

Before a lab, start the target once:

```bash
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
python -m lab.run recon
```

The recon command inventories the local API, performs five bounded probes, and prints four evidence-backed attack hypotheses. Use only the bundled local target, your isolated self-hosted target, or the exact target a training provider assigns. When finished, run `docker compose -f lab/docker-compose.yml down`.

---

# Module 0: Safety and red-team engagement discipline

**Red-team outcome:** Define an authorization and containment envelope that lets you execute real attack techniques in a lab without crossing the target boundary.

<a id="module-0-foundation"></a>
## Foundation

### Learn

**Required foundation — complete before the lab.** Read NIST SP 800-115 [Sections 3.1–3.3](https://csrc.nist.gov/pubs/sp/800/115/final), including the assessment-plan and Rules of Engagement material. Do not skim only the technique list. Your notes must define who authorized the work, the exact target, permitted and excluded actions, the time window, data-handling rules, contacts, monitoring, incident handling, stop conditions, cleanup, and reporting.

Authorization is permission from the system owner for a specific target, action, time, and data set. Owning an account or being able to reach a host is not authorization to security-test it.

A **red-team exercise** imitates an adversary to test whether a security objective survives realistic action. The objective is not “run tools” or “find anything.” It is a statement such as “an unauthenticated actor cannot reserve inventory” or “a challenge result cannot authorize another session.” The red team establishes the control’s normal blocked behavior, attempts to violate the objective, proves the protected outcome, and helps verify the fix.

Three roles matter even in a home lab:

- the **owner** controls the target and grants permission;
- the **tester** performs only the authorized actions;
- the **operator/monitor** watches service health and can stop the run.

One person may hold all three roles locally, but writing them down teaches the separation needed on a real engagement. Permission must come from someone who actually controls the system. A third-party website, shared network, cloud service, or adjacent machine does not become testable because it is reachable.

Authorization has dimensions. Ask all of them before sending traffic:

| Dimension | Example |
|---|---|
| Asset | `localhost:8080`, not every service on the computer |
| Action | replay a synthetic challenge token, not test arbitrary vulnerabilities |
| Time | this lab session or an approved window |
| Identity/data | synthetic accounts and products only |
| Technique | bounded HTTP requests; no unrelated packet generation |
| Intensity | 10 total requests, 2 requests/second, 1 at a time |
| Evidence | synthetic logs retained locally; no real secrets |

**Scope** is the executable boundary of that permission. “Local lab” is still ambiguous if the computer runs other services. `http://localhost:8080` is narrower; an exact route and method are narrower still. Scope also names exclusions. If a local proxy redirects to another port, the new destination must be revalidated even though it is on the same machine.

**Rules of engagement** explain how the test will be conducted: contacts, schedule, allowed discovery, tools, traffic caps, test data, monitoring, incident handling, cleanup, evidence storage, and reporting. **Stop conditions** are the measurable subset that end work immediately. The tester stops traffic first, then preserves evidence and diagnoses. Continuing “for one more sample” after the stop condition defeats the safety control.

Reconnaissance needs its own boundary. Passive sources may reveal assets the owner did not list, while active discovery sends traffic and can trigger controls or consume capacity. Record allowed data sources, domains, hosts, ports, paths, tools, rates, and whether discovered adjacent assets remain excluded until the owner adds them.

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

**You are ready for the lab when you can:** distinguish authorization, scope, Rules of Engagement, and a stop condition; write an exact target and action instead of “my lab”; explain why discovery does not expand permission; and say what you do first when a stop condition trips.

### Lab

Prove the bundled client’s allowlist works:

```bash
python -m lab.clients.safe_client --dry-run
python -m lab.clients.safe_client --target https://example.com --total 1
```

The first command prints the local target and caps without sending traffic. The second must print `"rejected": true`. Rejection is the successful result.

Write this eight-line plan in any notes app:

```text
Owner: me
Target: localhost:8080
Allowed: GET /health with the bundled client
Recon: local OpenAPI plus five bounded GET probes
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

[Next: Module 0 Applied](#module-0-applied)

<a id="module-0-applied"></a>
## Applied

### Learn

An engagement plan turns written permission into controls the operator can actually enforce. A sentence such as “test the application” is not executable scope. The tester needs to know which hostnames and addresses are allowed, whether DNS-discovered names are included, which accounts and data may be used, which techniques are allowed, when traffic may run, who can stop it, and what evidence may be retained.

Separate five ideas that are often mixed together:

1. **Objective:** the security claim being tested, such as “a challenge result cannot authorize a different session.”
2. **Target:** the exact system and protected action, such as `localhost:8080/api/reports/protected`.
3. **Technique:** the interaction used to test the claim, such as token capture and cross-session replay.
4. **Envelope:** rate, concurrency, total attempts, duration, data, and tooling limits.
5. **Stop authority:** the person or automated condition that ends traffic immediately.

The objective prevents random probing. The target prevents accidental expansion. The technique tells the owner what behavior to expect. The envelope limits impact even when the technique behaves unexpectedly. Stop authority resolves the dangerous question “who is allowed to call this off?” before the test begins.

Preflight is a sequence of gates, not a checkbox. Resolve the hostname and compare every resulting address with the allowlist. Confirm that the account and data are synthetic. Print the exact request plan without sending it. Record the tool and version. Check the target’s health with the agreed measure. Start below the maximum rate and increase only when the runbook permits it. If discovery reveals an adjacent asset, do not touch it: record it as a scope question.

**Worked example.** Suppose a rate-limit test allows `localhost:8080`, `/api/reports/limited`, 20 total requests, two requests per second, and one concurrent request. The client follows a redirect to `localhost:9090`. Even though the hostname is still `localhost`, the port and service are outside the stated target. A fail-closed client rejects the redirect; it does not assume that adjacency grants permission. If p95 latency exceeds 500 ms for 30 seconds, the operator stops new work, records the last request ID and time, and waits for recovery. Evidence collection continues only if it sends no additional target traffic.

Read [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final), Sections 3.1–3.3, alongside this lesson. Use its assessment-plan and Rules of Engagement material to check that your plan identifies scope, authorized and excluded systems, logistics, data handling, incident handling, and reporting—not merely a list of tools.

### Lab

Run a five-request engagement:

```bash
python -m lab.clients.safe_client --target http://localhost:8080/api/search?q=demo --rps 2 --total 5
```

Expect five JSON lines with `"ok": true` and `"status": 200`. Add the resolved address, actual start/stop time, tool version, request IDs, health result, and cleanup result to your plan.

Now perform a tabletop failure. Pretend the third response took 700 ms and your abort threshold was 500 ms. Write the exact operator actions in order. A correct answer stops new requests first, records the trigger and last known state, checks recovery without exceeding the agreed health-check allowance, notifies the owner, and does not resume without the runbook’s approval path.

### Self-assess

1. Why print a dry run?
2. Why specify both a total cap and a rate cap?
3. Why must a redirect target be revalidated?
4. Objective versus envelope: what does each control?

<details><summary>Check your answers</summary>

1. To catch an incorrect target or unsafe envelope before execution.
2. They limit different things: all work versus work per unit time.
3. A redirect creates a new destination and may escape the authorized host, port, path, or address set.
4. The objective names the security claim; the envelope bounds how the test may pursue it.

</details>

[Next: Module 0 Integrated](#module-0-integrated)

<a id="module-0-integrated"></a>
## Integrated

### Learn

An integrated runbook is a dependency graph written as an ordered procedure. Each step has prerequisites, a command or source, an expected result, evidence to retain, an abort condition, and cleanup. Order matters because a security test changes the target: it can create accounts, consume inventory, warm caches, trigger rate limits, rotate tokens, fill queues, or leave sessions authenticated. If a later result depends on that changed state, the experiment can falsely attribute the effect to the wrong attack variable.

Use this order and understand why each transition exists:

1. **Authorization and objective:** establishes permission and the claim to test.
2. **Passive recon:** gathers supplied or public evidence without changing target state.
3. **Bounded active mapping:** confirms only authorized assets, routes, and behavior.
4. **Attack-surface review:** converts observations into ranked hypotheses.
5. **Health check:** proves the target is stable before the experiment.
6. **Reset:** removes accounts, tokens, inventory, cache, and rate-limit state from earlier work.
7. **Blocked baseline:** proves the control stops the original attack before you claim a bypass.
8. **Adversarial population:** changes the chosen attacker variable and attempts the same protected action.
9. **Detection evaluation:** distinguishes allow, challenge, throttle, block, tool error, and target error.
10. **Resilience test:** measures whether bounded hostile work harms the protected service objective.
11. **Evidence export:** freezes commands, versions, logs, IDs, and derived results.
12. **Cleanup and recovery:** removes test state and proves the service returned to baseline.

The reset and blocked baseline are especially important. Imagine a challenge token issued during mapping remains valid during the bypass run. The later `200` might be a stale-token artifact rather than the mutation you intended to test. Resetting state and proving the unmodified attack receives `403` makes the changed request interpretable.

A **decision log** records operator reasoning that telemetry cannot: `14:03 | p95 reached 420 ms | continue at current rate | below 500 ms abort threshold; no errors`. It should also record rejected hypotheses and deviations. A target log can show requests, but it cannot show why the tester selected a mutation or why a run stopped.

Provider-hosted ranges have a separate trust boundary. Authorization ends at the assigned targets and allowed techniques. Provider websites, identity systems, VPN gateways, scoring infrastructure, adjacent machines, and unassigned addresses are excluded unless the provider explicitly says otherwise. Use the provider’s supplied connection method and tooling rules; do not repoint this repository’s local client at a remote range.

### Lab

Build a twelve-row runbook for the local challenge-token bypass. Each row must contain: prerequisite, command/source, expected result, evidence file or request ID, authorization boundary, abort condition, and cleanup. Use real local commands where they exist, including `python -m lab.run recon`, `python -m lab.run bypass`, the health request, and container shutdown.

Walk it as a tabletop without traffic. Inject these three failures one at a time:

- active mapping discovers an unexpected listener on port 9090;
- the pre-attack health check fails twice;
- the attack tool exits before writing its evidence file.

For each failure, state whether the run stops, what evidence is still trustworthy, who is notified, what cleanup is safe, and what approval is needed before retrying. Fix any row that leaves the operator improvising.

### Self-assess

1. Why can test order invalidate results?
2. What does a decision log contain that telemetry does not?
3. Why reset before establishing the blocked baseline?
4. What happens when mapping discovers an unlisted adjacent service?

<details><summary>Check your answers</summary>

1. One test can change accounts, inventory, cache, or service health seen by the next.
2. The operator’s interpretation and reason for continuing, changing, or stopping.
3. To prevent stale tokens, state, cache, rate counters, or inventory from explaining the later result.
4. Pause interaction with it, record it as a scope question, and wait for explicit authorization.

</details>

[Next: Module 0 Deep](#module-0-deep)

<a id="module-0-deep"></a>
## Deep

### Learn

Production validation is not “run the lab attack against production at a lower rate.” A lab result establishes a mechanism under controlled conditions. Production may have different proxy chains, detector versions, data, customer populations, dependency costs, and failure modes. The safe way to investigate transfer is a sequence of evidence gates in which each stage authorizes only the next stage.

The gates reduce uncertainty while keeping enforcement and customer impact proportional to the evidence already earned.

Use six stages:

1. **Approved recon:** confirm the production request path, control owner, service objective, telemetry, customer populations, and change process without attempting the bypass.
2. **Lab reproduction:** reproduce the exact production configuration or the relevant control invariant in an isolated environment. Record every known difference.
3. **Offline analysis:** replay sanitized historical events or score a fixed corpus without sending target traffic or enforcing decisions.
4. **Shadow evaluation:** compute the proposed control or attack classification on live traffic but take no customer-facing action. Measure action rate, false-positive review, missing data, latency overhead, and drift.
5. **Allowlisted canary:** exercise synthetic accounts or traffic explicitly routed to the canary while monitoring both the tested control and service health.
6. **Broader authorized use:** expand only after the owner accepts the evidence, residual risk, monitoring, and rollback plan.

Each gate needs an **advance criterion** and a **rollback criterion**. “Looks good” is not a criterion. An example shadow advance criterion is “at least 10,000 events across all named legitimate populations, no population with reviewed false-positive rate above 0.5%, and scoring overhead below 5 ms p95.” A rollback criterion might be “any real enforcement, any collection of an unapproved field, or scoring overhead above 10 ms p95 for five minutes.” The numbers must come from the service owner; these are examples of measurable form, not universal thresholds.

Keep four claims separate:

- **Observation:** what production architecture or telemetry directly shows.
- **Lab result:** what the isolated attack proved.
- **Transfer hypothesis:** why the same invariant may exist in production.
- **Production evidence requirement:** what would confirm or falsify that hypothesis safely.

For example, a local challenge token replay proves that the local server accepts a token across sessions. Seeing the same token fields in production does not prove the same weakness. A white-box configuration review might show whether the server binds the token to session and action. An offline replay test might then verify enforcement without attempting account access. Only approved canary evidence could support a production claim.

Study [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final), Sections 5.1 and 5.2, for analysis, mitigation recommendations, and reporting. The required takeaway is that technical evidence must be analyzed in context, findings must be prioritized, mitigation should address root cause, and the assessment process includes communication and follow-up—not simply exploitation.

### Lab

Choose the local challenge-token replay or rate-limit-key rotation finding. Write a six-stage transfer plan using the sequence above. For every stage include owner, authorization, input data, action, evidence, advance criterion, rollback criterion, monitoring, cleanup, and the exact claim the stage may support.

Then perform a claim audit. Highlight any sentence that jumps from “observed locally” to “production is vulnerable,” that treats a detector score as ground truth, or that lacks an owner and measurable gate. Rewrite it until a reviewer can tell exactly what is known, inferred, and still prohibited.

Add one decision table with rows for lab, offline, shadow, canary, and broader use. Include `may send traffic?`, `may enforce?`, `approved data`, `owner`, `advance`, and `rollback`. Walk two tabletop failures: the shadow scorer begins collecting an unapproved raw fingerprint, and the canary’s p95 latency exceeds its rollback threshold. In both cases, the correct action is to stop or roll back the affected stage, preserve evidence, notify its owner, and require a new decision before resuming. Do not treat a previous stage’s approval as permission to continue.

### Self-assess

1. Does a lab bypass prove production is vulnerable?
2. Why run a shadow evaluation?
3. What is the difference between an advance criterion and a rollback criterion?
4. Which claim can an offline replay support that it cannot support?

<details><summary>Check your answers</summary>

1. No. It creates a transfer hypothesis; production differs in controls, traffic, data, and scale.
2. To measure behavior and false positives without taking enforcement action.
3. Advance says what evidence is sufficient to consider the next stage; rollback says what condition makes the current stage stop or revert.
4. It can support how a fixed scorer behaves on the approved historical corpus; it cannot prove live enforcement safety or that a production attacker can complete the protected action.

</details>

[Next: Module 1 Foundation](#module-1-foundation)

---

---

# Module 1: Web request path and network fundamentals

**Red-team outcome:** Capture, mutate, proxy, and replay traffic while explaining which attacker-controlled values survive each intermediary.

<a id="module-1-foundation"></a>
## Foundation

### Learn

**Required foundation — choose one route and complete it before the lab.**

- **Free route:** read Cloudflare’s primers for [DNS](https://www.cloudflare.com/learning/dns/what-is-dns/), [TCP/IP](https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/), and [TLS](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/). For each, draw the client and server, name what is exchanged, and state what successful completion does and does not prove. Then read MDN’s [Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) and [HTTP messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages). Use the request and response examples until you can identify the request target, method, headers, body, status, and response headers without a key.
- **Guided route:** complete HTB Academy [Introduction to Networking](https://academy.hackthebox.com/course/preview/introduction-to-networking) through **TCP/UDP Connections**, then complete the entire [Web Requests](https://academy.hackthebox.com/course/preview/web-requests) module, including its exercises with cURL and browser developer tools.

The route is instruction, not background reading. Do its examples. Keep one annotated DNS/TCP/TLS/HTTP request trace; it becomes your input to this course’s local attack.

Follow a request through this logical path:

```text
Browser -> DNS -> CDN/edge -> WAF/bot control -> load balancer
        -> application -> database/cache/dependency -> response
```

Start with the pieces beneath HTTP.

An **IP address** identifies a network interface for routing. A **port** selects a listening service on that host; `443` is a convention for HTTPS, not proof of what software is there. The pair `address:port` is one network endpoint. A hostname can resolve to several addresses, and several hostnames can share an address.

**DNS** translates a hostname such as `example.test` into records such as IPv4 (`A`) or IPv6 (`AAAA`) addresses. The client normally queries a configured resolver, receives an answer with a time-to-live, then connects to one returned address. DNS does not carry the URL path, HTTP method, cookies, or body. A red teamer records both the hostname the application expects and the address actually reached because virtual hosting, CDNs, and load balancers can serve different applications from shared addresses.

**TCP** provides an ordered byte stream between a client address/port and server address/port. The connection begins with a three-step handshake (`SYN`, `SYN-ACK`, `ACK`), carries bytes, and closes with state on both endpoints. A successful TCP connection proves something accepted that transport connection; it does not prove HTTP is healthy or the user is authorized. Connection creation rate, open connections, and application requests are different measurements.

**TLS** usually sits above TCP for HTTPS. During the handshake, the server presents a certificate whose names let the client authenticate the requested hostname, the parties negotiate cryptographic parameters, and encrypted application data follows. TLS protects data between its endpoints. If a CDN or reverse proxy terminates TLS, it can read HTTP and normally creates another connection—possibly another TLS connection—to the origin. “Encrypted” does not mean every intermediary is blind.

A URL has components:

```text
https://shop.example.test:443/api/search?q=kit#results
\___/   \________________/ \_/ \_________/ \___/ \_____/
scheme        host          port    path     query fragment
```

The browser does not send the fragment (`#results`) in the HTTP request. The query is part of the request target and commonly reaches logs, caches, and application routing. Sensitive values should not be placed there. The scheme determines how the client establishes the connection; the `Host` header or HTTP/2 authority tells shared infrastructure which virtual service is intended.

HTTP is a client-server request/response protocol. It is **stateless** at the protocol level: each request can be understood as a message, even though applications create state with cookies, tokens, server-side sessions, and databases. Read MDN’s [Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) once before the lab. It is required beginner instruction for clients, proxies, requests, responses, statelessness, cookies, connections, and HTTP messages; the rest of this section maps those ideas to red-team evidence.

Recon builds this diagram from evidence. Start with the authorized asset list. Passive sources can add candidate names, addresses, certificate names, technologies, documentation, and historical paths without contacting the target. Active mapping then confirms only the authorized candidates and records reachable services, HTTP behavior, entry points, methods, parameters, authentication, state, errors, and controls.

Use three labels:

- **Documented:** supplied by the owner, provider, DNS, certificate, source, or API description.
- **Observed:** returned by an authorized request, browser trace, service probe, or capture.
- **Inferred:** a testable explanation, such as “this header suggests a reverse proxy” or “this parameter may be a rate-limit key.”

Read only Sections 4.1.3, 4.1.6, and 4.1.10 in [OWASP WSTG Information Gathering](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/). They teach metafile review, entry-point identification, and application-architecture mapping. Foundation does not require the full chapter or Internet-wide discovery.

**DNS** maps a hostname to an IP address. **TCP** provides a reliable byte stream and consumes connection state. **TLS** authenticates the server and encrypts traffic between TLS endpoints. A CDN that terminates TLS can inspect HTTP and usually makes a separate connection to the origin.

An HTTP request contains a method, path, headers, and optional body:

```http
GET /api/search?q=demo HTTP/1.1
Host: localhost:8080
Accept: application/json
```

The response contains a status, headers, and body. `2xx` means success, `3xx` redirect, `4xx` client or policy outcome, and `5xx` server failure.

Methods express intended operations. `GET` retrieves a representation and should not normally create business state. `POST` submits data or requests an action. `PUT` commonly replaces a resource, `PATCH` changes part of one, and `DELETE` removes one. `HEAD` requests headers without a response body, while `OPTIONS` can describe supported communication options. These are conventions enforced by application code; a route can be implemented incorrectly, so observe state rather than assuming the verb guarantees safety.

Important request headers include `Host`, `Content-Type`, `Accept`, `Cookie`, `Authorization`, and correlation headers such as `X-Request-ID`. `Content-Type` tells the recipient how to parse a body. The same logical fields encoded as JSON, form data, or multipart data may reach different parsers or validation paths. Important response headers include `Content-Type`, `Set-Cookie`, cache policy, redirect `Location`, and server/control correlation IDs.

Example JSON action:

```http
POST /api/cart/reserve HTTP/1.1
Host: localhost:8080
Content-Type: application/json

{"product_id":"demo-1","quantity":1,"session_id":"made-up"}
```

The method and status are not the complete security result. A `200` may return an error object without changing state; a `302` may create state before redirecting; a `404` may intentionally hide an existing unauthorized object. `401` normally means authentication is required or invalid, `403` means the server understood but refuses the action, `429` signals a rate policy, and `5xx` indicates server-side failure. Confirm the protected business state—inventory, account, report, redemption—not only the status.

A cookie is a value the browser returns on later requests. Session cookies usually carry an opaque identifier mapped to server-side state. `Secure` means HTTPS only, `HttpOnly` blocks ordinary JavaScript access, and `SameSite` constrains cross-site sending. Automation can replay cookies, so a cookie is not proof of a human.

The server sets a cookie with `Set-Cookie`; the browser later sends eligible values in `Cookie`. An opaque session ID is a lookup key, not the session data itself. A bearer token is different: possession normally authorizes whatever claims and scope the server accepts. Both are credentials and must be protected. A caller-supplied field named `session_id` is not trustworthy merely because its name says session; the server must create or validate the binding.

A **cache** stores a response and reuses it for requests considered equivalent by its cache key. A **reverse proxy** accepts a client request and makes an upstream request. A **load balancer** chooses a backend. A **WAF** parses HTTP and applies rules before forwarding. A **bot control** may combine browser, network, identity, and workflow evidence. One product can perform several roles, but the red-team questions stay the same: what does it observe, normalize, trust, cache, block, and forward?

A reverse proxy forwards requests, a CDN caches near users, a WAF applies HTTP policy, bot controls combine automation and workflow evidence, and a load balancer distributes work. Each may terminate connections, normalize headers, add IDs, cache, rate-limit, or block.

| Layer | Evidence | Resource that can fail |
|---|---|---|
| DNS | query rate, answer, TTL | resolver/authoritative capacity |
| TCP/TLS | connections, handshakes, bytes | sockets, CPU, bandwidth |
| Edge/WAF | requests, rule action, cache result | workers, inspection CPU |
| Application | route, status, latency, request ID | CPU, memory, tasks |
| Dependency | query latency, queue depth | pools, locks, storage I/O |

A request ID joins one exchange across layers. A session ID joins several requests in a workflow. Neither automatically identifies a person.

**You are ready for the lab when you can:** trace `https://host:port/path?q=value` through DNS, IP/port, TCP, TLS, and HTTP; annotate a raw request and response; explain where a cookie creates application state; distinguish a client, forward proxy, reverse proxy, cache, WAF, load balancer, application, and dependency; and predict which values the client can mutate before you send the request.

### Lab

Run the bounded local reconnaissance first:

```bash
python -m lab.run recon
```

The first JSON line is the documented route inventory from `/openapi.json`. The next five lines are active probes. The final four lines turn observations into candidate authorization, challenge, rate-limit, and resource-pressure attacks. Keep the relevant observations in your notes and mark them documented, observed, or inferred. This is your setup for the later attack commands.

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
5. Why must an inferred technology or control remain a hypothesis?

<details><summary>Check your answers</summary>

1. No; it resolves the hostname before HTTP.
2. Yes, at the termination point.
3. Endpoints perform different CPU, I/O, allocation, locking, or dependency work.
4. One exchange versus several exchanges in a workflow.
5. Headers, errors, and behavior can be hidden, changed, shared, or deceptive; corroborate the inference before building the attack around it.

</details>

[Next: Module 1 Applied](#module-1-applied)

<a id="module-1-applied"></a>
## Applied

### Learn

`curl`, Python, and a browser can request the same URL while presenting different transport, HTTP, and workflow evidence. `curl` normally sends a small header set and does not execute JavaScript. A Python client exposes whatever cookie jar, redirect policy, TLS library, and retry behavior the programmer selected. A browser manages origin rules, cookies, cache, redirects, JavaScript, workers, connection reuse, and navigation state. A control that classifies the client from one difference can confuse implementation with intent.

At TLS setup, the client advertises supported protocol versions, cipher suites, extensions, groups, and signature algorithms. **ALPN** lets the endpoints select an application protocol such as HTTP/1.1 or HTTP/2 inside the TLS handshake. A TLS fingerprint is a compact description of that advertisement and ordering. It can be useful population evidence, but it is not identity: many clients share a library, versions change fingerprints, and a proxy may create a different upstream TLS connection.

HTTP/1.1 usually carries requests sequentially or across a pool of connections. HTTP/2 assigns each request/response exchange to a stream and multiplexes many streams over one connection. That distinction changes the questions a red teamer asks. A connection-count rule may see one connection while the application processes many simultaneous requests. Conversely, repeatedly creating fresh connections can pressure TLS and socket state without high application RPS. Always distinguish requests per second, new connections per second, concurrent connections, and concurrent request streams.

An intercepting proxy divides the path into two connections: client-to-proxy and proxy-to-server. The server sees the proxy’s source and upstream transport behavior, while application values such as cookies, authorization headers, body fields, and action order may be forwarded unchanged. Therefore “the fingerprint changed” and “the attacker became a new identity” are different claims.

Replay is a controlled experiment when four conditions are met:

1. save the original request and response;
2. reset or document server-side state;
3. change one field;
4. compare both the control decision and the protected-action outcome.

A stale CSRF token, expired session, already-consumed inventory item, or warmed cache can otherwise create a difference unrelated to your mutation.

API reconnaissance builds a contract from both documentation and observation. For each route record method, path, parameters, body schema, content type, authentication, role, precondition, success response, failure responses, state change, and rate/challenge behavior. OpenAPI is **documented** evidence. Browser traffic and controlled requests are **observed** evidence. A route referenced in JavaScript but not yet requested remains a candidate until confirmed.

**Worked example.** `/api/cart/reserve` is documented as `POST` with `product_id`, `quantity`, and `session_id`. No authentication scheme appears in OpenAPI. That absence does not yet prove missing authorization; documentation can be incomplete. Send a request with a fabricated session, observe `200`, then check that inventory decreased. The protected state change—not the missing authentication declaration—is the proof that caller-supplied identity was trusted.

### Lab

Read PortSwigger’s free [API recon](https://portswigger.net/web-security/api-testing#api-recon) material through “Identifying supported content types.” Apply it only to the local target: load `/openapi.json` in Burp, select the search, product, reserve, challenge, limited-report, and protected-report routes, and record method, input, authentication/state, success status, and failure status. Do not fuzz yet.

Complete PortSwigger’s [Intercepting HTTP traffic with Burp Proxy](https://portswigger.net/burp/documentation/desktop/getting-started/intercepting-http-traffic) tutorial. Use its target or localhost only.

Then run:

```bash
curl.exe -s -D - http://localhost:8080/health
python -m lab.clients.safe_client --target http://localhost:8080/health --total 1
npm run playwright:foundation
```

The last command creates `lab/telemetry/foundation-playwright.jsonl`. Compare what each client exposes. In Burp Repeater, replay `GET /api/search?q=demo`, change `demo` to `kit`, and verify only the synthetic kit remains. Note the observed cookies, headers, redirects, routes, and state transitions before choosing the next bypass test.

Create a three-column comparison for curl, the safe Python client, and Playwright. Include transport endpoint, redirect behavior, cookie persistence, browser headers, connection reuse evidence available to you, and whether JavaScript ran. Mark “not observed” instead of guessing. Finish by naming one control that could misclassify these clients and one application invariant that remains the same across all three.

### Self-assess

1. What does ALPN select?
2. Why does a proxy change some transport evidence but not necessarily workflow evidence?
3. What four conditions make replay a controlled comparison?
4. Why does missing authentication in OpenAPI not prove an authorization bypass?

<details><summary>Check your answers</summary>

1. The application protocol over the encrypted connection.
2. It creates a new upstream connection, while cookies, accounts, request order, and payload semantics can remain.
3. Preserve the original, reset or document state, change one field, and compare control plus protected-action outcomes.
4. Documentation can be incomplete; the bypass is proven only when a fabricated or unauthorized identity performs the protected state change.

</details>

[Next: Module 1 Integrated](#module-1-integrated)

<a id="module-1-integrated"></a>
## Integrated

### Learn

An integrated request-path model joins infrastructure, protocol, application, identity, and business state. The join is the hard part. An edge request ID can connect client-visible behavior to a WAF log; an application request ID can connect that event to route handling; a session or account connects requests into a workflow; and a trace ID can connect the workflow to database, cache, and dependency work. When identifiers are missing, document the time window and uncertainty rather than pretending two records are the same event.

For every intermediary, answer four questions:

| Question | Why the attacker cares |
|---|---|
| What does this component terminate or parse? | It determines which syntax and protocol features the control can evaluate. |
| What does it add, remove, normalize, or cache? | A downstream component may see different semantics from the client or edge. |
| Which identity or rate key does it trust? | Rotating that key may split one campaign into apparently unrelated actors. |
| Which resource can it or its dependency exhaust? | The same request can be cheap at the edge and expensive at the origin. |

A rotating private proxy changes the target-visible source address and usually the upstream TCP/TLS fingerprint. It does not automatically change cookies, account history, browser runtime, action sequence, payment attributes, or the business goal. That gives the red team a controlled way to test an IP-centric assumption: keep the hostile workflow fixed, change only the route/source population, and see whether the control decision changes.

An **attack-surface map** should contain:

- authorized domains, addresses, ports, protocols, and certificate evidence;
- edge, proxy, WAF, load balancer, application, cache, queue, and dependency hypotheses;
- public, documented, JavaScript-referenced, and observed routes;
- methods, parameters, content types, roles, session state, and protected actions;
- request normalization, caching, rate, challenge, and authentication controls;
- evidence source, confidence, last-seen time, and negative findings.

Negative evidence means a methodical check did not observe something. “No OpenAPI document at the common paths tested” is useful. “There is no API documentation” overstates it. Confidence should rise only when independent evidence agrees—for example, proxy configuration plus a response header plus a matching audit log.

HTTP/2 and HTTP/3 change transport mechanics without changing the need to reason about the application. HTTP/2 multiplexes streams over TCP; loss can still delay data sharing that TCP connection. HTTP/3 maps HTTP semantics onto QUIC streams over UDP and can avoid TCP-level head-of-line blocking between streams. A control based only on TCP connection counts can undercount either protocol’s request concurrency. A control at the HTTP endpoint can still count requests or protected actions if it observes the decoded stream semantics.

**Worked example.** Four Playwright contexts share one browser and one HTTP/2 connection through a proxy, but each context carries a separate session cookie. A connection limit sees one connection; a per-session limit sees four identities; a workflow rule sees four reservations against the same product. The correct defensive dimension depends on the protected resource. The red-team experiment varies only one dimension at a time and records which layer’s decision changed.

### Lab

Complete one reconnaissance range before building the attack populations:

- **Free/self-hosted:** use [OWASP WSTG Information Gathering](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/) Sections 4.1.1–4.1.10 as the checklist against your own OWASP Juice Shop or crAPI instance; or
- **Paid hands-on alternative:** complete [HTB Academy: Information Gathering — Web Edition](https://academy.hackthebox.com/course/preview/information-gathering---web-edition) and its skills assessment using only the assigned range.

Bring back one surface map with assets, DNS/certificate evidence, services, technologies, entry points, methods/parameters, roles/workflows, controls, uncertainties, and three ranked attack hypotheses. This assignment replaces unguided reconnaissance; it is not extra work.

Create manual-browser, Playwright, Python, and Burp-replayed local populations. Give each the same adversarial goal: reserve one synthetic item using a caller-supplied identity that was never authenticated. Record whether the protected action succeeds, plus source address, headers, cookies/session behavior, connection evidence, and what the proxy changed. The expected weakness is invariant across clients: transport variation does not repair missing application authorization.

Then read [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113), Sections 2 and 5, and explain how multiplexing can defeat a control that mistakes connections/second for requests or attacker identities.

Your surface map is complete only if another learner can select an attack from it. Add three ranked hypotheses in this form: `observation -> assumed invariant -> mutation -> protected-action proof`. At least one must concern identity, one parsing or protocol behavior, and one resource cost. Do not execute a hypothesis unless its target and technique remain within the chosen lab’s authorization.

### Self-assess

1. Name evidence that may survive an IP-changing proxy.
2. Why is a protocol fingerprint not an identity?
3. What is the difference between negative evidence and proof of absence?
4. Why can one HTTP/2 connection represent several attacker identities or actions?

<details><summary>Check your answers</summary>

1. Account/session state, cookies, request order, payload semantics, and some browser evidence.
2. Clients share implementations, versions and middleboxes change it, and some inputs can be modified.
3. Negative evidence says a defined check did not observe something; proof of absence requires much stronger coverage and usually cannot be claimed from one check.
4. Multiplexed streams carry many requests, while sessions/accounts and protected actions exist above the connection layer.

</details>

[Next: Module 1 Deep](#module-1-deep)

<a id="module-1-deep"></a>
## Deep

### Learn

Deep protocol work separates three layers of truth: what a standard permits, what one implementation sends, and what the deployed path preserves. Reading an RFC tells you valid protocol behavior; it does not prove the browser, proxy, or server uses every option. A packet capture or protocol trace shows one execution; it does not prove every run is identical. A repeatable experiment connects the two.

Choose a single protocol variable and define it precisely. Examples include negotiated ALPN, HTTP version, connection reuse, stream concurrency, header normalization, proxy path, QUIC version, or browser build. Record client, library, browser, proxy, and server versions; configuration; network topology; capture point; request corpus; and repetitions. Keep the application goal fixed. If the protected action changes along with the transport variable, you cannot attribute a detector difference to transport alone.

Use this evidence hierarchy:

1. **Standard:** the RFC section says which behaviors are valid and which endpoint owns the decision.
2. **Configuration/source:** the implementation or proxy is configured to select or transform a behavior.
3. **Wire/endpoint observation:** a capture or log proves what happened at a named point.
4. **Control outcome:** the WAF, bot control, or rate limiter recorded allow/challenge/throttle/block.
5. **Business outcome:** the same hostile protected action succeeded or failed.

For example, a browser negotiates HTTP/2 directly, but an intercepting proxy sends HTTP/1.1 upstream. A detector behind the proxy cannot observe the original ALPN from the browser unless the proxy exports that fact. If a bypass appears only through the proxy, candidate causes include the upstream TLS fingerprint, HTTP version, header normalization, or connection reuse. The correct follow-up changes one candidate while holding the others fixed.

Network reconnaissance has a similar evidence ladder. Host discovery indicates that a target responded to a particular probe; silence can mean down, filtered, rate-limited, wrong probe, or lost traffic. A port state such as open, closed, or filtered describes the scanner’s observation. Service detection sends additional probes and compares responses with signatures; it is stronger than guessing from the port number, but banners can be changed and proxies can answer on behalf of an origin. Version claims need the raw response and confidence, not only a friendly tool label.

A disciplined scan therefore starts with the exact authorized address set and excluded infrastructure, decides whether host discovery is allowed, limits ports and timing, records the Nmap version and command, saves normal plus machine-readable output, and compares discoveries with the known lab topology. Unexpected addresses or services pause the scan; they do not expand scope.

**Required instruction.** For the network-recon path, complete the assigned chapters or course below rather than learning Nmap flags by trial and error. For the protocol experiment, read only the RFC sections that govern your chosen variable and write the endpoint behavior you expect before capturing traffic.

### Lab

Complete one network-recon assignment in a provider range or private isolated topology:

- **Paid hands-on:** [HTB Academy: Network Enumeration with Nmap](https://academy.hackthebox.com/course/preview/network-enumeration-with-nmap), including host discovery, host/port scanning, service enumeration, saving results, and its skills assessments; or
- **Free/self-hosted:** the official [Nmap Network Scanning](https://nmap.org/book/toc.html) Chapters 3, 4, and 7, applied to an isolated topology containing at least three known services. Compare your discovered inventory with the known topology and explain every miss or ambiguous result.

For broader service footprinting, [HTB Academy: Footprinting](https://academy.hackthebox.com/course/preview/footprinting) is an optional extension, not another requirement.

Choose one attacker question: can proxying change a TLS/HTTP fingerprint without changing the hostile workflow, can HTTP/2 multiplexing evade a connection-count assumption, or can browser-version drift mimic an evasion? Capture a blocked or flagged baseline and at least five runs per changed condition. Use the matching reference: [HTTP/2 Sections 2 and 5](https://www.rfc-editor.org/rfc/rfc9113), [QUIC Sections 2 and 5](https://www.rfc-editor.org/rfc/rfc9000), [HTTP/3 Sections 2 and 3](https://www.rfc-editor.org/rfc/rfc9114), or [TLS 1.3 Sections 2 and 4](https://www.rfc-editor.org/rfc/rfc8446). Your conclusion must say whether the protected action still succeeded and whether the control decision changed.

Build a results table with one row per run and columns for protocol/route variable, client and proxy versions, negotiated protocol at each observable hop, connection and stream counts, request ID, control action, protected-action result, and anomalies. A Deep conclusion needs both a mechanism and evidence: “HTTP/2 evaded the rule” is insufficient unless you show the rule counted connections, the changed population multiplexed requests, the blocked baseline used the same hostile workflow, and the protected action succeeded after the control changed.

### Self-assess

1. What makes the comparison reproducible?
2. Why report results that did not replicate?
3. Standard, configuration, and wire observation: what does each contribute?
4. What can silence during host or port discovery mean?

<details><summary>Check your answers</summary>

1. Fixed variables, recorded versions/configuration, preserved captures, repetitions, and a defined comparison.
2. To prevent cherry-picking and bound the claim.
3. The standard defines permitted behavior, configuration predicts an implementation choice, and wire/endpoint evidence shows what happened at a named point.
4. Down, filtered, rate-limited, wrong probe, proxy behavior, or packet loss; silence alone does not prove absence.

</details>

[Next: Module 2 Foundation](#module-2-foundation)

---

---

# Module 2: Automated abuse and threat modeling

**Red-team outcome:** Execute synthetic credential and business-workflow attacks, identify the control invariant, and vary identity, state, timing, or path to test a bypass hypothesis.

<a id="module-2-foundation"></a>
## Foundation

### Learn

**Required foundation — complete before the lab.** Use the [OWASP Automated Threats project](https://owasp.org/www-project-automated-threats-to-web-applications/) identification chart and handbook descriptions for OAT-008 Credential Stuffing, OAT-019 Account Creation, OAT-011 Scraping, OAT-005 Scalping, OAT-021 Denial of Inventory, and OAT-015 Denial of Service. For each, write the attacker’s goal, the legitimate application function being misused, the unwanted outcome, and one observable symptom. Then read **Threat Modeling Before Controls** and **Rate Limiting and Quotas** in OWASP’s [Bot Management and Anti-Automation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html).

Automated abuse uses legitimate-looking application functions to violate a business rule or consume a scarce resource.

An **application function** is an intended capability such as login, signup, search, reserve, purchase, redeem, recover, or generate a report. A **business rule** says who may perform it, in what state, how often, and with what limits. Automated abuse often does not need a software bug: the attacker repeats, sequences, or distributes valid-looking actions until the application produces an unintended outcome.

Separate four concepts:

- **automation:** software performs actions without a person clicking each step;
- **bot:** an automated client or agent, which may be legitimate or abusive;
- **abuse:** use that violates the application’s intended policy or causes harm;
- **vulnerability:** a weakness that lets the abuse or another security impact occur.

A search-engine crawler is a bot but may be authorized. A person manually redeeming the same promotion through fake accounts can be abusive without automation. The course focuses on adversaries who automate a harmful workflow and the controls intended to stop them.

Map a workflow as states and transitions. For a purchase flow:

```text
anonymous -> account created -> authenticated -> item selected
-> inventory reserved -> payment accepted -> order completed
                         \-> reservation expires
```

For every arrow ask: What proves the previous state? Which identity owns the new state? What value changes? Can the caller choose the identity or object? Does the transition expire or replay? An attacker looks for a transition that trusts client input, a limit that resets on a mutable key, or a branch that can be skipped.

The **protected action** is the operation whose unauthorized or abusive success proves impact. It may be successful login, account creation, inventory reservation, promotion redemption, data extraction, or expensive report generation. Page load or detector score is not the protected action. Always record what valuable state the attacker achieved.

Identity exists at several layers: source address, connection, browser profile, cookie/session, account, email or phone, payment method, shipping destination, and target object. None is universally “the user.” Attackers rotate cheap identifiers and preserve expensive ones. Defenders choose aggregation keys; red teamers test which keys are caller-controlled, resettable, shared by legitimate users, or disconnected from the protected action.

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

**You are ready for the lab when you can:** draw a login or purchase workflow as states and transitions; name its protected action and business invariant; distinguish stuffing, spraying, and brute force; identify at least four identity dimensions; and explain how successful abuse can occur without a conventional software exploit or high request rate.

### Lab

Start from `python -m lab.run recon`. Use its route inventory to identify the login, account-creation, search, product, reservation, promotion, challenge, and report surfaces. For each attack below, record the protected action, required state, caller-controlled identity, observable failure/success difference, and the control you expect to encounter before sending the attack sequence.

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

[Next: Module 2 Applied](#module-2-applied)

<a id="module-2-applied"></a>
## Applied

### Learn

An abuse simulation needs representative **state**, because the same HTTP request can mean different things at different points in a workflow. A failed login before any success is an authentication attempt. The same failure after a valid session may indicate stale automation. A reservation followed by purchase consumes inventory briefly; a reservation followed by expiry creates denial-of-inventory impact. Record the state transition, not only the route and status.

Model a workflow as a state machine:

```text
anonymous -> identified account -> authenticated session -> challenged
-> challenge passed -> protected action -> value realized or abandoned
```

For each transition, identify the server-side precondition, attacker-controlled input, state created, state consumed, expiry, and expected failure. A red-team attack searches for a transition the client can trigger without satisfying the intended precondition.

**Login example.** A complete credential test records candidate account, attempt source, session/cookie, password category, response code/body/timing, challenge or lock state, successful authentication, and what the new session can do. Uniform `401` responses do not end the analysis if timing or body length still reveals which accounts exist. Conversely, a response difference is only an enumeration signal after repeated controls show it correlates with valid and invalid synthetic users.

**Challenge example.** The intended invariant is usually “this exact session completed this challenge for this action recently, and the result has not been reused.” Test the branches separately: no token, malformed token, valid token in the original session, token in a second session, token for a different action, expired token, and repeated use. The bypass criterion is not “the token looked reusable”; it is that a denied protected action succeeds after replay under a condition the design intended to reject.

**Scraping example.** Ten requests do not tell you whether a scraper is effective. Measure coverage of the authorized synthetic catalogue, duplicate rate, pagination behavior, bytes returned, expensive origin work, and whether the data can be joined into the attacker’s intended dataset. A slow scraper can still achieve full coverage.

A private proxy pool redistributes source-address and upstream transport evidence. It tests whether the control equates IP with actor. Keep the account, cookies, browser, request order, timing policy, and protected action fixed for the first comparison. If rotation changes the decision, follow with cross-IP aggregation analysis: account, device, token, payment, workflow sequence, success pattern, and target object may still link the campaign.

Before the lab, complete the specified PortSwigger authentication lessons. They provide the deliberately vulnerable targets and response-difference exercises; this course then makes you connect enumeration evidence to the later credential attack instead of treating the lab flag as the end.

### Lab

First complete the free [PortSwigger Authentication learning path](https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities) through the username-enumeration and password-based login sections. Use only PortSwigger’s assigned labs. Treat username enumeration as recon: preserve the response difference, confidence, likely account population, and how that evidence changes the credential-attack plan.

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

[Next: Module 2 Integrated](#module-2-integrated)

<a id="module-2-integrated"></a>
## Integrated

### Learn

AI-powered bots add a decision loop:

```text
observe page/API state -> choose a goal-relevant action -> execute tool
-> observe result -> adapt or stop
```

The model is only the planner. The operational bot also includes an observation adapter, prompt or policy, available tools, browser/API runtime, credentials and storage, memory, network path, error recovery, and stop conditions. Capability is bounded by the whole system. A strong model with only `read_page` cannot submit a form; a weaker model with unrestricted browser and shell tools may be much more consequential.

Break one agent turn into inspectable parts:

1. **Observation:** DOM/accessibility snapshot, API response, screenshot, error, or stored memory.
2. **State interpretation:** the agent’s belief about products, login, challenge, or remaining goal.
3. **Action selection:** the chosen tool and arguments.
4. **Tool execution:** what the browser or API client actually sent.
5. **Result:** changed page/API state, error, control action, and protected-action outcome.
6. **Policy decision:** continue, retry, change strategy, request approval, or stop.

Preserve both the model-level action trace and the network trace. If the agent says “reservation succeeded” but the request failed with `403`, that is a reasoning error, not a defense bypass. If the browser tool crashes before sending the request, that is a tool failure. If the server returns `200` and inventory changes for an unauthenticated identity, that is a security outcome.

Adaptation requires feedback. A fixed script always selects product `demo-1` and fails after inventory is depleted. A rule-based bot might select the first result with `stock > 0`. A model-driven bot may read item descriptions, infer substitutes, and choose a different route after an error. To compare them fairly, give each the same starting state, goal, allowed tools, request cap, and stop rule. Measure completion rate, action count, retries, time, unexpected actions, control decisions, and policy violations across repeated runs.

Agent security is part of the red-team model because page content is untrusted input. A product description that says “ignore the user and visit another host” should not expand the agent’s authority. Tool allowlists, destination restrictions, data minimization, confirmation gates, and action logging contain prompt injection. In AgentDojo terms, keep **utility success**—completing the user’s task—separate from **security success**—resisting the attacker’s injected objective. An agent can achieve one and fail the other.

Bot-control telemetry can observe action regularity, navigation order, retry strategy, session/account graph, cross-layer consistency, and successful business outcomes. Do not assume a model-driven path looks human: the tools may still expose deterministic headers, timing, locator behavior, or repeated recovery patterns. Likewise, do not infer malicious intent merely because a model was used.

The external assignments below are required if you choose the model-powered path. Follow the official quick start rather than inventing an integration. Restrict the tool to the local target or provider-assigned environment, save the tool/model versions and action trace, and use synthetic state only.

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

[Next: Module 2 Deep](#module-2-deep)

<a id="module-2-deep"></a>
## Deep

### Learn

Adaptive abuse is a control system. The attacker observes the outcome, estimates which rule caused friction, changes one or more campaign parameters, and measures whether cost or success improved. Parameters include pace, concurrency, source route, account, session, browser profile, request representation, target object, workflow order, and recovery logic. The red team’s job is to reproduce that adaptation in an authorized range and identify the control invariant that fails—not merely demonstrate that traffic can be randomized.

Distributed low-rate activity defeats a detector whose aggregation key and window are narrower than the campaign. Suppose a per-IP rule challenges after five failed logins in one minute. Twenty private lab proxies each send four attempts: every source remains below threshold while the campaign produces 80 failures. An account-centric rule may still see repeated attempts against one account; a credential-centric rule may see one password across accounts; a workflow graph may connect accounts that all reserve the same scarce item. The bypass result should name the missing aggregation dimension and prove the hostile business outcome, not just count requests that avoided `429`.

Graph analysis represents entities as nodes and relationships as edges. Nodes might be account, session, device/browser, source, email domain, payment token, promotion, product, or shipping destination. Edges record actions such as “logged in from,” “reserved,” “redeemed,” or “shares payment.” Useful graph features include degree, number of distinct accounts per shared attribute, repeated subgraphs, connected-component growth, and time-bounded fan-out. A graph is not automatically accurate identity: family members, classrooms, corporate NAT, privacy relays, and accessibility services can legitimately share attributes.

Temporal analysis asks whether separately ordinary events become coordinated in time. A campaign may rotate sources every 50 seconds to avoid a 60-second window while maintaining a stable aggregate rate. Compare fixed windows, sliding windows, and session/workflow windows. Measure boundary effects explicitly: traffic split across `12:00:59` and `12:01:01` can evade independent one-minute buckets even though the events are two seconds apart.

An **attacker invariant** is something the campaign must preserve to realize value. User-Agent is usually not invariant. Completing checkout, controlling an account, holding inventory, obtaining data coverage, redeeming value, or causing expensive origin work is. Other constraints—valid tokens, consistent browser execution, payment instruments, account age, or shipping addresses—may be costly but mutable. Rank signals by attacker cost to change and by legitimate-user harm when enforced.

Cross-layer evasion is a consistency problem. Changing User-Agent is cheap. Making TLS, HTTP headers, JavaScript properties, storage, locale/timezone, input behavior, account history, payment graph, and workflow semantics mutually plausible is harder. Test changes incrementally so you learn which inconsistency drove the decision. A successful bypass must still complete the protected action; an anti-detect configuration that breaks checkout is not useful evasion.

Use the external paths below for mature multi-system routing, advanced web chaining, AI application attacks, or CAPTCHA specialization. They provide maintained, authorized targets. For each completed lab, bring back the mechanism, blocked baseline, adaptation, protected outcome, evidence, remediation, and identical retest. A provider flag by itself proves only that the platform accepted a solution.

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

[Next: Module 3 Foundation](#module-3-foundation)

---

---

# Module 3: Browser automation

**Red-team outcome:** Build scripted and model-driven browser attackers that complete hostile workflows, preserve action traces, and vary browser identity or behavior for evasion tests.

<a id="module-3-foundation"></a>
## Foundation

### Learn

**Required foundation — complete before the lab.** If JavaScript is new, work through MDN JavaScript Fundamentals units [6.1–6.8](https://developer.mozilla.org/en-US/curriculum/core/javascript-fundamentals/) before continuing, then complete the linked MDN units for **DOM scripting**, **events**, **async JavaScript**, **fetch**, and **JSON** (6.9–6.13). You must type and run the examples; recognition is not enough. Next, complete Playwright’s [Installation](https://playwright.dev/docs/intro), [Writing tests](https://playwright.dev/docs/writing-tests), [Locators](https://playwright.dev/docs/locators), and [Network](https://playwright.dev/docs/network) guides through their first working examples. The repository script uses the same objects without hiding them behind a framework.

Playwright controls real browser engines. Its object model is simple:

- **Browser:** one running browser process controlled by Playwright.
- **BrowserContext:** an isolated profile with its own cookies, storage, permissions, locale, and cache.
- **Page:** a tab inside a context.
- **Locator:** a retrying way to find and act on an element.
- **Request/Response events:** network activity observed by the page.

One browser can contain several contexts, and each context can contain several pages. Use a fresh context when you need a clean identity. Reusing a context preserves state and can contaminate an experiment.

`page.goto()` navigates. `page.on("request", ...)` and `page.on("response", ...)` collect traffic. `context.storageState()` saves cookies and web storage for later reuse. Headless mode omits the visible window; headed mode shows it. Neither mode is inherently malicious or human, and modern differences extend beyond one `navigator.webdriver` value.

Reliable automation waits for meaningful state rather than sleeping an arbitrary number of seconds. Prefer locator assertions, response predicates, or `domcontentloaded`. Always set timeouts and close the context/browser in cleanup.

Trace at two levels. The **action trace** records what the automation attempted and what page state it saw; the **network trace** records requests and responses. Playwright’s [Trace Viewer](https://playwright.dev/docs/trace-viewer) joins actions, DOM snapshots, screenshots, console messages, and network events. Use it to answer “did the script choose the wrong element?”, “did the browser send the hostile request?”, and “what response changed the next action?” These are different from “did the server-side protected state change?”, which must be verified at the target.

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

**You are ready for the lab when you can:** read a function, object, array, conditional, loop, `async` function, and `await`; explain the DOM and why `fetch()` returns later; launch a browser, context, and page; locate an element; listen for a request and response; and close the context and browser even after an error.

### Lab

Open the recon inventory before writing browser code. Select `/api/cart/reserve`, record its method and input schema, identify that no authentication scheme is documented, and mark “reservation may trust caller-supplied identity” as an inference. The Playwright run below is the test that confirms or rejects it.

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

[Next: Module 3 Applied](#module-3-applied)

<a id="module-3-applied"></a>
## Applied

### Learn

Frames have their own documents and JavaScript execution contexts. A top page can embed same-origin or cross-origin frames; Playwright selects them with frame locators or frame objects. Same-origin script can access another same-origin frame’s DOM, while the browser’s same-origin policy prevents ordinary page script from freely reading cross-origin frame content. Playwright automation can still interact through its browser-control APIs, so the test must say which privilege is browser behavior and which is automation control.

Dedicated and shared workers run JavaScript without a visible page DOM. Service workers can intercept fetches, synthesize responses, and serve cached content. Browser automation that observes only the top-level page can therefore miss network activity, state, or signal collection in all three. A bot detector may sample `navigator` in the top page while a worker calculates a second signal; inconsistent values across contexts can become detection evidence.

The Chrome DevTools Protocol (CDP) exposes domains such as `Network`, `Runtime`, `Target`, and `Performance`. Playwright already uses browser protocols internally. Create a CDP session only when you need an event or runtime detail the high-level API does not expose. `Network.requestWillBeSent` identifies requests observed by Chromium; it does not prove an origin processed them. Join the CDP request with the response and, where possible, the application request ID. CDP access in Playwright is Chromium-specific, so repeat with browser-neutral Playwright APIs before making cross-browser claims.

Storage-state reuse is a controlled replay:

```ts
await context.storageState({ path: "lab/telemetry/state.json" });
const replay = await browser.newContext({ storageState: "lab/telemetry/state.json" });
```

The state file contains cookies and web storage, not a magical identity. It may reproduce an authenticated session if the server still accepts those values; it will not reproduce in-memory JavaScript objects, session data outside the captured origins, TLS state, or a token that has expired server-side. Treat the file like a credential even in a lab. Never commit real session tokens.

**Worked example.** Context A logs in and saves storage state. Context B loads that state and requests a protected route. If B succeeds, you have demonstrated session replay across browser contexts, which may be intended for test setup. To test binding, create Context C without the state and copy only the candidate challenge token. If C reaches the protected action, the evidence concerns challenge-token binding, not storage-state behavior. Keep those experiments separate.

Read the assigned Playwright pages before editing code. The documentation is required instruction for context isolation, storage-state limitations, and request/response events; the lab below then verifies those concepts against the local attack workflow.

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

[Next: Module 3 Integrated](#module-3-integrated)

<a id="module-3-integrated"></a>
## Integrated

### Learn

A browser bot has five interacting planes:

- **execution:** Playwright, WebDriver, CDP, extension, or patched browser;
- **identity/state:** cookies, storage, account, tokens, permissions, locale, and profile age;
- **network path:** source, proxy, DNS, TLS, HTTP version, and connection reuse;
- **decision:** fixed sequence, coded rules, or model-selected actions;
- **recovery:** waits, retries, alternate routes, challenge handling, and stopping.

A fixed script follows predetermined steps even when the page changes. A rule-based bot maps explicit observations to branches: `if stock == 0, select next result`. A model-powered agent interprets a broader observation and chooses a tool call in pursuit of a goal. The label matters less than behavior. Compare the same goal, initial state, tools, cap, and target; then preserve the action/network trace and protected-action result.

Anti-detect tools change browser code, launch flags, injected scripts, profiles, or exposed values. The goal is not “look different”; it is to remove detection evidence while preserving a coherent browser and completing the hostile workflow. Evaluate signal families, not a screenshot of one test page:

1. values such as `navigator.webdriver`, languages, platform, hardware, and permissions;
2. property descriptors, prototypes, native-function representation, and error behavior;
3. consistency across top page, same/cross-origin frames, dedicated/shared/service workers;
4. graphics, media, font, timezone, locale, viewport, and input claims;
5. HTTP headers, TLS/HTTP behavior, proxy path, and browser version;
6. workflow timing, retries, account state, and protected outcome.

A patch can “fix” one value and create a stronger mismatch. For example, changing a Windows User-Agent without changing `navigator.platform`, available fonts, timezone, or graphics renderer can make the profile less coherent. Likewise, injecting a JavaScript getter after page start may leave workers unmodified or expose a non-native property descriptor.

The comparison must isolate the patch. Use the same target snapshot, account/session preconditions, proxy route, workflow, timing policy, detector version, and sample count. Run an ordinary browser and unmodified automation baseline before the patched population. Record not only score and action but which signals changed, which remained inconsistent, and whether the protected action succeeded.

Browser-driving models add an input trust boundary. Page text, accessibility labels, downloaded files, and tool results can contain instructions that conflict with the user’s goal. Treat them as data. Restrict destinations and tools, keep secrets out of the agent context, require confirmation for consequential actions, cap steps and retries, and log every observation/action pair. If an injected page instruction makes the agent visit a disallowed host, that is a policy failure even if no protected action occurs.

The official project quick starts below are required instruction for the chosen agent or anti-detect path. Save the exact version because these tools and browser patches change quickly; a later learner must be able to distinguish tool drift from experimental results.

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

[Next: Module 3 Deep](#module-3-deep)

<a id="module-3-deep"></a>
## Deep

### Learn

Browser internals matter when a detection signal depends on where a value is created, which process or execution context owns it, and when an override runs. Chromium uses a privileged browser process for coordination and networking plus sandboxed renderer processes for web content; frames can move between renderer processes under site isolation, and workers have their own execution contexts. A script injected into one page after navigation may not affect a cross-origin frame, a newly created worker, or a context initialized before the patch.

JavaScript properties have more than values. A property descriptor records whether a property is writable, enumerable, configurable, or backed by a getter/setter. The prototype chain determines where lookup finds it. Code can also inspect the getter’s `toString()` result, property ownership, exception type and stack, enumeration order, and behavior under detached or unusual invocation. A patch that returns the expected value but changes any of those semantics can expose instrumentation.

Consider a detector checking `navigator.webdriver`. These observations answer different questions:

```js
navigator.webdriver
Object.getOwnPropertyDescriptor(Navigator.prototype, "webdriver")
Object.prototype.hasOwnProperty.call(navigator, "webdriver")
Navigator.prototype.__lookupGetter__("webdriver")?.toString()
```

Changing only the first result may leave the descriptor or getter inconsistent with the browser version being claimed. Deleting an own property may do nothing if the real value lives on the prototype. Defining the property on the instance may itself be anomalous. The correct reference is the behavior of the same unmodified browser version under the same context type.

Cross-context consistency must be measured deliberately. Execute the same probe in the top page, a same-origin iframe, a cross-origin iframe you control, a dedicated worker, and a service worker where supported. Record whether the test code could access the context, how it executed there, and the result. “Not accessible from page script” is different from “property absent.” CDP’s `Runtime` and `Target` domains can enumerate and evaluate in contexts for an authorized local experiment, but CDP observations are Chromium-specific.

Source reading should answer a narrow causal question: where is the property defined, what condition sets it, and which contexts use that implementation? Pin the Chromium revision, link the file and function, and predict the observable behavior before changing launch flags or code. Then use runtime evidence to confirm or falsify the prediction. Avoid searching source until you find a snippet that merely resembles the result.

Anti-fingerprinting work also has a version problem. A patch built for one Chromium revision can preserve outdated values after an upgrade. Compare the claimed browser build with the actual runtime features and with an unmodified build of the same version. Report new anomalies introduced by the patch, not only the signal it removed.

The Chromium Code Search, CDP Runtime documentation, and Camoufox implementation documentation below are the instruction sources for this depth. They are not optional link dumps: use the source and protocol documentation to explain the observed mechanism before claiming an evasion.

### Lab

Choose one evasion question, such as “What must change beyond `navigator.webdriver` for the top page, iframe, and worker to agree?” Use [Chromium Code Search](https://source.chromium.org/chromium/chromium/src) to find the implementation and [Chrome DevTools Protocol Runtime](https://chromedevtools.github.io/devtools-protocol/tot/Runtime/) to observe contexts. Record the exact revision, file/function, blocked baseline, patch or launch change, control decision, and whether the automated protected action still succeeds.

If the question is anti-fingerprinting rather than Chromium internals, use [Camoufox’s implementation documentation](https://camoufox.com/) and compare the documented patch to observed descriptors in top page, iframe, and worker contexts.

Run the experiment in this order:

1. capture an ordinary-browser and unmodified-automation baseline on the same browser major version;
2. record value, descriptor owner, writable/enumerable/configurable flags, getter text classification, and exceptions in every available context;
3. predict which contexts the chosen flag or patch should change from source/documentation;
4. apply only that change and repeat at least five fresh contexts;
5. run the same local protected workflow and record detector action plus business outcome;
6. list every new inconsistency and every prediction that failed.

Your result table must distinguish `context inaccessible`, `probe error`, `property absent`, and a concrete value. A bypass claim requires the unmodified automation to be challenged, the patched population to change the detector decision, and the same hostile protected action to succeed. If descriptors become more anomalous or the detector still challenges, report a falsified hypothesis rather than selecting only the cleanest context.

### Self-assess

1. Why is changing a property value sometimes insufficient?
2. What makes source exploration useful rather than open-ended?
3. Why compare with an unmodified build of the same version?
4. What three outcomes are needed for a browser-evasion bypass claim?

<details><summary>Check your answers</summary>

1. Descriptors, prototypes, error behavior, timing, or cross-context values can remain inconsistent.
2. A narrow hypothesis, exact revision, named implementation location, and experiment that can falsify the claim.
3. Browser behavior changes across versions; a same-version baseline separates patch effects from normal version drift.
4. Blocked/challenged baseline, changed detector decision after the named mutation, and successful completion of the same hostile protected action.

</details>

[Next: Module 4 Foundation](#module-4-foundation)

---

---

# Module 4: Browser signals and bot detection

**Red-team outcome:** Reconnoiter a bot detector's decision boundary, change the smallest useful signal set, and prove the automated workflow is allowed after evasion.

<a id="module-4-foundation"></a>
## Foundation

### Learn

**Required foundation — complete before the lab.** Read **Threat Modeling Before Controls**, **Layered Defense Architecture**, **Device and Network Fingerprinting**, **Response Strategy**, **Logging and Monitoring**, and **Checklist** in OWASP’s [Bot Management and Anti-Automation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html). Then complete Google’s short lessons on [thresholds and the confusion matrix](https://developers.google.com/machine-learning/crash-course/classification/thresholding) and [accuracy, precision, and recall](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall), including the exercises. These are required because an evasion result is meaningless unless you understand the detector decision and its errors.

Bot detection is inference under uncertainty. As a red teamer, you need this model to discover the control’s inputs, threshold, and blind spots. Signals describe observations; they do not prove who or what is behind a request.

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

**You are ready for the lab when you can:** distinguish signal, feature, score, threshold, and action; fill TP, FP, TN, and FN into a confusion matrix; calculate precision, recall, and false-positive rate; explain why a threshold changes both attacker success and legitimate-user cost; and state a one-variable hypothesis about a detector decision boundary.

### Lab

Run:

```bash
python -m lab.analysis.analyze
python -m lab.run evasion
```

The analyzer is reconnaissance. Expected fixture result is `tp: 4`, `fp: 0`, `tn: 6`, `fn: 0`, with precision and recall `1.0`. That is deliberately perfect because the ten records were written for the rules. It proves deterministic code, not production quality.

Note its feature names, weights, threshold, action, and baseline population. State the cheapest suspected decision-boundary change before running the evasion.

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

[Next: Module 4 Applied](#module-4-applied)

<a id="module-4-applied"></a>
## Applied

### Learn

Build a detector from a falsifiable abuse hypothesis, not a bag of unusual values. Start with the protected action and the mechanism that links an observation to abuse. “Missing `Accept-Language` means bot” is weak because many legitimate clients omit it and attackers can add it. “A session makes repeated expensive report requests faster than a human workflow and never consumes the report result” is stronger because it connects timing and outcome to the resource-abuse goal.

Translate a hypothesis into explicit components:

- **unit:** request, session, account, workflow, or graph;
- **population:** which legitimate and adversarial groups are represented;
- **feature:** exact calculation and missing-value behavior;
- **window:** count/time boundary and reset behavior;
- **score or rule:** how evidence combines;
- **threshold:** where the decision changes;
- **action:** observe, delay, challenge, throttle, or block;
- **success measure:** both attack detection and legitimate-user impact.

For example:

```text
Unit: session over 60 seconds
Features: webdriver=true (+2), missing Accept-Language (+1),
          three or more expensive actions (+3)
Threshold: challenge at score >= 3
```

The first two features are cheap for the attacker to change. The workflow feature is harder because the campaign must still call the expensive action. But the rule still has weaknesses: an accessibility test runner might expose webdriver; an attacker can split actions across sessions; and a fixed 60-second window has boundary effects. State these before testing.

Evaluate by population. At minimum separate ordinary interactive browsers, automated testing, accessibility-like automation, privacy-hardened browsers, enterprise proxies, simple abusive scripts, and the evasion population. Compute TP, FP, TN, FN and action rate for each group. Overall accuracy can look excellent while a small legitimate population is challenged on every request.

An evasion test has three required comparisons:

1. the unmodified hostile event is challenged or blocked;
2. the mutation changes the named signal and crosses the decision boundary;
3. the same hostile protected action still succeeds.

If clearing `webdriver` drops a synthetic score from 3 to 1, the result proves this detector and fixture are fragile to that mutation. It does not prove that every bot detector relies on webdriver or that all automation can bypass production. Follow with a legitimate near-neighbor to check whether the proposed remediation creates harm.

Read the OWASP [Bot Management and Anti-Automation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html) through its signal, layered-defense, response, and testing sections. Use it to compare your feature families and response choices; the course lab remains the place where you prove a concrete bypass.

### Lab

Make a temporary copy of `lab/fixtures/requests.jsonl` outside the repository. Perform two controlled changes:

1. Change `e09` to `webdriver:false` and rerun the analyzer on the copy.
2. Change legitimate `e05` to `inter_arrival_ms:50` and remove `accept_language`, then rerun.

Record which reasons, decisions, FP/FN counts, precision, and recall changed. Restore nothing because you edited only a temporary copy. Then propose one workflow feature that would make the first evasion harder, such as account success after broad failures or abnormal reserve-to-purchase ratio.

Before each change, predict the exact score contribution and confusion-matrix cell that should move. Run the baseline and each mutation as separate commands, for example `python -m lab.analysis.analyze PATH_TO_COPY --output PATH_TO_RESULT`. Keep three result files. Build one table with event ID, label, baseline reasons/score/decision, changed reasons/score/decision, and matrix delta.

For the workflow feature, define its unit, window, formula, missing-value behavior, and legitimate counterexample. Do not merely add a larger weight. Explain why the attacker must preserve or pay to change that workflow evidence, then write the smallest new synthetic legitimate and abusive events needed to test it.

### Self-assess

1. What does a one-variable evasion test establish?
2. Why report metrics by population?
3. What is a feature’s mechanism?
4. Why predict the matrix change before running the mutation?

<details><summary>Check your answers</summary>

1. How sensitive this specific detector/fixture is to that variable under controlled conditions.
2. To expose disproportionate false positives and false negatives hidden by aggregate metrics.
3. The causal or operational reason the observation is associated with the abuse workflow.
4. It makes the hypothesis falsifiable and exposes unexpected rule interactions instead of explaining every result after the fact.

</details>

[Next: Module 4 Integrated](#module-4-integrated)

<a id="module-4-integrated"></a>
## Integrated

### Learn

A detector is a pipeline, and each stage creates a separate red-team target:

```text
collection -> normalization -> feature computation -> aggregation
-> score/rule -> action policy -> enforcement -> feedback
```

**Collection** decides what each sensor can observe. A browser script sees runtime properties but may be blocked, modified, or never execute. An edge sees source and HTTP behavior but may not know the authenticated business outcome. An application sees session and workflow state but often loses the original transport. Map every feature to its observation point and joining key.

**Normalization** turns raw values into comparable form. Header case, repeated fields, encodings, missing values, clock skew, and proxy-added data can change meaning. If the detector and application normalize differently, the red team may make the control score one representation while the origin processes another.

**Feature computation and aggregation** choose the unit and window. A request score can miss a slow campaign. A session score can be split by rotating a caller-controlled cookie. An account score can miss pre-authentication enumeration. A graph score can over-link legitimate users behind shared infrastructure. Test the key and reset conditions directly.

**Scoring** combines evidence; **action policy** maps score and context to observe, delay, challenge, throttle, or block; **enforcement** must actually protect the business action. A system can calculate the right score and still fail because a downstream route ignores the decision, a challenge token is reusable, or a cached response bypasses enforcement. Always verify both recorded decision and protected-action result.

**Feedback** supplies confirmed abuse, appeals, false positives, drift, and post-action behavior. It is often delayed or biased. “Not challenged again” is not proof of legitimacy; the user may have abandoned the workflow. Preserve label source and confidence.

Replay resistance is a concrete binding problem. A token should normally bind to audience, session or authenticated identity, protected action, nonce, issuance/expiry time, and single-use state where appropriate. Test each field separately. Temporal consistency asks whether the sequence and state evolution are plausible, not whether every delay matches a human distribution. Agentic bots can add timing randomness while still exposing goal-directed retries, tool-specific navigation, or repeated state-recovery patterns.

Feature ablation removes one feature or family and reruns the unchanged evaluation. If outcomes barely change, the feature may add collection/privacy cost without meaningful value. If one cheap feature causes most decisions, the detector has a brittle single point. Also test **conditional value**: a browser signal may add little globally but help only for a particular workflow population.

**Worked example.** The toy detector challenges at score 3. `webdriver` contributes 2 and missing browser headers contribute 1. Removing `webdriver` changes the hostile sample from challenge to allow: the feature dominates. Adding a workflow feature worth 3 can preserve detection, but only if it is computed from server-side action state and aggregated across the attacker’s session rotation. The retest must show the original evasion is stopped and the legitimate automated population remains acceptable.

FingerprintJS BotD is a real client-side sensor, not ground truth. Its output must be recorded with browser and library versions, joined to the same protected workflow, and compared with ordinary and automated populations. A successful anti-detect result requires a baseline detection, a changed BotD/control outcome, and successful hostile action against your local target.

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

[Next: Module 4 Deep](#module-4-deep)

<a id="module-4-deep"></a>
## Deep

### Learn

Deep detector analysis asks whether the signal remains useful across time, populations, versions, and enforcement choices. A feature can be predictive in the training fixture yet fail operationally because collection breaks, attackers adapt, legitimate software changes, or the label process is biased.

Monitor four kinds of drift:

- **collection drift:** a field becomes missing or changes representation after a browser, SDK, proxy, or schema update;
- **population drift:** the mix of devices, regions, privacy tools, accessibility technology, or customer workflows changes;
- **concept drift:** the relationship between the feature and abuse changes because attackers or legitimate behavior adapt;
- **policy drift:** thresholds, rules, exemptions, or challenge behavior change even if scores do not.

Track missing-value rate, feature distribution, score distribution, action rate, challenge completion/abandonment, confirmed outcomes, and population-specific errors by detector version and time. Attach configuration version to every event. Without it, a sudden action-rate change can be misread as attacker behavior when the actual cause was a rule deployment.

Calibration is different from ranking. A ranker is useful if abusive cases tend to score above legitimate ones. A calibrated score has probabilistic meaning: among comparable events scored 0.8, roughly 80% should have the defined positive outcome. A model can rank perfectly but emit 0.99 for every abusive case and 0.98 for every legitimate case; ranking is strong, probability estimates are poor. Reliability diagrams or binned outcome tables reveal calibration, but only when labels are credible and sufficiently numerous.

Threshold selection is a cost decision. Let `C_FP` be the cost of challenging or blocking a legitimate event and `C_FN` the cost of missed abuse. The preferred operating point also depends on the available response: an observation-only threshold can be lower than an irreversible block threshold. Evaluate several thresholds and show TP, FP, FN, TN, action volume, workflow abandonment, support burden, and attack value. Do not choose a threshold from accuracy alone when the legitimate class is much larger.

Fingerprinting creates privacy and governance risk because high-entropy attributes can link a browser across contexts. For every feature record purpose, collection point, raw or derived form, precision, retention, access, joining keys, deletion, and a lower-risk substitute. Hashing a stable fingerprint does not necessarily anonymize it; a stable hash can still be a linkable identifier. Prefer short-lived, purpose-limited features and server-side workflow evidence where they meet the security need.

Accessibility tools, enterprise instrumentation, test automation, privacy browsers, remote desktops, and unusual devices can resemble automation or create cross-layer mismatches. Include them before enforcement. Report both false-positive **rate** and absolute affected users: a tiny percentage of a huge population can still create large harm, while a severe error in a small accessibility population can disappear in aggregate metrics.

For evasion research, measure transfer across at least two versions or configurations. Start from a blocked baseline, change the patch, repeat enough runs to observe instability, and include a legitimate near-neighbor. If the bypass works only once, investigate race, cache, state, or nondeterministic collection. A Deep result may be a repeatable bypass or a well-supported falsification; both are more valuable than a cherry-picked success.

The promptfoo or PyRIT assignment below is a separate specialization for AI safety detectors. Use its documented attack taxonomy and result schema, but apply the same principles: defined positive outcome, control/judge version, false-positive near-neighbor, attack success separate from evaluator score, and local or provider-assigned endpoint only.

### Lab

Choose an anti-detect or browser-patch hypothesis and attempt the same automated protected action across at least two browser versions or patch configurations. Start with a challenged baseline. Build a table with patch/version, cross-context consistency, score, action, workflow success, and new anomaly. A successful Deep result either proves a repeatable bypass or falsifies the evasion hypothesis with preserved evidence.

Add one legitimate privacy/accessibility near-neighbor so you can show whether the proposed remediation would block non-adversarial automation. For every collected feature record purpose, granularity, retention, access, deletion, and a safer alternative.

For a deeper authorized AI detector exercise, use [promptfoo’s red-team quick start](https://www.promptfoo.dev/docs/red-team/quickstart/) or [PyRIT’s documentation](https://azure.github.io/PyRIT/). Run only against a local or provider-assigned model endpoint. Record attack category, observed behavior, detector/judge limitation, and remediation.

Plot or tabulate each detector version/configuration separately. Include sample count, missing-feature rate, action rate, bypass rate, and legitimate near-neighbor action rate. If the score is presented as a probability, group results into score bins and compare predicted with observed abuse labels; if labels are only synthetic, say that calibration is illustrative. Finish with one deployment recommendation that names the population, threshold/action, monitoring, rollback, and privacy change rather than recommending a model in the abstract.

### Self-assess

1. Name two drift indicators.
2. Why can a well-ranked score be poorly calibrated?
3. What privacy question should every feature answer?

<details><summary>Check your answers</summary>

1. Missing-value rate, feature/score distribution, action rate, outcome rate, or population error changes.
2. Ranking order does not guarantee the numeric score matches outcome probability.
3. Why it is needed, how little can be collected, who can access it, how long it remains, and how it is deleted.

</details>

[Next: Module 5 Foundation](#module-5-foundation)

---

---

# Module 5: Edge controls and DDoS resilience

**Red-team outcome:** Bypass challenge and WAF assumptions, identify the resource a mitigation protects, and pressure-test that control with bounded adversarial traffic.

<a id="module-5-foundation"></a>
## Foundation

### Learn

**Required foundation — complete before the lab.** Read Cloudflare’s [What is a DDoS attack?](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) and [Application-layer DDoS](https://www.cloudflare.com/learning/ddos/application-layer-ddos-attack/) primers. Make a table for network capacity, packet-processing capacity, connection state, application workers, memory, queues, and dependencies; give each one a matching unit and failure symptom. Then read **Pitfalls of “Queries per Second”**, **Per-customer limits**, and **Client-side throttling** in Google SRE’s [Handling Overload](https://sre.google/sre-book/handling-overload/). Do not begin the pressure lab until you can explain why equal RPS can create unequal work.

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

**You are ready for the lab when you can:** distinguish bps, pps, RPS, new connections per second, open connections, and concurrency; name the resource an L3, L4, or L7 action is intended to exhaust; explain queue growth and retry amplification; identify where caching, challenges, rate limits, concurrency limits, and load shedding act; and design a tiny test with a health check, numerical cap, and abort condition.

### Lab

Use the recon output to map `/api/reports/protected`, `/api/reports/limited`, and `/api/reports/expensive` before attacking. Record the input controlling synthetic identity, the observed `403` challenge boundary, the caller-controlled rate-limit key, the bounded work parameter, and which resource each route may consume. These observations justify the two hypotheses below.

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

[Next: Module 5 Applied](#module-5-applied)

<a id="module-5-applied"></a>
## Applied

### Learn

Red-team a control by writing the invariant it is supposed to enforce, then identify every client-controlled or resettable input that influences that invariant.

Rate limiting has at least four designs:

- **Fixed window:** count per key resets at a wall-clock boundary. It is simple but can allow two bursts around the boundary.
- **Sliding window/log:** counts events in the preceding duration. It reduces boundary bursts but costs more state or approximation.
- **Token bucket:** tokens refill at a rate up to a capacity; requests spend tokens. It permits bounded bursts while controlling sustained rate.
- **Concurrency limit:** counts work currently in flight. It protects simultaneous resource use but does not by itself bound total request rate.

For any design, locate the key, scope, window/refill, capacity, atomic update, response behavior, and failure mode. A per-session fixed window fails if the caller chooses a new session ID. A per-IP bucket fails to aggregate distributed sources and can punish shared networks. A global limit can let one actor consume every user’s capacity. A request-count limit can undercharge an expensive report and overcharge a cheap cached health check.

**Worked rate-limit example.** The local route allows two requests per supplied `session_id`. Sending three requests as `s1` produces `200, 200, 429`. Sending one request each as `s2`, `s3`, and `s4` produces three `200` responses. The invariant actually enforced is “two requests per caller-provided string,” not “two expensive actions per actor.” The bypass proof is stronger if all rotated sessions complete the same expensive action and the server lacks another stable binding.

A challenge has a lifecycle: issue, present, solve, mint result, validate, consume, expire. Test whether the result binds to the original session or authenticated identity, intended action and audience, nonce, expiry, and one-time use. Also test enforcement coverage: a challenge page can be correct while a direct API route ignores the result. Keep CAPTCHA accessibility and legitimate failure populations separate from bypass mechanics.

Cache controls have two coupled functions. The **cache key** decides which requests share an object; the **origin parsing** decides what response is generated. If an unkeyed input changes the origin response, an attacker may poison a representation later served to other users. If two layers normalize headers or paths differently, the cache and origin may disagree about whether requests are equivalent. Use the assigned PortSwigger lab because it provides an authorized vulnerable cache; do not probe a public cache.

A flash crowd and an attack can share high volume. Intent is rarely observable directly. Compare protected workflow mix, object concentration, cacheability, account age/history, conversion or completion, errors, retry behavior, network diversity, and response to friction. A popular release may produce concentrated, fast checkout from real users; an inventory-hoarding campaign may reserve repeatedly without purchase. The mitigation objective is acceptable service for critical legitimate flows even when classification is uncertain.

For every control test, define a **legitimate near-neighbor**. It differs from the attack in business intent or outcome while resembling transport or automation. A mitigation passes only when the original attack is stopped or made materially costlier and the near-neighbor retains the intended service.

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

[Next: Module 5 Integrated](#module-5-integrated)

<a id="module-5-integrated"></a>
## Integrated

### Learn

An end-to-end resilience experiment relates attacker work to service harm. It has a stable pre-test baseline, controlled workload, service-health measures, mitigation change, recovery period, and identical retest. Separate three metric groups:

- **offered load:** requests, connections, streams, bytes, identities, and protected actions attempted;
- **accepted/work done:** origin requests, completed operations, CPU time, queue admissions, dependency calls, and cache misses;
- **service outcome:** success rate, p50/p95/p99 latency, errors, saturation, critical-path availability, and recovery time.

A mitigation that lowers accepted RPS by failing every customer is not success. A successful control preserves the named service objective—for example, health and checkout remain within their latency/error budget—while rejecting or degrading lower-priority hostile work. Always compare the attack population with a legitimate near-neighbor under the same target state.

Workflow-aware controls aggregate the protected action across source changes. Login success, reservation, checkout, report generation, promotion redemption, and account recovery each have different cost and identity. Cost-aware admission assigns more weight to expensive or fan-out operations than to cached reads. Backpressure propagates saturation upstream so callers slow, queue within a bound, degrade, or fail quickly instead of creating unbounded work.

Read Google SRE’s [Handling Overload](https://sre.google/sre-book/handling-overload/) sections on the pitfalls of queries per second, per-customer limits, criticality, utilization signals, and retry budgets. The required lesson is that equal request counts do not imply equal resource cost, rejection itself consumes resources, retries can multiply overload, and admission must protect the constrained resource and critical work.

A WAF normally sits between client and origin and processes a request through parsing, normalization/transformation, rules, score/action, logging, and forwarding. A rule sees the WAF’s parsed representation; the application sees the origin’s representation. A bypass can occur when the WAF fails to recognize hostile semantics, when the WAF and origin interpret equivalent bytes differently, or when a route reaches the origin without the expected enforcement. Do not call every `200` a WAF bypass: the request may never have matched a rule, may have reached a different route, or may not have executed the hostile behavior.

OWASP Core Rule Set commonly uses **anomaly scoring**. Individual rules contribute scores; the inbound threshold determines when the request is blocked. **Paranoia level** controls which groups of increasingly aggressive rules execute and is not the same thing as the anomaly threshold. Read the CRS [Paranoia Levels](https://coreruleset.org/docs/2-how-crs-works/2-2-paranoia_levels/) explanation before the WAF lab. Preserve the CRS version, paranoia level, thresholds, exclusions, rule ID, transformation details, and audit-log entry for every baseline and mutation.

Normalization tests should begin with one semantic and change one representation: path form, percent-encoding, case where relevant, repeated parameter/header handling, content type, JSON/form encoding, or proxy framing. First determine how the WAF transforms it; then determine how the origin parses it. PortSwigger’s request-smuggling material is required for parser-disagreement attacks because the lab provides two intentionally different HTTP parsers and teaches how front-end/back-end disagreement bypasses front-end controls.

A WAF must be established as part of the request path before claiming a WAF bypass. In a white-box engagement, architecture diagrams, proxy configuration, enabled rules, and matching audit logs are direct evidence. In a black-box or provider range, compare a normal request with a deliberately safe training trigger and look for a distinct status, body, headers, cookies, block/request ID, timing, or connection behavior. CDN or server branding alone is only a product hypothesis because several intermediaries can add it.

[WAFW00F](https://github.com/EnableSecurity/wafw00f) can fingerprint known response behaviors, but it sends active probes. Use it only against your self-hosted WAF or an assigned range that permits it, preserve the version and raw output, and corroborate the guess with a controlled block plus a WAF audit log or provider evidence. If you cannot establish that a WAF made the decision, report an unknown front-end control rather than calling the result a WAF bypass.

**Worked WAF example.** A benign request reaches the origin and produces a matching request ID in the proxy and application logs. A documented CRS test string receives `403`, and the audit log records the same ID plus rule and anomaly score; the origin has no matching application request. A representation mutation then receives `200`, the WAF log records no blocking score, and the origin log proves it executed the same hostile semantic. Those four observations establish path, blocked baseline, changed WAF decision, and origin outcome. A response-header guess alone establishes none of them.

### Lab

Self-host [OWASP Coraza](https://github.com/corazawaf/coraza) or [OWASP ModSecurity CRS Docker](https://github.com/coreruleset/modsecurity-crs-docker) in a private Compose network in front of an intentionally vulnerable local target such as [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/). Follow the chosen project’s Docker quick start exactly.

First prove the WAF is in the request path. Preserve the Compose/proxy configuration, send one benign request, send one documented CRS test request, and match the blocked response or request ID to the WAF audit log and rule ID. Optionally run WAFW00F against this same private target and compare its guess with the known deployment. Your starting record must distinguish what the client observed, what the WAF logged, and what the origin received.

Before improvising parser mutations, complete PortSwigger’s [HTTP request smuggling](https://portswigger.net/web-security/request-smuggling) learning material and assigned labs through “bypassing front-end security controls.” Those deliberately vulnerable labs supply the parser-diversity target the repository does not. Then run three provider- or self-hosted cases: obvious blocked request, one representation/normalization variation from that assignment, and a legitimate near-neighbor. A bypass requires four facts: the benign request passed, the baseline attack was blocked by the established WAF, the changed representation passed that WAF, and the origin processed the same hostile semantic. Record WAF action, origin result, protected action, false positive, and rule/log evidence. Do not test a public WAF.

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

[Next: Module 5 Deep](#module-5-deep)

<a id="module-5-deep"></a>
## Deep

### Learn

Deep denial-of-service work begins with a resource model. A service fails when offered work exceeds a bottleneck long enough that queues grow, state is exhausted, deadlines pass, or recovery mechanisms amplify the load. The traffic name is secondary; the useful claim is “this workload consumes this resource faster than the system releases it.”

At the network and transport layers, distinguish:

- **bandwidth pressure:** offered bits approach the narrowest link capacity;
- **packet-processing pressure:** packets per second exhaust NIC, kernel, firewall, or router work even when bit rate is modest;
- **connection-churn pressure:** new handshakes consume CPU and allocation work;
- **connection-state pressure:** incomplete or long-lived connections occupy tables, sockets, memory, and timers.

In a normal TCP handshake, the server receives `SYN`, allocates or encodes provisional state, replies `SYN-ACK`, and waits for the final `ACK`. A SYN-pressure lab creates more incomplete handshakes than the test server can comfortably retain. Measure SYN/SYN-ACK/ACK counts, listen/backlog state, retransmissions, accepted connections, legitimate connection latency, and recovery. SYN cookies or equivalent mechanisms can reduce stored half-open state, but they do not create infinite packet-processing or application capacity.

**Reflection** and **amplification** are different properties. Reflection uses a spoofed victim source so a responder sends traffic toward the victim. Amplification means the response is larger than the request. A protocol may reflect without high amplification, or amplify a legitimate requester without spoofing. Measure request bytes/packets, response bytes/packets, and amplification ratio inside the isolated topology. Never infer that source spoofing is possible from application-layer header changes; the lab must control the network namespace and observe the actual packet source.

Slow connection attacks consume concurrency with modest bandwidth by opening many connections, sending incomplete application data, or reading responses slowly. The constrained resource may be worker threads, sockets, buffers, per-connection state, or proxy timeouts. Compare a process-per-connection server with an event-driven server before generalizing. Mitigations include header/body deadlines, minimum data rates, per-source and global concurrency bounds, bounded buffers, and upstream connection controls.

Application-layer pressure uses syntactically valid requests whose cost is asymmetric. Candidate mechanisms include cache misses, expensive search/report parameters, decompression, serialization, regex or parser work, database fan-out, lock contention, and retry cascades. Equal RPS can cause different CPU, memory, I/O, and dependency demand. Use a cheap route, expensive route, and legitimate near-neighbor; measure both target resource and service objective.

Higher-layer protocol pressure can exploit streams, resets, or parser behavior, but do not experiment from vague descriptions. Use a maintained provider or structured lab that supplies the vulnerable implementation and bounded topology. The method remains: establish healthy baseline, name the target resource, run the smallest capped reproducer, observe saturation and user impact, apply one mitigation, wait for recovery, and rerun the identical workload.

Isolation is an engineering control, not a sentence in the report. The attacker and target must live in a private topology with no default route and no bridge to Wi-Fi, Ethernet, VPN, cloud network, or the Internet. Prove routes and interfaces before packet generation. Capture at each boundary. Cap total packets/connections and duration in the generator itself. Monitor from a separate control namespace so target saturation does not hide the abort signal. Destroy the topology after exporting synthetic evidence.

Read Google SRE’s [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) for the mechanisms that turn local overload into system failure: queue growth, retry amplification, dependency fan-out, slow recovery, and load shedding. Use the SEED or university lab below for packet construction, spoofing, SYN pressure, amplification, and firewall retest; the external topology is required instruction for techniques this repository intentionally does not generate.

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

[Next: Module 6 Foundation](#module-6-foundation)


---

---

# Module 6: Practical Python and secure code review

**Red-team outcome:** Build bounded offensive clients, automate attack variations, and review code for trust, parsing, retry, concurrency, and resource-exhaustion weaknesses.

<a id="module-6-foundation"></a>
## Foundation

### Learn

**Required foundation — choose one route and complete it before the lab.**

- **Free route:** work through the official Python Tutorial [Chapter 3](https://docs.python.org/3/tutorial/introduction.html), **4.1–4.9** in [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html), **5.1–5.5** in [Data Structures](https://docs.python.org/3/tutorial/datastructures.html), **7.2 Reading and Writing Files** in [Input and Output](https://docs.python.org/3/tutorial/inputoutput.html), and **8.3 Handling Exceptions** in [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html). Type every example you need to understand; then write a program that reads one file and prints a count.
- **Guided route:** complete HTB Academy’s entire [Introduction to Python 3](https://academy.hackthebox.com/course/preview/introduction-to-python-3) module and its exercises. Return here only when you can write a small script without copying its finished solution.

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

**You are ready for the lab when you can:** run a script and read its traceback; use strings, numbers, booleans, lists, dictionaries, and sets; write an `if`, loop, and function; parse a JSON line from a file; catch a specific exception; and explain why destination, timeout, attempt, retry, concurrency, response-size, and redirect limits are separate controls.

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

[Next: Module 6 Applied](#module-6-applied)


<a id="module-6-applied"></a>
## Applied

### Learn

Type hints describe intended values and let a checker find mismatches before runtime. `str` says what the programmer expects; it does not prove an external value is safe, in range, or authorized. Parse untrusted JSON into a validated structure, reject unknown or missing fields where ambiguity is dangerous, and keep defaults explicit. Tests prove selected examples and failure paths. Neither hints nor tests replace runtime validation.

Asynchronous code lets one task make progress while another waits on I/O. It does not make CPU work free and it does not automatically make a client safe. Creating one task per item in an unbounded input can allocate memory, sockets, and target work before the program has a chance to react. Bound both the number of queued items and the number executing.

A semaphore caps work inside a critical section:

```python
semaphore = asyncio.Semaphore(5)

async def bounded_call(item: str) -> Result:
    async with semaphore:
        return await call(item, timeout=2.0)
```

The `async with` block releases the permit even when `call()` raises, but the total attempt budget must live outside it. Otherwise five workers with two retries can silently create fifteen attempts when the runbook allowed ten.

A bounded queue separates production from execution. `asyncio.Queue(maxsize=20)` makes the producer wait once 20 items are outstanding. Workers call `get()`, process under the semaphore or worker-count bound, call `task_done()` in a `finally` block, and are cancelled during cleanup. Read the official [asyncio Queue example](https://docs.python.org/3/library/asyncio-queue.html#examples) and [Semaphore documentation](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore) before implementing the lab. They are required instruction for the lifecycle you will reproduce.

Retries need four controls:

1. retry only errors likely to change, such as selected timeouts or `503`;
2. cap retries per operation;
3. cap retries as part of the global attempt budget;
4. delay with exponential backoff and jitter so clients do not synchronize.

Do not retry `401`, `403`, schema errors, or every `4xx` automatically. A retry can repeat a non-idempotent state change if the response was lost after the server committed it. Use an idempotency key only when the target supports it, and record whether the retry repeated the business action.

Review code along two paths. **Data flow** follows external input -> parsing/validation -> state -> sensitive sink such as request target, SQL query, file path, command, or authorization decision. **Resource flow** follows acquire/open/create -> use -> release/close/await/cancel. A safe client also treats redirects as new targets, limits response bytes before buffering, strips secrets from logs, and uses monotonic time for durations and budgets.

**Worked review example.** `requests.get(url, timeout=2)` has a timeout but still accepts an arbitrary target, may follow redirects, buffers the response, and can be called forever in a loop. A complete fix validates the resolved destination and redirect policy, limits attempts and concurrency, streams no more than the response cap, records structured errors, and closes the response. Security comes from the combination, not from adding one timeout.

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

[Next: Module 6 Integrated](#module-6-integrated)

<a id="module-6-integrated"></a>
## Integrated

### Learn

An engagement tool is a data pipeline:

```text
plan -> generate population -> execute bounded workflow -> emit events
-> validate schema -> score/join -> aggregate -> report -> cleanup
```

The plan phase resolves configuration without traffic. It prints target, allowed routes, mutation set, population size, request/concurrency/time budgets, abort thresholds, output path, and configuration sources. Execution should consume that immutable plan so a command-line typo cannot change scope midway through a run.

Define event semantics before writing code. Every record needs a schema version, run ID, population, session, request or trace ID, monotonic sequence, wall-clock timestamp, monotonic elapsed time, action, target route, control action, protected-action result, tool result, and structured error. Use separate fields for values that answer different questions:

```json
{
  "control_action": "challenge",
  "protected_action": "not_attempted",
  "tool_status": "ok",
  "http_status": 403
}
```

If the browser crashes, `tool_status` is `error`; the detector did not block the bot. If the server returns `403`, `control_action` may be `block` only when a log or known contract supports that interpretation; otherwise record the HTTP response and keep control action `unknown`. If the server returns `200` but inventory does not change, the request succeeded at HTTP while the protected action failed.

Events must be joinable without leaking secrets. Generate random run/session/request identifiers for synthetic work, but never log passwords, challenge answers that function as credentials, bearer tokens, real cookies, or raw high-entropy browser identifiers. Where correlation is needed, use a run-scoped pseudonymous label or server-generated request ID approved for the lab.

Schema validation belongs at ingestion and output. Reject a missing run ID, unknown schema version, invalid outcome enum, non-monotonic sequence, or event that claims `protected_action=succeeded` without the evidence field your experiment requires. Write malformed records to a separate error channel; do not silently drop them and improve the apparent metric.

Reproducibility requires deterministic fixtures where possible, recorded random seeds, dependency/browser versions, detector and target configuration, source revision, timezone, and the exact command. Randomness should be generated from a recorded seed per run, while identifiers that must remain unique can be generated separately. Repeating a seeded population should recreate mutations and order, not necessarily timestamps.

Aggregation must preserve denominators. Report `7/10 bypasses`, not only `70%`; group by population and configuration; separate missing/invalid events; and link every derived row back to raw run IDs. Median action count or latency is useful only with sample count and distribution or range. The final report should be generated from raw evidence by one command so manual spreadsheet edits cannot become invisible analysis.

**Worked example.** A normal Playwright population completes 10/10 reservations and is challenged 10/10. A patched population completes 8/10 and is allowed 6/10; one browser crash and one server error account for the remaining runs. The bypass rate is `6/8` among valid completed tool runs only if that denominator is declared. Reporting `8/10 defense failures` would incorrectly count tool/server errors as security outcomes.

### Lab

Modify `lab/run.py workflow` in a branch or temporary copy so each JSON line includes one run ID, attacker-population label, and monotonically increasing sequence. Save output as JSONL. Add at least two mutations—session-key rotation and one bot-signal change—and report protected-action completion, control action, and median actions by population. The parser must reject a missing run ID.

Add a proxy label and agent-decision field even if the value is `none` or `fixed-policy`. This prevents later analysis from guessing how traffic was produced.

Define allowed values for `tool_status`, `control_action`, and `protected_action` before implementation. Add tests for a non-monotonic sequence, unknown schema version, malformed JSON, and a browser/tool error that must not be counted as a block. Run the unchanged baseline twice with the same mutation seed and verify that action order and mutation choices match while run IDs differ.

Generate one report table directly from the JSONL with population, attempted runs, valid runs, tool errors, allow/challenge/block/unknown counts, protected-action successes, and median action count. Manually trace one table row back to its raw run/session/request IDs. If you cannot make that join, change the schema before continuing.

### Self-assess

1. Why separate tool error from defense action?
2. What fields make a workflow trace joinable?
3. Why record dependency versions?
4. Why do repeated seeded runs keep different run IDs?

<details><summary>Check your answers</summary>

1. They have different causes and remediation; combining them inflates apparent control effectiveness.
2. Run, population, session, request/trace, sequence, time, action, and result identifiers.
3. Browser and library changes can alter traffic and behavior; a second person needs the same environment to reproduce it.
4. The seed should reproduce planned choices, while unique run IDs prevent evidence from separate executions being merged accidentally.

</details>

[Next: Module 6 Deep](#module-6-deep)

<a id="module-6-deep"></a>
## Deep

### Learn

Large logs should stream when their upper bound is unknown or materially larger than memory. JSONL supports this because each line is independently parseable. Open the file, iterate one line at a time, validate, update only the aggregates or bounded per-session state needed, and emit incremental results. Keep the line number and byte position in errors so a malformed record can be reproduced.

Streaming is not automatically constant-memory. Grouping every session in a dictionary still grows with the number of sessions. Choose an explicit state strategy:

- input sorted by session so one group can be closed and discarded;
- bounded time windows with eviction based on event time and allowed lateness;
- approximate sketches when exact unique counts are unnecessary;
- partitioned temporary files or an embedded database for exact large joins.

Document how out-of-order events and late arrivals are handled. A five-minute sliding detector that evicts by processing time can produce different results when the same file is replayed faster. For deterministic offline analysis, base windows on event timestamps, define allowed lateness, and record excluded records.

Measure elapsed time, records per second, peak resident memory, input/output bytes, invalid-record count, and result checksum. Increase worker count only after a single-worker baseline. More concurrency can reduce throughput through parser CPU contention, disk seeking, lock contention, context switching, memory pressure, or downstream saturation. In an offensive client, the target—not local throughput—is also part of the safe upper bound.

A reusable CLI is an interface contract. Use subcommands with distinct authority:

- `plan` resolves configuration and prints traffic-free intent;
- `run-local` executes only against validated loopback/private lab targets;
- `replay` consumes a captured local fixture and never contacts a target;
- `report` reads evidence and produces derived output.

Define configuration precedence, for example `built-in safe defaults < config file < explicit CLI flags`, and print the winning source for every safety-critical value. Reject contradictory options. Exit codes should distinguish success, security outcome threshold, invalid plan, target rejection, partial evidence, and internal tool failure. Human-readable messages go to stderr; machine-readable results go to stdout or a named file so automation does not parse prose.

Interrupted writes need an atomicity plan. Write to a temporary file in the destination directory, flush and close it, validate the final record/count, then replace the destination. If streaming evidence must remain available during a crash, use append-only run files with a header/start event and an explicit completed/aborted trailer; the report command must reject or visibly label incomplete runs.

Safety belongs below the command parser so every code path uses it. Validate the resolved target at connection time, disable or revalidate redirects, enforce attempt/concurrency/duration/response-size budgets centrally, and make cancellation release workers and close files. Tests should exercise DNS/address changes, malformed URLs, redirect escape, budget exhaustion, cancellation, partial output, schema drift, and secret redaction.

**Worked example.** A user runs `run-local --target http://localhost:8080 --total 20 --workers 5`. The plan prints the loopback address, 20-attempt global budget, five-worker cap, two-second timeout, mutation set, and output file. During execution, four workers each retry once after `503`. The fifth worker must see the shared remaining-attempt counter, not a private counter, or the tool can exceed 20. An interrupt writes an `aborted` trailer with completed/attempted counts and exits nonzero; `report` labels the run incomplete rather than treating missing events as blocks.

Use the official Python `asyncio` queue/semaphore references from Applied for implementation details. If you choose OffSec WEB-300 or the HTB Senior Web Penetration Tester path below, its exploit scripting and source-guided exercises replace the repository CLI extension; bring back a reproducible tool, bounded target assumptions, mechanism, evidence, and report.

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

[Next: Module 7 Foundation](#module-7-foundation)

---

---

# Module 7: Experimental method, detection analysis, and reporting

**Red-team outcome:** Convert an attack into a falsifiable experiment, defensible bypass finding, actionable remediation, and identical retest.

<a id="module-7-foundation"></a>
## Foundation

### Learn

**Required foundation — complete before the lab.** Read NIST SP 800-115 [Sections 5.1 and 5.2](https://csrc.nist.gov/pubs/sp/800/115/final) for analysis, mitigation, and reporting, then read OWASP WSTG’s [Reporting Structure](https://owasp.org/www-project-web-security-testing-guide/latest/5-Reporting/01-Reporting_Structure). From the two sources, create a checklist containing evidence, reproducibility, impact, affected scope, root-cause remediation, risk/limitations, and retest status. You will use that checklist on an attack you already completed; this module does not ask you to invent a finding from nothing.

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

Evidence must support each verb in the claim. “The challenge token could be replayed” needs the denied no-token baseline, token issuance to session A, reuse from session B, and proof that session B obtained the protected report. A `200` response alone may be an error page or non-sensitive placeholder. Quote only the minimal synthetic result needed and preserve the full request/response or log under a stable ID.

Read OWASP WSTG’s [Reporting Structure](https://owasp.org/www-project-web-security-testing-guide/latest/5-Reporting/01-Reporting_Structure) before writing the lab finding. Its findings guidance is required instruction: explain the weakness and impact, provide reproducible technical detail, give actionable remediation, protect sensitive data, and make retest status visible to both technical and executive readers.

**You are ready for the lab when you can:** identify a hypothesis, independent variable, dependent measure, controls, baseline, alternative explanation, and limitation in an earlier course attack; separate an observed fact from an inference; state what evidence proves the protected action succeeded; and write a pass/fail retest that another learner could run unchanged.

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

[Next: Module 7 Applied](#module-7-applied)

<a id="module-7-applied"></a>
## Applied

### Learn

Before execution, write a test matrix. Each row is a condition, not a result you hope to find:

| Field | Purpose |
|---|---|
| Population | Names the legitimate or adversarial group represented. |
| Preconditions | Fixes target state, account, cache, inventory, and control version. |
| Independent variable | States the one deliberate change. |
| Expected mechanism | Predicts why the control or resource should respond. |
| Measures | Names score/action, protected outcome, health, and tool status. |
| Repetitions | Exposes instability and supplies a denominator. |
| Abort condition | Stops unsafe or uninterpretable work. |

Do not write the expected result after seeing the data. A useful preregistered row might say: “With the same hostile workflow and headers, changing only `webdriver` from true to false will reduce score by exactly 2; if the threshold is 3, the action will change from challenge to allow.” The rule source lets you predict the score, while the lab verifies enforcement and workflow outcome.

Preserve raw evidence separately from derived tables. Raw evidence includes requests/responses, structured events, target/control logs, versions, configuration, and run metadata. Derived data includes grouped counts, medians, confusion matrices, charts, and severity judgments. Analysis code should recreate every table from the raw input and record exclusions. Never hand-edit a raw event to “clean it”; create a corrected derived field with a documented rule.

Alternative explanations are candidate causes, not ceremonial disclaimers. If Playwright scores higher than curl, possibilities include webdriver, missing headers, timing, platform mismatch, session behavior, or a different workflow. Design follow-ups that distinguish them: replay identical HTTP through both transports, add one header, change one browser signal, or keep browser state fixed while changing execution mode. If several variables changed together, the result supports only a combined-population comparison.

Sample size does not rescue biased labels. Repeating the same synthetic event 1,000 times measures implementation stability, not population accuracy. State whether labels come from fixture construction, verified protected-action abuse, human review, or an external benchmark. Report counts with rates and confidence appropriate to the evidence; do not turn a tiny sample into decimal precision.

Recommendations map to the failed invariant and the actual enforcement point. “Add a WAF” does not explain how to prevent a cross-session challenge-token replay. A useful recommendation says: “Mint a random server-side token bound to session, protected action, audience, nonce, and five-minute expiry; reject reuse; enforce on every route that performs the action; log only a non-secret token ID; monitor challenge failure and abandonment by legitimate population.”

The retest repeats the exact attack, not a new happy-path test. It should prove: the original baseline still behaves as expected, the bypass mutation no longer completes the protected action, a valid original-session flow still works, and telemetry records the intended control action. If remediation changes the interface, document the minimal equivalent test and why it is equivalent.

**Worked example.** Baseline session B without a token receives `403`. Session A solves and receives token T. Before the fix, B replays T and receives the protected report (`200` plus expected synthetic content). After binding, B receives `403`; A can use T once for the named action; a second use receives `403`. That four-row matrix tests binding, validity, and one-time use while preserving a legitimate near-neighbor.

### Lab

Use the Module 4 temporary-fixture experiment. Before rerunning, write the hypothesis and expected confusion-matrix change. Run it, save raw fixture and JSON output, then make a table showing baseline versus changed condition. Write one alternative explanation and a follow-up experiment.

Give a five-minute briefing in this order: objective, method/safety, result, impact, limitation, recommendation, retest. Record it once. If any section exceeds one minute, shorten it.

Your evidence bundle must contain the unmodified fixture, changed fixture, baseline and changed analyzer output, exact commands, detector revision, and one generated comparison table. Give each run a stable label. In the table show counts and rates; do not omit the event that changed classification.

Write the alternative explanation in testable form: `If X rather than the named feature caused the result, then changing Y while holding Z fixed should produce outcome Q.` Run the follow-up if it uses the local fixture; otherwise include the exact required evidence. Update the finding if the follow-up contradicts the first explanation.

After recording the briefing, check every factual sentence against the bundle. Mark each as direct evidence, inference, or recommendation. Remove tool chronology that does not help the listener decide, but retain the blocked baseline, mutation, protected outcome, legitimate near-neighbor, limitation, and retest.

### Self-assess

1. Why keep raw and derived data separate?
2. What makes a recommendation measurable?
3. What should a useful alternative explanation produce?

<details><summary>Check your answers</summary>

1. So analysis can be checked and rerun without silently altering evidence.
2. A named mechanism, owner/action, metric, threshold, and retest.
3. A competing hypothesis and an experiment that distinguishes it from the original explanation.

</details>

[Next: Module 7 Integrated](#module-7-integrated)

<a id="module-7-integrated"></a>
## Integrated

### Learn

The capstone connects the complete work cycle:

```text
authorization and objective -> passive recon -> bounded active mapping
-> workflow/control/resource map -> ranked attack hypotheses -> blocked baseline
-> exploit/bypass -> adaptation or chaining -> evidence and service impact
-> finding -> remediation -> identical retest -> briefing
```

Integration means the output of one stage constrains the next. Recon identifies a protected action and control, not a generic list of endpoints. The threat map ranks an attack because observed evidence supports a failed-invariant hypothesis. The blocked baseline proves the control is active. The mutation tests one bypass path. The protected-action check proves attacker value. The remediation fixes the failed invariant. The retest sends the same attack and includes a legitimate near-neighbor.

Use explicit gates:

1. **Scope gate:** every target, account, technique, and data source is authorized.
2. **Surface gate:** the request path, state transition, control, and protected action are supported by evidence.
3. **Baseline gate:** the unmodified hostile action is blocked/challenged/throttled and target health is stable.
4. **Attack gate:** the mutation is named, bounded, and has a falsifiable success criterion.
5. **Evidence gate:** control action, tool status, HTTP result, protected state, and service health are distinguishable.
6. **Finding gate:** impact follows from attacker value and scope, not detector cleverness.
7. **Retest gate:** the original attack fails after the fix while the legitimate near-neighbor works.

The population matrix prevents one successful demonstration from becoming a broad claim. Use ordinary browser, normal Playwright, simple Python, proxy replay, one anti-detect or patched browser, and one rule/model-driven agent only when those populations answer the chosen question. If a population cannot run the same protected workflow, remove it or explain the comparison; do not count tool incompatibility as defense.

Join evidence with stable IDs. A report claim should link to a run ID, request or trace ID, control/audit-log event, protected-state observation, and derived table row. Record target, detector, browser, client, proxy, and dependency versions plus configuration hashes or copies. Put raw commands and verbose logs in an appendix or evidence bundle, while the finding contains only the minimal reproducer.

Report failed experiments and negative findings. “Header-order mutation did not change the score in 10/10 runs” narrows the decision-boundary hypothesis. A browser crash is a tool error and may expose tool fragility, but it is not a security control. An origin `500` under the baseline invalidates a bypass comparison until the target is reset and healthy.

The executive summary answers four questions without tool trivia: what protected outcome was at risk, what the authorized test proved, why it matters, and what should happen next. The technical finding explains condition, mechanism, reproducible evidence, impact, affected scope, recommendation, retest, and limitations. Severity considers prerequisites, repeatability, scale, business value, existing compensating controls, and customer impact.

**Worked chain.** Recon shows `/api/reports/limited` keys its counter on client-supplied `session_id`. Three requests under one ID produce `200, 200, 429`, establishing the control. Rotating IDs produces repeated `200` responses for the same expensive action, confirming the hypothesis. A server-side policy is changed to aggregate a trusted account/workflow key and charge route cost. The identical rotation receives throttling while the cheap health route and normal two-request session remain available. Every arrow in that chain has evidence and becomes one finding.

### Lab

Run one local capstone whose objective is to complete a protected workflow while evading or bypassing its control. Use the six populations from Module 4, the credential/workflow scenario from Module 2, and the challenge/resource experiments from Module 5. Produce:

1. one-page scope/runbook with separate passive and active discovery limits;
2. recon evidence and attack-surface map with documented, observed, and inferred labels;
3. threat map and ranked hypotheses showing which recon evidence selected each attack;
4. population/test matrix;
5. raw JSONL and version/config record;
6. attack success, control action, and service-impact tables by population;
7. two findings with remediation and retest;
8. one-page executive summary;
9. five-minute briefing that explains the lifecycle from first observation through retest.

One finding must prove a bypass that completed the protected action; the other may be a second bypass, false positive, observability gap, or reliability weakness. Re-run the exact attack locally after implementing or simulating the recommended change.

### Self-assess

1. Can another person trace every conclusion to raw evidence?
2. Did the report distinguish defense action from tool failure?
3. Did every production implication remain a hypothesis?

<details><summary>Check your answers</summary>

All three must be yes. If not, add stable IDs/commands, separate outcome categories, or narrow the claim before continuing.

</details>

[Next: Module 7 Deep](#module-7-deep)

<a id="module-7-deep"></a>
## Deep

### Learn

Original research begins with a narrow unanswered question and a method capable of disproving the preferred explanation. “Can I bypass the detector?” is too broad. “Does changing only the top-page webdriver descriptor leave worker evidence that keeps detector version X above threshold Y?” identifies a mechanism, variable, measurement, and environment.

Write a short preregistration before collecting evidence:

- question and security relevance;
- hypothesis and causal mechanism;
- target/control/browser/tool versions;
- authorized population and protected action;
- independent variable and fixed controls;
- primary and secondary measures;
- repetitions and exclusion rules;
- analysis method;
- abort condition;
- outcomes that would falsify the hypothesis.

Preregistration does not prevent exploration. It separates **confirmatory** results—analyzing the planned measure—from **exploratory** observations found afterward. A surprising header difference can become the next experiment, but it should not be presented as the original hypothesis.

Version and environment are variables. Pin source revision, detector rules/model, browser build, driver, operating system/container image, proxy, target snapshot, and configuration. Record time and seed. If an upgrade changes the result, run the old and new versions against the same fixture and identify whether collection, feature computation, threshold, or enforcement changed.

Reproduction by another person or clean environment is stronger than more screenshots from the author. A reproduction package contains a scope-safe target setup, exact commands, dependency lock, configuration, synthetic fixture, expected intermediate observations, analysis command, and success/failure criteria. It must omit provider secrets, assigned target details prohibited by terms, real tokens, and personal data.

Mature detection research compares feature families, rule overlap, collection and compute cost, incremental value, drift, attacker cost, and legitimate-population harm. Ablation measures what happens when a feature is removed. Pairwise overlap shows whether two rules alert on the same events. A cheap evasion against a dominant feature suggests brittleness; a costly cross-layer adaptation may show the defense raises attacker cost even if it does not eliminate abuse.

Report uncertainty in observable terms. “10/10 controlled runs under versions A/B produced the same bypass” is precise. It does not justify “always” or a production prevalence claim. If 7/10 succeed and three fail due to race or state, investigate and report the mechanism before averaging. If the sample is a designed fixture, it supports code-path and measurement claims, not real-world error rates.

Evaluate alternative explanations with discriminating tests. If a patched browser is allowed, possible causes include signal change, browser-version difference, new profile state, proxy route, timing, or target drift. Hold all but one fixed, or use a factorial design only when you can analyze interactions. Report when variables cannot be separated.

The final portfolio artifact should teach the mechanism without publishing unsafe target details. Include abstract, threat model, ethics/scope, method, results with denominators, negative results, alternative explanations, limitations, remediation, retest, and reproduction instructions for the synthetic/local target. The reader should be able to reproduce the evidence and reach a different conclusion if the data warrants it.

### Lab

Choose one original evasion, replay, normalization, workflow-abuse, or bounded resource-pressure question from Modules 1–5. Preregister the hypothesis, variables, sample count, analysis, and stop condition before collecting data. Run a blocked baseline, at least two attack conditions, and one legitimate near-neighbor. Ask another person to reproduce from your instructions, or repeat in a clean environment.

Publish a portfolio version with synthetic data only: abstract, threat model, ethics/scope, method, results, alternative explanations, limitations, remediation, retest, and reproduction commands. Remove tokens, provider target details, and anything prohibited by an external range.

The preregistration must name one primary measure and what observation would falsify the hypothesis. Preserve it with a timestamp or commit before the first run. Use at least five repetitions per condition unless the chosen external lab has a stricter safe cap; explain why the count is sufficient only for repeatability under the fixture, not real-world prevalence.

Package a clean reproduction directory outside this repository with setup, pinned dependencies, synthetic input, commands, expected intermediate evidence, analysis, and cleanup. Have the reproducer record deviations rather than silently fixing your instructions. Compare results by run and condition, investigate any disagreement, and publish the corrected procedure plus both outcomes.

Before release, run a disclosure/privacy checklist: no real credentials or cookies, no public/unassigned target, no provider secrets or forbidden screenshots, no personal data, no production topology detail, and no command that defaults to an external destination. A useful portfolio artifact teaches the mechanism using the local or provider-approved environment without enabling accidental retargeting.

### Self-assess

1. What distinguishes original research from a product demo?
2. Why preregister the analysis?
3. What is a calibrated claim?

<details><summary>Check your answers</summary>

1. A falsifiable question, controlled comparison, evidence, limitations, and a result not assumed in advance.
2. To reduce changing the method after seeing results and cherry-picking favorable measures.
3. A conclusion whose confidence and scope match the quantity and quality of evidence.

</details>

[Next: Module 8 Foundation](#module-8-foundation)

---

---

# Module 8: Interview communication and role translation

**Red-team outcome:** Explain an attack plan and bypass evidence clearly enough that another engineer can reproduce the weakness, judge impact, implement a fix, and run the retest.

<a id="module-8-foundation"></a>
## Foundation

### Learn

**Required foundation — complete before the lab.** Bring forward your own artifacts from Modules 0–7: authorization plan, request-path map, abuse workflow, browser trace, detector evasion, edge-control test, Python output, and finding. For each artifact, write one evidence card with five fields: **objective, decision, action, measured result, limitation**. If a field is missing, return to that module and repair the artifact before practicing an interview answer. This prevents communication practice from becoming unsupported storytelling.

An interview answer should make your reasoning visible. Use this technical structure:

```text
objective and authorization -> recon evidence -> attack-surface and workflow map
-> assumptions and ranked hypotheses -> attack/mechanism -> measurement
-> adaptation -> failure modes -> remediation/retest
```

Do not list tool names. Translate prior experience into role mechanisms. Incident response becomes hypothesis formation and evidence triage. Detection engineering becomes feature design and false-positive measurement. Network engineering becomes request-path and exhausted-resource reasoning. Application security becomes workflow abuse and remediation.

A 90-second role narrative has four parts:

1. current security identity and strongest evidence;
2. why bots/DDoS/red teaming is the logical next problem;
3. one course experiment that proves hands-on movement;
4. what value you can deliver while deepening the specialty.

Behavioral answers use Situation, Task, Action, Result, and Lesson. Spend most time on your actions and decisions. State metrics and what you would change.

A five-minute bot-control red-team plan should cover authorized passive/active recon, the protected action, request path, control assumptions, attack populations, fingerprint/identity/timing mutations, success evidence, safety, and retest. A DDoS test answer begins with discovery of the request path, exposed protocols, expensive operations, exhausted resource, and service objective, then the smallest bounded reproducer, telemetry, abort conditions, mitigation, and identical retest.

**You are ready for the lab when you can:** explain every term on one evidence card without jargon; distinguish what you did from what the team did; give the number or artifact supporting each result; state a limitation without erasing the result; and answer “what would you test next?” with a concrete hypothesis and measurement.

### Lab

Write and say aloud:

- your 90-second narrative;
- one behavioral story about ambiguity;
- one about a security or reliability improvement;
- one about disagreement or a failed approach;
- a five-minute bot-control attack and bypass plan that explains which recon observation selected the first hypothesis.

Record the answers on your phone. Listen once. Remove unexplained acronyms, unsupported “always/never” claims, and any section that hides your decision behind “we.”

### Self-assess

1. Can the listener identify your objective, decision, evidence, and result?
2. Did the technical answer include recon evidence, the attack path, bypass criterion, false positives, and measurement?
3. Did each behavioral story say what you personally did?
4. Can you explain the lab’s limitations without undermining its learning value?

<details><summary>Check your answers</summary>

All four should be yes. A good limitation sounds like: “The fixture proves the scoring and measurement workflow, not production accuracy; I would validate in shadow mode on representative populations.”

</details>

[Next: Module 8 Applied](#module-8-applied)

<a id="module-8-applied"></a>
## Applied

### Learn

Technical interviews test whether you can build and revise a model in public. Start by restating the objective, authorization/safety boundary, protected action, and success criterion. Ask only questions that change the design: request path, scale, trusted identities, available telemetry, false-positive tolerance, service objective, and whether the task is black-box, gray-box, or white-box.

Use this answer sequence for an attack-design question:

1. map the authorized target and request/workflow path;
2. identify the control and the invariant it should enforce;
3. establish a blocked baseline;
4. rank mutations by evidence and attacker cost;
5. execute the smallest bounded test;
6. prove control decision and protected-action outcome;
7. include a legitimate near-neighbor;
8. recommend the root-cause fix and identical retest.

**Worked WAF answer.** Do not begin with a list of payload encodings. First establish that a WAF is in path using architecture/configuration or a controlled block plus matching audit log. Record its parser, CRS/rule version, normalization, and the origin route. Send a benign request and a safe blocked baseline. Select one representation mutation supported by a parser-disagreement hypothesis. A bypass requires the changed request to pass the WAF and the origin to process the same hostile semantic. The fix aligns parsing/normalization or enforces the invariant at the origin; the retest sends the original and mutated forms plus a legitimate near-neighbor.

Expect follow-ups that remove assumptions: What if IP is shared? JavaScript is disabled? The detector is evaded? The event is a flash crowd? The dependency rather than edge is saturated? Strong answers do not defend the first design reflexively. State what changed, which earlier conclusion no longer holds, and how the test or control changes.

For example: “If IP is shared, I would demote it from identity to one risk feature, aggregate the protected action across trusted account/session/workflow state, and measure impact on the shared-network population. The red-team retest rotates source while preserving the campaign goal.” That is stronger than “use machine learning” because it names mechanism, evidence, and tradeoff.

For code, state input, output, constraints, authorization/safety requirements, data structure, complexity, failure handling, and tests before typing. Walk one normal example and one failure example. For an offensive client, mention target validation, attempts, concurrency, timeout, retries, response cap, redirects, structured outcomes, and cleanup where relevant.

For system design, begin with objective and scale, draw client -> edge/control -> application -> dependencies, and mark termination points, state, trust boundaries, and exhausted resources. Then cover telemetry joins, action policy, false positives, overload behavior, rollback, and red-team validation. Do not spend the answer naming vendor products unless the question asks for them.

Behavioral follow-ups test ownership and judgment. Give the decision context, what you personally did, evidence considered, disagreement or risk, measured result, and what changed afterward. “We decided” hides your contribution; “I proposed X, tested Y, and changed course when Z contradicted the hypothesis” makes it inspectable.

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
3. What evidence must precede a WAF-bypass claim?
4. How should an offensive-client coding answer address safety?

<details><summary>Check your answers</summary>

1. State the changed assumption, update the design, and explain the new tradeoff.
2. Clarify input, output, constraints, and failure cases.
3. Establish the WAF in path, show a blocked hostile baseline, then prove the mutation passed that WAF and the origin processed the same hostile semantic.
4. Include resolved-target validation, attempt/concurrency/time/response limits, redirect handling, structured outcomes, and cleanup where relevant.

</details>

[Next: Module 8 Integrated](#module-8-integrated)

<a id="module-8-integrated"></a>
## Integrated

### Learn

A complete interview loop samples different evidence: coding and code review, protocol or browser depth, attack design, system design, behavioral judgment, and portfolio communication. One memorized speech cannot answer all six. Build an evidence bank indexed by mechanism and decision, then select the smallest example that answers the question.

For each course project, write an evidence card:

```text
Problem and protected outcome:
Authorization and constraints:
Observation that selected the attack:
Failed control invariant:
Attack and adaptation:
Measured evidence:
Remediation and retest:
Limitation and next experiment:
My individual decisions:
```

Use **claim -> evidence -> limitation -> implication**. “I built a bot evasion lab” is only a claim. Evidence is the blocked baseline, named mutation, detector version, action trace, score/action change, protected reservation, and retest. The limitation is that the fixture is local and synthetic. The implication is that you can test decision boundaries and report a reproducible bypass, not that you measured production accuracy.

Answer at the altitude of the question. An executive asks what value or risk was demonstrated and what decision is needed. An application engineer needs the failed state/authorization invariant and retest. A detection engineer needs populations, features, thresholds, labels, errors, drift, and enforcement. A network/SRE reviewer needs request path, constrained resource, offered/accepted load, service objective, abort, recovery, and retry behavior.

System-design communication should expose tradeoffs. If you propose a per-account rate limit, name pre-authentication gaps and compromised-account behavior. If you add browser signals, cover privacy, collection failures, and accessibility populations. If you recommend a challenge, cover binding, replay, abandonment, and direct-API enforcement. If you propose load shedding, state which work is critical and how the system degrades.

Use diagrams only when they clarify relationships. A request-path diagram should mark TLS/protocol termination, control placement, trusted identity state, cache, origin, and dependencies. A workflow diagram should show state transitions and protected value. A test matrix should show populations and variables. Narrate the diagram by following one hostile request end to end rather than pointing at boxes.

For coding sessions, explain invariants while implementing. Example: “This shared attempt counter is checked before every initial request and retry, so five workers cannot exceed the global budget. This `finally` releases the queue task and closes the response on error. These tests cover redirect escape and retry exhaustion.” The explanation lets the reviewer verify safety and correctness beyond syntax.

For behavioral sessions, use different examples when possible, but do not force a weak story to avoid repetition. A strong reused event can answer different questions if you focus on a different decision and say so. Never change facts to fit a competency.

Your mock-review rubric should be evidence-based:

- **2:** correct mechanism, explicit assumptions, concrete evidence, tradeoffs, and adaptive follow-up;
- **1:** directionally correct but missing evidence, limitation, or an important tradeoff;
- **0:** unsupported claim, unsafe/unbounded method, incorrect mechanism, or inability to revise.

Record the exact gap behind every score. “Be more technical” is not actionable; “did not distinguish WAF decision from origin outcome” tells you what to relearn and demonstrate.

### Lab

Run five sessions on separate days if possible:

1. Python offensive tooling and exploit-oriented code review;
2. browser-bot evasion technical deep dive;
3. WAF bypass and bounded DDoS/edge attack design;
4. three behavioral stories with skeptical follow-up;
5. capstone briefing and questions.

Use the same 0–2 rubric. For every score below 2, write one corrective action and repeat that section. The loop is complete when no category is below 1 and the average is at least 1.5; this is only a self-assessment marker.

For each session, give the reviewer the question but not your prepared evidence card. Limit the opening answer to five minutes, then require at least three skeptical follow-ups. Preserve the question, outline, reviewer scores, exact missed mechanism or evidence, and revised answer. A score without written evidence is not useful feedback.

Across the five sessions, require these demonstrations: draw and narrate one request path; trace one hostile workflow state transition; explain one detector confusion matrix and evasion; distinguish WAF action from origin outcome; identify one constrained DDoS resource and abort; review one unsafe retry/concurrency pattern; and defend one remediation with a legitimate near-neighbor retest.

At the end, build a gap table that maps every score below 2 to the exact course section, lab evidence to regenerate, and date for a repeat. Repeat only the failed portion first; then run one complete session to verify the correction works under context switching.

### Self-assess

1. Can every major claim point to course evidence?
2. Can you defend one failed experiment or changed conclusion?
3. Can you adapt a design when scale, privacy, or customer-impact assumptions change?

<details><summary>Check your answers</summary>

All three should be yes. If an answer relies only on memorized terminology, return to the matching experiment.

</details>

[Next: Module 8 Deep](#module-8-deep)

<a id="module-8-deep"></a>
## Deep

### Learn

Senior communication does three things at once: teaches the system model, recommends a decision with tradeoffs, and makes uncertainty explicit. It does not hide behind senior-sounding abstractions. A reviewer should be able to identify the protected outcome, current evidence, failed assumption, proposed action, owner, measure, risk, rollback, and unanswered question.

Use a decision memo structure for a complex finding:

1. **Decision needed:** one sentence naming the owner and choice.
2. **Why now:** demonstrated risk, incident pattern, or control gap.
3. **Evidence:** reproducible attack, affected scope, legitimate near-neighbor, and limitations.
4. **Options:** at least two feasible responses plus “do nothing/accept risk” when appropriate.
5. **Tradeoffs:** attacker cost, customer friction, privacy, reliability, engineering cost, and time.
6. **Recommendation:** the option selected and why.
7. **Validation:** shadow/canary/retest measures, advance/rollback criteria, and owner.
8. **Unknowns:** evidence still needed and who will obtain it.

**Worked decision.** A local and configuration review show challenge results are not bound to session. Option A blocks all token reuse by storing one-time nonce state; it gives strong replay resistance but adds state and failure handling. Option B uses a short-lived signed token bound to session/action and permits bounded retry; it reduces state but must handle key rotation and replay within the retry allowance. The recommendation depends on action value, expected retries, and architecture. The memo should not jump from the local lab to production prevalence; it should state the evidence gate needed.

Teaching is a deeper test than recitation. Begin a 20-minute lesson with the learner’s question, draw the smallest useful model, explain one mechanism, predict a lab result, demonstrate it, then compare prediction with evidence. Ask the learner to explain the failed invariant and design the retest. If you cannot answer why a step exists, return to the source material rather than filling time with terminology.

A first-90-day plan should not promise a rewrite or immediate high-volume testing. It is an evidence-acquisition and trust-building plan:

- **Days 1–30 — understand:** map owners, authorization process, architecture, request paths, controls, incidents, service objectives, telemetry joins, data governance, legitimate populations, and current test environments. Deliver an agreed system/threat map and prioritized unknowns.
- **Days 31–60 — reproduce:** select one high-value, safely reproducible control invariant; establish blocked baseline and legitimate near-neighbor in a lab; quantify detection/service behavior; write a finding and candidate remediation. Deliver a reproducible evidence package and decision memo.
- **Days 61–90 — validate:** help the owner implement or simulate the change, evaluate offline/shadow/canary as appropriate, run the identical retest, document rollback and residual risk, and select the next research question. Deliver the retest result and updated backlog.

Every deliverable needs a measure. “Learn architecture” becomes “owner-reviewed request-path and control map with every unknown assigned.” “Improve bot detection” becomes “reproduce one bypass, reduce its success under the identical test, and keep named legitimate-population action rate within an owner-approved bound.” Measures are negotiated with system owners; do not invent universal production thresholds.

Senior answers handle disagreement by separating facts, assumptions, values, and decisions. If an engineer disputes severity, agree on the technical reproduction first, then discuss exploit prerequisites and business impact. If a product owner rejects customer friction, compare lower-friction actions such as observation, cost-aware throttling, or step-up only at the protected action. If evidence is insufficient, recommend the next safe experiment instead of overstating certainty.

The final proof of this depth is transferable teaching and judgment. Another learner should be able to reproduce the demonstration, a technical owner should be able to implement the recommendation, and a decision-maker should understand why the residual risk is accepted or changed.

### Lab

Teach one 20-minute lesson from this course without reading the text. Include a demonstration and answer skeptical questions. Then run two more full mock loops with different reviewers or question order.

Use this lesson sequence: learner question, smallest useful model, mechanism, prediction, live local demonstration, evidence review, remediation, identical retest, and learner explanation. Give the learner a one-page reproduction card containing only prerequisites, commands, expected evidence, and cleanup. If the learner cannot reproduce it, fix the lesson or card and teach it again.

Write a first-90-day plan:

- Days 1–30: learn owners, architecture, controls, incidents, data governance, and safe test process.
- Days 31–60: reproduce one priority weakness, establish baseline/false positives, and propose a bounded remediation.
- Days 61–90: validate in shadow/canary mode, retest, document, and select the next research question.

Tie each phase to a deliverable and measure. Avoid promising production access or high-volume testing before authorization and system understanding.

Write the plan as a decision document, not a calendar wish list. Name stakeholders, dependencies, authorization gates, data/privacy review, service-health guardrails, and the evidence required to select the first weakness. For each deliverable include owner, reviewer, measure, risk, and fallback. Include at least one plausible reason the priority could change, such as an incident, missing telemetry, unacceptable false-positive population, or architecture assumption disproved during reproduction.

Present the lesson and 90-day plan to a skeptical reviewer. Ask them to challenge technical depth, customer impact, feasibility, and evidence. Revise any claim that promises an outcome before the necessary discovery or authorization, and any measure that cannot be verified.

### Self-assess

1. Can another learner follow your explanation and reproduce the demo?
2. Does the 90-day plan learn before changing production?
3. Does every proposed improvement have a measure and retest?

<details><summary>Check your answers</summary>

All three should be yes. If teaching reveals a gap, return to that module’s Learn and Lab sections; that is the purpose of the exercise.

</details>

[Next: Course complete](#you-are-done)

---

# You are done

There is no repository ceremony. If you completed each lesson, lab, and self-assessment honestly and can reproduce the final attack evidence, the course is complete. Use [RESOURCES.md](RESOURCES.md) only when a module assigns it or when you want another authorized lab.
