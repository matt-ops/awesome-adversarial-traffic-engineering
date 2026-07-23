# The canonical path

There is one sequence. A later lesson may assume the knowledge and guided
exercise behavior taught by every prerequisite lesson.

`curriculum/manifest.yaml` is the authoritative machine-readable record for
lesson IDs, depth, estimates, prerequisites, source IDs, module
indexes, optional appendix metadata, and checkpoint membership. Visible lesson
progress boxes and checkpoint pages are validated against it.

| Order | Module | Offensive outcome |
|---:|---|---|
| 01 | [HTTP and the edge](modules/01-http-edge/index.md) | Trace and map the complete request/control/resource path |
| 02 | [Browser and JavaScript](modules/02-browser-javascript/index.md) | Explain the runtime that collects and exposes browser signals |
| 03 | [Playwright](modules/03-playwright/index.md) | Build and instrument a representative automated browser |
| 04 | [Automated abuse](modules/04-automated-abuse/index.md) | Reproduce credential, rate, challenge-proof, inventory, promotion, and race abuse with protected-action evidence |
| 05 | [Control reconnaissance](modules/05-control-recon/index.md) | Map relied-upon signals, establish a blocked baseline, and evaluate classifier thresholds and adversarial drift |
| 06 | [Browser evasion](modules/06-browser-evasion/index.md) | Test controlled changes, coherence, replay, and version drift |
| 07 | [Protocol identity foundations](modules/07-protocol-identity/index.md) | Capture real available local clients and use source-led models for browser/protocol coherence |
| 08 | [DDoS and resilience](modules/08-ddos-resilience/index.md) | Test resource assumptions with bounded load and translate evidence into an authorized pre-production plan |
| 09 | [Tooling and code review](modules/09-tooling-code-review/index.md) | Build safe attack tooling and find exploitable implementation flaws |
| 10 | [Findings and interview](modules/10-findings-interview/index.md) | Turn evidence into remediation, retest, briefing, and role narrative |

The core technical path starts with HTTP and the edge. Modules 01 through 10
keep their existing numbers.

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
| [24 focused hours](checkpoints/24-hours.md) | Foundation | 2 / 285 minutes | 11 | 1,250 minutes / 20.83 hours |
| [7 days](checkpoints/7-days.md) | Applied | 5 / 885 minutes | 16 | 2,210 minutes / 36.83 hours |
| [21 days](checkpoints/21-days.md) | Integrated | 9 / 1,485 minutes | 30 | 4,430 minutes / 73.83 hours |
| [6 weeks](checkpoints/6-weeks.md) | Deep | 13 / 2,505 minutes | 47 | 7,650 minutes / 127.50 hours |

The closure total, not the direct-selection total, is the checkpoint time for a
learner starting at the course entry point. Each closure contains every
recursive prerequisite lesson exactly once.

## Optional appendix

| Appendix | Best time to use it |
|---|---|
| [Red-team method and engagement practice](modules/00-method/index.md) | Before an interview, provider-hosted assessment, organization-owned engagement, or capstone |
| [Traffic and Bot Threat Intelligence](appendices/traffic-bot-threat-intelligence/index.md) | Before intelligence-informed emulation, regression planning, or interview discussion |

Appendix pages are not included in prerequisite closure or checkpoint time.

Experienced practitioners can use the [Experienced Practitioner Fast
Track](experienced-practitioner-fast-track.md) as a diagnostic router. It is not
canonical lesson metadata and does not alter any prerequisite or checkpoint.
