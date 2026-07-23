# Source ledger

The machine-readable source of truth is `sources/sources.yaml` in the repository.
It currently contains 60 unique entries with:

- source type and publisher;
- version/access information, human content-review date, and automated
  link-check date;
- exact assigned sections;
- supported claims;
- limitations; and
- module mapping.

Every lesson exposes the relevant subset in its **Source basis** table. Source
types and review policy are described in the repository's
`sources/README.md`.

`python scripts/validate_sources.py` treats this ledger as the single source of
truth for each visible table's source type and URL. It also verifies that every
**Direct link** belongs to a declared source ID and blocks known-obsolete FIRST
and STIX references.

## Pinned traffic-intelligence sources

- `first-cti-source-evaluation` — `OFFICIAL_DOCUMENTATION` —
  [Source Evaluation and Information Reliability](https://www.first.org/global/sigs/cti/curriculum/source-evaluation) —
  Source reliability A-F and Information reliability 1-6. The course uses
  “information credibility” only when explicitly identifying it as an
  equivalent analyst term.
- `oasis-stix-21` — `STANDARD` —
  [STIX Version 2.1 Errata 01](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html) —
  3.2 Common Properties, specifically the confidence property; 4.7 Indicator;
  4.14 Observed Data; 5.1 Relationship; 5.2 Sighting; and Appendix A:
  Confidence Scales.

## Required spine

The path is anchored in NIST SP 800-115, MITRE adversary-emulation guidance,
versioned OWASP WSTG pages, MDN and Chrome documentation, Microsoft Learn and
Playwright documentation, OWASP Automated Threats, provider-assigned PortSwigger
labs, inspectable browser-control projects, named research papers, IETF RFCs,
bounded-load documentation, official Python material, and reporting/interview
guidance.

Vendor, project, preprint, version-sensitive, lab-specific, and course-synthesis
sources are visibly labeled so the learner can constrain the claim.
