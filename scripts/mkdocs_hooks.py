"""Narrow MkDocs rendering adjustments for canonical lesson answer keys."""

from __future__ import annotations

from typing import Any

ANSWER_DETAILS = "<details>\n<summary>Show answers</summary>"
RENDERED_ANSWER_DETAILS = '<details markdown="1">\n<summary>Show answers</summary>'


def on_page_markdown(markdown: str, **_: Any) -> str:
    """Enable Markdown parsing inside the exact source-level answer-key block."""

    if "## Answer key" not in markdown:
        return markdown
    return markdown.replace(ANSWER_DETAILS, RENDERED_ANSWER_DETAILS)
