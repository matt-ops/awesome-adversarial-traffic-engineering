"""A bounded standard-library client for the local AATE application."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
import urllib.error
import urllib.request
from dataclasses import asdict
from email.message import Message
from typing import Any

from lab.safety import LoadEnvelope, SafetyError, validate_course_client_url

MAX_REQUEST_TIMEOUT_SECONDS = 2.0
DURATION_BUDGET_ERROR = "duration_budget_exceeded"


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Make every 3xx response a hard boundary failure instead of another hop."""

    def redirect_request(
        self,
        request: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Message,
        newurl: str,
    ) -> urllib.request.Request | None:
        del request, fp, code, msg, headers
        raise SafetyError(f"redirects are not allowed for the course client: {newurl}")


def _validated_timeout(timeout_seconds: float) -> float:
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
        or timeout_seconds > MAX_REQUEST_TIMEOUT_SECONDS
    ):
        raise SafetyError(f"timeout_seconds must be greater than 0 and at most {MAX_REQUEST_TIMEOUT_SECONDS:g}")
    return float(timeout_seconds)


def fetch_once(url: str, timeout_seconds: float = 2.0) -> dict[str, object]:
    validate_course_client_url(url)
    timeout_seconds = _validated_timeout(timeout_seconds)
    request = urllib.request.Request(  # noqa: S310 - URL scheme and hostname validated above.
        url, headers={"User-Agent": "aate-safe-client/0.1"}
    )
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        RejectRedirects(),
    )
    started = time.monotonic()
    try:
        with opener.open(request, timeout=timeout_seconds) as response:  # noqa: S310 - validated fixed local origin
            body = response.read(4096).decode("utf-8", errors="replace")
            return {
                "ok": True,
                "status": response.status,
                "elapsed_ms": round((time.monotonic() - started) * 1000, 2),
                "body": body,
            }
    except urllib.error.HTTPError as exc:
        if 300 <= exc.code < 400:
            location = exc.headers.get("Location", "")
            raise SafetyError(f"redirects are not allowed for the course client: {location}") from exc
        body = exc.read(4096).decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": exc.code,
            "elapsed_ms": round((time.monotonic() - started) * 1000, 2),
            "body": body,
        }
    except (urllib.error.URLError, TimeoutError) as exc:
        return {
            "ok": False,
            "error": type(exc).__name__,
            "elapsed_ms": round((time.monotonic() - started) * 1000, 2),
        }


def run(url: str, envelope: LoadEnvelope, *, dry_run: bool, seed: int = 20260714) -> list[dict[str, object]]:
    validate_course_client_url(url)
    envelope.validate()
    if dry_run:
        print(json.dumps({"target": url, "envelope": asdict(envelope), "dry_run": True}, indent=2))
        return []

    rng = random.Random(seed)  # noqa: S311 - deterministic timing fixture, not a security token.
    results: list[dict[str, object]] = []
    interval = 1 / envelope.requests_per_second
    monotonic_start = time.monotonic()
    deadline = monotonic_start + envelope.duration_seconds
    for index in range(envelope.total_requests):
        request_start = time.monotonic()
        remaining_seconds = deadline - request_start
        if remaining_seconds <= 0:
            results.append(
                {
                    "ok": False,
                    "error": DURATION_BUDGET_ERROR,
                    "duration_budget_exceeded": True,
                    "request_started": False,
                    "sequence": index,
                    "elapsed_ms": round((request_start - monotonic_start) * 1000, 2),
                }
            )
            break

        result = fetch_once(url, timeout_seconds=min(MAX_REQUEST_TIMEOUT_SECONDS, remaining_seconds))
        result["sequence"] = index
        request_end = time.monotonic()
        if request_end >= deadline:
            prior_error = result.get("error")
            result["ok"] = False
            result["error"] = DURATION_BUDGET_ERROR
            result["duration_budget_exceeded"] = True
            result["request_started"] = True
            result["elapsed_budget_ms"] = round((request_end - monotonic_start) * 1000, 2)
            if prior_error is not None:
                result["request_error"] = prior_error
            results.append(result)
            break

        results.append(result)
        if index + 1 < envelope.total_requests:
            delay = interval + rng.uniform(0, min(0.05, interval / 4))
            time.sleep(min(delay, max(0.0, deadline - request_end)))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="http://localhost:8080/health")
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--rps", type=int, default=2)
    parser.add_argument("--total", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        envelope = LoadEnvelope(duration_seconds=args.duration, requests_per_second=args.rps, total_requests=args.total)
        results = run(args.target, envelope, dry_run=args.dry_run)
    except SafetyError as exc:
        print(json.dumps({"error": str(exc), "rejected": True}))
        return 2
    for result in results:
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
