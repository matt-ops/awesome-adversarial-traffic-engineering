# Local lab guide

The course uses only synthetic loopback targets or explicitly assigned training
providers. The first target is a static application and requires no Docker.

Commands use portable executable names such as `python`, `npm`, `npx`,
`docker`, and `k6`. When a command sets environment variables, lab pages show
separate PowerShell and Bash/zsh examples; use the block for your shell.

- [Foundation static site](foundation/static-site.md)
- [First Playwright workflow](foundation/first-playwright.md)
- [Integrated local API](applied/local-api.md)
- [Challenge systems and protected-action enforcement](applied/challenge-systems.md)
- [Workflow authorization](applied/workflow-authorization.md)
- [Python tooling](applied/python-tooling.md)
- [Control reconnaissance and one-variable experiment](integrated/control-recon.md)
- [Protocol identity](integrated/protocol-identity.md)
- [Bounded application-layer load](deep/bounded-load.md)
- [Synthetic code review](deep/code-review.md)
- [Finding, briefing, and mock](deep/finding-briefing.md)

Every later lab page states authorization boundary, target, objective, protected
action, baseline, hypothesis, variables, success, evidence, limitations,
cleanup, remediation, and retest.

The maintenance-level command index is `lab/LAB_COURSE_MAP.md` in the repository.
