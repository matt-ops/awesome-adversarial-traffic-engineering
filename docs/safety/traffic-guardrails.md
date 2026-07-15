# Traffic guardrails

The repository hard-caps educational application-layer traffic:

| Dimension | Maximum |
|---|---:|
| Duration | 15 seconds |
| Concurrency | 5 |
| Request rate | 10 requests/second |
| Total requests | 100 |
| Expensive requests | 20 |

Lessons normally use less. Every load exercise must also name a health signal,
threshold, abort condition, dry-run display, recovery observation, and cleanup.
The ceilings are defense in depth, not a claim that any particular rate is safe
for an arbitrary target.
