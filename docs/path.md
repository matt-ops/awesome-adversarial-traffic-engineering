# The canonical path

There is one sequence. A later lesson may assume the knowledge and guided
exercise behavior taught by every prerequisite lesson.

`curriculum/manifest.yaml` is the authoritative machine-readable record for
lesson IDs, depth, estimates, prerequisites, source IDs, module
indexes, and checkpoint membership. Visible lesson progress boxes and the
checkpoint pages are validated against it.

| Order | Module | Offensive outcome |
|---:|---|---|
| 00 | [Method and authorization](modules/00-method/index.md) | Design a legal, falsifiable, evidence-producing engagement |
| 01 | [HTTP and the edge](modules/01-http-edge/index.md) | Trace and map the complete request/control/resource path |
| 02 | [Browser and JavaScript](modules/02-browser-javascript/index.md) | Explain the runtime that collects and exposes browser signals |
| 03 | [Playwright](modules/03-playwright/index.md) | Build and instrument a representative automated browser |
| 04 | [Automated abuse](modules/04-automated-abuse/index.md) | Reproduce credential, inventory, promotion, race, and rate abuse |
| 05 | [Control reconnaissance](modules/05-control-recon/index.md) | Map candidate relied-upon signals and establish a blocked baseline |
| 06 | [Browser evasion](modules/06-browser-evasion/index.md) | Test controlled changes, coherence, replay, and version drift |
| 07 | [Protocol identity foundations](modules/07-protocol-identity/index.md) | Generate Python/OpenSSL fixtures and use source-led models for browser/protocol coherence |
| 08 | [DDoS and resilience](modules/08-ddos-resilience/index.md) | Test resource assumptions with bounded, abortable load |
| 09 | [Tooling and code review](modules/09-tooling-code-review/index.md) | Build safe attack tooling and find exploitable implementation flaws |
| 10 | [Findings and interview](modules/10-findings-interview/index.md) | Turn evidence into remediation, retest, briefing, and role narrative |

## Depth in every module

Each module index identifies four cumulative depths:

- **Foundation:** terminology, source instruction, worked example, and first guided exercise
- **Applied:** a guided tool or provider-assigned exercise
- **Integrated:** a chained attack that uses earlier knowledge and exercise behavior
- **Deep:** version, scale, false-positive, research, or remediation extension

You do not choose a separate course. Follow the Next link, and use checkpoint
pages only when you want to assess whether you can pause with an honest claim.

## Validated cumulative checkpoints

| Checkpoint | Depth ceiling | Direct targets/time | Closure lessons | From-zero closure time |
|---|---:|---:|---:|---:|
| [24 focused hours](checkpoints/24-hours.md) | Foundation | 1 / 180 minutes | 12 | 1,300 minutes / 21.67 hours |
| [7 days](checkpoints/7-days.md) | Applied | 3 / 540 minutes | 18 | 2,235 minutes / 37.25 hours |
| [21 days](checkpoints/21-days.md) | Integrated | 6 / 960 minutes | 31 | 4,275 minutes / 71.25 hours |
| [6 weeks](checkpoints/6-weeks.md) | Deep | 10 / 1,800 minutes | 47 | 7,195 minutes / 119.92 hours |

The closure total, not the direct-selection total, is the checkpoint time for a
learner starting at the course entry point. Each closure contains every
recursive prerequisite lesson exactly once.
