# Module 01 - HTTP and the edge

**Outcome:** trace one user action through an HTTP exchange, state, workflow,
intermediaries, application code, and dependencies before reasoning about where
an adversary can observe or influence a control.

This is the technical starting point. **No earlier course module is required.**

## Foundation

Complete [request and response](01-http-request-response.md), [sessions and
workflows](02-sessions-and-workflows.md), and [DevTools Network](03-devtools-network.md).
Produce a request worksheet and one browser trace.

## Applied

Complete [the edge request path](04-edge-request-path.md) and label the zero-Docker
path from browser through intermediary roles to application/resource.

## Integrated

Revisit that diagram during Module 04. Add the API route, state mutation,
authentication decision, rate key, and evidence points used by the attack.

## Deep

Compare origin and intermediary views: routing, connection termination, session
state, caching, normalization, forwarded claims, and what evidence each can observe.

Start with [HTTP request and response](01-http-request-response.md). No Docker is
needed in this module.
