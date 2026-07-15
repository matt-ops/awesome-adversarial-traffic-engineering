# Local lab

You do not need to read the lab source code before learning. Start it, run the course command, and stop it.

## Start

```bash
docker compose -f lab/docker-compose.yml up --build -d
curl.exe http://localhost:8080/health
```

Expected:

```json
{"status":"ok","service":"aate-local-app"}
```

## Course exercises

```bash
# Show the safety envelope without traffic
python -m lab.clients.safe_client --dry-run

# Synthetic login attempts
python -m lab.run credential

# Account, login, search, inventory, promotion, and challenge workflow
python -m lab.run workflow

# Five cheap versus five bounded expensive requests
python -m lab.run resilience

# Evaluate the transparent detector on the fixed fixture
python -m lab.analysis.analyze
```

Every runner is fixed to `localhost`. The bundled general client rejects non-local targets and caps duration, rate, concurrency, and total requests.

## Browser exercise

Install once:

```bash
npm install
npx playwright install chromium
```

Run:

```bash
npm run playwright:foundation
```

Expected output names `lab/telemetry/foundation-playwright.jsonl` and reports the number of saved local request/response events.

## Tests

```bash
python -m unittest discover -s lab/tests -v
npm run typecheck
```

## Stop and reset

Reset synthetic state while the lab is running:

```bash
curl.exe -X POST http://localhost:8080/api/reset
```

Stop containers:

```bash
docker compose -f lab/docker-compose.yml down
```

Generated telemetry is ignored by Git. Use only the fixed/generated identities in the lab. See [SAFETY.md](../SAFETY.md).
