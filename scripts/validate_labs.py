"""Validate the required instructional contract on every learner lab page."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = ROOT / "docs" / "labs"
SAMPLE_REPORT = ROOT / "lab" / "reports" / "synthetic-finding.md"
REQUIRED_CONCEPTS = (
    "authorization",
    "target",
    "objective",
    "protected action",
    "baseline",
    "hypothesis",
    "changed variable",
    "fixed variable",
    "success",
    "evidence",
    "limitation",
    "cleanup",
    "remediation",
    "retest",
)


def main() -> int:
    pages = sorted(path for path in LAB_ROOT.glob("*/*.md") if path.name != "index.md")
    errors: list[str] = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for concept in REQUIRED_CONCEPTS:
            if re.search(rf"\b{re.escape(concept)}s?\b", text, re.IGNORECASE) is None:
                errors.append(f"{page.relative_to(ROOT)}: missing lab concept {concept!r}")
        if (
            "```" not in text
            and "| Command |" not in text
            and "| Case |" not in text
            and "scorecard" not in text.casefold()
        ):
            errors.append(f"{page.relative_to(ROOT)}: no command, command table, or scored action")

    if not SAMPLE_REPORT.is_file():
        errors.append("lab/reports/synthetic-finding.md: sample report is missing")
    else:
        report = SAMPLE_REPORT.read_text(encoding="utf-8")
        for heading in (
            "## Summary",
            "## Evidence",
            "## Impact",
            "## Recommendation",
            "## Retest",
            "## Limitations",
        ):
            if report.count(heading) != 1:
                errors.append(f"lab/reports/synthetic-finding.md: expected exactly one {heading}")

    if errors:
        print("Lab validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Lab validation: PASS")
    print(f"- {len(pages)} lab pages contain the complete experiment contract")
    print("- the synthetic sample report contains evidence, impact, remediation, retest, and limits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
