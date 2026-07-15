# Local target policy

The bundled clients accept only explicit loopback and Compose-internal names.
The validator rejects arbitrary public IPs, private LAN addresses, credentialed
URLs, lookalike hostnames, and non-HTTP schemes.

| Allowed example | Reason |
|---|---|
| `http://localhost:8080/health` | Explicit loopback name |
| `http://127.0.0.1:8080/` | IPv4 loopback |
| `https://[::1]/` | IPv6 loopback |
| `http://app:8000/health` | Named service inside the isolated Compose network |

`localhost.example.com`, `10.0.0.1`, `192.168.1.5`, and public URLs are rejected.
Do not modify the allowlist for a lesson. A separate written authorization and a
separate tool configuration are required for organization-owned environments.
