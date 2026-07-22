"""Validate the full remediation teaching contract on every canonical lesson."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_ROOT = ROOT / "docs" / "modules"

REQUIRED_HEADINGS = (
    "## Progress",
    "## Role outcome",
    "## Source basis",
    "## Mental model",
    "## Required external instruction",
    "## Course bridge",
    "## Worked example",
    "## Guided exercise",
    "## Why this matters offensively",
    "## Check your understanding",
    "## Answer key",
    "## Next lesson",
)
PROGRESS_FIELDS = (
    "- Module:",
    "- Lesson:",
    "- Depth:",
    "- Estimated time:",
    "- Prerequisites:",
    "- Next lesson:",
)
EXERCISE_HEADINGS = (
    "### Objective",
    "### Setup",
    "### Exact actions or commands",
    "### Expected output",
    "### Interpretation",
    "### Common failure modes",
    "### Cleanup",
)
ASSIGNMENT_FIELDS = (
    "**Direct link:**",
    "**Exact section, chapter, or unit:**",
    "**What to focus on:**",
    "**What to skip:**",
    "**Estimated time:**",
    "**Expected takeaway:**",
)
DEPTH_HEADINGS = ("## Foundation", "## Applied", "## Integrated", "## Deep")
REJECTED_PATTERNS = {
    r"\bTODO\b": "TODO placeholder",
    r"\bTKTK\b": "TKTK placeholder",
    r"research this(?: topic)?": "vague research assignment",
    r"explore the docs": "vague documentation assignment",
    r"learn more about": "vague learn-more assignment",
    r"understand this topic": "vague understanding assignment",
    r"\bproduction-ready\b": "unsupported production-ready claim",
    r"\bundetectable\b": "unsupported undetectable claim",
    r"detects all bots": "unsupported universal detection claim",
    r"\brun the following\b": "unexplained command lead-in",
}
FOUNDATION_SLICE = (
    "docs/modules/01-http-edge/01-http-request-response.md",
    "docs/modules/01-http-edge/02-sessions-and-workflows.md",
    "docs/modules/01-http-edge/03-devtools-network.md",
    "docs/modules/01-http-edge/04-edge-request-path.md",
    "docs/modules/02-browser-javascript/01-browser-process-model.md",
    "docs/modules/02-browser-javascript/02-dom-and-web-apis.md",
    "docs/modules/02-browser-javascript/03-javascript-core.md",
    "docs/modules/02-browser-javascript/04-async-fetch-and-errors.md",
    "docs/modules/03-playwright/01-object-model.md",
    "docs/modules/03-playwright/02-first-browser.md",
    "docs/modules/03-playwright/03-contexts-and-state.md",
    "docs/modules/03-playwright/04-network-events.md",
)


def lesson_files() -> list[Path]:
    return sorted(path for path in LESSON_ROOT.glob("*/*.md") if path.name != "index.md")


def module_indexes() -> list[Path]:
    return sorted(LESSON_ROOT.glob("*/index.md"))


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    end = text.find(next_heading, start + len(heading)) if next_heading else len(text)
    return text[start : end if end >= 0 else len(text)]


def subsection_blocks(text: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"^### .+$", text, re.MULTILINE)]
    return [
        text[start : starts[index + 1] if index + 1 < len(starts) else len(text)]
        for index, start in enumerate(starts)
    ]


def numbered_questions(block: str) -> list[tuple[int, str]]:
    """Return numbered questions, including any wrapped continuation lines."""

    matches = list(re.finditer(r"^(\d+)\.\s+", block, re.MULTILINE))
    return [
        (
            int(match.group(1)),
            block[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(block)].strip(),
        )
        for index, match in enumerate(matches)
    ]


def answer_word_count(block: str) -> int:
    """Count readable answer words after removing Markdown and HTML markers."""

    plain = re.sub(r"<[^>]+>", " ", block)
    plain = re.sub(r"[`*_\[\]()#>-]", " ", plain)
    return len(re.findall(r"\b[\w'-]+\b", plain))


def validate_answer_key(relative: Path, answer_key: str, question_numbers: list[int]) -> list[str]:
    """Validate the exact collapsible numbered-bullet answer-key contract."""

    errors: list[str] = []
    for marker in ("<details>", "<summary>Show answers</summary>", "</details>"):
        if answer_key.count(marker) != 1:
            errors.append(f"{relative}: Answer key requires exactly one {marker}")
    details_match = re.search(
        r"<details>\s*<summary>Show answers</summary>\s*(.*?)\s*</details>",
        answer_key,
        re.DOTALL,
    )
    if details_match is None or not details_match.group(1).strip():
        errors.append(f"{relative}: Answer key collapsible block is empty or malformed")
        return errors
    content = details_match.group(1)
    if re.search(r"^\d+\.\s+", content, re.MULTILINE):
        errors.append(f"{relative}: Answer key uses an old numbered-paragraph answer")
    matches = list(re.finditer(r"^- \*\*(\d+)\.\s+", content, re.MULTILINE))
    answer_numbers = [int(match.group(1)) for match in matches]
    if answer_numbers != question_numbers:
        errors.append(
            f"{relative}: Answer bullets {answer_numbers} do not match questions {question_numbers}"
        )
    if len(answer_numbers) != len(set(answer_numbers)):
        errors.append(f"{relative}: Answer key has duplicate answer numbers")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        answer = content[match.start() : end].strip()
        words = answer_word_count(answer)
        if words < 15:
            errors.append(f"{relative}: answer {match.group(1)} has {words} words; minimum is 15")
        if words > 120:
            errors.append(f"{relative}: answer {match.group(1)} has {words} words; maximum is 120")
    return errors


def main() -> int:
    errors: list[str] = []
    lessons = lesson_files()
    indexes = module_indexes()

    for foundation_relative in FOUNDATION_SLICE:
        if not (ROOT / foundation_relative).is_file():
            errors.append(f"required Foundation page is missing: {foundation_relative}")

    for index in indexes:
        text = index.read_text(encoding="utf-8")
        index_relative = index.relative_to(ROOT)
        for heading in DEPTH_HEADINGS:
            if text.count(heading) != 1:
                errors.append(f"{index_relative}: expected exactly one {heading} section")

    for lesson in lessons:
        text = lesson.read_text(encoding="utf-8")
        relative = lesson.relative_to(ROOT)
        lines = text.splitlines()
        if len(lines) > 560:
            errors.append(f"{relative}: {len(lines)} lines; split distinct outcomes")
        previous = -1
        for heading in REQUIRED_HEADINGS:
            if text.count(heading) != 1:
                errors.append(f"{relative}: expected exactly one {heading}")
                continue
            position = text.find(heading)
            if position <= previous:
                errors.append(f"{relative}: {heading} is out of template order")
            previous = position
        if "## Prerequisites" in text:
            errors.append(f"{relative}: prerequisites belong in Progress, not a duplicate section")

        progress = section(text, "## Progress", "## Role outcome")
        for field in PROGRESS_FIELDS:
            if progress.count(field) != 1:
                errors.append(f"{relative}: Progress requires exactly one {field}")

        source_block = section(text, "## Source basis", "## Mental model")
        if "| Type | Source | Exact assigned area | What it supports | Limitation |" not in source_block:
            errors.append(f"{relative}: Source basis lacks the exact remediation table")

        assignment = section(text, "## Required external instruction", "## Course bridge")
        blocks = subsection_blocks(assignment)
        if not blocks:
            errors.append(f"{relative}: external instruction needs at least one named resource block")
        for number, block in enumerate(blocks, start=1):
            for field in ASSIGNMENT_FIELDS:
                if block.count(field) != 1:
                    errors.append(f"{relative}: resource block {number} requires exactly one {field}")
            direct = re.search(r"\*\*Direct link:\*\*\s*(.+)", block)
            if direct is None or "http" not in direct.group(1):
                errors.append(f"{relative}: resource block {number} needs a direct HTTP(S) link")
            elif len(re.findall(r"https?://", direct.group(1))) != 1:
                errors.append(f"{relative}: resource block {number} must assign exactly one external resource")

        exercise = section(text, "## Guided exercise", "## Why this matters offensively")
        for heading in EXERCISE_HEADINGS:
            if exercise.count(heading) != 1:
                errors.append(f"{relative}: Guided exercise requires exactly one {heading}")
        expected = section(exercise, "### Expected output", "### Interpretation")
        interpretation = section(exercise, "### Interpretation", "### Common failure modes")
        failures = section(exercise, "### Common failure modes", "### Cleanup")
        if len(expected.split()) < 20:
            errors.append(f"{relative}: Expected output is too thin to verify the exercise")
        if len(interpretation.split()) < 20:
            errors.append(f"{relative}: Interpretation is too thin to teach the result")
        if len(re.findall(r"^- ", failures, re.MULTILINE)) < 2:
            errors.append(f"{relative}: Common failure modes needs at least two concrete failures")

        knowledge_check = section(text, "## Check your understanding", "## Answer key")
        questions = numbered_questions(knowledge_check)
        question_numbers = [number for number, _ in questions]
        expected_numbers = list(range(1, len(questions) + 1))
        if not 3 <= len(questions) <= 5:
            errors.append(
                f"{relative}: Check your understanding needs three to five questions; got {len(questions)}"
            )
        if question_numbers != expected_numbers:
            errors.append(
                f"{relative}: question numbers {question_numbers} are duplicate or nonsequential"
            )
        for number, question in questions:
            if not question.endswith("?"):
                errors.append(f"{relative}: question {number} must end with a question mark")
        answer_key = section(text, "## Answer key", "## Next lesson")
        errors.extend(validate_answer_key(relative, answer_key, question_numbers))

        if re.search(r"^- Depth: Foundation\s*$", progress, re.MULTILINE | re.IGNORECASE):
            mental_model = section(text, "## Mental model", "## Required external instruction")
            if "```" not in mental_model and "|" not in mental_model:
                errors.append(f"{relative}: Foundation mental model needs a diagram or comparison table")

        for pattern, label in REJECTED_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{relative}: rejected placeholder/claim: {label}")
        if re.search(r"amazon\.jobs|leadership principles", text, re.IGNORECASE):
            errors.append(f"{relative}: employer-specific material is prohibited")

    first_browser = (LESSON_ROOT / "03-playwright" / "02-first-browser.md").read_text(encoding="utf-8")
    for marker in (
        "### Every import",
        "### Browser, BrowserContext, Page, and Locator",
        "### Every asynchronous step",
        "without Docker",
        "manual and automated",
        "Microsoft Learn",
    ):
        if marker not in first_browser:
            errors.append(f"docs/modules/03-playwright/02-first-browser.md: release-blocker marker missing: {marker}")

    if errors:
        print("Lesson validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Lesson validation: PASS")
    print(f"- {len(lessons)} canonical lessons satisfy the learning-experience template")
    print(f"- {len(indexes)} module indexes expose Foundation, Applied, Integrated, and Deep")
    print(f"- {len(FOUNDATION_SLICE)} mandatory Foundation pages and the first-browser release gate pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
