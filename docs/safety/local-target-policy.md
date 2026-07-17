# Local target policy

The bundled fixed course client accepts only exact loopback and Compose-internal
origins. It rejects every redirect rather than following a second network hop.
The destination boundary therefore applies before the first request and cannot
be changed by a response `Location` header.

| Allowed example | Reason |
|---|---|
| `http://localhost:8080/health` | Explicit loopback name |
| `http://127.0.0.1:8080/` | IPv4 loopback |
| `http://app:8000/health` | Named service inside the isolated Compose network |
| `http://edge:8080/health` | Named edge inside the isolated Compose network |

Scheme and port are part of the fixed origin. For example,
`http://localhost:8081`, `https://localhost:8080`, and
`http://127.0.0.1` on its default port are not course-client targets. A redirect
to a public hostname, public IP, private-network IP, different port, different
scheme, or even another approved local URL is rejected on the first 3xx response.

`validate_local_url()` is a separate general local-development validator. It
accepts the approved loopback and Compose hostnames on arbitrary valid ports so
deterministic in-process HTTP tests and early local exercises can bind an
ephemeral port. The executable `safe_client` does not use that broader policy;
it calls `validate_course_client_url()` and exposes no command-line bypass.

The application container remains only on the internal `aate-local` network and
publishes no host port. The nginx edge also joins a small bridge network solely
so Docker Desktop can honor `127.0.0.1:8080:8080`; no wildcard host address is
published. This preserves the application isolation boundary while making the
documented loopback endpoint reachable on Windows, macOS, and Linux engines.

`localhost.example.com`, `10.0.0.1`, `192.168.1.5`, and public URLs are rejected.
Do not modify the allowlist for a lesson. A separate written authorization and a
separate tool configuration are required for organization-owned environments.
