# Bounded application-layer load lab

All traffic is fixed to the local synthetic API. The script rejects non-loopback
targets, unassigned scenarios, duration over 15 seconds, more than 5 VUs, an
effective rate over 10 requests/second, and a worst-case total over 100 requests
including setup/teardown. Threshold failure aborts the test. There is no L3/L4
traffic generation.

## Dry run first

```powershell
$env:AATE_DRY_RUN='1'
k6 run lab/load/bounded.js
```

Expected network totals are zero and the console prints target, scenario,
duration, rate, and maximum VUs.

## Assigned scenarios

Remove the dry-run variable, use conservative values, and set one scenario:

```powershell
Remove-Item Env:AATE_DRY_RUN -ErrorAction SilentlyContinue
$env:AATE_DURATION='5'
$env:AATE_RATE='2'
$env:AATE_MAX_VUS='3'
$env:AATE_SCENARIO='cheap-expensive'
k6 run lab/load/bounded.js
```

The seven assigned values are `cheap-expensive`, `cache-bypass`, `identity-key`,
`endpoint-specific`, `workflow-aware`, `retry-amplification`, and `recovery`.
Execute only the scenario assigned by the current lesson. Setup resets synthetic
state; teardown checks recovery health.

## Evidence and limits

Preserve configuration, thresholds, checks, request count, p50/p95/p99 where
available, errors, abort status, and recovery result. These tiny local runs prove
relative route/control behavior and safety logic—not DDoS capacity or production
mitigation effectiveness.

