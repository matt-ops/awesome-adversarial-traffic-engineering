"""Stage canonical Markdown sources for MkDocs without duplicating curriculum content."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = (ROOT / ".docs-build").resolve()
DIRECTORIES = ("awesome", "curriculum", "docs", "interview")
ROOT_FILES = (
    "README.md",
    "SAFETY.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "NOTICE.md",
)


def assert_safe_staging_path() -> None:
    if STAGING.parent != ROOT.resolve() or STAGING.name != ".docs-build":
        raise RuntimeError(f"refusing to stage documentation outside the repository: {STAGING}")


def main() -> int:
    assert_safe_staging_path()
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir()
    for directory in DIRECTORIES:
        shutil.copytree(ROOT / directory, STAGING / directory)
    # `templates` is reserved by MkDocs. Stage the canonical artifact templates
    # under a site-only name and rewrite staged links without changing sources.
    shutil.copytree(ROOT / "templates", STAGING / "artifact-templates")
    for filename in ROOT_FILES:
        shutil.copy2(ROOT / filename, STAGING / filename)
    (STAGING / "lab").mkdir()
    shutil.copy2(ROOT / "lab" / "README.md", STAGING / "lab" / "README.md")
    (STAGING / "scripts").mkdir()
    shutil.copy2(ROOT / "scripts" / "README.md", STAGING / "scripts" / "README.md")
    for markdown_file in STAGING.rglob("*.md"):
        content = markdown_file.read_text(encoding="utf-8")
        markdown_file.write_text(content.replace("templates/", "artifact-templates/"), encoding="utf-8")
    print(f"Staged canonical documentation in {STAGING}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
