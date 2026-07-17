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

For the Python `safe_client`, duration is a real monotonic wall-clock deadline.
Before each request, the client calculates the remaining budget and refuses to
start when no time remains. Its per-request timeout is at most two seconds and
is reduced to the remaining duration when that is smaller. If a request consumes
the deadline, the result records `duration_budget_exceeded` and the run stops.
Direct calls to `fetch_once()` reject non-finite, non-positive, Boolean, and
greater-than-two-second timeout values.

Rate, total-request, and expensive-request ceilings remain independent of the
deadline. Retry exercises retain their separate maximum of three attempts and
two seconds per attempt. The client rejects every redirect, so a 3xx response
cannot move a bounded run to a new hostname, IP, port, or scheme.
