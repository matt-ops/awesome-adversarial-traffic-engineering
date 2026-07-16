# Local lab

Do not start by learning this directory. Start with the course's [first
lesson](../docs/modules/00-method/01-red-team-role.md); each lesson introduces
one command only after its prerequisites and explains output, interpretation,
failure modes, and cleanup.

The progression is deliberately simple:

1. Static loopback page with no Docker
2. Headed Playwright workflow
3. Synthetic API/edge after the foundations
4. Workflow and control attacks
5. Protocol, bounded resilience, and Python tooling
6. Findings and exact retest

Every executable target is fixed to loopback or an internal Compose name.
Repeated-traffic tools enforce hard ceilings. The application is deliberately
small and vulnerable; no result generalizes to an external service.

Use [LAB_COURSE_MAP.md](LAB_COURSE_MAP.md) as the complete command-to-lesson
index. Use [the learner lab guide](../docs/labs/index.md) for normal navigation.

To validate the repository after making changes:

```text
make validate
```

On Windows without `make`, execute the validation commands listed in the map's
final table.
