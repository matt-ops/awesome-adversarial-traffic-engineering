# Protocol fingerprinting

- [Wireshark documentation](https://www.wireshark.org/docs/) — `[L2 Applied]` `[Required]` · Module 1 · Official documentation. Packet and protocol analysis guidance. It matters for naming exactly which handshake or connection evidence was observed.
- [mitmproxy documentation](https://docs.mitmproxy.org/stable/) — `[L2 Applied]` `[Recommended]` · Module 1 · Official documentation. Local HTTP(S) inspection and scripting. It matters for controlled client comparison while making proxy effects explicit.
- [FoxIO JA4 repository](https://github.com/FoxIO-LLC/ja4) — `[L2 Applied]` `[Recommended]` · Modules 1 and 4 · Project repository. Tools and background for the JA4 family. It matters for understanding the project’s intended scope and verifying any implementation claim.
- [JA4 technical details](https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md) — `[L2 Applied]` `[Required]` · Modules 1 and 4 · Project technical specification. Describes JA4 structure and normalization. It matters for discussing fingerprints as pivots with implementation and observation limits.
- [RFC 9113: HTTP/2](https://www.rfc-editor.org/rfc/rfc9113) — `[L3 Integrated]` `[Required]` · Modules 1 and 5 · Internet standard. Defines HTTP/2 framing, streams, flow control, and settings. Selected sections matter for multiplexing and stream-pressure analysis.
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446) — `[L4 Deep]` `[Optional]` · Module 1 · Internet standard. Normative TLS 1.3 protocol. It matters when an original question requires details beyond the practical handshake model; full reading is not an early requirement.
- [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114) — `[L4 Deep]` `[Optional]` · Modules 1 and 5 · Internet standard. Defines HTTP over QUIC. It matters for advanced observability and stream behavior.
- [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000) — `[L4 Deep]` `[Optional]` · Modules 1 and 5 · Internet standard. Defines QUIC transport. It matters for advanced connection, migration, and network-observation questions.

