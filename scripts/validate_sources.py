"""Validate the AATE source ledger and lesson source references."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "sources" / "sources.yaml"
LESSON_ROOT = ROOT / "docs" / "modules"

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
    "published_or_updated",
    "last_verified",
    "assigned_sections",
    "supports",
    "limitations",
    "modules",
}
SOURCE_COMMENT = re.compile(r"<!--\s*source-ids:\s*([^>]+?)\s*-->", re.IGNORECASE)


def load_ledger() -> list[dict[str, Any]]:
    raw = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("sources/sources.yaml must contain a top-level list")
    entries: list[dict[str, Any]] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"source entry {index} must be a mapping")
        entries.append(item)
    return entries


def lesson_files() -> list[Path]:
    if not LESSON_ROOT.exists():
        return []
    return sorted(path for path in LESSON_ROOT.glob("*/*.md") if path.name != "index.md")


def cited_ids(text: str) -> list[str]:
    match = SOURCE_COMMENT.search(text)
    if match is None:
        return []
    return [part.strip() for part in match.group(1).split(",") if part.strip()]


def main() -> int:
    errors: list[str] = []
    try:
        entries = load_ledger()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Source validation: FAIL\n- {exc}")
        return 1

    by_id: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries, start=1):
        missing = sorted(REQUIRED_FIELDS - entry.keys())
        if missing:
            errors.append(f"entry {index}: missing fields: {', '.join(missing)}")
            continue
        source_id = entry.get("id")
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", source_id):
            errors.append(f"entry {index}: invalid id: {source_id!r}")
            continue
        if source_id in by_id:
            errors.append(f"duplicate source id: {source_id}")
        by_id[source_id] = entry
        if entry.get("source_type") not in SOURCE_TYPES:
            errors.append(f"{source_id}: invalid source_type: {entry.get('source_type')!r}")
        for field in ("title", "url", "publisher", "published_or_updated", "last_verified"):
            if entry.get(field) in (None, ""):
                errors.append(f"{source_id}: {field} must not be empty")
        for field in ("assigned_sections", "supports", "limitations", "modules"):
            value = entry.get(field)
            if not isinstance(value, list) or not value or any(item in (None, "") for item in value):
                errors.append(f"{source_id}: {field} must be a non-empty list")

    for lesson in lesson_files():
        text = lesson.read_text(encoding="utf-8")
        ids = cited_ids(text)
        relative = lesson.relative_to(ROOT)
        if not ids:
            errors.append(f"{relative}: missing source-ids comment")
            continue
        unknown = sorted(set(ids) - by_id.keys())
        for source_id in unknown:
            errors.append(f"{relative}: cited source id is absent from ledger: {source_id}")
        known_entries = [by_id[source_id] for source_id in ids if source_id in by_id]
        if "COURSE_SYNTHESIS" in text:
            if not any(entry["source_type"] == "COURSE_SYNTHESIS" for entry in known_entries):
                errors.append(f"{relative}: COURSE_SYNTHESIS used without a synthesis source")
            if "Course synthesis" not in text:
                errors.append(f"{relative}: COURSE_SYNTHESIS must be visibly labeled as Course synthesis")
        if re.search(r"^>?\s*Depth:\s*Foundation\s*$", text, re.MULTILINE | re.IGNORECASE):
            for entry in known_entries:
                if entry["source_type"] == "UNVERIFIED":
                    errors.append(f"{relative}: Foundation cannot require UNVERIFIED source {entry['id']}")

    if errors:
        print("Source validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Source validation: PASS")
    print(f"- {len(entries)} unique ledger entries")
    print(f"- {len(lesson_files())} lesson source blocks resolve")
    print("- source types, assigned sections, synthesis labels, and Foundation verification are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
