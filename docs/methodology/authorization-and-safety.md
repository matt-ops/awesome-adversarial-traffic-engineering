# Authorization and safety

Authorization is a written grant from the owner of the target environment. It
must identify systems, actions, timing, data, safety controls, stop conditions,
contacts, cleanup, evidence handling, and reporting. NIST SP 800-115 treats the
assessment plan and Rules of Engagement as operational controls, not ceremonial
paperwork.[^nist]

[^nist]: NIST SP 800-115, §6.5 and Appendix B.

Discovery does not expand scope. A hostname found in documentation, a redirect,
an adjacent container, or a provider platform remains excluded until the owner
adds it. Provider-hosted labs authorize only the assigned target and techniques.

Use [the local target policy](../safety/local-target-policy.md) and [traffic
guardrails](../safety/traffic-guardrails.md) for repository exercises.
