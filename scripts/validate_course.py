"""Validate the simple public course contract."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = ("README.md", "COURSE.md", "RESOURCES.md", "SAFETY.md", "lab/README.md")
LEVELS = ("foundation", "applied", "integrated", "deep")

FOUNDATION_INSTRUCTION = {
    0: ("csrc.nist.gov/pubs/sp/800/115/final",),
    1: (
        "developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview",
        "academy.hackthebox.com/course/preview/web-requests",
    ),
    2: ("www-project-automated-threats-to-web-applications",),
    3: (
        "developer.mozilla.org/en-US/curriculum/core/javascript-fundamentals",
        "playwright.dev/docs/intro",
    ),
    4: (
        "Bot_Management_and_Anti-Automation_Cheat_Sheet",
        "developers.google.com/machine-learning/crash-course/classification",
    ),
    5: (
        "cloudflare.com/learning/ddos/application-layer-ddos-attack",
        "sre.google/sre-book/handling-overload",
    ),
    6: (
        "docs.python.org/3/tutorial/controlflow.html",
        "academy.hackthebox.com/course/preview/introduction-to-python-3",
    ),
    7: (
        "csrc.nist.gov/pubs/sp/800/115/final",
        "5-Reporting/01-Reporting_Structure",
    ),
    8: ("objective, decision, action, measured result, limitation",),
}


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
                section_match = re.search(
                    r"### Learn\s*(.*?)\s*### Lab\s*(.*?)\s*### Self-assess\s*(.*?)<details>",
                    section,
                    re.DOTALL,
                )
                if section_match is None:
                    continue
                learn, _lab, self_assess = section_match.groups()
                question_count = len(re.findall(r"^\d+\. ", self_assess, re.MULTILINE))
                if question_count < 3:
                    errors.append(
                        f"Module {index} {level}: Self-assess needs at least three questions; "
                        f"got {question_count}"
                    )
                if level == "foundation":
                    if section.count("**Required foundation") != 1:
                        errors.append(
                            f"Module {index} foundation: expected one explicit required-instruction route"
                        )
                    if section.count("**You are ready for the lab when you can:**") != 1:
                        errors.append(
                            f"Module {index} foundation: expected one prerequisite competency gate"
                        )
                    for marker in FOUNDATION_INSTRUCTION[index]:
                        if marker.casefold() not in learn.casefold():
                            errors.append(
                                f"Module {index} foundation: missing required instruction marker: {marker}"
                            )

                level_index = LEVELS.index(level)
                if level_index < len(LEVELS) - 1:
                    next_anchor = f"#module-{index}-{LEVELS[level_index + 1]}"
                elif index < 8:
                    next_anchor = f"#module-{index + 1}-foundation"
                else:
                    next_anchor = "#you-are-done"
                if section.count("[Next:") != 1 or f"]({next_anchor})" not in section:
                    errors.append(
                        f"Module {index} {level}: Next must follow the linear path to {next_anchor}"
                    )

    if course.count("**Red-team outcome:**") != 9:
        errors.append("COURSE.md must state one red-team outcome for every module")
    for command in (
        "python -m lab.run recon",
        "python -m lab.run credential",
        "python -m lab.run evasion",
        "python -m lab.run bypass",
    ):
        if command not in course:
            errors.append(f"COURSE.md must assign the Foundation offensive exercise: {command}")

    recon_contract = (
        "## Recon before attack",
        "passive reconnaissance",
        "bounded active mapping",
        "documented`, `observed`, or `inferred",
        "workflow/control/resource map",
    )
    lifecycle_text = course + read("README.md")
    for marker in recon_contract:
        if marker.casefold() not in lifecycle_text.casefold():
            errors.append(f"missing recon-to-attack lifecycle marker: {marker}")
    if "python -m lab.run recon" not in read("lab/README.md"):
        errors.append("lab/README.md must put the local recon command before the attacks")
    if "**Recon question:**" in course:
        errors.append("COURSE.md must integrate recon into the lifecycle and concrete attacks, not every module")

    external_coverage = {
        "automated-threat taxonomy": "www-project-automated-threats-to-web-applications",
        "real browser sensor": "github.com/fingerprintjs/BotD",
        "proxy-chain range": "pivoting-tunneling-and-port-forwarding",
        "front-end parsing bypass": "portswigger.net/web-security/request-smuggling",
        "isolated packet spoofing": "Networking/Sniffing_Spoofing",
        "isolated DoS range": "research.cec.sc.edu/cyberinfra/cybertraining",
        "advanced exploit-development range": "WEB-300-Advanced-Web-Attacks-and-Exploitation",
        "visual CAPTCHA-solving range": "hacking-captcha-systems",
        "web reconnaissance methodology": "01-Information_Gathering",
        "API reconnaissance assignment": "api-testing#api-recon",
        "hands-on web reconnaissance range": "information-gathering---web-edition",
        "network enumeration range": "network-enumeration-with-nmap",
        "WAF discovery before bypass": "github.com/EnableSecurity/wafw00f",
    }
    coverage_text = course + read("RESOURCES.md")
    for capability, marker in external_coverage.items():
        if marker not in coverage_text:
            errors.append(f"missing explicit external coverage for {capability}: {marker}")
    if "## Coverage fallback" not in read("RESOURCES.md"):
        errors.append("RESOURCES.md must explain how restricted or unrealistic in-repo labs are replaced")

    public_text = "\n".join(read(path) for path in PUBLIC_FILES)
    for term in ("amazon", "atoz", "10428500", "mattn", "matt-ops"):
        if term in public_text.casefold():
            errors.append(f"public course contains prohibited personal/employer term: {term}")
    obsolete_schedule_terms = (
        "24-hour",
        "24 hour",
        "7-day",
        "7 day",
        "21-day",
        "21 day",
        "6-week",
        "6 week",
        "checkpoint",
        "exit ramp",
    )
    for obsolete in obsolete_schedule_terms:
        if obsolete in public_text.casefold():
            errors.append(f"public course still contains obsolete schedule/checkpoint language: {obsolete}")

    readme = read("README.md")
    if "[Open the course](COURSE.md)" not in readme:
        errors.append("README.md must expose one obvious course start link")
    for phrase in ("red-team-first", "execute attack", "prove bypass"):
        if phrase not in readme.casefold():
            errors.append(f"README.md must make the offensive course contract explicit: {phrase}")

    validate_links(errors)
    if errors:
        print("Course validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Course validation: PASS")
    print("- one start page and one course file")
    print("- nine modules follow one linear Foundation -> Applied -> Integrated -> Deep path")
    print("- every Foundation names exact prerequisite instruction and a competency gate")
    print("- every section provides an answer-key self-assessment")
    print("- every module states an offensive outcome and includes real local or assigned attacks")
    print("- recon is one lifecycle phase and directly prepares concrete attacks without repeated module prompts")
    print("- restricted or unrealistic attack skills route to exact external ranges")
    print("- obsolete schedules, checkpoints, exit ramps, and word-count proxies are absent")
    print("- public pages exclude personal and employer context")
    print("- internal links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
