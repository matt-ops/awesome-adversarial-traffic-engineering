# Methodology provenance

> The complete AATE loop is a course synthesis. It is not quoted verbatim from
> a single industry standard.

The loop combines four kinds of support. [NIST SP
800-115](https://csrc.nist.gov/pubs/sp/800/115/final) directly supports
assessment planning, Rules of Engagement, penetration-test phases, analysis,
reporting, mitigation, and follow-up. [MITRE Adversary Emulation
Plans](https://attack.mitre.org/resources/adversary-emulation-plans/) directly
supports behavior-focused emulation and chained operator actions. [OWASP WSTG
v4.2 entry-point
mapping](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/06-Identify_Application_Entry_Points)
and [architecture
mapping](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture)
directly support mapping requests, parameters, state, components, and trust
boundaries. Baselines, controlled changes, falsifiability, repeated measurement,
and alternative explanations are controlled-experiment principles. The
protected-action, trusted-signal, coherent-identity, residual-anomaly, and exact
retest rules are AATE specializations.

## Step-by-step provenance map

| Step | Classification | Direct support and boundary | AATE use |
|---:|---|---|---|
| 1. Authorize and define scope. | Directly supported by NIST SP 800-115 | §6.5 and Appendix B define assessment-plan and Rules-of-Engagement fields. | Convert written scope into executable target, traffic, abort, data, and cleanup controls. |
| 2. Define the adversary objective and protected action. | MITRE support + AATE specialization | MITRE supports objective-driven behavior chains; it does not define AATE's protected-action term. | Name the server-side state change or service effect that decides success. |
| 3. Map the application, workflow, control, and resource path. | Directly supported by OWASP WSTG + AATE specialization | WSTG-INFO-06 and WSTG-INFO-10 support mapping entry points, messages, parameters, components, and architecture. | Join business workflow, enforcement point, and consumed resource in one attack map. |
| 4. Record the legitimate baseline. | Controlled-experiment principle | A comparison requires a measured reference condition using the same method. | Record action result, control decision, state, versions, and health for the legitimate client. |
| 5. Build the simplest representative adversary. | Directly supported by MITRE adversary-emulation principles | MITRE permits implementation choices that reproduce relevant behavior rather than a named tool. | Start with the least complex client that can complete the hostile workflow. |
| 6. Record the blocked or challenged baseline. | Controlled-experiment principle + AATE specialization | The initial treatment condition must be measured before a change. | Prove that the intended control—not a broken script, stale state, or unrelated failure—blocked the same action. |
| 7. Enumerate candidate trusted signals and assumptions. | OWASP mapping + AATE specialization | Mapping exposes state, parameters, clients, and intermediaries. | Treat what the control appears to trust as the offensive attack surface. |
| 8. State a falsifiable bypass or pressure hypothesis. | Controlled-experiment principle | A hypothesis predicts an observable result and names a refuting result before execution. | Predict control response, protected-action result, and state/resource evidence. |
| 9. Change one variable or one deliberately coherent signal set. | Controlled-experiment principle + AATE specialization | A controlled treatment supports causal interpretation. | Permit a predeclared coherent set only when one identity claim necessarily spans related values. |
| 10. Repeat the same protected action. | Controlled-experiment principle | Outcomes are comparable only when the measured action and fixed variables remain stable. | Never replace business-action proof with a score, challenge disappearance, or fingerprint change. |
| 11. Prove whether the adversarial objective succeeded. | Directly supported by NIST SP 800-115 + AATE specialization | §5.2.1's Attack phase and §8.1 analysis validate consequences. | Require a state change, accepted hostile action, or measured service effect. |
| 12. Record residual anomalies and alternative explanations. | Controlled-experiment principle + AATE specialization | Confounders and competing explanations constrain causal claims. | Preserve remaining browser, protocol, session, behavior, and workflow contradictions even after success. |
| 13. Explain impact and limitations. | Directly supported by NIST SP 800-115 | §§8.1-8.3 support analysis and communication in operational context. | Separate the bounded local proof from claims that would require different evidence. |
| 14. Recommend remediation and measurable success criteria. | Directly supported by NIST SP 800-115 + AATE specialization | §§8.2-8.3 support communicating mitigation. | Fix the overtrusted assumption and define hostile plus legitimate-neighbor outcomes. |
| 15. Repeat the same attack after remediation. | NIST follow-up + AATE specialization | NIST supports mitigation and follow-up but does not prescribe this exact AATE replay. | Reuse the objective, action, procedure, fixed variables, and evidence schema. |

## What each provenance class does not claim

- **NIST support** does not mean NIST publishes a browser-evasion or
  application-layer pressure recipe.
- **MITRE support** does not mean enterprise ATT&CK procedures directly model
  automated-abuse controls.
- **OWASP support** does not authorize scanning and does not prove a mapped
  parameter is exploitable.
- **Controlled-experiment principles** improve causal reasoning but cannot turn
  an unrepresentative lab into production evidence.
- **AATE specialization** is explicitly course synthesis and must remain labeled
  `COURSE_SYNTHESIS` wherever a lesson depends on it.

Continue to [authorization and safety](authorization-and-safety.md), then use
the [fifteen-step operational loop](adversarial-control-loop.md) during every
lab and retest.
