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
- Hypothesis: named per selected route-cost, cache, identity-key, endpoint-cost, workflow-sequence, retry, or recovery observation
- Changed variable: exactly the selected scenario's paired condition
- Fixed variables: target, duration, rate, VUs, reset, thresholds, probes, and evidence schema
- Success: scenario-specific assertions pass, thresholds do not abort, and teardown health returns `200` within 1,000 ms
- Evidence: configuration, check/metric output, threshold status, request total, and recovery probe
- Limitations: tiny single-host L7 fixture; not capacity, L3/L4, or production mitigation evidence
- Cleanup: stop k6, reset synthetic state, and stop the local stack
- Remediation: map cache/admission/key/retry/dependency changes to the observed resource
- Retest: repeat identical configuration and legitimate-health criteria after the change

## Dry run first

### PowerShell

```powershell
$env:AATE_DRY_RUN = "1"
k6 run lab/load/bounded.js
```

### Bash or zsh

```bash
AATE_DRY_RUN=1 k6 run lab/load/bounded.js
```

Expected network totals are zero and the console prints target, scenario,
duration, rate, and maximum VUs.

## Assigned scenarios

Remove the dry-run variable, use conservative values, and set one scenario:

### PowerShell

```powershell
Remove-Item Env:AATE_DRY_RUN -ErrorAction SilentlyContinue
$env:AATE_DURATION = "5"
$env:AATE_RATE = "2"
$env:AATE_MAX_VUS = "3"
$env:AATE_SCENARIO = "cheap-expensive"
k6 run lab/load/bounded.js
```

### Bash or zsh

```bash
unset AATE_DRY_RUN
AATE_DURATION=5 AATE_RATE=2 AATE_MAX_VUS=3 \
  AATE_SCENARIO=cheap-expensive k6 run lab/load/bounded.js
```

The seven assigned values are `cheap-expensive`, `cache-bypass`, `identity-key`,
`endpoint-cost-observation`, `workflow-sequence-observation`,
`retry-amplification`, and `recovery`. Execute only the scenario assigned by the
current lesson. Setup resets synthetic state, primes the cache or fixed identity
counter only when its scenario requires that deterministic baseline, and
teardown checks immediate recovery health.

Stateful per-iteration values use k6's test-wide
`exec.scenario.iterationInTest`. The older `__ITER` counter is unsafe for these
keys because it starts at zero independently for every VU, so multiple VUs can
reuse the same rotated session, cache, or retry-operation identity. Prefixing
the scenario iteration ID keeps each purpose distinct while preserving
deterministic evidence.

| Scenario | Runtime observation | Deterministic assertion | Course interpretation |
|---|---|---|---|
| `cheap-expensive` | `/health` latency versus bounded report latency | report body confirms `work=100`; report request takes longer in the local pair | route cost can differ at equal request count; no mitigation is compared |
| `cache-bypass` | warmed fixed key versus bypassed unique key | `cache_hit` is true/false respectively and result digests match | the application cache changes work; this is not CDN or production-cache evidence |
| `identity-key` | fixed caller key after two setup calls versus a rotated key | fixed key receives `429`; rotated key receives `200` with count 1 | the real synthetic per-session quota trusts caller-controlled input; Nginx's per-IP limit is not the treatment |
| `endpoint-cost-observation` | `work=1` versus `work=100` on the same endpoint | response bodies preserve both work values; higher work takes longer locally | an input changes bounded endpoint cost; no endpoint-specific admission control exists |
| `workflow-sequence-observation` | search followed by product detail | search contains `demo-1`; detail resolves the same ID | the sequence is observable; no workflow-aware quota or mitigation exists |
| `retry-amplification` | one operation requested twice | first response is `503`; the one retry is accepted as attempt 2 | one bounded retry doubles requests for this fixture; no general retry policy is proved |
| `recovery` | bounded report work followed by teardown health | work is 50; health returns `200` within 1,000 ms | immediate toy-app health only, not sustained queue/dependency recovery |

The edge always has one global per-IP Nginx rate limit. None of these scenario
names claims to compare that configuration before and after, and the two
observation-only scenarios are not mitigation tests.

## Evidence and limits

Preserve configuration, thresholds, named assertions, request count, p50/p95/p99
where available, errors, abort status, and recovery result. Keep runtime timing,
deterministic fixture assertions, and course interpretation in separate columns.
Most two-request scenarios use six requests in the one-second initial envelope;
cache priming raises that scenario to seven and fixed-key seeding raises it to
eight. The recovery scenario uses four. These tiny local runs prove only the
listed synthetic behavior and safety logic—not DDoS capacity or production
mitigation effectiveness.
