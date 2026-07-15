# AATE implementation plan

## Authoritative decisions

- `01-AATE-CODEX-MASTER-PROMPT-FINAL.md` defines the product and safety scope.
- `codex-addendum-single-progressive-path.md` is authoritative for curriculum architecture.
- The repository has one learning path, nine canonical modules, and four cumulative exit ramps.
- The depth names are Foundation, Applied, Integrated, and Deep.
- “24 hours” means approximately 24 cumulative focused study hours.
- Checkpoint pages are completion views; lesson content lives only in module pages.

## Milestones

1. Establish project, safety, documentation, and validation foundations.
2. Build the canonical path, nine modules, four checkpoint views, and four readiness gates.
3. Label the resource catalog by depth, priority, module, and source type.
4. Map the safe local lab and interview system directly to module outcomes.
5. Implement module-and-level progress tracking with a human-readable report.
6. Validate curriculum structure, internal links, safety language, and the 24-hour budget.
7. Expand the runnable lab, exercises, concept guides, and interview assets without changing the path.

## Dependencies and risks

- The host currently has Node.js and Docker, but no directly invokable Python or Make command. Python checks may run through a bundled runtime or a container.
- External-link availability is not required for structural validation; provided primary-source URLs are preserved.
- The prior `codex-master-prompt-awesome-adversarial-traffic-engineering-v2-progressive-path.md` conflicts with the addendum on module count, depth naming, and the meaning of the first checkpoint. It remains source material only.

## Curriculum acceptance criteria

- Exactly nine canonical module pages exist.
- Every module contains Foundation, Applied, Integrated, and Deep sections with outcomes, artifact, completion test, time, and resources.
- `curriculum/path.md` is the only canonical sequence.
- Four checkpoint pages link to module sections and do not repeat lesson content.
- Foundation time totals 24 focused hours and contains only minimum role skills.
- Every resource entry has one depth label and one priority label.
- Lab and interview work map to module-level outcomes.
- Progress is recorded per module on the integer scale 0–4 and reports all four gates.
- README and documentation navigation lead with “Start the Path,” not a course chooser.

## Validation strategy

- Run the curriculum contract validator.
- Run progress-reporter unit tests and a sample report.
- Audit links and prohibited legacy curriculum terms in implementation files.
- Validate the documentation configuration.
- Record results and limitations in `STATUS.md`.

