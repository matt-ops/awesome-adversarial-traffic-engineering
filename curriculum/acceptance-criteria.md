# Curriculum architecture acceptance criteria

This contract implements the authoritative addendum and supersedes conflicting older curriculum layouts.

## Structure

- [x] `curriculum/path.md` is the only canonical sequence.
- [x] Exactly nine canonical module pages exist, numbered 00 through 08.
- [x] Every module has Foundation, Applied, Integrated, and Deep sections.
- [x] Every level states knowledge, hands-on, interview, artifact, completion test, estimated time, required resources, and optional deeper resources.
- [x] Four checkpoint pages act only as section/artifact/gate views.
- [x] Four gates test explain, build or run, measure, communicate, and operate safely.

## Progression

- [x] Foundation work totals approximately 24 cumulative focused hours; the canonical budget totals exactly 24.
- [x] Foundation includes only minimum skills needed to understand, discuss, and demonstrate the role.
- [x] Applied continues the same modules and independently demonstrates each core skill.
- [x] Integrated combines all modules into an end-to-end engagement.
- [x] Deep adds original research, comparison, teaching, and production-validation planning.
- [x] Chromium source, deep JavaScript analysis, HTTP/3/QUIC internals, statistical modeling, advanced evasion, and agent frameworks do not block Foundation.

## Cross-repository consistency

- [x] README exposes one prominent `Start the Path` link and four exit ramps.
- [x] Documentation navigation uses singular “Learning path” and nests checkpoints under it.
- [x] Every catalog resource has one level and one priority label.
- [x] Lab work maps to module-level outcomes rather than a separate schedule.
- [x] Interview work references artifacts from Modules 0–7.
- [x] Progress uses levels 0–4 per module and reports missing artifacts and all gates.
- [x] No implementation page calls the exits separate courses or uses “Practitioner” as Level 4.

## Automated evidence

Run:

```bash
python scripts/validate_curriculum.py
python scripts/progress.py --check
python -m unittest discover -s tests -v
```

The validator checks the module count and headings, checkpoint links, Foundation budget, resource labels, progress schema, README entry point, and lab mapping. Human review remains required for lesson quality and the purity of Foundation scope.
