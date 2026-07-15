# Domain question bank

Use the same answer frame for every question: clarify scope → state assumptions → explain mechanism → compare alternatives → add measurement and safety → state limitations → define validation.

## Safety and engagement — Module 0

**Prompt:** Design a safe test of a local edge control.  
**Testing:** judgment, scope, caps, abort, recovery.  
**Strong structure:** objective; authorization; environment; exclusions; baseline; traffic envelope; monitoring; stop owner; cleanup; evidence; remediation; retest.  
**Weak answer:** begins with a load tool or maximum rate.  
**Follow-up:** What if monitoring becomes unreliable midway through the run?

## Request path — Module 1

**Prompt:** Trace a browser request through an edge-protected application.  
**Testing:** network and systems reasoning.  
**Strong structure:** DNS; transport/TLS; edge termination; WAF/bot controls; balancing; app/cache/dependencies; response; state; telemetry; failure points.  
**Weak answer:** treats CDN, WAF, and load balancer as interchangeable.  
**Follow-up:** Which observations change behind a proxy?

## Automated abuse — Module 2

**Prompt:** Detect distributed low-rate promotion abuse.  
**Testing:** business-workflow and false-positive reasoning.  
**Strong structure:** actor/goal; state transitions; request/session/account/global evidence; household/shared-network risks; tiered controls; metrics; retest.  
**Weak answer:** block by IP or “use fingerprinting.”  
**Follow-up:** How do you measure displaced abuse?

## Browser automation — Module 3

**Prompt:** Explain Browser, BrowserContext, Page, Frame, Worker, and CDPSession.  
**Testing:** browser object and observation model.  
**Strong structure:** lifecycle, isolation, state, renderer contexts, event sources, server-visible versus browser-visible evidence.  
**Weak answer:** equates a Context with a separate device.  
**Follow-up:** How would you isolate a Playwright artifact from task behavior?

## Detection — Module 4

**Prompt:** Design and evaluate a layered bot detector.  
**Testing:** signal quality, state, metrics, rollout.  
**Strong structure:** abuse goal; populations; observation layers; explainable features; state scopes; threshold/action tiers; confusion matrix; per-population error; drift; shadow launch; retest.  
**Weak answer:** one magic signal or aggregate accuracy.  
**Follow-up:** How does a challenge contaminate feedback?

## DDoS and edge — Module 5

**Prompt:** Distinguish a flash crowd from Layer 7 attack traffic.  
**Testing:** resource, ambiguity, and operational judgment.  
**Strong structure:** constrained resource; baseline; workflow intent/state; cacheability; identity distribution; errors and recovery; legitimate cohorts; progressive controls.  
**Weak answer:** high rps means attack.  
**Follow-up:** What if per-IP limiting improves CPU but raises customer errors?

## Python and review — Module 6

**Prompt:** Review an asynchronous client with no timeout and unlimited retries.  
**Testing:** realistic impact and remediation.  
**Strong structure:** failure precondition; task/connection accumulation; outage amplification; deadline; retry budget/jitter; concurrency cap; cancellation; tests; telemetry.  
**Weak answer:** labels it “DoS” without reachability or bounds.  
**Follow-up:** Which regression test proves amplification is bounded?

## Experiment and reporting — Module 7

**Prompt:** Turn a browser inconsistency into a defensible finding.  
**Testing:** experimental method and communication.  
**Strong structure:** hypothesis; baseline; controlled variable; populations; evidence; alternative explanations; error; impact; specific remediation; falsifiable retest.  
**Weak answer:** a public detector screenshot and a bypass claim.  
**Follow-up:** What result would cause you to withdraw the finding?

