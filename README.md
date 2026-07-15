# Adversarial Traffic Engineering

A hands-on course for automated abuse, browser bots, bot detection, edge controls, DDoS resilience, safe red teaming, and AI-powered agents.

## Start

**[Open the course](COURSE.md)**

Then do only this:

1. Read **Learn**.
2. Do **Lab**.
3. Answer **Self-assess** and check your answers.
4. Click **Next**.

Nothing else in the repository is required to understand the course.

## What you need

- Python 3.12+
- Docker with Compose
- Node.js 22+ for the browser labs
- An editor and terminal

The first browser lab tells you exactly when to install Playwright. External labs are linked at the point where they are used.

## The path

The course has nine modules:

1. Safety and red-team engagement discipline
2. Web request path and network fundamentals
3. Automated abuse and threat modeling
4. Browser automation
5. Browser signals and bot detection
6. Edge controls and DDoS resilience
7. Practical Python and secure code review
8. Experimental method, analysis, and reporting
9. Technical and career communication

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

All bundled exercises are restricted to the local lab. External exercises must use only their assigned targets. Read [SAFETY.md](SAFETY.md).

## More labs

[RESOURCES.md](RESOURCES.md) lists exact free, paid, and self-hosted alternatives. You never need to choose one unless a course section assigns it.
