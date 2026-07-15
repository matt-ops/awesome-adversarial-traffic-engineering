"""Non-bypassable local-target and load-envelope validation."""

from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_address
from urllib.parse import urlsplit

APPROVED_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "app", "edge", "aate-app", "aate-edge"})


class SafetyError(ValueError):
    """Raised when a requested local experiment violates a hard safety boundary."""


def validate_local_url(url: str) -> str:
    """Return *url* only when it names an explicitly approved local target."""

    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise SafetyError(f"invalid target URL: {exc}") from exc

    if parsed.scheme not in {"http", "https"}:
        raise SafetyError("target scheme must be http or https")
    if not parsed.hostname:
        raise SafetyError("target must include a hostname")
    if parsed.username or parsed.password:
        raise SafetyError("target credentials are not allowed")
    if port is not None and not 1 <= port <= 65535:
        raise SafetyError("target port is outside the valid range")

    host = parsed.hostname.lower().rstrip(".")
    if host in APPROVED_HOSTS:
        return url

    try:
        address = ip_address(host)
    except ValueError:
        address = None
    if address is not None:
        raise SafetyError(f"IP address {host!r} is not an approved loopback target")
    raise SafetyError(f"hostname {host!r} is not an approved local service")


@dataclass(frozen=True)
class LoadEnvelope:
    """Hard ceilings for educational application-layer traffic."""

    duration_seconds: int = 5
    concurrency: int = 1
    requests_per_second: int = 2
    total_requests: int = 10
    expensive_requests: int = 0

    MAX_DURATION_SECONDS = 15
    MAX_CONCURRENCY = 5
    MAX_REQUESTS_PER_SECOND = 10
    MAX_TOTAL_REQUESTS = 100
    MAX_EXPENSIVE_REQUESTS = 20

    def validate(self) -> "LoadEnvelope":
        values = {
            "duration_seconds": self.duration_seconds,
            "concurrency": self.concurrency,
            "requests_per_second": self.requests_per_second,
            "total_requests": self.total_requests,
            "expensive_requests": self.expensive_requests,
        }
        if any(not isinstance(value, int) or isinstance(value, bool) for value in values.values()):
            raise SafetyError("all load-envelope values must be integers")
        if self.duration_seconds < 1 or self.duration_seconds > self.MAX_DURATION_SECONDS:
            raise SafetyError(f"duration_seconds must be 1..{self.MAX_DURATION_SECONDS}")
        if self.concurrency < 1 or self.concurrency > self.MAX_CONCURRENCY:
            raise SafetyError(f"concurrency must be 1..{self.MAX_CONCURRENCY}")
        if self.requests_per_second < 1 or self.requests_per_second > self.MAX_REQUESTS_PER_SECOND:
            raise SafetyError(f"requests_per_second must be 1..{self.MAX_REQUESTS_PER_SECOND}")
        if self.total_requests < 1 or self.total_requests > self.MAX_TOTAL_REQUESTS:
            raise SafetyError(f"total_requests must be 1..{self.MAX_TOTAL_REQUESTS}")
        if self.expensive_requests < 0 or self.expensive_requests > self.MAX_EXPENSIVE_REQUESTS:
            raise SafetyError(f"expensive_requests must be 0..{self.MAX_EXPENSIVE_REQUESTS}")
        if self.expensive_requests > self.total_requests:
            raise SafetyError("expensive_requests cannot exceed total_requests")
        if self.total_requests > self.duration_seconds * self.requests_per_second:
            raise SafetyError("total_requests exceeds the duration/rate envelope")
        return self

