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

## Lifecycle

```powershell
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
```

Expected health body is `{"status":"ok","service":"aate-local-app"}`. Reset
state with `curl.exe -X POST http://localhost:8080/api/reset`. Stop and remove
the course containers with `docker compose -f lab/docker-compose.yml down`.

The application intentionally includes missing reservation authorization,
replayable challenge state, a caller-controlled rate key, and bounded expensive
work. These are lab-specific behaviors, not production claims.

