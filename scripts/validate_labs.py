"""Validate the required instructional contract on every learner lab page."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = ROOT / "docs" / "labs"
SAMPLE_REPORT = ROOT / "lab" / "reports" / "synthetic-finding.md"
LAB_MAP = ROOT / "lab" / "LAB_COURSE_MAP.md"
PUBLIC_LAB_MAP = ROOT / "docs" / "labs" / "course-map.md"
COMPOSE_FILE = ROOT / "lab" / "docker-compose.yml"
CHALLENGE_LAB_PAGE = LAB_ROOT / "applied" / "challenge-systems.md"
CLASSIFIER_LAB_PAGE = LAB_ROOT / "integrated" / "classifier-evaluation.md"
PROTOCOL_LAB_PAGE = LAB_ROOT / "integrated" / "multi-client-protocol-comparison.md"
CHALLENGE_LAB_MARKERS = (
    "POST /api/challenge",
    "GET /api/reports/protected",
    "npm run playwright:challenge-flow",
    "python -m lab.analysis.challenge_metrics",
    "no visual CAPTCHA widget or iframe",
    "Session B's first transfer receives `403`",
    "Session A's intended request succeeds once before expiry",
)
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
MAP_FIELDS = (
    "- **Canonical lesson:**",
    "- **Checkpoint:**",
    "- **Prerequisite:**",
    "- **Offensive objective:**",
    "- **Protected action or service effect:**",
    "- **Expected output:**",
    "- **Interpretation:**",
    "- **Source basis:**",
    "- **Safety boundary:**",
    "- **Expected evidence or output:**",
    "- **Cleanup:**",
    "- **Retest use:**",
)
REQUIRED_COMMAND_MARKERS = (
    "lab.clients.safe_client --dry-run",
    "python -m http.server 4173",
    "playwright:first",
    "docker compose -f lab/docker-compose.yml up",
    "python -m lab.run recon",
    "python -m lab.run credential",
    "python -m lab.run workflow",
    "playwright:workflow-authorization",
    "python -m lab.run ratelimit",
    "playwright:challenge-flow",
    "python -m lab.analysis.challenge_metrics",
    "python -m lab.analysis.analyze",
    "playwright:control-recon",
    "python -m lab.run bypass",
    "python -m lab.analysis.traffic_intelligence",
    "python -m lab.analysis.classifier_tradeoffs",
    "python -m lab.protocol.compare automated",
    "k6 run lab/load/bounded.js",
    "lab.tooling.client telemetry",
    "lab.tooling.client concurrent",
    "lab.tooling.client retry",
)


def command_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^### `([^`]+)`\s*$", text, re.MULTILINE))
    return [
        (match.group(1), text[match.start() : matches[index + 1].start() if index + 1 < len(matches) else len(text)])
        for index, match in enumerate(matches)
    ]


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

    if not CHALLENGE_LAB_PAGE.is_file():
        errors.append("docs/labs/applied/challenge-systems.md: required challenge lab page is missing")
    else:
        challenge_lab = CHALLENGE_LAB_PAGE.read_text(encoding="utf-8")
        for marker in CHALLENGE_LAB_MARKERS:
            if marker not in challenge_lab:
                errors.append(f"{CHALLENGE_LAB_PAGE.relative_to(ROOT)}: challenge marker missing: {marker}")

    for page, markers in (
        (
            CLASSIFIER_LAB_PAGE,
            (
                "python -m lab.analysis.classifier_tradeoffs",
                "0.50",
                "0.75",
                "near-neighbor",
                "adapted",
                "protected-action",
            ),
        ),
        (
            PROTOCOL_LAB_PAGE,
            (
                "python -m lab.protocol.compare automated",
                "127.0.0.1",
                "one connection per raw client observer",
                "eight HTTP/2 streams",
                "45-second whole command",
                "external_request_attempt_count",
                "not JA4; not identity proof",
                "unsupported",
            ),
        ),
    ):
        if not page.is_file():
            errors.append(f"{page.relative_to(ROOT)}: required practical lab page is missing")
            continue
        page_text = page.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in page_text:
                errors.append(f"{page.relative_to(ROOT)}: practical marker missing: {marker}")

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

    if not LAB_MAP.is_file():
        errors.append("lab/LAB_COURSE_MAP.md: complete command map is missing")
        blocks: list[tuple[str, str]] = []
    else:
        map_text = LAB_MAP.read_text(encoding="utf-8")
        blocks = command_blocks(map_text)
        for command, block in blocks:
            for field in MAP_FIELDS:
                if block.count(field) != 1:
                    errors.append(f"lab/LAB_COURSE_MAP.md: {command!r} requires exactly one {field}")
        for marker in REQUIRED_COMMAND_MARKERS:
            if marker not in map_text:
                errors.append(f"lab/LAB_COURSE_MAP.md: required command is orphaned: {marker}")
    if not PUBLIC_LAB_MAP.is_file():
        errors.append("docs/labs/course-map.md: public command map is missing")
    elif LAB_MAP.is_file() and PUBLIC_LAB_MAP.read_text(encoding="utf-8") != LAB_MAP.read_text(encoding="utf-8"):
        errors.append("docs/labs/course-map.md: public map drifted from lab/LAB_COURSE_MAP.md")

    if not COMPOSE_FILE.is_file():
        errors.append("lab/docker-compose.yml: local lab definition is missing")
    else:
        compose = COMPOSE_FILE.read_text(encoding="utf-8")
        for required_safety_text in (
            '"127.0.0.1:8080:8080"',
            "aate-local:",
            "internal: true",
            "aate-loopback-publish:",
            "networks: [aate-local, aate-loopback-publish]",
        ):
            if required_safety_text not in compose:
                errors.append(
                    "lab/docker-compose.yml: missing loopback/isolation control "
                    f"{required_safety_text!r}"
                )
        app_block, _, remainder = compose.partition("\n  edge:")
        edge_block, _, _ = remainder.partition("\nnetworks:")
        if "networks: [aate-local]" not in app_block or "ports:" in app_block:
            errors.append("lab/docker-compose.yml: app must stay internal and publish no host port")
        if "networks: [aate-local, aate-loopback-publish]" not in edge_block:
            errors.append("lab/docker-compose.yml: only the edge may join the loopback-publish network")

    if errors:
        print("Lab validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Lab validation: PASS")
    print(f"- {len(pages)} lab pages contain the complete experiment contract")
    print(f"- {len(blocks)} command records contain every course-map field and the public copy is synchronized")
    print("- the synthetic sample report contains evidence, impact, remediation, retest, and limits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
