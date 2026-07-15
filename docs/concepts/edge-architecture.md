# Edge architecture

A useful request model is client → DNS → edge/CDN → WAF or bot defense → load balancer → application → cache/database/dependencies. Each hop can terminate connections, transform observations, retain state, enforce a control, and become constrained.

Ask four questions at each hop: what is observed, what state is kept, what resource can be exhausted, and which legitimate traffic resembles abuse? A local reverse proxy teaches placement and correlation, but not anycast, global caches, carrier networks, or commercial edge behavior.

Interview use: draw the path first, then place signals, controls, failure modes, telemetry, customer impact, and retest.

