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

## Course attacks

```bash
# Show the safety envelope without traffic
python -m lab.clients.safe_client --dry-run

# Inventory the local surface, run five bounded probes, and form attack hypotheses
python -m lab.run recon

# Execute synthetic password spraying and credential stuffing patterns
python -m lab.run credential

# Automate an account, inventory, promotion, and challenge workflow
python -m lab.run workflow

# Evade one toy bot-control decision by changing one signal
python -m lab.run evasion

# Capture and replay a challenge token across synthetic sessions
python -m lab.run bypass

# Defeat a per-session limit by rotating its attacker-controlled key
python -m lab.run ratelimit

# Apply bounded pressure to cheap and expensive routes
python -m lab.run resilience

# Detector reconnaissance: learn the toy detector's decision boundary
python -m lab.analysis.analyze
```

Run `recon` before the attacks. It prints the route inventory, bounded observations, and the authorization, challenge, rate-limit, and resource-protection hypotheses that the later commands test. The attack commands print the baseline, changed condition, protected action, and bypass evidence. The weaknesses are intentional and exist only in this local target.

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
