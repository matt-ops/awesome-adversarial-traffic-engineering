"""Classify every external source-ledger URL without treating transients as permanent failures."""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "sources" / "sources.yaml"
REDIRECT_STATUSES = {301, 302, 303, 307, 308}
PERMANENT_NOT_FOUND_STATUSES = {404, 410}
TEMPORARY_SERVER_STATUSES = {408, 425, 429, 500, 502, 503, 504}


@dataclass(frozen=True)
class LinkResult:
    source_id: str
    url: str
    category: str
    http_status: int | None = None
    detail: str = ""
    redirect_target: str | None = None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Surface redirects as responses so they can be recorded explicitly."""

    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: Any,
        code: int,
        message: str,
        headers: Any,
        new_url: str,
    ) -> None:
        return None


def classify_http_status(status: int) -> str:
    if 200 <= status < 300:
        return "successful_response"
    if status in REDIRECT_STATUSES:
        return "redirect"
    if status in PERMANENT_NOT_FOUND_STATUSES:
        return "permanent_not_found"
    if status in TEMPORARY_SERVER_STATUSES or 500 <= status < 600:
        return "temporary_server_error"
    return "client_error"


def valid_http_url(url: str) -> bool:
    try:
        parsed = urlsplit(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and parsed.username is None
    except ValueError:
        return False


def check_url(source_id: str, url: str, timeout_seconds: float) -> LinkResult:
    if not valid_http_url(url):
        return LinkResult(source_id, url, "malformed_url", detail="expected an HTTP(S) URL without user info")
    request = urllib.request.Request(  # noqa: S310 - URL is restricted to validated HTTP(S).
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.5",
            "Range": "bytes=0-1023",
            "User-Agent": "AATE-Link-Review/1.0 (+local release validation)",
        },
        method="GET",
    )
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            status = int(response.status)
            return LinkResult(source_id, url, classify_http_status(status), http_status=status)
    except urllib.error.HTTPError as exc:
        status = int(exc.code)
        return LinkResult(
            source_id,
            url,
            classify_http_status(status),
            http_status=status,
            detail=str(exc.reason),
            redirect_target=exc.headers.get("Location") if status in REDIRECT_STATUSES else None,
        )
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            return LinkResult(source_id, url, "dns_failure", detail=str(reason))
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return LinkResult(source_id, url, "timeout", detail=str(reason))
        if isinstance(reason, ssl.SSLError):
            return LinkResult(source_id, url, "tls_error", detail=str(reason))
        return LinkResult(source_id, url, "network_error", detail=str(reason))
    except (TimeoutError, socket.timeout) as exc:
        return LinkResult(source_id, url, "timeout", detail=str(exc))
    except (ValueError, OSError) as exc:
        return LinkResult(source_id, url, "network_error", detail=str(exc))


def load_sources() -> list[tuple[str, str]]:
    raw = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("sources/sources.yaml must contain a top-level list")
    sources: list[tuple[str, str]] = []
    for entry in raw:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str) or not isinstance(entry.get("url"), str):
            raise ValueError("every source entry must contain string id and url fields")
        if entry.get("source_type") not in {"COURSE_SYNTHESIS", "LAB_SPECIFIC"}:
            sources.append((entry["id"], entry["url"]))
    return sources


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=12.0, help="Per-request timeout in seconds")
    parser.add_argument("--workers", type=int, default=8, help="Maximum concurrent link checks")
    parser.add_argument("--output", type=Path, help="Optional JSON result path")
    parser.add_argument(
        "--fail-on-permanent",
        action="store_true",
        help="Exit nonzero for malformed URLs or permanent not-found responses; transients remain warnings",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sources = load_sources()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = sorted(
            executor.map(lambda item: check_url(item[0], item[1], args.timeout), sources),
            key=lambda result: result.source_id,
        )
    for result in results:
        status = "" if result.http_status is None else f" HTTP {result.http_status}"
        target = "" if result.redirect_target is None else f" -> {result.redirect_target}"
        detail = "" if not result.detail else f" ({result.detail})"
        print(f"{result.category:24} {result.source_id}{status}{target}{detail}")
    counts = Counter(result.category for result in results)
    print("External-link classification summary")
    for category, count in sorted(counts.items()):
        print(f"- {category}: {count}")
    print("- transient DNS, timeout, TLS, network, rate-limit, and server errors do not fail this command")

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "policy": "Only malformed URLs and permanent not-found responses can fail --fail-on-permanent.",
            "counts": dict(sorted(counts.items())),
            "results": [asdict(result) for result in results],
        }
        args.output.write_text(f"{json.dumps(payload, indent=2)}\n", encoding="utf-8")

    permanent = [result for result in results if result.category in {"malformed_url", "permanent_not_found"}]
    return 1 if args.fail_on_permanent and permanent else 0


if __name__ == "__main__":
    raise SystemExit(main())
