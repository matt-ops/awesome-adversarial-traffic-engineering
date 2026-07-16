"""Validate the structure and minimum teaching contract of AATE lesson pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_ROOT = ROOT / "docs" / "modules"

REQUIRED_HEADINGS = (
    "## Role outcome",
    "## Prerequisites",
    "## Source basis",
    "## Mental model",
    "## Required external instruction",
    "## Course bridge",
    "## Worked example",
    "## Guided exercise",
    "## Why this matters offensively",
    "## Required artifact",
    "## Pass gate",
    "## Answer key",
    "## Next lesson",
)
PROGRESS_FIELDS = ("Module:", "Lesson:", "Depth:", "Estimated time:", "Prerequisites:", "Artifact:", "Next:")
EXERCISE_FIELDS = (
    "### Objective",
    "### Setup",
    "### Actions",
    "### Expected output",
    "### Interpretation",
    "### Common failure modes",
    "### Cleanup",
)
ASSIGNMENT_FIELDS = (
    "**Direct link:**",
    "**Exact assignment:**",
    "**Estimated time:**",
    "**Focus on:**",
    "**Skip:**",
    "**Expected takeaway:**",
)
DEPTH_HEADINGS = ("## Foundation", "## Applied", "## Integrated", "## Deep")
REJECTED_PATTERNS = {
    r"\bTODO\b": "TODO placeholder",
    r"\bTKTK\b": "TKTK placeholder",
    r"learn more about": "vague learn-more assignment",
    r"research this topic": "vague research assignment",
    r"explore the docs": "vague documentation assignment",
    r"unsupported production-ready": "unsupported production-ready claim",
    r"\bundetectable\b": "unsupported undetectable claim",
    r"\ball bots\b": "unsupported all-bots claim",
}


def lesson_files() -> list[Path]:
    if not LESSON_ROOT.exists():
        return []
    return sorted(path for path in LESSON_ROOT.glob("*/*.md") if path.name != "index.md")


def module_indexes() -> list[Path]:
    if not LESSON_ROOT.exists():
        return []
    return sorted(LESSON_ROOT.glob("*/index.md"))


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    end = text.find(next_heading, start + len(heading)) if next_heading else len(text)
    return text[start : end if end >= 0 else len(text)]


def main() -> int:
    errors: list[str] = []
    lessons = lesson_files()
    indexes = module_indexes()
    for index in indexes:
        text = index.read_text(encoding="utf-8")
        relative = index.relative_to(ROOT)
        for heading in DEPTH_HEADINGS:
            if text.count(heading) != 1:
                errors.append(f"{relative}: expected exactly one {heading} section")
    for lesson in lessons:
        text = lesson.read_text(encoding="utf-8")
        relative = lesson.relative_to(ROOT)
        lines = text.splitlines()
        if len(lines) > 520:
            errors.append(f"{relative}: {len(lines)} lines; split pages at distinct outcomes")
        for heading in REQUIRED_HEADINGS:
            if text.count(heading) != 1:
                errors.append(f"{relative}: expected exactly one {heading}")
        for field in PROGRESS_FIELDS:
            if field not in text[:1200]:
                errors.append(f"{relative}: progress box missing {field}")
        source_block = section(text, "## Source basis", "## Mental model")
        if "| Label | Source | Assigned area | Why it is used |" not in source_block:
            errors.append(f"{relative}: Source basis must use the required table")
        assignment = section(text, "## Required external instruction", "## Course bridge")
        for field in ASSIGNMENT_FIELDS:
            if field not in assignment:
                errors.append(f"{relative}: external instruction missing {field}")
        exercise = section(text, "## Guided exercise", "## Why this matters offensively")
        for field in EXERCISE_FIELDS:
            if field not in exercise:
                errors.append(f"{relative}: Guided exercise missing {field}")
        pass_gate = section(text, "## Pass gate", "## Answer key")
        question_count = len(re.findall(r"^\d+\.\s+", pass_gate, re.MULTILINE))
        if question_count < 5:
            errors.append(f"{relative}: Pass gate needs at least five numbered questions; got {question_count}")
        answer_key = section(text, "## Answer key", "## Next lesson")
        if "<details>" not in answer_key or "<summary>" not in answer_key or "</details>" not in answer_key:
            errors.append(f"{relative}: Answer key must be collapsible")
        if len(re.findall(r"^\d+\.\s+", answer_key, re.MULTILINE)) < question_count:
            errors.append(f"{relative}: Answer key must explain every pass-gate question")
        if re.search(r"^>?\s*Depth:\s*Foundation\s*$", text, re.MULTILINE | re.IGNORECASE):
            mental_model = section(text, "## Mental model", "## Required external instruction")
            if "```" not in mental_model and "|" not in mental_model:
                errors.append(f"{relative}: Foundation mental model needs a diagram or comparison table")
        for pattern, label in REJECTED_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{relative}: rejected placeholder/claim: {label}")
        if re.search(r"understand the concept", text, re.IGNORECASE) and question_count < 5:
            errors.append(f"{relative}: vague understanding claim lacks a measurable pass gate")
        if re.search(r"run the following", text, re.IGNORECASE):
            errors.append(f"{relative}: replace 'run the following' with explanation before the command")

    if errors:
        print("Lesson validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Lesson validation: PASS")
    print(f"- {len(lessons)} lesson pages meet the teaching template")
    print(f"- {len(indexes)} module indexes expose Foundation, Applied, Integrated, and Deep")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
