"""A bounded standard-library client for the local AATE application."""

from __future__ import annotations

import argparse
import json
import random
import time
import urllib.error
import urllib.request
from dataclasses import asdict

from lab.safety import LoadEnvelope, SafetyError, validate_local_url


def fetch_once(url: str, timeout_seconds: float = 2.0) -> dict[str, object]:
    validate_local_url(url)
    request = urllib.request.Request(  # noqa: S310 - URL scheme and hostname validated above.
        url, headers={"User-Agent": "aate-safe-client/0.1"}
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - validated URL
            body = response.read(4096).decode("utf-8", errors="replace")
            return {
                "ok": True,
                "status": response.status,
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                "body": body,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(4096).decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": exc.code,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
            "body": body,
        }
    except (urllib.error.URLError, TimeoutError) as exc:
        return {
            "ok": False,
            "error": type(exc).__name__,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        }


def run(url: str, envelope: LoadEnvelope, *, dry_run: bool, seed: int = 20260714) -> list[dict[str, object]]:
    validate_local_url(url)
    envelope.validate()
    if dry_run:
        print(json.dumps({"target": url, "envelope": asdict(envelope), "dry_run": True}, indent=2))
        return []

    rng = random.Random(seed)  # noqa: S311 - deterministic timing fixture, not a security token.
    results: list[dict[str, object]] = []
    interval = 1 / envelope.requests_per_second
    for index in range(envelope.total_requests):
        result = fetch_once(url)
        result["sequence"] = index
        results.append(result)
        if index + 1 < envelope.total_requests:
            time.sleep(interval + rng.uniform(0, min(0.05, interval / 4)))
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
