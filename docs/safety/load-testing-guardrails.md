# Load-testing guardrails

All AATE load is local, synthetic, and conservative. Safe design uses defense in depth:

- allowlist target validation before resolution or connection;
- no command-line remote-target override;
- hard-coded ceilings for duration, virtual users, concurrency, requests per second, and total requests;
- a configuration-print or dry-run mode;
- thresholds and automatic abort conditions;
- service-health monitoring and a named stop authority;
- cleanup and recovery validation;
- tests for every rejection and allowed local name.

Rate alone is not a safety measure. Estimate endpoint cost, cache behavior, state changes, dependency calls, retries, queue occupancy, and recovery time. Begin with a baseline and the smallest traffic that can answer the question.

