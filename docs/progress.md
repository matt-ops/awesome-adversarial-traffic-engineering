# Progress

Follow modules in order. Copy this table into a private notes file and mark a
cell only when its linked section's artifact and pass gate are complete. The
repository does not need an account, plugin, or tracking framework.

| Module | Foundation | Applied | Integrated | Deep |
|---|---|---|---|---|
| 00 Method | [ ] [section](modules/00-method/index.md#foundation) | [ ] [section](modules/00-method/index.md#applied) | [ ] [section](modules/00-method/index.md#integrated) | [ ] [section](modules/00-method/index.md#deep) |
| 01 HTTP/edge | [ ] [section](modules/01-http-edge/index.md#foundation) | [ ] [section](modules/01-http-edge/index.md#applied) | [ ] [section](modules/01-http-edge/index.md#integrated) | [ ] [section](modules/01-http-edge/index.md#deep) |
| 02 Browser/JS | [ ] [section](modules/02-browser-javascript/index.md#foundation) | [ ] [section](modules/02-browser-javascript/index.md#applied) | [ ] [section](modules/02-browser-javascript/index.md#integrated) | [ ] [section](modules/02-browser-javascript/index.md#deep) |
| 03 Playwright | [ ] [section](modules/03-playwright/index.md#foundation) | [ ] [section](modules/03-playwright/index.md#applied) | [ ] [section](modules/03-playwright/index.md#integrated) | [ ] [section](modules/03-playwright/index.md#deep) |
| 04 Automated abuse | [ ] [section](modules/04-automated-abuse/index.md#foundation) | [ ] [section](modules/04-automated-abuse/index.md#applied) | [ ] [section](modules/04-automated-abuse/index.md#integrated) | [ ] [section](modules/04-automated-abuse/index.md#deep) |
| 05 Control recon | [ ] [section](modules/05-control-recon/index.md#foundation) | [ ] [section](modules/05-control-recon/index.md#applied) | [ ] [section](modules/05-control-recon/index.md#integrated) | [ ] [section](modules/05-control-recon/index.md#deep) |
| 06 Browser evasion | [ ] [section](modules/06-browser-evasion/index.md#foundation) | [ ] [section](modules/06-browser-evasion/index.md#applied) | [ ] [section](modules/06-browser-evasion/index.md#integrated) | [ ] [section](modules/06-browser-evasion/index.md#deep) |
| 07 Protocol identity foundations | [ ] [section](modules/07-protocol-identity/index.md#foundation) | [ ] [section](modules/07-protocol-identity/index.md#applied) | [ ] [section](modules/07-protocol-identity/index.md#integrated) | [ ] [section](modules/07-protocol-identity/index.md#deep) |
| 08 DDoS/resilience | [ ] [section](modules/08-ddos-resilience/index.md#foundation) | [ ] [section](modules/08-ddos-resilience/index.md#applied) | [ ] [section](modules/08-ddos-resilience/index.md#integrated) | [ ] [section](modules/08-ddos-resilience/index.md#deep) |
| 09 Tooling/review | [ ] [section](modules/09-tooling-code-review/index.md#foundation) | [ ] [section](modules/09-tooling-code-review/index.md#applied) | [ ] [section](modules/09-tooling-code-review/index.md#integrated) | [ ] [section](modules/09-tooling-code-review/index.md#deep) |
| 10 Findings/mock | [ ] [section](modules/10-findings-interview/index.md#foundation) | [ ] [section](modules/10-findings-interview/index.md#applied) | [ ] [section](modules/10-findings-interview/index.md#integrated) | [ ] [section](modules/10-findings-interview/index.md#deep) |

When a box remains open, write the exact missing lesson, source section, lab
action, expected output, and artifact repair. Do not substitute time spent or a
provider completion badge for the pass gate.

## Checkpoint progress

The checkpoint definitions are cumulative and validator-backed. Mark a row only
when every required lesson artifact and the checkpoint exit gate pass.

| Checkpoint | Depth ceiling | Direct targets | Closure lessons | From-zero time | Complete |
|---|---:|---:|---:|---:|---:|
| [24 focused hours](checkpoints/24-hours.md) | Foundation | 1 | 12 | 21.67 hours | [ ] |
| [7 days](checkpoints/7-days.md) | Applied | 3 | 18 | 37.25 hours | [ ] |
| [21 days](checkpoints/21-days.md) | Integrated | 6 | 31 | 71.25 hours | [ ] |
| [6 weeks](checkpoints/6-weeks.md) | Deep | 10 | 47 | 119.92 hours | [ ] |

Canonical direct membership, complete prerequisite closure, closure artifacts,
and both time calculations live in `curriculum/manifest.yaml` and are enforced
by `scripts/validate_curriculum.py`. Mark a checkpoint complete only after all
closure lessons and artifacts pass; direct-selection time alone is not enough.
