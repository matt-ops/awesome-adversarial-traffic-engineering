# Edge security and resilience

- [AWS Builders’ Library](https://aws.amazon.com/builders-library/) — `[L2 Applied]` `[Recommended]` · Modules 1 and 5 · Vendor-specific engineering essays. Distributed-system operational patterns. It matters for connecting traffic controls to service behavior.
- [Using load shedding to avoid overload](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) — `[L2 Applied]` `[Required]` · Module 5 · Vendor-specific primary engineering reference. Explains shedding work before collapse. It matters for interpreting bounded expensive-endpoint experiments.
- [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — `[L3 Integrated]` `[Required]` · Modules 5–6 · Vendor-specific primary engineering reference. Connects client behavior to outage amplification. It matters for safe-client and resilience design.
- [AWS WAF rate-based rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html) — `[L2 Applied]` `[Recommended]` · Module 5 · Vendor-specific official documentation. Shows concrete rate-based control semantics and limitations. It matters for comparing per-key limits with workflow-aware controls.
- [Prometheus documentation](https://prometheus.io/docs/) — `[L3 Integrated]` `[Optional]` · Modules 5 and 7 · Official documentation. Metrics collection and query model. It matters when the capstone adds time-series service evidence.
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) — `[L3 Integrated]` `[Optional]` · Modules 1 and 7 · Official documentation. Telemetry and correlation standards. It matters for tracing evidence across local components.

