# DDoS and safe traffic testing

- [CISA understanding denial-of-service attacks](https://www.cisa.gov/news-events/news/understanding-denial-service-attacks) — `[L1 Foundation]` `[Required]` · Module 5 · Government guidance. Provides a high-level DoS/DDoS model. It matters for minimum vocabulary without introducing attack tooling.
- [Cloudflare DDoS Learning Center](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) — `[L1 Foundation]` `[Recommended]` · Module 5 · Vendor-specific secondary reference. A readable attack-category overview. It matters as reinforcement, not as a complete architecture model.
- [Grafana k6 documentation](https://grafana.com/docs/k6/latest/) — `[L2 Applied]` `[Required]` · Module 5 · Official documentation. Local load scripting, thresholds, and metrics. It matters for bounded application-layer experiments.
- [Locust documentation](https://docs.locust.io/) — `[L2 Applied]` `[Optional]` · Modules 5–6 · Official documentation. Python-based load generation. It matters as an alternative when a research question benefits from Python workflows; do not run both by default.
- [AWS DDoS resiliency whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/welcome.html) — `[L3 Integrated]` `[Required]` · Module 5 · Vendor-specific architecture guidance. Maps protection patterns across layers. It matters for system-design tradeoffs, not for copying vendor configuration into the local lab.
- [AWS Shield documentation](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html) — `[L3 Integrated]` `[Recommended]` · Module 5 · Vendor-specific official documentation. Describes managed DDoS concepts. It matters for comparing local controls with production service capabilities.

