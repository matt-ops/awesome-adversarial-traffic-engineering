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

## The red-team loop

Every core lab follows the same simple loop:

```text
target and control -> attack hypothesis -> execute attack -> prove bypass
-> explain impact -> recommend a fix -> retest
```

Seeing a signal or calculating a detector score is preparation. The result is the adversarial action you completed, the control you defeated or stressed, and the evidence that proves it.

## What you need

- Python 3.12+
- Docker with Compose
- Node.js 22+ for the browser labs
- An editor and terminal

The first browser lab tells you exactly when to install Playwright. External labs are linked at the point where they are used.

## The path

The course has nine modules. The skill areas stay broad; the outcome of each is offensive:

1. Safety and red-team engagement discipline — authorize and contain real adversary techniques
2. Web request path and network fundamentals — intercept, mutate, proxy, and replay traffic
3. Automated abuse and threat modeling — execute credential, account, inventory, and workflow attacks
4. Browser automation — build scripted and AI-powered browser attackers
5. Browser signals and bot detection — fingerprint the control, then evade it
6. Edge controls and DDoS resilience — bypass challenges/WAF assumptions and pressure-test mitigations
7. Practical Python and secure code review — build bounded offensive tooling and find exploitable trust failures
8. Experimental method, analysis, and reporting — turn a bypass into a defensible finding and retest
9. Technical and career communication — explain the attack path, evidence, impact, and next test

Each module has Foundation, Applied, Integrated, and Deep sections. Finish Foundation across all nine modules first. Continue at the same depth across all modules before moving deeper.

[Checkpoints](CHECKPOINTS.md) are optional stopping points, not tests or separate courses.

## Lab start and stop

```bash
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
```

Expected response:

```json
{"status":"ok","service":"aate-local-app"}
```

Stop when finished:

```bash
docker compose -f lab/docker-compose.yml down
```

All bundled attacks are restricted to the local lab. External exercises must use only their assigned targets. Read [SAFETY.md](SAFETY.md).

## More labs

[RESOURCES.md](RESOURCES.md) lists exact free, paid, and self-hosted ranges. The course assigns them at the point of use; you are never told to find a lab on your own.

If a technique is unsafe or unrealistic to reproduce in this small repository, the objective is not skipped. The matching course section sends you to a named provider-assigned or isolated lab and tells you what evidence to bring back.
