# Lab-to-module mapping

The Adversarial Traffic Lab is evidence infrastructure for the canonical modules. It is not a separate lab course. A component may support several outcomes, but each exercise records a primary module and depth.

| Module | Foundation evidence | Applied evidence | Integrated evidence | Deep extension |
|---:|---|---|---|---|
| 0 Safety | Target validator dry run and checklist | Engagement plan with caps and aborts | Capstone runbook and decision log | Staged production-validation proposal |
| 1 Request path | Local request-path diagram and `/health` trace | Client/protocol comparison | Cross-layer telemetry correlation | HTTP/2, HTTP/3, QUIC, or middlebox study |
| 2 Abuse | Six-row synthetic workflow threat map | Ten workflows with state/distribution | Multi-stage account, inventory, and promotion case | Original adaptive-abuse hypothesis |
| 3 Browser automation | Basic local Playwright navigation | Context, storage, frame, worker, and CDP capture | Four populations plus rule-based agent | Runtime instrumentation or browser-source question |
| 4 Signals and detection | Signal-family matrix and fixture score | Manual/headed/headless comparison | Layered detector, ablation, per-population metrics | Drift, privacy, accessibility, and rule-overlap study |
| 5 Edge and DDoS | Bounded test plan and metric explanation | Cheap/expensive endpoint run | Naive versus workflow-aware mitigation and recovery | Backpressure, queue, shielding, or protocol-pressure extension |
| 6 Python/review | JSONL analyzer and one code review | Async client, three drills, four reviews | Six drills and all ten reviews integrated into tooling | Reusable streaming CLI with performance analysis |
| 7 Experiment/reporting | One synthetic finding | Controlled experiment and chart/table | Full report, executive summary, remediation, retest | Reproducible portfolio paper and calibrated conclusions |
| 8 Communication | Narrative and architecture explanation | Two domain mocks | Full five-session mock loop | Teach a module, two more loops, 90-day proposal |

## Current vertical slice

The initial runnable slice provides:

- a FastAPI synthetic application with `/health`, `/api/search`, `/api/reports/expensive`, and `/telemetry/events`;
- a local-target validator shared by the client and safety tests;
- a bounded Python client;
- deterministic JSONL fixtures;
- an explainable educational detector and metric report.

These components support Foundation outcomes in Modules 0, 1, 2, 5, 6, and 7. Browser evidence for Modules 3 and 4 is documented as the next vertical expansion; interview evidence is maintained under `interview/`.

## Mapping rule for additions

Every new lab walkthrough must declare:

- primary module and level;
- prerequisite module sections;
- expected artifact and completion test;
- target restrictions, hard caps, abort conditions, and cleanup;
- production differences and false-positive or ambiguity concerns.

