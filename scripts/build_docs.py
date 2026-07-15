"""Stage only public course content for the static site."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / ".docs-build"
PUBLIC_FILES = ("README.md", "COURSE.md", "RESOURCES.md", "SAFETY.md")


def main() -> int:
    if STAGING.resolve().parent != ROOT.resolve() or STAGING.name != ".docs-build":
        raise RuntimeError(f"unsafe staging path: {STAGING}")
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir()
    for filename in PUBLIC_FILES:
        shutil.copy2(ROOT / filename, STAGING / filename)
    (STAGING / "lab").mkdir()
    shutil.copy2(ROOT / "lab" / "README.md", STAGING / "lab" / "README.md")
    print("Staged public course pages only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
