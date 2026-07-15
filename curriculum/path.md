# The canonical progressive path

This is the only canonical curriculum sequence. Choose an exit ramp, then move through every module at that depth in numerical order. Continue from the same path when ready; do not restart with a different schedule.

## How progression works

```text
Start
  -> Modules 0–8 Foundation
  -> Foundation gate / 24 focused hours
  -> Modules 0–8 Applied
  -> Applied gate / 7 days
  -> Modules 0–8 Integrated
  -> Integrated gate / 21 days
  -> Modules 0–8 Deep
  -> Deep gate / 6 weeks
```

The skill progression is recognize → explain → demonstrate → integrate → investigate independently → teach or defend. Each later level assumes the earlier level and adds evidence; it does not repeat the lesson.

## Cycle 1: Foundation

Complete the Foundation section of all nine modules. The listed time is focused work and totals exactly 24 hours.

| Order | Module section | Time | Primary artifact |
|---:|---|---:|---|
| 0 | [Safety and engagement — Foundation](modules/00-safety-and-engagement.md#level-1-foundation-24-hour-checkpoint) | 1.5 h | Safe engagement checklist |
| 1 | [Request path and network — Foundation](modules/01-request-path-and-network.md#level-1-foundation-24-hour-checkpoint) | 3 h | Request-path diagram |
| 2 | [Automated abuse — Foundation](modules/02-automated-abuse.md#level-1-foundation-24-hour-checkpoint) | 2 h | Six-row threat map |
| 3 | [Browser automation — Foundation](modules/03-browser-automation.md#level-1-foundation-24-hour-checkpoint) | 4 h | Local Playwright script |
| 4 | [Browser signals and detection — Foundation](modules/04-browser-signals-and-detection.md#level-1-foundation-24-hour-checkpoint) | 3 h | Browser-signal matrix |
| 5 | [Edge and DDoS — Foundation](modules/05-edge-and-ddos.md#level-1-foundation-24-hour-checkpoint) | 3 h | Safe Layer 7 plan |
| 6 | [Python and code review — Foundation](modules/06-python-and-code-review.md#level-1-foundation-24-hour-checkpoint) | 5 h | Log analysis and one review |
| 7 | [Experiment, analysis, reporting — Foundation](modules/07-experiment-analysis-reporting.md#level-1-foundation-24-hour-checkpoint) | 1.5 h | Synthetic finding |
| 8 | [Interview communication — Foundation](modules/08-interview-communication.md#level-1-foundation-24-hour-checkpoint) | 1 h | Practice answers |
|  | **Total** | **24 h** | |

Then use the [24-hour checkpoint view](checkpoints/24-hours.md) and pass the [Foundation gate](gates/foundation-gate.md).

## Cycle 2: Applied

Return to Module 0 and complete the Applied section of each module. You will independently demonstrate the core skills: a scoped plan, local traffic comparisons, browser events, layered detection, a bounded resilience run, practical tooling, a controlled experiment, and domain mocks.

0. [Safety and engagement — Applied](modules/00-safety-and-engagement.md#level-2-applied-7-day-checkpoint)
1. [Request path and network — Applied](modules/01-request-path-and-network.md#level-2-applied-7-day-checkpoint)
2. [Automated abuse — Applied](modules/02-automated-abuse.md#level-2-applied-7-day-checkpoint)
3. [Browser automation — Applied](modules/03-browser-automation.md#level-2-applied-7-day-checkpoint)
4. [Browser signals and detection — Applied](modules/04-browser-signals-and-detection.md#level-2-applied-7-day-checkpoint)
5. [Edge and DDoS — Applied](modules/05-edge-and-ddos.md#level-2-applied-7-day-checkpoint)
6. [Python and code review — Applied](modules/06-python-and-code-review.md#level-2-applied-7-day-checkpoint)
7. [Experiment, analysis, reporting — Applied](modules/07-experiment-analysis-reporting.md#level-2-applied-7-day-checkpoint)
8. [Interview communication — Applied](modules/08-interview-communication.md#level-2-applied-7-day-checkpoint)

Then use the [7-day checkpoint view](checkpoints/7-days.md) and pass the [Applied gate](gates/applied-gate.md).

## Cycle 3: Integrated

Complete every Integrated section, using the Adversarial Traffic Lab as one connected engagement. Integrate threat model → experiment → telemetry → detection → service impact → finding → remediation → retest.

0. [Safety and engagement — Integrated](modules/00-safety-and-engagement.md#level-3-integrated-21-day-checkpoint)
1. [Request path and network — Integrated](modules/01-request-path-and-network.md#level-3-integrated-21-day-checkpoint)
2. [Automated abuse — Integrated](modules/02-automated-abuse.md#level-3-integrated-21-day-checkpoint)
3. [Browser automation — Integrated](modules/03-browser-automation.md#level-3-integrated-21-day-checkpoint)
4. [Browser signals and detection — Integrated](modules/04-browser-signals-and-detection.md#level-3-integrated-21-day-checkpoint)
5. [Edge and DDoS — Integrated](modules/05-edge-and-ddos.md#level-3-integrated-21-day-checkpoint)
6. [Python and code review — Integrated](modules/06-python-and-code-review.md#level-3-integrated-21-day-checkpoint)
7. [Experiment, analysis, reporting — Integrated](modules/07-experiment-analysis-reporting.md#level-3-integrated-21-day-checkpoint)
8. [Interview communication — Integrated](modules/08-interview-communication.md#level-3-integrated-21-day-checkpoint)

Then use the [21-day checkpoint view](checkpoints/21-days.md) and pass the [Integrated gate](gates/integrated-gate.md).

## Cycle 4: Deep

Complete every Deep section around one original, safe research question. Compare alternatives, make limitations explicit, improve the capstone, teach the result, and propose production validation without claiming the local result transfers directly.

0. [Safety and engagement — Deep](modules/00-safety-and-engagement.md#level-4-deep-6-week-checkpoint)
1. [Request path and network — Deep](modules/01-request-path-and-network.md#level-4-deep-6-week-checkpoint)
2. [Automated abuse — Deep](modules/02-automated-abuse.md#level-4-deep-6-week-checkpoint)
3. [Browser automation — Deep](modules/03-browser-automation.md#level-4-deep-6-week-checkpoint)
4. [Browser signals and detection — Deep](modules/04-browser-signals-and-detection.md#level-4-deep-6-week-checkpoint)
5. [Edge and DDoS — Deep](modules/05-edge-and-ddos.md#level-4-deep-6-week-checkpoint)
6. [Python and code review — Deep](modules/06-python-and-code-review.md#level-4-deep-6-week-checkpoint)
7. [Experiment, analysis, reporting — Deep](modules/07-experiment-analysis-reporting.md#level-4-deep-6-week-checkpoint)
8. [Interview communication — Deep](modules/08-interview-communication.md#level-4-deep-6-week-checkpoint)

Then use the [6-week checkpoint view](checkpoints/6-weeks.md) and pass the [Deep gate](gates/deep-gate.md).

## Track evidence, not elapsed time

Update [`progress.yaml`](progress.yaml) only after a module completion test passes and the artifact exists. Run `python scripts/progress.py` from the repository root for the current checkpoint, missing evidence, next three tasks, and gate status. The report is not a hiring prediction.

