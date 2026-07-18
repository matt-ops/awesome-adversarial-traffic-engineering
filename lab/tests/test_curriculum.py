"""Focused tests for closure-accurate curriculum checkpoint helpers."""

from typing import Any

from scripts.validate_curriculum import (
    calculate_checkpoint_stats,
    cumulative_checkpoint_errors,
    cycle_errors,
    required_closure_artifacts,
)


def lesson(minutes: int, prerequisites: list[str], artifact: str) -> dict[str, Any]:
    return {
        "estimated_minutes": minutes,
        "prerequisites": prerequisites,
        "required_artifacts": [artifact],
    }


def test_hidden_prerequisite_time_is_included_in_checkpoint_closure() -> None:
    lessons = {
        "foundation": lesson(90, [], "foundation.md"),
        "selected": lesson(60, ["foundation"], "selected.md"),
    }

    stats = calculate_checkpoint_stats(["selected"], lessons)

    assert stats.direct_selection_minutes == 60
    assert stats.prerequisite_closure_minutes == 150
    assert stats.closure_lesson_ids == frozenset({"foundation", "selected"})


def test_shared_prerequisite_is_counted_exactly_once() -> None:
    lessons = {
        "shared": lesson(30, [], "shared.md"),
        "left": lesson(40, ["shared"], "left.md"),
        "right": lesson(50, ["shared"], "right.md"),
    }

    stats = calculate_checkpoint_stats(["left", "right"], lessons)

    assert stats.direct_selection_minutes == 90
    assert stats.prerequisite_closure_minutes == 120
    assert len(stats.closure_lesson_ids) == 3


def test_prerequisite_cycle_is_preserved_as_a_validation_error() -> None:
    lessons = {
        "one": lesson(30, ["two"], "one.md"),
        "two": lesson(30, ["one"], "two.md"),
    }

    assert cycle_errors(lessons) == ["one -> two -> one"]


def test_cumulative_checkpoint_cannot_drop_an_earlier_selection() -> None:
    checkpoints = [
        ("first", ["a"]),
        ("second", ["a", "b"]),
        ("third", ["b", "c"]),
    ]

    assert cumulative_checkpoint_errors(checkpoints) == [
        "third: cumulative checkpoint dropped lessons ['a']"
    ]


def test_checkpoint_requires_artifacts_from_prerequisite_closure() -> None:
    lessons = {
        "prerequisite": lesson(30, [], "prerequisite.md"),
        "selected": lesson(30, ["prerequisite"], "selected.md"),
    }
    stats = calculate_checkpoint_stats(["selected"], lessons)
    required = required_closure_artifacts(stats.closure_lesson_ids, lessons)

    assert required == {"prerequisite.md", "selected.md"}
    assert required - {"selected.md"} == {"prerequisite.md"}
