"""Validate the remediation source ledger and lesson-level attribution contract."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "sources" / "sources.yaml"
LESSON_ROOT = ROOT / "docs" / "modules"
PROVENANCE_FILES = (
    ROOT / "docs" / "methodology" / "provenance.md",
    ROOT / "sources" / "methodology-provenance.md",
)
PROVENANCE_STATEMENT = (
    "The complete AATE loop is a course synthesis. It is not quoted verbatim from "
    "a single industry standard."
)

SOURCE_TYPES = {
    "STANDARD",
    "OFFICIAL_DOCUMENTATION",
    "PEER_REVIEWED_RESEARCH",
    "PREPRINT_RESEARCH",
    "PROJECT_DOCUMENTATION",
    "VENDOR_RESEARCH",
    "COURSE_SYNTHESIS",
    "LAB_SPECIFIC",
    "VERSION_SENSITIVE",
    "PRACTITIONER_PERSPECTIVE",
    "UNVERIFIED",
}
REQUIRED_FIELDS = {
    "id",
    "title",
    "url",
    "source_type",
    "publisher",
    "version_or_accessed",
    "last_content_reviewed",
    "last_link_checked",
    "assigned_sections",
    "supports",
    "limitations",
    "modules",
}
REQUIRED_SOURCE_IDS = {
    "nist-sp-800-115",
    "mitre-adversary-emulation-plans",
    "mdn-http-overview",
    "chrome-devtools-network",
    "chrome-browser-process-model",
    "mdn-dom",
    "tau-javascript-introduction",
    "mdn-promises",
    "mdn-async-function",
    "mdn-try-catch",
    "mdn-using-fetch",
    "microsoft-learn-playwright",
    "playwright-browser-contexts",
    "playwright-network",
    "playwright-auth",
    "fpscanner-project",
    "rebrowser-bot-detector",
    "fp-inconsistent",
    "gummy-browsers",
    "ja4-project",
    "rfc-8446",
    "rfc-9113",
    "rfc-9114",
    "rfc-9000",
    "cloudflare-ddos-introduction",
    "aws-waf-app-layer-ddos",
    "aws-waf-rate-based-rules",
    "aws-builders-library-load-shedding",
    "k6-thresholds",
    "aate-adversarial-control-loop",
    "aate-local-lab",
}
SOURCE_COMMENT = re.compile(r"<!--\s*source-ids:\s*([^>]+?)\s*-->", re.IGNORECASE)
SOURCE_HEADER = "| Type | Source | Exact assigned area | What it supports | Limitation |"


def load_ledger() -> list[dict[str, Any]]:
    raw = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("sources/sources.yaml must contain a top-level list")
    if not all(isinstance(item, dict) for item in raw):
        raise ValueError("every source entry must be a mapping")
    return raw


def lesson_files() -> list[Path]:
    return sorted(path for path in LESSON_ROOT.glob("*/*.md") if path.name != "index.md")


def cited_ids(text: str) -> list[str]:
    match = SOURCE_COMMENT.search(text)
    return [] if match is None else [part.strip() for part in match.group(1).split(",") if part.strip()]


def source_rows(text: str) -> list[list[str]]:
    match = re.search(r"## Source basis\n\n(?P<body>.*?)\n\n## Mental model", text, re.DOTALL)
    if match is None:
        return []
    lines = [line for line in match.group("body").splitlines() if line.startswith("|")]
    rows: list[list[str]] = []
    for line in lines[2:]:
        rows.append([cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))])
    return rows


def main() -> int:
    errors: list[str] = []
    try:
        entries = load_ledger()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Source validation: FAIL\n- {exc}")
        return 1

    by_id: dict[str, dict[str, Any]] = {}
    today = dt.date.today()
    for index, entry in enumerate(entries, start=1):
        missing = sorted(REQUIRED_FIELDS - entry.keys())
        if missing:
            errors.append(f"entry {index}: missing fields: {', '.join(missing)}")
            continue
        source_id = entry.get("id")
        if not isinstance(source_id, str) or re.fullmatch(r"[a-z0-9][a-z0-9-]*", source_id) is None:
            errors.append(f"entry {index}: invalid id: {source_id!r}")
            continue
        if source_id in by_id:
            errors.append(f"duplicate source id: {source_id}")
        by_id[source_id] = entry
        if entry.get("source_type") not in SOURCE_TYPES:
            errors.append(f"{source_id}: invalid source_type: {entry.get('source_type')!r}")
        for field in ("title", "url", "publisher", "version_or_accessed"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{source_id}: {field} must be a non-empty string")
        for field in ("assigned_sections", "supports", "limitations", "modules"):
            value = entry.get(field)
            if (
                not isinstance(value, list)
                or not value
                or any(not isinstance(item, str) or not item.strip() for item in value)
            ):
                errors.append(f"{source_id}: {field} must be a non-empty string list")
        for date_field in ("last_content_reviewed", "last_link_checked"):
            date_value = entry.get(date_field)
            date_text = date_value if isinstance(date_value, str) else ""
            if date_field == "last_link_checked" and entry.get("source_type") in {"COURSE_SYNTHESIS", "LAB_SPECIFIC"}:
                if date_text != "not-applicable":
                    errors.append(f"{source_id}: local source last_link_checked must be not-applicable")
                continue
            try:
                checked_date = dt.date.fromisoformat(date_text)
                if checked_date > today:
                    errors.append(f"{source_id}: {date_field} is in the future: {date_value}")
            except (TypeError, ValueError):
                errors.append(f"{source_id}: {date_field} must use YYYY-MM-DD")
        if "published_or_updated" in entry or "last_verified" in entry:
            errors.append(f"{source_id}: legacy source-review metadata fields are prohibited")
        if entry.get("source_type") == "STANDARD" and source_id == "mitre-adversary-emulation-plans":
            errors.append(f"{source_id}: project guidance must not be classified as a formal standard")
        url = str(entry.get("url", ""))
        if entry.get("source_type") not in {"COURSE_SYNTHESIS", "LAB_SPECIFIC"}:
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{source_id}: external source requires an HTTP(S) URL")
        if "amazon.jobs" in url.casefold() or "leadership principles" in str(entry.get("title", "")).casefold():
            errors.append(f"{source_id}: employer-specific material is prohibited in the generic course")

    missing_required = sorted(REQUIRED_SOURCE_IDS - by_id.keys())
    for source_id in missing_required:
        errors.append(f"required remediation source is absent: {source_id}")

    for provenance_file in PROVENANCE_FILES:
        try:
            provenance = provenance_file.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{provenance_file.relative_to(ROOT)}: cannot read provenance file: {exc}")
            continue
        normalized = " ".join(provenance.replace(">", " ").split())
        if PROVENANCE_STATEMENT not in normalized:
            errors.append(
                f"{provenance_file.relative_to(ROOT)}: missing exact course-synthesis provenance statement"
            )
        if provenance_file == PROVENANCE_FILES[0]:
            step_rows = re.findall(r"^\|\s*(\d+)\.", provenance, re.MULTILINE)
            if step_rows != [str(number) for number in range(1, 16)]:
                errors.append(
                    f"{provenance_file.relative_to(ROOT)}: provenance map must contain ordered steps 1 through 15"
                )

    for lesson in lesson_files():
        text = lesson.read_text(encoding="utf-8")
        relative = lesson.relative_to(ROOT)
        ids = cited_ids(text)
        if not ids:
            errors.append(f"{relative}: missing source-ids comment")
            continue
        if len(ids) != len(set(ids)):
            errors.append(f"{relative}: duplicate source id in source-ids comment")
        unknown = sorted(set(ids) - by_id.keys())
        for source_id in unknown:
            errors.append(f"{relative}: source id is absent from ledger: {source_id}")
        if text.count(SOURCE_HEADER) != 1:
            errors.append(f"{relative}: Source basis must use the exact five-column header")
        rows = source_rows(text)
        if len(rows) != len(ids):
            errors.append(f"{relative}: {len(ids)} cited IDs require {len(ids)} source rows; found {len(rows)}")
        for row_number, row in enumerate(rows, start=1):
            if len(row) != 5:
                errors.append(f"{relative}: source row {row_number} has {len(row)} cells; expected 5")
                continue
            source_type, source, area, support, limitation = row
            if source_type not in SOURCE_TYPES:
                errors.append(f"{relative}: source row {row_number} has invalid type {source_type!r}")
            for label, value in (
                ("source", source),
                ("assigned area", area),
                ("support", support),
                ("limitation", limitation),
            ):
                if not value.strip():
                    errors.append(f"{relative}: source row {row_number} has empty {label}")
        known_entries = [by_id[source_id] for source_id in ids if source_id in by_id]
        if any(entry["source_type"] == "COURSE_SYNTHESIS" for entry in known_entries):
            if "**COURSE_SYNTHESIS:**" not in text or "Course synthesis" not in text:
                errors.append(f"{relative}: course synthesis must be visibly labeled")
        if any(entry["source_type"] == "LAB_SPECIFIC" for entry in known_entries) and "LAB_SPECIFIC" not in text:
            source_block = re.search(r"## Source basis\n\n.*?\n\n## Mental model", text, re.DOTALL)
            if source_block is None or "LAB_SPECIFIC" not in source_block.group(0):
                errors.append(f"{relative}: lab-specific behavior must be visibly labeled")
        has_version_sensitive_source = any(
            entry["source_type"] == "VERSION_SENSITIVE" for entry in known_entries
        )
        if has_version_sensitive_source and "VERSION_SENSITIVE" not in text:
            errors.append(f"{relative}: version-sensitive evidence must be visibly labeled")
        if re.search(r"^- Depth: Foundation\s*$", text, re.MULTILINE | re.IGNORECASE):
            for entry in known_entries:
                if entry["source_type"] == "UNVERIFIED":
                    errors.append(f"{relative}: Foundation cannot require UNVERIFIED source {entry['id']}")

    if errors:
        print("Source validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Source validation: PASS")
    print(f"- {len(entries)} unique ledger entries with complete schema")
    print(f"- {len(lesson_files())} lessons have one traceable five-column row per cited source")
    print(f"- all {len(REQUIRED_SOURCE_IDS)} mandated source IDs are present")
    print("- synthesis, lab-specific, version-sensitive, Foundation, and 15-step provenance rules pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
