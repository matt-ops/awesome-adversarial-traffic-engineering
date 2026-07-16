"""Generate bounded local ClientHello fixtures and observe fixed-loopback HTTP."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import ssl
from typing import Any

HOST = "localhost"
PORT = 8080


def client_hello(alpn: tuple[str, ...] = ()) -> bytes:
    """Return the first TLS bytes produced by Python without opening a socket."""
    context = ssl.create_default_context()
    if alpn:
        context.set_alpn_protocols(list(alpn))
    incoming = ssl.MemoryBIO()
    outgoing = ssl.MemoryBIO()
    connection = context.wrap_bio(incoming, outgoing, server_side=False, server_hostname=HOST)
    try:
        connection.do_handshake()
    except ssl.SSLWantReadError:
        pass
    return outgoing.read()


def summarize_client_hello(data: bytes, label: str) -> dict[str, Any]:
    """Parse only stable outer fields; this is deliberately not a JA4 parser."""
    if len(data) < 11 or data[0] != 22 or data[5] != 1:
        raise ValueError("expected a TLS handshake record containing ClientHello")
    return {
        "label": label,
        "record_type": data[0],
        "record_legacy_version": f"0x{int.from_bytes(data[1:3], 'big'):04x}",
        "record_length": int.from_bytes(data[3:5], "big"),
        "handshake_type": data[5],
        "clienthello_legacy_version": f"0x{int.from_bytes(data[9:11], 'big'):04x}",
        "bytes": len(data),
        "sha256_prefix": hashlib.sha256(data).hexdigest()[:16],
        "limitation": "process-local Python/OpenSSL fixture; digest is not JA4 and not identity",
    }


def compare_client_hellos() -> dict[str, Any]:
    default = client_hello()
    with_alpn = client_hello(("h2", "http/1.1"))
    return {
        "default": summarize_client_hello(default, "python-default"),
        "with_alpn": summarize_client_hello(with_alpn, "python-alpn-h2-http11"),
        "bytes_differ": default != with_alpn,
        "changed": "ALPN configuration; random/session fields may also vary between generated hellos",
    }


def observe_http() -> dict[str, Any]:
    connection = http.client.HTTPConnection(HOST, PORT, timeout=3)
    try:
        connection.request("GET", "/api/protocol/observe", headers={"User-Agent": "aate-protocol-helper/1.0"})
        response = connection.getresponse()
        body = json.loads(response.read().decode("utf-8"))
        return {
            "target": f"http://{HOST}:{PORT}/api/protocol/observe",
            "status": response.status,
            "response_http_version": f"HTTP/{response.version // 10}.{response.version % 10}",
            "server_observation": body,
        }
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("clienthello", "http", "all"), nargs="?", default="all")
    args = parser.parse_args()
    if args.mode in {"clienthello", "all"}:
        print(json.dumps({"clienthello": compare_client_hellos()}, indent=2, sort_keys=True))
    if args.mode in {"http", "all"}:
        try:
            print(json.dumps({"http": observe_http()}, indent=2, sort_keys=True))
        except OSError as exc:
            print(json.dumps({"error": str(exc), "hint": "start the fixed local API"}))
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
