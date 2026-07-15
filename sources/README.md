# Source policy

The course is source-first: an authoritative standard, official documentation,
research paper, or mature training range teaches the underlying concept. AATE
then supplies the offensive bridge, guided exercise, artifact, and pass gate.

## Labels

- `STANDARD` — formal standards and recognized testing frameworks
- `OFFICIAL_DOCUMENTATION` — documentation maintained by the platform or tool
- `PEER_REVIEWED_RESEARCH` — published peer-reviewed research
- `PREPRINT_RESEARCH` — research not treated as peer-reviewed authority
- `PROJECT_DOCUMENTATION` — documentation maintained by an open-source or
  training project
- `VENDOR_RESEARCH` — vendor educational or research material
- `COURSE_SYNTHESIS` — an AATE method assembled from multiple sources
- `LAB_SPECIFIC` — behavior that exists only in the bundled synthetic lab
- `VERSION_SENSITIVE` — an observation whose meaning depends on exact versions
- `PRACTITIONER_PERSPECTIVE` — experience-based guidance, not a standard
- `UNVERIFIED` — a source or assignment that could not be confirmed

Community posts and discussion threads can suggest questions. They cannot be the
sole authority for a core fact. `UNVERIFIED` sources cannot be required at
Foundation depth.

## Lesson contract

Every lesson begins with a source-basis table and a machine-readable
`source-ids` comment. The assignment identifies exact sections, what to skip,
time, expected takeaway, bridge exercise, artifact, and pass gate. A factual
claim uses a nearby footnote or source callout. AATE-specific reasoning is
visibly labeled **COURSE_SYNTHESIS**.

## Verification

`last_verified` means that the URL and title were checked on that date. It does
not mean every future version will preserve the same headings or behavior.
Version-sensitive projects require the learner to record the commit, package,
browser, and framework versions used in the experiment.

Run:

```text
python scripts/validate_sources.py
```

The validator checks schema, source IDs, lesson citations, synthesis labels,
duplicate IDs, and Foundation use of unverified material.
