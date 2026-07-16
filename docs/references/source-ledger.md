# Source ledger

The machine-readable source of truth is `sources/sources.yaml` in the repository.
It currently contains 48 unique entries with:

- source type and publisher;
- publication/update and verification dates;
- exact assigned sections;
- supported claims;
- limitations; and
- module mapping.

Every lesson exposes the relevant subset in its **Source basis** table. Source
types and verification policy are described in the repository's
`sources/README.md`.

## Required spine

The path is anchored in NIST SP 800-115, MITRE adversary-emulation guidance,
versioned OWASP WSTG pages, MDN and Chrome documentation, Microsoft Learn and
Playwright documentation, OWASP Automated Threats, provider-assigned PortSwigger
labs, inspectable browser-control projects, named research papers, IETF RFCs,
bounded-load documentation, official Python material, and reporting/interview
guidance.

Vendor, project, preprint, version-sensitive, lab-specific, and course-synthesis
sources are visibly labeled so the learner can constrain the claim.
