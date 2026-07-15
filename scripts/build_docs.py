"""Verify that the source-first MkDocs tree is ready to build."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REQUIRED = (
    "index.md",
    "start-here.md",
    "path.md",
    "methodology/provenance.md",
    "references/source-ledger.md",
    "safety/index.md",
)


def main() -> int:
    missing = [relative for relative in REQUIRED if not (DOCS / relative).is_file()]
    if missing:
        for relative in missing:
            print(f"missing public documentation page: docs/{relative}")
        return 1
    print(f"Source-first documentation tree ready: {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
