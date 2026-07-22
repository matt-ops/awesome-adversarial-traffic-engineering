"""Validate lesson assessments and flag wording that needs human review."""

from __future__ import annotations

import re
from pathlib import Path

from validate_lessons import (  # type: ignore[import-not-found]
    numbered_questions,
    section,
    validate_answer_key,
)

ROOT = Path(__file__).resolve().parents[1]
LESSON_ROOT = ROOT / "docs" / "modules"
VAGUE_QUESTION_PATTERNS = (
    r"\bthis scenario\b",
    r"\bthat result\b",
    r"\bthe transition\b",
    r"\bthe control\b(?!\s+(?:map|evaluation|endpoint|decision|token|rule|output))",
    r"\bthe action\b(?!\s+(?:token|request|result|body|endpoint))",
    r"\bit\b",
    r"\bthey\b",
)
EXPLANATION_MARKERS = {
    "authoritative": r"server-side|source of truth|verified|independent|final truth",
    "invariant": r"rule|property|must|allowed|one-use",
    "principal": r"caller|identity|account|subject",
    "binding": r"tie|connect|associate|derive|session|token|weak|former",
    "context": (
        r"browser\s+context|execution\s+context|collection\s+context|contexts?|page|frame|worker|condition|"
        r"boundary|environment|recorded"
    ),
    "state": (
        r"server|record|storage|condition|value|session|workflow|inventory|token|connection|transport|application|"
        r"promotion|account|starting|final|shared"
    ),
}


def answer_blocks(answer_key: str) -> list[tuple[int, str]]:
    """Return the top-level numbered answer bullets from a valid or partial key."""

    details = re.search(r"<summary>Show answers</summary>\s*(.*?)\s*</details>", answer_key, re.DOTALL)
    if details is None:
        return []
    content = details.group(1)
    matches = list(re.finditer(r"^- \*\*(\d+)\.\s+", content, re.MULTILINE))
    return [
        (
            int(match.group(1)),
            content[match.start() : matches[index + 1].start() if index + 1 < len(matches) else len(content)].strip(),
        )
        for index, match in enumerate(matches)
    ]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    lessons = sorted(path for path in LESSON_ROOT.glob("*/*.md") if path.name != "index.md")
    question_total = 0

    for lesson in lessons:
        relative = lesson.relative_to(ROOT)
        text = lesson.read_text(encoding="utf-8")
        for legacy in ("## Pass gate", "## Required artifact", "- Required artifact:"):
            if legacy in text:
                errors.append(f"{relative}: legacy assessment/artifact marker remains: {legacy}")

        knowledge_check = section(text, "## Check your understanding", "## Answer key")
        questions = numbered_questions(knowledge_check)
        question_total += len(questions)
        numbers = [number for number, _ in questions]
        expected = list(range(1, len(questions) + 1))
        if not 3 <= len(questions) <= 5:
            errors.append(f"{relative}: expected three to five questions; got {len(questions)}")
        if numbers != expected:
            errors.append(f"{relative}: question numbers {numbers} are duplicate or nonsequential")
        for number, question in questions:
            if not question.endswith("?"):
                errors.append(f"{relative}: question {number} does not end with ?")
            for pattern in VAGUE_QUESTION_PATTERNS:
                if re.search(pattern, question, re.IGNORECASE):
                    warnings.append(
                        f"{relative}: question {number} may need a clearer noun for {pattern!r}"
                    )

        answer_key = section(text, "## Answer key", "## Next lesson")
        errors.extend(validate_answer_key(relative, answer_key, numbers))
        for number, answer in answer_blocks(answer_key):
            lower = answer.casefold()
            for term, explanation_pattern in EXPLANATION_MARKERS.items():
                term_present = re.search(rf"\b{term}\b", lower) is not None
                if term == "state" and re.search(r"\b(?:should|to|must)\s+state\b", lower):
                    term_present = False
                if term_present and not re.search(
                    explanation_pattern, lower, re.IGNORECASE
                ):
                    warnings.append(
                        f"{relative}: answer {number} uses {term!r} without an obvious plain-language explanation"
                    )

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print("Assessment validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Assessment validation: PASS")
    print(f"- {len(lessons)} lesson assessments contain {question_total} concrete questions")
    print("- answer bullets are sequential, complete, collapsible, and 15-120 words")
    print(f"- {len(warnings)} human-review warning(s) printed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
