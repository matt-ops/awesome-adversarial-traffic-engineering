# Getting started

## 1. Establish the boundary

Read [`SAFETY.md`](../SAFETY.md). Confirm that generated traffic can reach only local loopback addresses or repository-approved Compose service names. Do not proceed if the target, authorization, owner, cap, or abort condition is ambiguous.

## 2. Start the single path

Open [`curriculum/path.md`](../curriculum/path.md). Choose an exit ramp based on the evidence you need, then begin with Module 0 at your next incomplete depth. Even if you intend to study for six weeks, complete the Foundation cycle first.

## 3. Record evidence

Update `curriculum/progress.yaml` after a completion test passes. Use integer levels:

- `0`: not started
- `1`: Foundation complete
- `2`: Applied complete
- `3`: Integrated complete
- `4`: Deep complete

Add artifact paths to the module’s `artifacts` list and set each gate dimension only after a review.

## 4. Report progress

```bash
python scripts/progress.py
```

Expected initial summary:

```text
Current checkpoint: Foundation in progress
Completed modules at current level: 0/9
Recommended next three tasks:
  1. Complete Module 0 Foundation
  2. Complete Module 1 Foundation
  3. Complete Module 2 Foundation
```

The report describes curriculum evidence and never predicts interview or hiring outcomes.

## 5. Run the local vertical slice

If Docker is available:

```bash
docker compose -f lab/docker-compose.yml up --build
curl http://localhost:8080/health
```

Expected health response:

```json
{"status":"ok","service":"aate-local-app"}
```

Stop and remove the local containers:

```bash
docker compose -f lab/docker-compose.yml down
```

See the [lab guide](../lab/README.md) for caps, dry-run behavior, fixture analysis, and limitations.

