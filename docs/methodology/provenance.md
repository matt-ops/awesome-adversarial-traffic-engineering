# Method provenance

The AATE adversarial-control loop is a **course synthesis**, not a verbatim NIST,
MITRE, or OWASP method.

| Provenance class | Contribution |
|---|---|
| NIST SP 800-115 | Planning, Rules of Engagement, discovery, attack, reporting, analysis, mitigation, and follow-up |
| MITRE adversary emulation | Behavior-focused objectives and chained operator actions |
| OWASP WSTG | Entry-point, request/response, parameter, state, intermediary, and architecture mapping |
| Controlled experiments | Reference conditions, predictions, controlled changes, repeated measurement, and alternative explanations |
| AATE specialization | Protected-action proof, relied-upon-signal analysis, coherent identity, resource-path mapping, residual anomalies, and exact adversarial retest |

The complete step-by-step mapping is maintained in the repository source record,
and the learner-facing sequence is explained in [the adversarial-control
loop](adversarial-control-loop.md).

## Citation rule

When a lesson states what a standard or project says, it cites that source
nearby. When it joins ideas into a role-specific procedure, it labels the
paragraph or callout **COURSE_SYNTHESIS**. Lab behavior is separately labeled
**LAB_SPECIFIC**, and observations that can drift with versions are labeled
**VERSION_SENSITIVE**.
