"""Run bounded telemetry, concurrency, and retry exercises on local fixtures."""

from __future__ import annotations

import argparse
import asyncio
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from lab.analysis.analyze import load_jsonl
from lab.clients.safe_client import fetch_once
from lab.safety import LoadEnvelope, validate_local_url

RETRYABLE_STATUS = frozenset({429, 502, 503, 504})


def summarize(records: list[dict[str, Any]]) -> dict[str, object]:
    """Return transparent counts without assigning identity or intent."""

    populations = Counter(str(record.get("population", "unknown")) for record in records)
    abuse_labels = Counter(bool(record.get("is_abuse", False)) for record in records)
    return {
        "records": len(records),
        "populations": dict(sorted(populations.items())),
        "labels": {"abuse": abuse_labels[True], "benign": abuse_labels[False]},
        "limitations": [
            "Counts describe a small synthetic fixture.",
            "A population label is not proof of identity or intent.",
        ],
    }


async def bounded_fetch(url: str, *, total: int, concurrency: int) -> list[dict[str, object]]:
    """Fetch a local URL with explicit total-work and in-flight ceilings."""

    validate_local_url(url)
    LoadEnvelope(
        duration_seconds=15,
        concurrency=concurrency,
        requests_per_second=10,
        total_requests=total,
    ).validate()
    semaphore = asyncio.Semaphore(concurrency)

    async def one(sequence: int) -> dict[str, object]:
        async with semaphore:
            result = await asyncio.to_thread(fetch_once, url, 2.0)
            return {"sequence": sequence, **result}

    return await asyncio.gather(*(one(sequence) for sequence in range(total)))


async def fetch_with_retry(
    url: str,
    *,
    attempts: int = 3,
    timeout_seconds: float = 2.0,
    base_delay_seconds: float = 0.05,
    seed: int = 20260715,
) -> list[dict[str, object]]:
    """Retry a local request within one explicit attempt and delay budget."""

    validate_local_url(url)
    if attempts < 1 or attempts > 3:
        raise ValueError("attempts must be 1..3")
    if timeout_seconds <= 0 or timeout_seconds > 2:
        raise ValueError("timeout_seconds must be greater than 0 and at most 2")
    if base_delay_seconds < 0 or base_delay_seconds > 0.25:
        raise ValueError("base_delay_seconds must be 0..0.25")

    rng = random.Random(seed)  # noqa: S311 - deterministic scheduling fixture.
    events: list[dict[str, object]] = []
    for attempt in range(1, attempts + 1):
        result = await asyncio.to_thread(fetch_once, url, timeout_seconds)
        retryable = not result.get("ok", False) and (
            result.get("status") in RETRYABLE_STATUS or "status" not in result
        )
        event = {"attempt": attempt, "retryable": retryable, **result}
        events.append(event)
        if result.get("ok", False) or not retryable or attempt == attempts:
            break
        delay = min(base_delay_seconds * (2 ** (attempt - 1)), 0.25)
        delay += rng.uniform(0, delay / 2 if delay else 0)
        event["next_delay_ms"] = round(delay * 1000, 2)
        await asyncio.sleep(delay)
    return events


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    telemetry = commands.add_parser("telemetry", help="summarize a JSONL fixture")
    telemetry.add_argument("fixture", nargs="?", type=Path, default=Path("lab/fixtures/requests.jsonl"))

    concurrent = commands.add_parser("concurrent", help="run bounded local requests")
    concurrent.add_argument("--target", default="http://localhost:8080/health")
    concurrent.add_argument("--total", type=int, default=6)
    concurrent.add_argument("--concurrency", type=int, default=2)

    retry = commands.add_parser("retry", help="observe a bounded local retry")
    retry.add_argument("--target", default="http://localhost:8080/api/reports/unstable")
    retry.add_argument("--attempts", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "telemetry":
        output: object = summarize(load_jsonl(args.fixture))
    elif args.command == "concurrent":
        output = asyncio.run(bounded_fetch(args.target, total=args.total, concurrency=args.concurrency))
    else:
        output = asyncio.run(fetch_with_retry(args.target, attempts=args.attempts))
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
