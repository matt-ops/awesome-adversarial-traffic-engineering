"""Focused tests for closure-accurate curriculum checkpoint helpers."""

from typing import Any

from scripts.validate_curriculum import (
    calculate_checkpoint_stats,
    cumulative_checkpoint_errors,
    cycle_errors,
    required_checkpoint_membership_errors,
)


def lesson(minutes: int, prerequisites: list[str]) -> dict[str, Any]:
    return {
        "estimated_minutes": minutes,
        "prerequisites": prerequisites,
    }


def test_hidden_prerequisite_time_is_included_in_checkpoint_closure() -> None:
    lessons = {
        "foundation": lesson(90, []),
        "selected": lesson(60, ["foundation"]),
    }

    stats = calculate_checkpoint_stats(["selected"], lessons)

    assert stats.direct_selection_minutes == 60
    assert stats.prerequisite_closure_minutes == 150
    assert stats.closure_lesson_ids == frozenset({"foundation", "selected"})


def test_shared_prerequisite_is_counted_exactly_once() -> None:
    lessons = {
        "shared": lesson(30, []),
        "left": lesson(40, ["shared"]),
        "right": lesson(50, ["shared"]),
    }

    stats = calculate_checkpoint_stats(["left", "right"], lessons)

    assert stats.direct_selection_minutes == 90
    assert stats.prerequisite_closure_minutes == 120
    assert len(stats.closure_lesson_ids) == 3


def test_prerequisite_cycle_is_preserved_as_a_validation_error() -> None:
    lessons = {
        "one": lesson(30, ["two"]),
        "two": lesson(30, ["one"]),
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


def test_required_core_lesson_must_be_directly_selected_at_earliest_checkpoint() -> None:
    checkpoints = [("7-days", ["m04-l03"]), ("21-days", ["m04-l03", "m04-l06"])]

    assert required_checkpoint_membership_errors(checkpoints, {"m04-l06": "7-days"}) == [
        "7-days: required core lesson m04-l06 is not a direct selection"
    ]
