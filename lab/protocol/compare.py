"""Capture real loopback ClientHello and HTTP/2 observations from local clients."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import platform
import queue
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from collections import defaultdict
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import IO, Any
from urllib.parse import urlsplit

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

ROOT = Path(__file__).resolve().parents[2]
HOST = "127.0.0.1"
MAX_CLIENTHELLO_BYTES = 65_540
MAX_CONNECTIONS = 4
MAX_HTTP2_STREAMS = 8
AUTOMATED_WALL_TIMEOUT_SECONDS = 45
RAW_OBSERVER_TIMEOUT_SECONDS = 4.0
HTTP2_OBSERVER_TIMEOUT_SECONDS = 30.0
PER_CLIENT_TIMEOUT_SECONDS = 15.0
PROCESS_CLEANUP_TIMEOUT_SECONDS = 2.0


class ProtocolDeadlineExceeded(TimeoutError):
    """The absolute whole-command deadline expired."""


class ProtocolSafetyError(RuntimeError):
    """A protocol client violated the loopback-only page-request boundary."""


def remaining_seconds(deadline: float, label: str, cap: float | None = None) -> float:
    """Return positive remaining budget, capped for one operation."""
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise ProtocolDeadlineExceeded(f"whole-command deadline exceeded before {label}")
    return remaining if cap is None else min(remaining, cap)


def _operation_deadline(deadline: float | None, cap: float) -> float:
    local_deadline = time.monotonic() + cap
    return local_deadline if deadline is None else min(deadline, local_deadline)


def require_loopback_host(host: str) -> str:
    """Return a normalized host or reject every non-loopback bind/target."""
    if host.casefold() == "localhost":
        return "localhost"
    try:
        address = ipaddress.ip_address(host)
    except ValueError as exc:
        raise ValueError("host must be localhost or a loopback address") from exc
    if not address.is_loopback:
        raise ValueError("host must be localhost or a loopback address")
    return str(address)


def require_loopback_url(url: str) -> str:
    """Reject credentials, fragments, and destinations outside loopback."""
    parsed = urlsplit(url)
    if parsed.scheme not in {"https", "http"} or parsed.hostname is None:
        raise ValueError("target must be an HTTP(S) loopback URL")
    require_loopback_host(parsed.hostname)
    if parsed.username is not None or parsed.password is not None or parsed.fragment:
        raise ValueError("target must not contain credentials or a fragment")
    return url


def validate_cap(value: int, maximum: int, label: str) -> int:
    """Enforce small positive hard caps."""
    if isinstance(value, bool) or value <= 0 or value > maximum:
        raise ValueError(f"{label} must be between 1 and {maximum}")
    return value


def client_hello(alpn: tuple[str, ...] = ()) -> bytes:
    """Return Python/OpenSSL ClientHello bytes without opening a socket."""
    context = ssl.create_default_context()
    if alpn:
        context.set_alpn_protocols(list(alpn))
    incoming = ssl.MemoryBIO()
    outgoing = ssl.MemoryBIO()
    connection = context.wrap_bio(incoming, outgoing, server_side=False, server_hostname="localhost")
    try:
        connection.do_handshake()
    except ssl.SSLWantReadError:
        pass
    return outgoing.read()


def _read_u16(data: bytes, offset: int, label: str) -> tuple[int, int]:
    if offset + 2 > len(data):
        raise ValueError(f"truncated ClientHello while reading {label}")
    return int.from_bytes(data[offset : offset + 2], "big"), offset + 2


def _read_vector(data: bytes, offset: int, length_size: int, label: str) -> tuple[bytes, int]:
    if offset + length_size > len(data):
        raise ValueError(f"truncated ClientHello while reading {label} length")
    length = int.from_bytes(data[offset : offset + length_size], "big")
    start = offset + length_size
    end = start + length
    if end > len(data):
        raise ValueError(f"truncated ClientHello while reading {label}")
    return data[start:end], end


def _u16_list(data: bytes, label: str) -> list[int]:
    if len(data) % 2:
        raise ValueError(f"{label} must contain two-byte values")
    return [int.from_bytes(data[index : index + 2], "big") for index in range(0, len(data), 2)]


def parse_client_hello(data: bytes, label: str, runtime_version: str) -> dict[str, Any]:
    """Parse the first TLS record when it contains one complete ClientHello."""
    if len(data) < 9:
        raise ValueError("truncated TLS record or handshake header")
    if data[0] != 22:
        raise ValueError("expected TLS handshake record type 22")
    record_length = int.from_bytes(data[3:5], "big")
    if record_length > MAX_CLIENTHELLO_BYTES - 5:
        raise ValueError("TLS record exceeds the ClientHello byte cap")
    if len(data) != record_length + 5:
        raise ValueError("truncated or trailing TLS record data")
    if data[5] != 1:
        raise ValueError("expected ClientHello handshake type 1")
    handshake_length = int.from_bytes(data[6:9], "big")
    if handshake_length + 4 != record_length:
        raise ValueError("ClientHello handshake length does not match its TLS record")

    body = data[9:]
    if len(body) < 35:
        raise ValueError("truncated ClientHello fixed fields")
    legacy_version = int.from_bytes(body[0:2], "big")
    offset = 34
    _, offset = _read_vector(body, offset, 1, "session id")
    cipher_bytes, offset = _read_vector(body, offset, 2, "cipher suites")
    cipher_suites = _u16_list(cipher_bytes, "cipher suites")
    _, offset = _read_vector(body, offset, 1, "compression methods")

    extensions: list[tuple[int, bytes]] = []
    if offset < len(body):
        extension_bytes, offset = _read_vector(body, offset, 2, "extensions")
        if offset != len(body):
            raise ValueError("unexpected bytes after ClientHello extensions")
        extension_offset = 0
        while extension_offset < len(extension_bytes):
            extension_id, extension_offset = _read_u16(extension_bytes, extension_offset, "extension id")
            value, extension_offset = _read_vector(
                extension_bytes, extension_offset, 2, f"extension {extension_id}"
            )
            extensions.append((extension_id, value))

    extension_ids = [extension_id for extension_id, _ in extensions]
    extension_map = {extension_id: value for extension_id, value in extensions}
    supported_groups: list[int] = []
    if 10 in extension_map:
        group_bytes, group_end = _read_vector(extension_map[10], 0, 2, "supported groups")
        if group_end != len(extension_map[10]):
            raise ValueError("unexpected bytes after supported groups")
        supported_groups = _u16_list(group_bytes, "supported groups")
    signature_algorithms: list[int] = []
    if 13 in extension_map:
        signature_bytes, signature_end = _read_vector(
            extension_map[13], 0, 2, "signature algorithms"
        )
        if signature_end != len(extension_map[13]):
            raise ValueError("unexpected bytes after signature algorithms")
        signature_algorithms = _u16_list(signature_bytes, "signature algorithms")
    alpn_offers: list[str] = []
    if 16 in extension_map:
        alpn_bytes, alpn_end = _read_vector(extension_map[16], 0, 2, "ALPN list")
        if alpn_end != len(extension_map[16]):
            raise ValueError("unexpected bytes after ALPN list")
        alpn_offset = 0
        while alpn_offset < len(alpn_bytes):
            protocol, alpn_offset = _read_vector(alpn_bytes, alpn_offset, 1, "ALPN protocol")
            alpn_offers.append(protocol.decode("ascii", errors="replace"))

    digest_input = {
        "record_type": data[0],
        "record_legacy_version": int.from_bytes(data[1:3], "big"),
        "clienthello_legacy_version": legacy_version,
        "cipher_suite_ids": cipher_suites,
        "extension_ids": extension_ids,
        "supported_groups": supported_groups,
        "signature_algorithms": signature_algorithms,
        "alpn_offers": alpn_offers,
        "sni_present": 0 in extension_map,
    }
    digest = hashlib.sha256(
        json.dumps(digest_input, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    return {
        "client": label,
        "runtime_version": runtime_version,
        "record_type": data[0],
        "record_legacy_version": f"0x{int.from_bytes(data[1:3], 'big'):04x}",
        "clienthello_legacy_version": f"0x{legacy_version:04x}",
        "cipher_suite_ids": cipher_suites,
        "extension_ids": extension_ids,
        "supported_groups": supported_groups,
        "signature_algorithms": signature_algorithms,
        "alpn_offers": alpn_offers,
        "sni_present": 0 in extension_map,
        "total_bytes": len(data),
        "comparison_digest": digest,
        "digest_label": "not JA4; not identity proof",
    }


def summarize_client_hello(data: bytes, label: str) -> dict[str, Any]:
    """Compatibility wrapper for the earlier fixture-focused lab and tests."""
    return parse_client_hello(data, label, f"Python {platform.python_version()} / {ssl.OPENSSL_VERSION}")


class RawClientHelloObserver:
    """A fixed-loopback TLS-record observer with explicit connection and time caps."""

    def __init__(
        self,
        host: str = HOST,
        max_connections: int = 1,
        wall_timeout: float = RAW_OBSERVER_TIMEOUT_SECONDS,
        deadline: float | None = None,
    ) -> None:
        self.host = require_loopback_host(host)
        self.max_connections = validate_cap(max_connections, MAX_CONNECTIONS, "connection cap")
        if wall_timeout <= 0 or wall_timeout > RAW_OBSERVER_TIMEOUT_SECONDS:
            raise ValueError(f"observer timeout must be within {RAW_OBSERVER_TIMEOUT_SECONDS} seconds")
        self.wall_timeout = wall_timeout
        self.deadline = _operation_deadline(deadline, wall_timeout)
        self.port = 0
        self.connection_count = 0
        self._listener: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._result: queue.Queue[bytes | BaseException] = queue.Queue(maxsize=max_connections)

    def start(self) -> None:
        family = socket.AF_INET6 if ":" in self.host else socket.AF_INET
        listener = socket.socket(family, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self.host, 0))
        listener.listen(self.max_connections)
        listener.settimeout(0.2)
        self.port = int(listener.getsockname()[1])
        self._listener = listener
        self._thread = threading.Thread(target=self._serve, name="aate-clienthello-observer", daemon=True)
        self._thread.start()

    def _serve(self) -> None:
        listener = self._listener
        if listener is None:
            self.error = RuntimeError("ClientHello observer listener was not initialized")
            return
        try:
            while self.connection_count < self.max_connections and time.monotonic() < self.deadline:
                try:
                    listener.settimeout(remaining_seconds(self.deadline, "ClientHello accept", 0.2))
                    connection, address = listener.accept()
                except (TimeoutError, ProtocolDeadlineExceeded):
                    continue
                peer = str(address[0])
                if not ipaddress.ip_address(peer).is_loopback:
                    connection.close()
                    self._result.put(ValueError("observer rejected a non-loopback peer"))
                    continue
                self.connection_count += 1
                with connection:
                    connection.settimeout(remaining_seconds(self.deadline, "ClientHello header read", 2.0))
                    header = self._recv_exact(connection, 5, self.deadline)
                    if len(header) != 5:
                        self._result.put(ValueError("truncated TLS record header"))
                        continue
                    length = int.from_bytes(header[3:5], "big")
                    if length + 5 > MAX_CLIENTHELLO_BYTES:
                        self._result.put(ValueError("TLS record exceeds the ClientHello byte cap"))
                        continue
                    payload = self._recv_exact(connection, length, self.deadline)
                    if len(payload) != length:
                        self._result.put(ValueError("truncated TLS record payload"))
                        continue
                    self._result.put(header + payload)
        except OSError as exc:
            if self.connection_count == 0:
                self._result.put(exc)
        finally:
            try:
                listener.close()
            except OSError:
                pass

    @staticmethod
    def _recv_exact(connection: socket.socket, length: int, deadline: float) -> bytes:
        chunks: list[bytes] = []
        remaining = length
        while remaining:
            connection.settimeout(remaining_seconds(deadline, "ClientHello socket read", 2.0))
            chunk = connection.recv(min(remaining, 4096))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def result(self, deadline: float | None = None) -> bytes:
        result_deadline = self.deadline if deadline is None else min(self.deadline, deadline)
        try:
            value = self._result.get_nowait()
        except queue.Empty:
            try:
                value = self._result.get(timeout=remaining_seconds(result_deadline, "ClientHello result queue"))
            except queue.Empty as exc:
                raise TimeoutError("ClientHello observer timed out") from exc
        if isinstance(value, BaseException):
            raise value
        return value

    def close(self, deadline: float | None = None) -> None:
        if self._listener is not None:
            try:
                self._listener.close()
            except OSError:
                pass
        if self._thread is not None:
            close_deadline = (
                time.monotonic() + PROCESS_CLEANUP_TIMEOUT_SECONDS
                if deadline is None
                else deadline
            )
            try:
                self._thread.join(timeout=remaining_seconds(close_deadline, "ClientHello observer shutdown"))
            except ProtocolDeadlineExceeded:
                self._thread.join(timeout=0)


def _proxy_free_environment() -> dict[str, str]:
    environment = os.environ.copy()
    for name in ("ALL_PROXY", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "http_proxy", "https_proxy"):
        environment.pop(name, None)
    environment["NO_PROXY"] = "127.0.0.1,localhost,::1"
    environment["no_proxy"] = environment["NO_PROXY"]
    return environment


def _capture_trigger(
    client: str,
    runtime_version: str,
    trigger: Callable[[int, float], dict[str, Any]],
    deadline: float | None = None,
) -> dict[str, Any]:
    observer_deadline = _operation_deadline(deadline, RAW_OBSERVER_TIMEOUT_SECONDS)
    client_deadline = _operation_deadline(deadline, PER_CLIENT_TIMEOUT_SECONDS)
    observer = RawClientHelloObserver(deadline=observer_deadline)
    observer.start()
    try:
        trigger_result = trigger(observer.port, client_deadline)
        data = observer.result(observer_deadline)
        parsed = parse_client_hello(data, client, str(trigger_result.get("runtime_version", runtime_version)))
        parsed["status"] = "observed"
        return parsed
    except ProtocolDeadlineExceeded as exc:
        if deadline is not None and time.monotonic() >= deadline:
            raise
        return {
            "client": client,
            "runtime_version": runtime_version,
            "status": "unsupported",
            "reason": f"per-observer or per-client deadline exceeded: {exc}",
            "digest_label": "not JA4; not identity proof",
        }
    except (OSError, TimeoutError, ValueError, subprocess.SubprocessError) as exc:
        return {
            "client": client,
            "runtime_version": runtime_version,
            "status": "unsupported",
            "reason": str(exc),
            "digest_label": "not JA4; not identity proof",
        }
    finally:
        observer.close(client_deadline)


def _python_tls_trigger(port: int, deadline: float) -> dict[str, Any]:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection(
            (HOST, port),
            timeout=remaining_seconds(deadline, "Python TLS connection", 2.0),
        ) as raw:
            raw.settimeout(remaining_seconds(deadline, "Python TLS handshake", 2.0))
            with context.wrap_socket(raw, server_hostname="localhost"):
                pass
    except (OSError, ssl.SSLError):
        pass
    return {"runtime_version": f"Python {platform.python_version()} / {ssl.OPENSSL_VERSION}"}


def _curl_version(deadline: float | None = None) -> tuple[str | None, str]:
    executable = shutil.which("curl.exe") or shutil.which("curl")
    if executable is None:
        return None, "curl executable not found"
    operation_deadline = _operation_deadline(deadline, 3.0)
    completed = subprocess.run(  # noqa: S603 - executable is resolved locally and arguments are fixed.
        [executable, "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=remaining_seconds(operation_deadline, "curl version", 3.0),
        env=_proxy_free_environment(),
    )
    lines = completed.stdout.splitlines()
    return executable, lines[0] if lines else "curl version unavailable"


def _curl_tls_trigger(executable: str, version: str, port: int, deadline: float) -> dict[str, Any]:
    target = require_loopback_url(f"https://{HOST}:{port}/aate-clienthello")
    subprocess.run(  # noqa: S603 - executable is resolved locally and target is loopback-validated.
        [
            executable,
            "--noproxy",
            "*",
            "--proxy",
            "",
            "--connect-timeout",
            "2",
            "--max-time",
            "3",
            "--insecure",
            "--silent",
            "--show-error",
            target,
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=remaining_seconds(deadline, "curl ClientHello client", 4.0),
        env=_proxy_free_environment(),
    )
    return {"runtime_version": version}


def _npx_command() -> str | None:
    return shutil.which("npx.cmd") or shutil.which("npx")


def _run_protocol_client(mode: str, target: str, deadline: float | None = None) -> dict[str, Any]:
    require_loopback_url(target)
    operation_deadline = _operation_deadline(deadline, PER_CLIENT_TIMEOUT_SECONDS)
    npx = _npx_command()
    if npx is None:
        return {"status": "unsupported", "reason": "npx executable not found", "runtime_version": "unavailable"}
    try:
        completed = subprocess.run(  # noqa: S603 - npx is local and target is loopback-validated.
            [
                npx,
                "tsx",
                "lab/protocol/protocol_clients.ts",
                mode,
                target,
                str(max(1, int(remaining_seconds(operation_deadline, f"{mode} client") * 1000))),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=remaining_seconds(operation_deadline, f"{mode} subprocess", PER_CLIENT_TIMEOUT_SECONDS),
            env=_proxy_free_environment(),
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "unsupported",
            "reason": f"{mode} exceeded its per-client timeout",
            "runtime_version": "unavailable",
            "non_loopback_page_requests_observed": [],
        }
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if completed.returncode != 0 or not lines:
        reason = completed.stderr.strip() or "protocol client returned no result"
        return {"status": "unsupported", "reason": reason, "runtime_version": "unavailable"}
    try:
        parsed: Any = json.loads(lines[-1])
    except json.JSONDecodeError:
        return {
            "status": "unsupported",
            "reason": "protocol client emitted invalid JSON",
            "runtime_version": "unavailable",
        }
    if not isinstance(parsed, dict):
        return {
            "status": "unsupported",
            "reason": "protocol client result was not an object",
            "runtime_version": "unavailable",
        }
    return parsed


def _playwright_tls_trigger(port: int, deadline: float) -> dict[str, Any]:
    return _run_protocol_client(
        "browser-clienthello",
        f"https://{HOST}:{port}/aate-clienthello",
        deadline,
    )


def capture_client_hellos(deadline: float | None = None) -> list[dict[str, Any]]:
    """Capture each installed client against a separately capped observer run."""
    operation_deadline = _operation_deadline(deadline, AUTOMATED_WALL_TIMEOUT_SECONDS)
    results = [
        _capture_trigger(
            "python-openssl",
            "Python/OpenSSL unavailable",
            _python_tls_trigger,
            operation_deadline,
        )
    ]
    curl, curl_version = _curl_version(operation_deadline)
    if curl is None:
        results.append(
            {
                "client": "curl",
                "runtime_version": curl_version,
                "status": "unsupported",
                "reason": "curl executable not found",
                "digest_label": "not JA4; not identity proof",
            }
        )
    else:
        results.append(
            _capture_trigger(
                "curl",
                curl_version,
                lambda port, client_deadline: _curl_tls_trigger(
                    curl,
                    curl_version,
                    port,
                    client_deadline,
                ),
                operation_deadline,
            )
        )
    results.append(
        _capture_trigger(
            "playwright-chromium",
            "Playwright Chromium unavailable",
            _playwright_tls_trigger,
            operation_deadline,
        )
    )
    results.append(
        {
            "client": "manual-chrome-or-chromium",
            "runtime_version": "not launched",
            "status": "unsupported",
            "reason": "optional manual comparison is intentionally not automated",
            "digest_label": "not JA4; not identity proof",
        }
    )
    return results


@dataclass(frozen=True)
class CertificatePaths:
    directory: Path
    certificate: Path
    private_key: Path


@contextmanager
def ephemeral_certificate() -> Iterator[CertificatePaths]:
    """Generate a one-run localhost certificate outside the tracked tree and remove it."""
    with tempfile.TemporaryDirectory(prefix="aate-protocol-") as directory_text:
        directory = Path(directory_text)
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
        now = datetime.now(UTC)
        certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(minutes=1))
            .not_valid_after(now + timedelta(hours=1))
            .add_extension(
                x509.SubjectAlternativeName(
                    [x509.DNSName("localhost"), x509.IPAddress(ipaddress.ip_address(HOST))]
                ),
                critical=False,
            )
            .sign(private_key, hashes.SHA256())
        )
        certificate_path = directory / "localhost-cert.pem"
        private_key_path = directory / "localhost-key.pem"
        certificate_path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
        private_key_path.write_bytes(
            private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )
        yield CertificatePaths(directory, certificate_path, private_key_path)


def _curl_supports_http2(deadline: float | None = None) -> tuple[bool, str, str | None]:
    operation_deadline = _operation_deadline(deadline, 3.0)
    executable, version = _curl_version(operation_deadline)
    if executable is None:
        return False, version, None
    completed = subprocess.run(  # noqa: S603 - executable is resolved locally and arguments are fixed.
        [executable, "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=remaining_seconds(operation_deadline, "curl HTTP/2 capability check", 3.0),
        env=_proxy_free_environment(),
    )
    features = " ".join(
        line.partition(":")[2]
        for line in completed.stdout.splitlines()
        if line.casefold().startswith("features:")
    ).split()
    return "HTTP2" in {feature.upper() for feature in features}, version, executable


def _curl_http2_client(
    executable: str,
    version: str,
    target: str,
    deadline: float | None = None,
) -> dict[str, Any]:
    operation_deadline = _operation_deadline(deadline, 6.0)
    urls = [f"{target}/curl-one", f"{target}/curl-two"]
    completed = subprocess.run(  # noqa: S603 - executable is resolved locally and target is loopback-validated.
        [
            executable,
            "--http2",
            "--insecure",
            "--noproxy",
            "*",
            "--proxy",
            "",
            "--connect-timeout",
            "2",
            "--max-time",
            "5",
            "--silent",
            "--show-error",
            "--header",
            "x-aate-client: curl-http2",
            *urls,
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=remaining_seconds(operation_deadline, "curl HTTP/2 client", 6.0),
        env=_proxy_free_environment(),
    )
    if completed.returncode != 0:
        return {
            "client": "curl-http2",
            "status": "unsupported",
            "runtime_version": version,
            "reason": completed.stderr.strip(),
        }
    return {"client": "curl-http2", "status": "observed", "runtime_version": version, "requests": 2}


def _readline_with_deadline(stream: IO[str], deadline: float) -> str:
    result: queue.Queue[str | BaseException] = queue.Queue(maxsize=1)

    def read() -> None:
        try:
            result.put(stream.readline())
        except BaseException as exc:  # pragma: no cover - platform pipe failures are uncommon.
            result.put(exc)

    thread = threading.Thread(target=read, name="aate-http2-ready-reader", daemon=True)
    thread.start()
    try:
        value = result.get(timeout=remaining_seconds(deadline, "HTTP/2 observer ready output"))
    except queue.Empty as exc:
        raise ProtocolDeadlineExceeded("whole-command deadline exceeded waiting for HTTP/2 observer") from exc
    if isinstance(value, BaseException):
        raise RuntimeError(f"HTTP/2 observer ready output failed: {value}") from value
    return value


def _request_graceful_stop(process: subprocess.Popen[str]) -> None:
    stream = process.stdin
    if process.poll() is not None or stream is None or stream.closed:
        return
    try:
        stream.write("STOP\n")
        stream.flush()
    except (BrokenPipeError, OSError, ValueError):
        pass
    finally:
        try:
            stream.close()
        except OSError:
            pass


def _wait_with_remaining(process: subprocess.Popen[str], deadline: float, label: str) -> bool:
    try:
        process.wait(timeout=remaining_seconds(deadline, label, PROCESS_CLEANUP_TIMEOUT_SECONDS))
        return True
    except (ProtocolDeadlineExceeded, subprocess.TimeoutExpired):
        return process.poll() is not None


def _cleanup_observer_process(process: subprocess.Popen[str], deadline: float) -> None:
    """Close pipes and guarantee graceful-stop, terminate, then kill escalation."""
    _request_graceful_stop(process)
    if process.poll() is None and not _wait_with_remaining(process, deadline, "HTTP/2 graceful shutdown"):
        process.terminate()
    if process.poll() is None and not _wait_with_remaining(process, deadline, "HTTP/2 terminate wait"):
        process.kill()
    if process.poll() is None:
        try:
            process.wait(timeout=max(0.01, min(PROCESS_CLEANUP_TIMEOUT_SECONDS, deadline - time.monotonic())))
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=PROCESS_CLEANUP_TIMEOUT_SECONDS)
    for stream in (process.stdin, process.stdout, process.stderr):
        if stream is not None and not stream.closed:
            try:
                stream.close()
            except OSError:
                pass


def _load_observer_output(output_path: Path) -> dict[str, Any]:
    observations: Any = json.loads(output_path.read_text(encoding="utf-8"))
    if not isinstance(observations, dict):
        raise RuntimeError("HTTP/2 observer result was not an object")
    return observations


def assert_no_non_loopback_page_requests(clients: list[dict[str, Any]]) -> list[str]:
    """Fail when a Playwright client reports an aborted non-loopback page request."""
    violations: list[str] = []
    for client in clients:
        reported = client.get("non_loopback_page_requests_observed", [])
        if not isinstance(reported, list) or not all(isinstance(item, str) for item in reported):
            raise ProtocolSafetyError("protocol client returned an invalid page-request violation list")
        violations.extend(reported)
    unique = sorted(set(violations))
    if unique:
        raise ProtocolSafetyError(f"non-loopback page requests were aborted: {unique}")
    return unique


def observe_http2(deadline: float | None = None) -> dict[str, Any]:
    """Run the ephemeral Node HTTP/2 observer and supported local clients."""
    operation_deadline = _operation_deadline(deadline, HTTP2_OBSERVER_TIMEOUT_SECONDS)
    npx = _npx_command()
    if npx is None:
        return {
            "status": "unsupported",
            "reason": "npx executable not found",
            "clients": [],
            "sessions": [],
            "non_loopback_page_requests_observed": [],
            "cleanup": "no temporary certificate created",
        }
    with ephemeral_certificate() as certificate:
        output_path = certificate.directory / "http2-observations.json"
        process: subprocess.Popen[str] | None = None
        try:
            observer_timeout_ms = max(
                100,
                int(
                    remaining_seconds(
                        operation_deadline,
                        "HTTP/2 observer launch",
                        HTTP2_OBSERVER_TIMEOUT_SECONDS,
                    )
                    * 1000
                ),
            )
            process = subprocess.Popen(  # noqa: S603 - fixed local project command and validated fixed arguments.
                [
                    npx,
                    "tsx",
                    "lab/protocol/http2_observer.ts",
                    "--host",
                    HOST,
                    "--port",
                    "0",
                    "--cert",
                    str(certificate.certificate),
                    "--key",
                    str(certificate.private_key),
                    "--output",
                    str(output_path),
                    "--max-connections",
                    str(MAX_CONNECTIONS),
                    "--max-streams",
                    str(MAX_HTTP2_STREAMS),
                    "--timeout-ms",
                    str(min(30_000, observer_timeout_ms)),
                ],
                cwd=ROOT,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=_proxy_free_environment(),
            )
            stdout = process.stdout
            stderr_stream = process.stderr
            if stdout is None or stderr_stream is None or process.stdin is None:
                raise RuntimeError("HTTP/2 observer pipes were not created")
            ready_line = _readline_with_deadline(stdout, operation_deadline).strip()
            try:
                ready: Any = json.loads(ready_line)
            except json.JSONDecodeError as exc:
                raise RuntimeError("HTTP/2 observer emitted malformed ready JSON") from exc
            if not isinstance(ready, dict) or ready.get("status") != "ready":
                raise RuntimeError("HTTP/2 observer did not report a ready state")
            target = require_loopback_url(f"https://{HOST}:{int(ready['port'])}")
            clients: list[dict[str, Any]] = [
                _run_protocol_client("node-http2", target, operation_deadline),
                _run_protocol_client("browser-http2", target, operation_deadline),
            ]
            curl_supported, curl_version, curl = _curl_supports_http2(operation_deadline)
            if curl_supported and curl is not None:
                clients.append(_curl_http2_client(curl, curl_version, target, operation_deadline))
            else:
                clients.append(
                    {
                        "client": "curl-http2",
                        "status": "unsupported",
                        "runtime_version": curl_version,
                        "reason": "installed curl build does not report HTTP2 support",
                    }
                )
            violations = assert_no_non_loopback_page_requests(clients)
            _cleanup_observer_process(process, operation_deadline)
            if process.returncode != 0:
                raise RuntimeError("HTTP/2 observer failed or exceeded a configured cap")
            observations = _load_observer_output(output_path)
            observations["clients"] = clients
            observations["target"] = target
            observations["non_loopback_page_requests_observed"] = violations
            observations["cleanup"] = "temporary certificate and private key removed after the command"
            return observations
        finally:
            if process is not None:
                _cleanup_observer_process(process, operation_deadline)


def _join_client_results(
    clienthellos: list[dict[str, Any]], http2: dict[str, Any]
) -> list[dict[str, Any]]:
    h2_clients = {
        str(client.get("client")): client
        for client in http2.get("clients", [])
        if isinstance(client, dict)
    }
    session_by_client: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for session in http2.get("sessions", []):
        if not isinstance(session, dict):
            continue
        for client in session.get("clients", []):
            session_by_client[str(client)].append(session)

    rows: list[dict[str, Any]] = []
    hello_by_client = {str(item["client"]): item for item in clienthellos}
    mappings = (
        ("python-openssl", "python-openssl", None),
        ("curl", "curl", "curl-http2"),
        ("playwright-chromium", "playwright-chromium", "playwright-chromium"),
        ("node-http2", None, "node-http2"),
        ("manual-chrome-or-chromium", "manual-chrome-or-chromium", None),
    )
    for display, hello_name, h2_name in mappings:
        hello = hello_by_client.get(hello_name or "", {})
        h2_client = h2_clients.get(h2_name or "", {})
        sessions = session_by_client.get(h2_name or "", [])
        missing = ["HTTP/2 header order not exposed by the observer runtime"]
        if not hello or hello.get("status") != "observed":
            missing.append("ClientHello fields unsupported or not captured")
        if not sessions:
            missing.append("HTTP/2 remote settings and reuse not observed")
        runtime = str(hello.get("runtime_version") or h2_client.get("runtime_version") or "unavailable")
        remote_settings = sessions[0].get("remote_settings", {}) if sessions else {}
        reused = any(int(session.get("stream_count", 0)) >= 2 for session in sessions)
        rows.append(
            {
                "client": display,
                "runtime_version": runtime,
                "clienthello_fields_observed": (
                    "record/version, ciphers, extensions, groups, signatures, ALPN, SNI, bytes"
                    if hello.get("status") == "observed"
                    else "unsupported"
                ),
                "extension_order": hello.get("extension_ids", "unsupported"),
                "alpn_offers": hello.get("alpn_offers", "unsupported"),
                "negotiated_protocol": sessions[0].get("negotiated_alpn", "unsupported") if sessions else "unsupported",
                "http2_remote_settings": remote_settings or "missing",
                "reuse_observation": "two streams on one connection" if reused else "not observed",
                "unsupported_or_missing_fields": missing,
                "limitations": "grouping label only; fingerprint is not identity proof",
            }
        )
    return rows


def run_automated_comparison(
    wall_timeout: float = AUTOMATED_WALL_TIMEOUT_SECONDS,
    capture: Callable[[float], list[dict[str, Any]]] = capture_client_hellos,
    observe: Callable[[float], dict[str, Any]] = observe_http2,
) -> dict[str, Any]:
    """Run both observers, all supported clients, and cleanup in one bounded command."""
    if wall_timeout <= 0 or wall_timeout > AUTOMATED_WALL_TIMEOUT_SECONDS:
        raise ValueError(
            f"automated wall timeout must be within {AUTOMATED_WALL_TIMEOUT_SECONDS} seconds"
        )
    started = time.monotonic()
    deadline = started + wall_timeout
    remaining_seconds(deadline, "ClientHello comparison start")
    clienthellos = capture(deadline)
    remaining_seconds(deadline, "HTTP/2 comparison start")
    http2 = observe(deadline)
    remaining_seconds(deadline, "structured result assembly")
    page_violations = assert_no_non_loopback_page_requests(
        clienthellos
        + [
            client
            for client in http2.get("clients", [])
            if isinstance(client, dict)
        ]
    )
    return {
        "safety": {
            "bind": HOST,
            "configured_targets": "loopback only",
            "non_loopback_page_requests_observed": page_violations,
            "proxy_environment_inherited": False,
            "packet_level_external_traffic": "not measured",
            "max_connections_per_observer": MAX_CONNECTIONS,
            "max_http2_streams": MAX_HTTP2_STREAMS,
            "whole_command_wall_budget_seconds": wall_timeout,
            "raw_observer_connection_timeout_seconds": RAW_OBSERVER_TIMEOUT_SECONDS,
            "http2_observer_timeout_seconds": HTTP2_OBSERVER_TIMEOUT_SECONDS,
            "per_client_timeout_seconds": PER_CLIENT_TIMEOUT_SECONDS,
        },
        "clienthello_observations": clienthellos,
        "http2_observations": http2,
        "comparison_table": _join_client_results(clienthellos, http2),
        "labels": ["not JA4", "not identity proof"],
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "unsupported_capabilities": [
            "production JA4 parity",
            "universal browser fingerprinting",
            "HTTP/3 or QUIC capture",
            "real proxy-chain comparison",
            "commercial control conclusions",
            "HTTP/2 header order",
        ],
    }


def compare_client_hellos() -> dict[str, Any]:
    """Retain the earlier in-memory comparison while parsing real fields."""
    default = client_hello()
    with_alpn = client_hello(("h2", "http/1.1"))
    return {
        "default": summarize_client_hello(default, "python-default"),
        "with_alpn": summarize_client_hello(with_alpn, "python-alpn-h2-http11"),
        "bytes_differ": default != with_alpn,
        "changed": "ALPN configuration; random and session fields can also vary",
    }


def _format_cell(value: Any) -> str:
    rendered = json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else str(value)
    return rendered.replace("|", "\\|").replace("\n", " ")


def render_comparison_table(rows: list[dict[str, Any]]) -> str:
    """Render the learner-facing comparison as a Markdown table."""
    columns = [
        "client",
        "runtime_version",
        "clienthello_fields_observed",
        "extension_order",
        "alpn_offers",
        "negotiated_protocol",
        "http2_remote_settings",
        "reuse_observation",
        "unsupported_or_missing_fields",
        "limitations",
    ]
    lines = [
        "| " + " | ".join(column.replace("_", " ") for column in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    lines.extend(
        "| " + " | ".join(_format_cell(row[column]) for column in columns) + " |" for row in rows
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        choices=("clienthello-fixture", "clienthello", "http2", "automated"),
        nargs="?",
        default="automated",
    )
    args = parser.parse_args()
    if args.mode == "clienthello-fixture":
        print(json.dumps(compare_client_hellos(), indent=2, sort_keys=True))
        return 0
    if args.mode == "clienthello":
        print(json.dumps(capture_client_hellos(), indent=2, sort_keys=True))
        return 0
    if args.mode == "http2":
        print(json.dumps(observe_http2(), indent=2, sort_keys=True))
        return 0
    try:
        result = run_automated_comparison()
    except ProtocolDeadlineExceeded as exc:
        print(f"Protocol comparison timeout: {exc}", file=sys.stderr)
        return 2
    except ProtocolSafetyError as exc:
        print(f"Protocol comparison safety failure: {exc}", file=sys.stderr)
        return 3
    print(render_comparison_table(result["comparison_table"]))
    print("\nStructured observations:\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
