# Adversarial Traffic Lab

This is a synthetic, local-only educational lab. It demonstrates safety validation, request flow, bounded client behavior, transparent detection, and reproducible analysis. It is not a production bot manager, WAF, CDN, or DDoS platform.

## Safety envelope

- Targets: `localhost`, `127.0.0.1`, `::1`, and approved Compose names only
- Maximum duration: 15 seconds
- Maximum concurrency: 5
- Maximum rate: 10 requests/second
- Maximum total requests: 100
- Maximum expensive requests: 20
- No safety-disable flag and no redirect following in the provided client

Read [SAFETY.md](../SAFETY.md) and the [guardrails](../docs/safety/load-testing-guardrails.md).

## Architecture

```text
Bounded local client -> Nginx edge on 127.0.0.1:8080 -> FastAPI synthetic app
Deterministic fixture -> explainable detector -> metrics and limitations
```

## Start and stop

```bash
docker compose -f lab/docker-compose.yml up --build
curl http://localhost:8080/health
docker compose -f lab/docker-compose.yml down
```

Expected health response:

```json
{"status":"ok","service":"aate-local-app"}
```

## Dry run and analysis

```bash
python -m lab.clients.safe_client --dry-run
python -m lab.analysis.analyze
```

The fixture is deliberately simple. Perfect seeded metrics prove deterministic code paths only and must never be presented as real-world detector quality.

## Curriculum mapping

See the direct [lab-to-module map](../curriculum/lab-mapping.md). This slice supports Foundation evidence for safety, request path, synthetic abuse, edge/DDoS planning, Python/review, and reporting. Browser/Playwright and sensor expansion belongs to Modules 3 and 4 at their specified levels—not to a separate lab course.

## Cleanup

Stop containers after use. Generated telemetry and reports are ignored by Git. Use only synthetic identities and do not paste production data into fixtures.

