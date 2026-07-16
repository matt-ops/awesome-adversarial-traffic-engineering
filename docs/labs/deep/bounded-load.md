# Bounded application-layer load lab

All traffic is fixed to the local synthetic API. The script rejects non-loopback
targets, unassigned scenarios, duration over 15 seconds, more than 5 VUs, an
effective rate over 10 requests/second, and a worst-case total over 100 requests
including setup/teardown. Threshold failure aborts the test. There is no L3/L4
traffic generation.

## Lab contract

- Authorization boundary: repository-owned fixed loopback API only
- Target: `http://localhost:8080`
- Adversary objective: challenge one application-resource/control assumption within hard ceilings
- Protected action: service health and scenario-specific work named in Module 08
- Baseline: reset state, healthy probe, and scenario configuration
- Hypothesis: named per selected cheap/expensive, cache, identity, endpoint, workflow, retry, or recovery comparison
- Changed variable: exactly the selected scenario's paired condition
- Fixed variables: target, duration, rate, VUs, reset, thresholds, probes, and evidence schema
- Success: scenario checks pass, thresholds do not abort, and teardown health returns `200`
- Evidence: configuration, check/metric output, threshold status, request total, and recovery probe
- Limitations: tiny single-host L7 fixture; not capacity, L3/L4, or production mitigation evidence
- Cleanup: stop k6, reset synthetic state, and stop the local stack
- Remediation: map cache/admission/key/retry/dependency changes to the observed resource
- Retest: repeat identical configuration and legitimate-health criteria after the change

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
