"""Check relative Markdown links without making network requests."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
EXCLUDED_FILES = {
    "01-AATE-CODEX-MASTER-PROMPT-FINAL.md",
    "codex-addendum-single-progressive-path.md",
    "codex-master-prompt-awesome-adversarial-traffic-engineering-v2-progressive-path.md",
    "awesome-red-team-bots-ddos-interview-prep.md",
}


def main() -> int:
    errors: list[str] = []
    for source in ROOT.rglob("*.md"):
        if source.name in EXCLUDED_FILES or any(
            part in {".docs-build", ".git", "node_modules", "site"} for part in source.parts
        ):
            continue
        for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
            for raw_target in LINK.findall(line):
                target = raw_target.strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path_part = unquote(target.split("#", 1)[0])
                if not path_part:
                    continue
                resolved = (source.parent / path_part).resolve()
                try:
                    resolved.relative_to(ROOT.resolve())
                except ValueError:
                    errors.append(f"{source.relative_to(ROOT)}:{line_number}: link escapes repository: {target}")
                    continue
                if not resolved.exists():
                    errors.append(f"{source.relative_to(ROOT)}:{line_number}: missing target: {target}")
    if errors:
        print("Relative links: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Relative links: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
