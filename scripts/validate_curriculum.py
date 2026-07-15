"""Validate the authoritative one-path curriculum contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__ in {None, ""}:  # Support direct execution as documented.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.progress import EXPECTED_MODULES, load_progress, validate_progress

ROOT = Path(__file__).resolve().parents[1]
MODULE_FILES = (
    "00-safety-and-engagement.md",
    "01-request-path-and-network.md",
    "02-automated-abuse.md",
    "03-browser-automation.md",
    "04-browser-signals-and-detection.md",
    "05-edge-and-ddos.md",
    "06-python-and-code-review.md",
    "07-experiment-analysis-reporting.md",
    "08-interview-communication.md",
)
LEVEL_HEADINGS = (
    "## Level 1: Foundation, 24-hour checkpoint",
    "## Level 2: Applied, 7-day checkpoint",
    "## Level 3: Integrated, 21-day checkpoint",
    "## Level 4: Deep, 6-week checkpoint",
)
REQUIRED_LEVEL_FIELDS = (
    "### Knowledge outcome",
    "### Hands-on outcome",
    "### Interview outcome",
    "### Required artifact",
    "### Completion test",
    "### Estimated time",
    "### Required resources only",
    "### Optional deeper resources",
)
CHECKPOINTS = ("24-hours.md", "7-days.md", "21-days.md", "6-weeks.md")
DEPTH_LABELS = ("[L1 Foundation]", "[L2 Applied]", "[L3 Integrated]", "[L4 Deep]")
PRIORITY_LABELS = ("[Required]", "[Recommended]", "[Optional]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_modules(errors: list[str]) -> None:
    module_dir = ROOT / "curriculum" / "modules"
    actual = tuple(path.name for path in sorted(module_dir.glob("*.md")))
    if actual != MODULE_FILES:
        errors.append(f"expected exactly nine canonical modules in order; found {actual}")
        return
    for filename in MODULE_FILES:
        text = read(module_dir / filename)
        for index, heading in enumerate(LEVEL_HEADINGS):
            if text.count(heading) != 1:
                errors.append(f"{filename}: expected one {heading!r}")
                continue
            start = text.index(heading)
            end = (
                text.find(LEVEL_HEADINGS[index + 1], start)
                if index + 1 < len(LEVEL_HEADINGS)
                else text.find("## Common misconceptions", start)
            )
            section = text[start:end if end != -1 else None]
            for field in REQUIRED_LEVEL_FIELDS:
                if field not in section:
                    errors.append(f"{filename}: {heading} missing {field}")


def validate_checkpoints(errors: list[str]) -> None:
    checkpoint_dir = ROOT / "curriculum" / "checkpoints"
    for checkpoint_index, filename in enumerate(CHECKPOINTS, start=1):
        text = read(checkpoint_dir / filename)
        if re.search(r"^## Level [1-4]:", text, re.MULTILINE):
            errors.append(f"{filename}: checkpoint duplicates a module level section")
        anchor = LEVEL_HEADINGS[checkpoint_index - 1][3:].lower().replace(",", "").replace(":", "").replace(" ", "-")
        for module_file in MODULE_FILES:
            link = f"../modules/{module_file}#{anchor}"
            if link not in text:
                errors.append(f"{filename}: missing canonical link {link}")

    foundation = read(checkpoint_dir / "24-hours.md")
    times = [float(value) for value in re.findall(r"^\| [0-8] \| .*?\| ([0-9.]+) h \|", foundation, re.MULTILINE)]
    if len(times) != 9 or sum(times) != 24.0:
        errors.append(f"24-hours.md: Foundation budget must contain nine rows totaling 24 hours; got {times}")


def validate_resources(errors: list[str]) -> None:
    for path in sorted((ROOT / "awesome").glob("*.md")):
        if path.name == "README.md":
            continue
        for line_number, line in enumerate(read(path).splitlines(), start=1):
            if not line.startswith("- [") or "](" not in line:
                continue
            depths = sum(label in line for label in DEPTH_LABELS)
            priorities = sum(label in line for label in PRIORITY_LABELS)
            if depths != 1 or priorities != 1:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: resource needs exactly one depth and priority label"
                )
            if " · Module" not in line:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: resource needs canonical module mapping")
            if line.count(" · ") < 2:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: resource needs a source type")


def validate_cross_repository(errors: list[str]) -> None:
    readme = read(ROOT / "README.md")
    if "[Start the Path](curriculum/path.md)" not in readme:
        errors.append("README.md: missing prominent Start the Path link")
    if "24 cumulative focused hours" not in readme:
        errors.append("README.md: first checkpoint is not defined as 24 cumulative focused hours")

    path_text = read(ROOT / "curriculum" / "path.md")
    for filename in MODULE_FILES:
        if f"modules/{filename}" not in path_text:
            errors.append(f"curriculum/path.md: missing {filename}")

    lab_map = read(ROOT / "curriculum" / "lab-mapping.md")
    for index in range(9):
        if not re.search(rf"^\| {index} ", lab_map, re.MULTILINE):
            errors.append(f"curriculum/lab-mapping.md: missing Module {index}")

    implementation_text = "\n".join(
        [read(ROOT / "README.md"), path_text]
        + [read(ROOT / "curriculum" / "checkpoints" / name) for name in CHECKPOINTS]
        + [read(ROOT / "curriculum" / "modules" / name) for name in MODULE_FILES]
    )
    if re.search(r"Level 4: Practitioner|Practitioner, 6-week|8 to 10 focused", implementation_text, re.IGNORECASE):
        errors.append("implementation contains a conflicting legacy depth or abbreviated first-checkpoint term")

    try:
        progress = load_progress(ROOT / "curriculum" / "progress.yaml")
    except ValueError as exc:
        errors.append(str(exc))
    else:
        errors.extend(f"curriculum/progress.yaml: {error}" for error in validate_progress(progress))
        if tuple(progress.get("modules", {})) != EXPECTED_MODULES:
            errors.append("curriculum/progress.yaml: module keys do not match the nine canonical modules")


def main() -> int:
    errors: list[str] = []
    validate_modules(errors)
    validate_checkpoints(errors)
    validate_resources(errors)
    validate_cross_repository(errors)
    if errors:
        print("Curriculum contract: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Curriculum contract: PASS")
    print("- one canonical path")
    print("- nine modules with Foundation, Applied, Integrated, and Deep sections")
    print("- checkpoint views reference module sections")
    print("- Foundation budget totals 24 cumulative focused hours")
    print("- resource, lab, and progress mappings satisfy the addendum")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
