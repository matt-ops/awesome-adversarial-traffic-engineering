# Provenance of the AATE adversarial-control loop

> **AATE course synthesis:** no single standard defines this exact fifteen-step
> sequence. It combines NIST assessment planning and penetration-test phases,
> MITRE adversary-emulation principles, OWASP application mapping, controlled
> experimental design, and specialization for bot-control and DDoS red teaming.

| Step | Primary provenance | What is directly supported | AATE specialization |
|---:|---|---|---|
| 1. Authorize and define scope. | NIST SP 800-115 §6.5 and Appendix B | Assessment plans and Rules of Engagement define authorized systems, activities, logistics, data handling, incident handling, and reporting. | Hard local target and traffic ceilings are mandatory run-time controls. |
| 2. Define the adversary objective and protected action. | MITRE Adversary Emulation Plans | Emulation models adversary behavior and objectives rather than only tools or indicators. | AATE requires one observable business action or service effect. |
| 3. Map the application, workflow, control, and resource path. | OWASP WSTG-INFO-06 and WSTG-INFO-10 | Testers map entry points, requests, responses, parameters, components, and architecture before deeper testing. | AATE joins business workflow, enforcement point, and exhausted resource in one map. |
| 4. Record the legitimate baseline. | Controlled-experiment principle | A comparison requires a reference condition measured with the same method. | The baseline includes both control decision and protected-action result. |
| 5. Build the simplest representative adversary. | MITRE Adversary Emulation Plans | Operators reproduce relevant behavior with implementation latitude. | Start with the minimum client that can perform the hostile workflow. |
| 6. Record the blocked or challenged baseline. | Controlled-experiment principle | The treatment can be evaluated only after the initial condition is measured. | AATE requires proof that the intended control, not an unrelated failure, made the decision. |
| 7. Enumerate candidate trusted signals and assumptions. | OWASP mapping plus AATE specialization | Mapping reveals parameters, state, and intermediaries. | Treat the control's presumed trust inputs as the offensive attack surface. |
| 8. State a falsifiable bypass or pressure hypothesis. | Controlled-experiment principle | A useful hypothesis predicts an observable result before the test. | The prediction names the protected action, control response, and resource/telemetry change. |
| 9. Change one variable or one deliberately coherent signal set. | Controlled-experiment principle | Controlled variables support causal interpretation. | Coherent sets are allowed when one identity claim necessarily spans related signals. |
| 10. Repeat the same protected action. | Controlled-experiment principle | The outcome must be measured under comparable conditions. | Do not substitute a detector-score change for the original adversarial objective. |
| 11. Prove whether the adversarial objective succeeded. | NIST SP 800-115 §5.2.1 Attack and §8.1 analysis | Exploitation and analysis establish the consequence of the discovered weakness. | Required evidence is a state change, successful action, or measured service effect. |
| 12. Record residual anomalies and alternative explanations. | Controlled-experiment principle | Confounders and competing explanations constrain causal claims. | Browser, protocol, session, and workflow inconsistencies remain part of the result even after success. |
| 13. Explain impact and limitations. | NIST SP 800-115 §§8.1-8.3 | Findings are analyzed, communicated, and placed in operational context. | Separate local proof from claims that would require production evidence. |
| 14. Recommend remediation and measurable success criteria. | NIST SP 800-115 §§8.2-8.3 | Mitigation addresses findings and should be communicated to stakeholders. | Fix the overtrusted assumption and define both hostile and legitimate near-neighbor outcomes. |
| 15. Repeat the same attack after remediation. | NIST mitigation/follow-up plus AATE specialization | Assessment findings and mitigation require follow-up. | The retest uses the identical adversary objective, protected action, and evidence schema. |

## Source boundaries

- **Directly supported by NIST:** planning, scope, Rules of Engagement,
  discovery/attack/reporting phases, analysis, mitigation, and follow-up.
- **Directly supported by MITRE:** behavior-focused emulation and chaining actions
  into an operator plan.
- **Directly supported by OWASP:** entry-point, request/response, parameter,
  state, and application-architecture mapping.
- **Controlled-experiment principle:** baselines, predictions, controlled changes,
  repeated measurement, and alternative explanations.
- **AATE specialization:** protected-action proof, trusted-signal analysis,
  coherent identity changes, residual anomalies, resource-path modeling, and
  exact adversarial retest.

The course must cite the underlying sources for their actual claims and label the
fifteen-step loop as `COURSE_SYNTHESIS`; it must never claim that NIST, MITRE, or
OWASP publishes the AATE sequence.
