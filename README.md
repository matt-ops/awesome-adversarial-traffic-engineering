# Adversarial Traffic Engineering

A red-team-first course for attacking automated-abuse controls: intercept and replay traffic, automate hostile workflows, evade bot detection, bypass challenge and WAF assumptions, pressure-test DDoS mitigations, and report reproducible findings.

You learn how a control works only so you can identify what it trusts and attack that assumption. The course does not end at detection design or defensive observation.

## Start

**[Open the course](COURSE.md)**

Then do only this:

1. Read **Learn**.
2. Do **Lab**.
3. Answer **Self-assess** and check your answers.
4. Click **Next**.

Nothing else in the repository is required to understand the course.

Every section explains the mechanism and the evidence the lab must produce. When a mature external course or isolated range is required, the exact lesson is linked inside **Learn** or **Lab** and is part of that section—you are not expected to invent the missing curriculum yourself.

Your progress is simply the last **Next** link you completed. Bookmark that heading in the public page; there is no tracker or repository file to maintain.

## The red-team loop

Every core lab follows the same simple loop:

```text
scope and objective -> passive recon -> bounded active mapping
-> workflow/control/resource map -> attack hypothesis -> blocked baseline
-> execute attack -> prove bypass -> explain impact -> recommend a fix -> retest
```

Recon is required setup, not optional background reading. The course teaches how to map the authorized surface and then assigns mature external reconnaissance labs where they are better than the toy target. Seeing a signal or calculating a detector score is still preparation; the result is the adversarial action you completed, the control you defeated or stressed, and the evidence that proves it.

## What you need

- Python 3.12+
- Docker with Compose
- Node.js 22+ for the browser labs
- An editor and terminal

The first browser lab tells you exactly when to install Playwright. External labs are linked at the point where they are used.

## The path

The course has nine modules. The skill areas stay broad; the outcome of each is offensive:

1. Safety and red-team engagement discipline — authorize and contain real adversary techniques
2. Web request path and network fundamentals — map the attack surface, then intercept, mutate, proxy, and replay traffic
3. Automated abuse and threat modeling — execute credential, account, inventory, and workflow attacks
4. Browser automation — build scripted and AI-powered browser attackers
5. Browser signals and bot detection — fingerprint the control, then evade it
6. Edge controls and DDoS resilience — bypass challenges/WAF assumptions and pressure-test mitigations
7. Practical Python and secure code review — build bounded offensive tooling and find exploitable trust failures
8. Experimental method, analysis, and reporting — turn a bypass into a defensible finding and retest
9. Technical and career communication — explain the attack path, evidence, impact, and next test

Complete one module at a time. Within that module, work through **Foundation -> Applied -> Integrated -> Deep**, then continue to the next module. Each stage assumes the earlier stages are complete. There is no schedule or alternate path to choose among.

## Lab start and stop

```bash
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
python -m lab.run recon
```

Expected response:

```json
{"status":"ok","service":"aate-local-app"}
```

The recon command inventories routes, performs five bounded local probes, and turns the observations into attack hypotheses used by the later commands.

Stop when finished:

```bash
docker compose -f lab/docker-compose.yml down
```

All bundled attacks are restricted to the local lab. External exercises must use only their assigned targets. Read [SAFETY.md](SAFETY.md).

## More labs

[RESOURCES.md](RESOURCES.md) lists exact free, paid, and self-hosted ranges. The course assigns them at the point of use; you are never told to find a lab on your own.

If a technique is unsafe or unrealistic to reproduce in this small repository, the objective is not skipped. The matching course section sends you to a named provider-assigned or isolated lab and tells you what evidence to bring back.
