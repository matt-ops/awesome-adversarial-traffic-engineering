"""Validate canonical curriculum metadata, dependencies, and checkpoints."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "curriculum" / "manifest.yaml"
LESSON_ROOT = ROOT / "docs" / "modules"
SOURCE_LEDGER = ROOT / "sources" / "sources.yaml"
REQUIRED_LESSON_FIELDS = {
    "id",
    "path",
    "module",
    "title",
    "depth",
    "estimated_minutes",
    "prerequisites",
    "required_artifacts",
    "source_ids",
}
REQUIRED_INDEX_FIELDS = {"id", "path", "module", "title", "lesson_ids"}
REQUIRED_CHECKPOINT_FIELDS = {
    "id",
    "path",
    "title",
    "depth_ceiling",
    "target_minutes",
    "lesson_ids",
    "required_artifacts",
    "capability_claim",
}
CHECKPOINT_HEADINGS = (
    "## Direct capability selection",
    "## Required lessons",
    "## Required artifacts",
    "## Capability claim",
    "## What this does not claim",
    "## Exit gate",
)


@dataclass(frozen=True)
class CheckpointStats:
    """Direct-selection and from-zero prerequisite-closure totals."""

    direct_lesson_count: int
    direct_selection_minutes: int
    closure_lesson_ids: frozenset[str]
    prerequisite_closure_minutes: int


def as_mapping(value: object, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label}: expected a mapping")
        return {}
    return value


def as_list(value: object, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label}: expected a list")
        return []
    return value


def load_yaml(path: Path, errors: list[str]) -> object:
    if not path.is_file():
        errors.append(f"missing YAML file: {path.relative_to(ROOT)}")
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return {}


def canonical_lesson_files() -> list[Path]:
    return sorted(path for path in LESSON_ROOT.glob("*/*.md") if path.name != "index.md")


def canonical_module_indexes() -> list[Path]:
    return sorted(LESSON_ROOT.glob("*/index.md"))


def visible_field(text: str, labels: tuple[str, ...]) -> str | None:
    alternatives = "|".join(re.escape(label) for label in labels)
    match = re.search(
        rf"^(?:>\s*)?(?:-\s*)?(?:{alternatives}):\s*(.+?)\s*$",
        text,
        re.MULTILINE,
    )
    if match is None:
        return None
    return match.group(1).strip().strip("`").rstrip()


def visible_minutes(value: str | None) -> int | None:
    if value is None:
        return None
    minute_match = re.match(r"(\d+)\s+minutes?", value, re.IGNORECASE)
    if minute_match:
        return int(minute_match.group(1))
    hour_match = re.match(r"(\d+)\s+hours?", value, re.IGNORECASE)
    if hour_match:
        return int(hour_match.group(1)) * 60
    return None


def source_ids_from_lesson(text: str) -> list[str]:
    match = re.search(r"<!-- source-ids:\s*(.*?)\s*-->", text)
    if match is None:
        return []
    return [source_id.strip() for source_id in match.group(1).split(",")]


def markdown_links(text: str) -> list[str]:
    return re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)


def resolve_markdown_link(source: Path, target: str) -> Path | None:
    split = urlsplit(target)
    if split.scheme or split.netloc or not split.path:
        return None
    decoded = unquote(split.path)
    candidate = (source.parent / decoded).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def prerequisite_closure(start_ids: list[str], lessons_by_id: dict[str, dict[str, Any]]) -> set[str]:
    closure: set[str] = set()
    pending = list(start_ids)
    while pending:
        current = pending.pop()
        if current in closure or current not in lessons_by_id:
            continue
        closure.add(current)
        pending.extend(str(value) for value in lessons_by_id[current].get("prerequisites", []))
    return closure


def lesson_minutes(lesson_ids: set[str] | list[str], lessons_by_id: dict[str, dict[str, Any]]) -> int:
    """Sum valid integer lesson estimates exactly once."""

    total = 0
    for lesson_id in set(lesson_ids):
        lesson = lessons_by_id.get(lesson_id)
        if lesson is None:
            continue
        estimate = lesson.get("estimated_minutes")
        if isinstance(estimate, int) and not isinstance(estimate, bool):
            total += estimate
    return total


def calculate_checkpoint_stats(
    direct_lesson_ids: list[str], lessons_by_id: dict[str, dict[str, Any]]
) -> CheckpointStats:
    """Calculate both selected work and complete from-zero prerequisite work."""

    closure = prerequisite_closure(direct_lesson_ids, lessons_by_id)
    return CheckpointStats(
        direct_lesson_count=len(set(direct_lesson_ids)),
        direct_selection_minutes=lesson_minutes(direct_lesson_ids, lessons_by_id),
        closure_lesson_ids=frozenset(closure),
        prerequisite_closure_minutes=lesson_minutes(closure, lessons_by_id),
    )


def cumulative_checkpoint_errors(checkpoints: list[tuple[str, list[str]]]) -> list[str]:
    """Report any cumulative checkpoint that drops an earlier direct selection."""

    errors: list[str] = []
    previous_lesson_ids: set[str] = set()
    for checkpoint_id, lesson_ids in checkpoints:
        current_ids = set(lesson_ids)
        if previous_lesson_ids and not previous_lesson_ids.issubset(current_ids):
            missing = sorted(previous_lesson_ids - current_ids)
            errors.append(f"{checkpoint_id}: cumulative checkpoint dropped lessons {missing}")
        previous_lesson_ids = current_ids
    return errors


def required_closure_artifacts(
    closure_lesson_ids: set[str] | frozenset[str], lessons_by_id: dict[str, dict[str, Any]]
) -> set[str]:
    """Return every artifact assigned along a checkpoint's prerequisite closure."""

    artifacts: set[str] = set()
    for lesson_id in closure_lesson_ids:
        lesson = lessons_by_id.get(lesson_id)
        if lesson is None:
            continue
        raw_artifacts = lesson.get("required_artifacts", [])
        if isinstance(raw_artifacts, list):
            artifacts.update(str(value) for value in raw_artifacts)
    return artifacts


def visible_checkpoint_minutes(text: str, label: str) -> int | None:
    """Read an explicitly displayed checkpoint minute total."""

    match = re.search(rf"^- {re.escape(label)}: \*\*(\d+) minutes", text, re.MULTILINE)
    return int(match.group(1)) if match else None


def cycle_errors(lessons_by_id: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(lesson_id: str) -> None:
        state[lesson_id] = 1
        stack.append(lesson_id)
        for raw_prerequisite in lessons_by_id[lesson_id].get("prerequisites", []):
            prerequisite = str(raw_prerequisite)
            if prerequisite not in lessons_by_id:
                continue
            if state.get(prerequisite, 0) == 0:
                visit(prerequisite)
            elif state.get(prerequisite) == 1:
                start = stack.index(prerequisite)
                cycle = stack[start:] + [prerequisite]
                message = " -> ".join(cycle)
                if message not in errors:
                    errors.append(message)
        stack.pop()
        state[lesson_id] = 2

    for current_id in lessons_by_id:
        if state.get(current_id, 0) == 0:
            visit(current_id)
    return errors


def format_hours(minutes: int) -> str:
    return f"{minutes / 60:.2f}"


def main() -> int:
    errors: list[str] = []
    manifest = as_mapping(load_yaml(MANIFEST, errors), "curriculum/manifest.yaml", errors)
    depth_order_raw = as_list(manifest.get("depth_order"), "depth_order", errors)
    depth_order = [str(value) for value in depth_order_raw]
    expected_depths = ["foundation", "applied", "integrated", "deep"]
    if depth_order != expected_depths:
        errors.append(f"depth_order must be {expected_depths}; got {depth_order}")
    depth_rank = {depth: index for index, depth in enumerate(depth_order)}

    source_data = as_list(load_yaml(SOURCE_LEDGER, errors), "sources/sources.yaml", errors)
    known_source_ids = {
        str(entry.get("id")) for raw_entry in source_data if (entry := as_mapping(raw_entry, "source", errors))
    }

    lesson_entries = as_list(manifest.get("lessons"), "lessons", errors)
    lessons: list[dict[str, Any]] = []
    lesson_ids: list[str] = []
    lesson_paths: list[str] = []
    for number, raw_entry in enumerate(lesson_entries, start=1):
        entry = as_mapping(raw_entry, f"lessons[{number}]", errors)
        missing = REQUIRED_LESSON_FIELDS - set(entry)
        if missing:
            errors.append(f"lessons[{number}]: missing metadata fields {sorted(missing)}")
        current_id = str(entry.get("id", ""))
        current_path = str(entry.get("path", ""))
        lesson_ids.append(current_id)
        lesson_paths.append(current_path)
        lessons.append(entry)

    duplicate_ids = sorted(value for value, count in Counter(lesson_ids).items() if count > 1)
    duplicate_paths = sorted(value for value, count in Counter(lesson_paths).items() if count > 1)
    if duplicate_ids:
        errors.append(f"duplicate lesson IDs: {duplicate_ids}")
    if duplicate_paths:
        errors.append(f"duplicate lesson paths: {duplicate_paths}")
    lessons_by_id = {str(entry.get("id")): entry for entry in lessons if entry.get("id")}
    lessons_by_path = {str(entry.get("path")): entry for entry in lessons if entry.get("path")}

    actual_lesson_paths = {path.relative_to(ROOT).as_posix() for path in canonical_lesson_files()}
    manifest_lesson_paths = set(lesson_paths)
    for missing_path in sorted(actual_lesson_paths - manifest_lesson_paths):
        errors.append(f"missing lesson metadata: {missing_path}")
    for extra_path in sorted(manifest_lesson_paths - actual_lesson_paths):
        errors.append(f"manifest references non-canonical lesson: {extra_path}")

    artifact_owners: dict[str, set[str]] = {}
    for entry in lessons:
        current_id = str(entry.get("id", ""))
        current_path = str(entry.get("path", ""))
        current_depth = str(entry.get("depth", ""))
        if current_depth not in depth_rank:
            errors.append(f"{current_id}: unsupported depth {current_depth!r}")
        estimate = entry.get("estimated_minutes")
        if not isinstance(estimate, int) or isinstance(estimate, bool) or estimate <= 0:
            errors.append(f"{current_id}: estimated_minutes must be a positive integer")
        prerequisites = as_list(entry.get("prerequisites"), f"{current_id}.prerequisites", errors)
        artifacts = as_list(entry.get("required_artifacts"), f"{current_id}.required_artifacts", errors)
        source_ids = [str(value) for value in as_list(entry.get("source_ids"), f"{current_id}.source_ids", errors)]
        if not artifacts:
            errors.append(f"{current_id}: at least one required artifact must be defined")
        for raw_artifact in artifacts:
            artifact = str(raw_artifact)
            if not artifact:
                errors.append(f"{current_id}: required artifact is blank")
            artifact_owners.setdefault(artifact, set()).add(current_id)
        for source_id in source_ids:
            if source_id not in known_source_ids:
                errors.append(f"{current_id}: missing source ID {source_id}")
        for raw_prerequisite in prerequisites:
            prerequisite = str(raw_prerequisite)
            if prerequisite not in lessons_by_id:
                errors.append(f"{current_id}: missing prerequisite ID {prerequisite}")
                continue
            prerequisite_depth = str(lessons_by_id[prerequisite].get("depth", ""))
            if current_depth in depth_rank and prerequisite_depth in depth_rank:
                if depth_rank[prerequisite_depth] > depth_rank[current_depth]:
                    errors.append(
                        f"{current_id}: {current_depth} lesson depends on later-depth "
                        f"{prerequisite} ({prerequisite_depth})"
                    )

        lesson_path = ROOT / current_path
        if not lesson_path.is_file():
            continue
        text = lesson_path.read_text(encoding="utf-8")
        title = text.splitlines()[0].removeprefix("# ") if text.splitlines() else ""
        if title != str(entry.get("title", "")):
            errors.append(f"{current_path}: visible title disagrees with canonical metadata")
        if lesson_path.parent.name != str(entry.get("module", "")):
            errors.append(f"{current_path}: module disagrees with canonical metadata")
        visible_depth = visible_field(text, ("Depth",))
        if visible_depth is None or visible_depth.lower() != current_depth:
            errors.append(
                f"{current_path}: visible depth {visible_depth!r} disagrees with canonical {current_depth!r}"
            )
        page_minutes = visible_minutes(visible_field(text, ("Estimated time",)))
        if page_minutes != estimate:
            errors.append(
                f"{current_path}: visible estimate {page_minutes!r} disagrees with canonical {estimate!r}"
            )
        visible_artifact = visible_field(text, ("Required artifact", "Artifact"))
        if len(artifacts) != 1 or visible_artifact != str(artifacts[0]):
            errors.append(f"{current_path}: visible required artifact disagrees with canonical metadata")
        if source_ids_from_lesson(text) != source_ids:
            errors.append(f"{current_path}: visible source IDs disagree with canonical metadata")

    for cycle in cycle_errors(lessons_by_id):
        errors.append(f"circular prerequisite graph: {cycle}")

    index_entries = as_list(manifest.get("module_indexes"), "module_indexes", errors)
    index_paths: list[str] = []
    for number, raw_entry in enumerate(index_entries, start=1):
        entry = as_mapping(raw_entry, f"module_indexes[{number}]", errors)
        missing = REQUIRED_INDEX_FIELDS - set(entry)
        if missing:
            errors.append(f"module_indexes[{number}]: missing metadata fields {sorted(missing)}")
        current_path = str(entry.get("path", ""))
        index_paths.append(current_path)
        index_path = ROOT / current_path
        if not index_path.is_file():
            errors.append(f"missing module index: {current_path}")
            continue
        text = index_path.read_text(encoding="utf-8")
        title = text.splitlines()[0].removeprefix("# ") if text.splitlines() else ""
        if title != str(entry.get("title", "")):
            errors.append(f"{current_path}: visible title disagrees with module-index metadata")
        module = str(entry.get("module", ""))
        if index_path.parent.name != module:
            errors.append(f"{current_path}: module disagrees with module-index metadata")
        indexed_ids = {str(value) for value in as_list(entry.get("lesson_ids"), f"{current_path}.lesson_ids", errors)}
        actual_ids = {lesson_id for lesson_id, lesson in lessons_by_id.items() if lesson.get("module") == module}
        if indexed_ids != actual_ids:
            errors.append(f"{current_path}: module-index lesson IDs do not match canonical module lessons")
        for depth in depth_order:
            block = section(text, f"## {depth.title()}")
            if not block:
                errors.append(f"{current_path}: missing ## {depth.title()} section")
                continue
            for target in markdown_links(block):
                resolved = resolve_markdown_link(index_path, target)
                if resolved is None:
                    continue
                relative = resolved.relative_to(ROOT).as_posix()
                linked = lessons_by_path.get(relative)
                if linked is None:
                    continue
                linked_depth = str(linked.get("depth", ""))
                if linked_depth in depth_rank and depth_rank[linked_depth] > depth_rank[depth]:
                    errors.append(
                        f"{current_path}: {depth.title()} section links to "
                        f"{linked.get('id')} ({linked_depth})"
                    )

    actual_index_paths = {path.relative_to(ROOT).as_posix() for path in canonical_module_indexes()}
    if set(index_paths) != actual_index_paths:
        for missing_path in sorted(actual_index_paths - set(index_paths)):
            errors.append(f"missing module-index metadata: {missing_path}")
        for extra_path in sorted(set(index_paths) - actual_index_paths):
            errors.append(f"manifest references non-canonical module index: {extra_path}")

    checkpoint_entries = as_list(manifest.get("checkpoints"), "checkpoints", errors)
    checkpoint_stats: list[tuple[str, CheckpointStats]] = []
    checkpoint_selections: list[tuple[str, list[str]]] = []
    for number, raw_entry in enumerate(checkpoint_entries, start=1):
        entry = as_mapping(raw_entry, f"checkpoints[{number}]", errors)
        missing = REQUIRED_CHECKPOINT_FIELDS - set(entry)
        if missing:
            errors.append(f"checkpoints[{number}]: missing metadata fields {sorted(missing)}")
        checkpoint_id = str(entry.get("id", ""))
        ceiling = str(entry.get("depth_ceiling", ""))
        if ceiling not in depth_rank:
            errors.append(f"{checkpoint_id}: unsupported depth ceiling {ceiling!r}")
        ids = [str(value) for value in as_list(entry.get("lesson_ids"), f"{checkpoint_id}.lesson_ids", errors)]
        if len(ids) != len(set(ids)):
            errors.append(f"{checkpoint_id}: duplicate lesson IDs")
        checkpoint_selections.append((checkpoint_id, ids))
        for current_id in ids:
            lesson = lessons_by_id.get(current_id)
            if lesson is None:
                errors.append(f"{checkpoint_id}: missing lesson ID {current_id}")
                continue
            lesson_depth = str(lesson.get("depth", ""))
            if ceiling in depth_rank and lesson_depth in depth_rank:
                if depth_rank[lesson_depth] > depth_rank[ceiling]:
                    errors.append(
                        f"{checkpoint_id}: includes {current_id} ({lesson_depth}) above {ceiling} ceiling"
                    )
        stats = calculate_checkpoint_stats(ids, lessons_by_id)
        target_range = as_mapping(entry.get("target_minutes"), f"{checkpoint_id}.target_minutes", errors)
        minimum = target_range.get("minimum")
        maximum = target_range.get("maximum")
        if not isinstance(minimum, int) or not isinstance(maximum, int):
            errors.append(f"{checkpoint_id}: target minimum and maximum must be integers")
        elif not minimum <= stats.prerequisite_closure_minutes <= maximum:
            errors.append(
                f"{checkpoint_id}: prerequisite closure {stats.prerequisite_closure_minutes} minutes "
                f"falls outside declared range {minimum}-{maximum}"
            )
        for closure_id in stats.closure_lesson_ids:
            lesson_depth = str(lessons_by_id[closure_id].get("depth", ""))
            if ceiling in depth_rank and lesson_depth in depth_rank:
                if depth_rank[lesson_depth] > depth_rank[ceiling]:
                    errors.append(
                        f"{checkpoint_id}: prerequisite closure adds {closure_id} "
                        f"({lesson_depth}) above {ceiling} ceiling"
                    )
        checkpoint_stats.append((checkpoint_id, stats))

        page_path = ROOT / str(entry.get("path", ""))
        if not page_path.is_file():
            errors.append(f"{checkpoint_id}: missing checkpoint page {entry.get('path')}")
            continue
        page_text = page_path.read_text(encoding="utf-8")
        for heading in CHECKPOINT_HEADINGS:
            if page_text.count(heading) != 1:
                errors.append(f"{entry.get('path')}: expected exactly one {heading}")
        marker = re.search(r"<!-- checkpoint-id:\s*(.*?)\s*-->", page_text)
        if marker is None or marker.group(1) != checkpoint_id:
            errors.append(f"{entry.get('path')}: checkpoint ID marker disagrees with manifest")
        direct_marker = re.search(r"<!-- direct-selection-minutes:\s*(\d+)\s*-->", page_text)
        if direct_marker is None or int(direct_marker.group(1)) != stats.direct_selection_minutes:
            errors.append(f"{entry.get('path')}: direct-selection-minute marker disagrees with manifest")
        closure_marker = re.search(r"<!-- prerequisite-closure-minutes:\s*(\d+)\s*-->", page_text)
        if closure_marker is None or int(closure_marker.group(1)) != stats.prerequisite_closure_minutes:
            errors.append(f"{entry.get('path')}: prerequisite-closure-minute marker disagrees with manifest")
        displayed_direct = visible_checkpoint_minutes(page_text, "Direct capability-selection time")
        if displayed_direct != stats.direct_selection_minutes:
            errors.append(f"{entry.get('path')}: displayed direct-selection time disagrees with manifest")
        displayed_closure = visible_checkpoint_minutes(page_text, "From-zero prerequisite-closure time")
        if displayed_closure != stats.prerequisite_closure_minutes:
            errors.append(f"{entry.get('path')}: displayed prerequisite-closure time disagrees with manifest")
        capability_claim = str(entry.get("capability_claim", ""))
        if capability_claim not in section(page_text, "## Capability claim"):
            errors.append(f"{entry.get('path')}: capability claim disagrees with manifest")

        linked_lesson_paths: set[str] = set()
        for target_link in markdown_links(page_text):
            resolved = resolve_markdown_link(page_path, target_link)
            if resolved is None:
                continue
            relative = resolved.relative_to(ROOT).as_posix()
            if relative.startswith("docs/modules/") and relative.endswith(".md"):
                if relative.endswith("/index.md"):
                    continue
                if relative not in lessons_by_path:
                    errors.append(f"{entry.get('path')}: links to non-canonical lesson {relative}")
                else:
                    linked_lesson_paths.add(relative)
        expected_lesson_paths = {
            str(lessons_by_id[current_id].get("path"))
            for current_id in stats.closure_lesson_ids
            if current_id in lessons_by_id
        }
        if linked_lesson_paths != expected_lesson_paths:
            missing_links = sorted(expected_lesson_paths - linked_lesson_paths)
            extra_links = sorted(linked_lesson_paths - expected_lesson_paths)
            if missing_links:
                errors.append(f"{entry.get('path')}: missing canonical lesson links {missing_links}")
            if extra_links:
                errors.append(f"{entry.get('path')}: links unlisted canonical lessons {extra_links}")

        checkpoint_artifacts = [
            str(value)
            for value in as_list(entry.get("required_artifacts"), f"{checkpoint_id}.required_artifacts", errors)
        ]
        expected_artifacts = required_closure_artifacts(stats.closure_lesson_ids, lessons_by_id)
        missing_artifacts = sorted(expected_artifacts - set(checkpoint_artifacts))
        extra_artifacts = sorted(set(checkpoint_artifacts) - expected_artifacts)
        if missing_artifacts:
            errors.append(f"{checkpoint_id}: missing prerequisite closure artifacts {missing_artifacts}")
        if extra_artifacts:
            errors.append(f"{checkpoint_id}: artifacts are outside prerequisite closure {extra_artifacts}")
        for artifact in checkpoint_artifacts:
            owners = artifact_owners.get(artifact)
            if not owners:
                errors.append(f"{checkpoint_id}: required artifact is not defined: {artifact}")
            elif not owners.intersection(stats.closure_lesson_ids):
                errors.append(f"{checkpoint_id}: required artifact owner is not in checkpoint closure: {artifact}")
            if artifact not in page_text:
                errors.append(f"{entry.get('path')}: required artifact is not linked or named: {artifact}")

    errors.extend(cumulative_checkpoint_errors(checkpoint_selections))

    depth_counts = Counter(str(entry.get("depth", "")) for entry in lessons)
    print("Lesson count by depth")
    for depth in depth_order:
        print(f"- {depth}: {depth_counts[depth]}")
    print("Checkpoint calculations")
    for checkpoint_id, stats in checkpoint_stats:
        print(
            f"- {checkpoint_id}: direct selection {stats.direct_lesson_count} lessons, "
            f"{stats.direct_selection_minutes} minutes ({format_hours(stats.direct_selection_minutes)} hours); "
            f"prerequisite closure {len(stats.closure_lesson_ids)} lessons, "
            f"{stats.prerequisite_closure_minutes} minutes "
            f"({format_hours(stats.prerequisite_closure_minutes)} hours)"
        )
    if errors:
        print("Curriculum validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Curriculum validation: PASS")
    print(f"- {len(lessons)} canonical lessons and {len(index_entries)} module indexes have metadata")
    print("- prerequisite graph is complete, acyclic, and depth-safe")
    print("- checkpoint depth, closure time, link, cumulative-selection, and closure-artifact gates pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
