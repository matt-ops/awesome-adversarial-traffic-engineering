# DDoS by exhausted resource

Classify denial of service by constrained resource: link bandwidth, packet processing, connection state, TLS handshakes, streams, CPU, memory, worker pools, queues, cache, database connections, third-party dependencies, or expensive workflows.

Match metrics to the resource: bps, pps, connection rate, concurrency, rps, latency percentiles, errors, timeouts, queue depth, cache hit ratio, saturation, and recovery time. The same rps can be harmless or severe depending on request cost and state.

Local Layer 7 tests teach experiment design. They do not model raw packet attacks, global scrubbing, or production capacity.

