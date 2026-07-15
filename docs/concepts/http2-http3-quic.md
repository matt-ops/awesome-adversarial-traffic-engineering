# HTTP/2, HTTP/3, and QUIC

HTTP/2 multiplexes streams over a connection and compresses headers; HTTP/3 maps HTTP semantics onto QUIC, which integrates TLS and supports transport behavior different from TCP. These mechanisms change observability and make per-connection assumptions incomplete.

At Integrated depth, focus on streams, flow control, connection reuse, settings, observation points, and how proxies terminate or normalize behavior. Defer frame and QUIC internals to Deep work. Protocol features are evidence, not stable client identity.

