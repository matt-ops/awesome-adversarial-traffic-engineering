"""Check Markdown internal links and optionally classify external link failures."""

from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    files = list((ROOT / "docs").rglob("*.md")) if (ROOT / "docs").exists() else []
    for relative in ("README.md", "lab/README.md", "sources/README.md", "sources/methodology-provenance.md"):
        path = ROOT / relative
        if path.exists():
            files.append(path)
    return sorted(set(files))


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^a-z0-9 _-]", "", value.casefold()).strip().replace(" ", "-")
    return re.sub(r"-+", "-", value)


def anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    found = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    found.update(slugify(heading) for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE))
    return found


def classify_external(url: str) -> tuple[str, str]:
    request = urllib.request.Request(  # noqa: S310 - caller supplies only validated HTTP(S) Markdown links.
        url, headers={"User-Agent": "aate-link-check/1.0"}, method="HEAD"
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:  # noqa: S310 - explicit public link check
            return "ok", str(response.status)
    except urllib.error.HTTPError as exc:
        if exc.code in {401, 403, 405, 429} or 500 <= exc.code <= 599:
            return "transient", str(exc.code)
        return "broken", str(exc.code)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return "transient", type(exc).__name__


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", action="store_true", help="also check remote URLs; transient failures only warn")
    args = parser.parse_args()
    errors: list[str] = []
    warnings: list[str] = []
    external_urls: set[str] = set()

    for source in markdown_files():
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("mailto:", "#")):
                if target.startswith("#") and target[1:] not in anchors(source):
                    errors.append(f"{source.relative_to(ROOT)}: missing anchor {target}")
                continue
            if target.startswith(("http://", "https://")):
                parsed = urlsplit(target)
                if not parsed.netloc:
                    errors.append(f"{source.relative_to(ROOT)}: malformed external URL {target}")
                external_urls.add(target)
                continue
            path_text, _, anchor = target.partition("#")
            destination = (source.parent / path_text).resolve() if path_text else source.resolve()
            try:
                destination.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{source.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if destination.is_dir():
                destination = destination / "index.md"
            if not destination.is_file():
                errors.append(f"{source.relative_to(ROOT)}: missing file {target}")
            elif anchor and anchor not in anchors(destination):
                errors.append(f"{source.relative_to(ROOT)}: missing anchor {target}")

    if args.external:
        for url in sorted(external_urls):
            category, detail = classify_external(url)
            if category == "broken":
                errors.append(f"external link returned permanent failure {detail}: {url}")
            elif category == "transient":
                warnings.append(f"external link could not be conclusively verified ({detail}): {url}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print("Internal link validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Internal link validation: PASS")
    print(f"- checked {len(markdown_files())} Markdown files")
    if args.external:
        print(f"- checked {len(external_urls)} external URLs; transient failures were warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
