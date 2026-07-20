# Integrated local API

The Docker Compose lab places a synthetic FastAPI application behind an Nginx
edge bound to `localhost:8080`. Docker is introduced here only after the learner
has traced HTTP, browser, DOM, JavaScript, and Playwright behavior.

## Boundary and target

- Authorization: repository-owned synthetic application
- Target: `http://localhost:8080`
- Adversary objectives: named by the assigning lesson
- Safety: edge port is loopback-only; app is internal to Compose; runners use
  fixed relative paths and bounded counts

## Lab contract

- Protected action: assigned by the current workflow/control lesson
- Baseline: `/health` returns `200` immediately after a reset
- Hypothesis: assigned per attack; the API itself is only the target fixture
- Changed variable: named by the assigning lesson
- Fixed variables: target, version, reset state, and evidence schema
- Success: the assigning lesson's protected action or service effect occurs
- Evidence: response plus state/telemetry query named by that lesson
- Limitations: single-process synthetic state and deliberately vulnerable routes
- Cleanup: reset state between cases and stop/remove the course Compose stack
- Remediation: named as a security invariant by the assigning lesson
- Retest: reset, repeat the former attack, and run the legitimate near-neighbor

## Lifecycle

### PowerShell

```powershell
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
```

### Bash or zsh

```bash
docker compose -f lab/docker-compose.yml up --build -d
curl http://localhost:8080/health
```

Expected health body is `{"status":"ok","service":"aate-local-app"}`. Reset
state with `curl.exe -X POST http://localhost:8080/api/reset` in PowerShell or
`curl -X POST http://localhost:8080/api/reset` in Bash or zsh. Stop and remove
the course containers with `docker compose -f lab/docker-compose.yml down`.

The application intentionally includes missing reservation authorization,
replayable challenge state, a caller-controlled rate key, and bounded expensive
work. These are lab-specific behaviors, not production claims.
