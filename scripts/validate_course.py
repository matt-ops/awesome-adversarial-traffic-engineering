"""Validate the simple public course contract."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = ("README.md", "COURSE.md", "CHECKPOINTS.md", "RESOURCES.md", "SAFETY.md", "lab/README.md")
LEVELS = ("foundation", "applied", "integrated", "deep")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def heading_slugs(text: str) -> set[str]:
    slugs: set[str] = set(re.findall(r'<a id="([^"]+)"></a>', text))
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^a-z0-9 -]", "", heading.casefold()).strip().replace(" ", "-")
        slugs.add(re.sub(r"-+", "-", slug))
    return slugs


def validate_links(errors: list[str]) -> None:
    for relative in PUBLIC_FILES:
        text = read(relative)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_text, _, anchor = target.partition("#")
            target_path = ((ROOT / relative).parent / path_text if path_text else ROOT / relative).resolve()
            try:
                target_path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{relative}: link escapes repository: {target}")
                continue
            if not target_path.is_file():
                errors.append(f"{relative}: missing linked file: {target}")
                continue
            if anchor and anchor not in heading_slugs(target_path.read_text(encoding="utf-8")):
                errors.append(f"{relative}: missing anchor: {target}")


def main() -> int:
    errors: list[str] = []
    course = read("COURSE.md")
    module_matches = list(re.finditer(r"^# Module ([0-8]): .+$", course, re.MULTILINE))
    if [int(match.group(1)) for match in module_matches] != list(range(9)):
        errors.append("COURSE.md must contain Modules 0-8 exactly once and in order")
    else:
        finish = course.index("# You are done")
        for index, match in enumerate(module_matches):
            end = module_matches[index + 1].start() if index < 8 else finish
            module = course[match.start():end]
            for level in LEVELS:
                anchor = f'<a id="module-{index}-{level}"></a>'
                if module.count(anchor) != 1:
                    errors.append(f"Module {index}: expected one {level} anchor")
                level_start = module.find(anchor)
                next_starts = [module.find(f'<a id="module-{index}-{other}"></a>', level_start + 1) for other in LEVELS]
                next_starts = [position for position in next_starts if position > level_start]
                level_end = min(next_starts) if next_starts else len(module)
                section = module[level_start:level_end]
                for field in ("### Learn", "### Lab", "### Self-assess", "<summary>Check your answers</summary>"):
                    if section.count(field) != 1:
                        errors.append(f"Module {index} {level}: expected one {field}")

    times = [float(value) for value in re.findall(r"^\| [0-8] \| ([0-9.]+) h \|", read("CHECKPOINTS.md"), re.MULTILINE)]
    if len(times) != 9 or sum(times) != 24.0:
        errors.append(f"Foundation checkpoint must have nine rows totaling 24 hours; got {times}")

    public_text = "\n".join(read(path) for path in PUBLIC_FILES)
    for term in ("amazon", "atoz", "10428500", "mattn", "matt-ops"):
        if term in public_text.casefold():
            errors.append(f"public course contains prohibited personal/employer term: {term}")

    if "[Open the course](COURSE.md)" not in read("README.md"):
        errors.append("README.md must expose one obvious course start link")

    validate_links(errors)
    if errors:
        print("Course validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Course validation: PASS")
    print("- one start page and one course file")
    print("- nine modules in order with four depths")
    print("- every depth teaches, runs a lab, and provides answer-key self-assessment")
    print("- Foundation totals 24 focused hours")
    print("- public pages exclude personal and employer context")
    print("- internal links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
