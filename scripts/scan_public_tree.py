"""Validate the tracked public release boundary and scan text for sensitive data."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_ROOT_FILES = frozenset(
    {
        ".editorconfig",
        ".env.example",
        ".gitattributes",
        ".gitignore",
        ".markdownlint-cli2.jsonc",
        ".prettierrc.json",
        "LICENSE",
        "Makefile",
        "README.md",
        "RESOURCES.md",
        "SAFETY.md",
        "eslint.config.mjs",
        "mkdocs.yml",
        "package-lock.json",
        "package.json",
        "pyproject.toml",
        "tsconfig.json",
    }
)
ALLOWED_TOP_LEVEL_DIRECTORIES = frozenset({".github", "curriculum", "docs", "lab", "scripts", "sources", "tests"})
APPROVED_LEARNER_REPORTS = frozenset({"lab/reports/synthetic-finding.md"})
APPROVED_LEARNER_MEDIA_PREFIXES = ("docs/assets/",)
GENERATED_DIRECTORY_NAMES = frozenset({".docs-build", "site"})
LOCAL_OUTPUT_DIRECTORY_NAMES = frozenset({"telemetry"})
AUDIT_EVIDENCE_DIRECTORY_NAMES = frozenset({"audit", "audits", "audit-evidence", "evidence"})
IMAGE_SUFFIXES = frozenset({".gif", ".jpeg", ".jpg", ".png", ".webp"})

LOCAL_USER_PATH_PATTERN = re.compile(
    r"(?:[A-Z]:\\Users\\|" + "/" + "Users/|" + "/" + r"home/)[^/\\\s]+",
    re.IGNORECASE,
)
CONTENT_PATTERNS: dict[str, re.Pattern[str]] = {
    "private-key block": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "local user path": LOCAL_USER_PATH_PATTERN,
    "employer-specific URL": re.compile(r"https?://[^\s]*(?:amazon\.jobs|corp(?:orate)?\.|internal\.)", re.IGNORECASE),
    "employer email": re.compile(r"\b[A-Za-z0-9._%+-]+@(?:amazon|aws)\.com\b", re.IGNORECASE),
}


def tracked_files(root: Path) -> list[Path]:
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable is required for the public-tree scan")
    completed = subprocess.run(  # noqa: S603 - fixed Git command, no shell or untrusted arguments.
        [git, "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [root / path for path in completed.stdout.decode("utf-8").split("\0") if path]


def path_findings(relative: str) -> list[str]:
    """Return release-boundary findings for one repository-relative path."""
    findings: list[str] = []
    public_path = PurePosixPath(relative)
    parts = public_path.parts
    if not parts:
        return ["empty tracked path"]

    if len(parts) == 1:
        if relative not in ALLOWED_ROOT_FILES:
            findings.append("unapproved root file")
    else:
        top_level = parts[0]
        if top_level in GENERATED_DIRECTORY_NAMES:
            findings.append("generated site or documentation output")
        elif top_level not in ALLOWED_TOP_LEVEL_DIRECTORIES:
            findings.append("unapproved top-level directory")

    directory_names = {part.casefold() for part in parts[:-1]}
    if directory_names & GENERATED_DIRECTORY_NAMES:
        findings.append("generated site or documentation output")
    if directory_names & LOCAL_OUTPUT_DIRECTORY_NAMES:
        findings.append("local telemetry output")
    if "reports" in directory_names and relative not in APPROVED_LEARNER_REPORTS:
        findings.append("unapproved generated report")
    if directory_names & AUDIT_EVIDENCE_DIRECTORY_NAMES:
        findings.append("audit evidence directory")

    name = public_path.name.casefold()
    if public_path.suffix.casefold() == ".zip":
        findings.append("ZIP archive")
    if name == ".env":
        findings.append("local environment file")
    if "screenshot" in name:
        findings.append("review screenshot")
    if public_path.suffix.casefold() in IMAGE_SUFFIXES and not relative.startswith(APPROVED_LEARNER_MEDIA_PREFIXES):
        findings.append("image outside the approved learner-facing media location")
    return findings


def scan_paths(root: Path, paths: list[Path]) -> list[str]:
    """Scan an explicit set of paths, allowing unit tests to exercise the policy without Git."""
    findings: list[str] = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        findings.extend(f"{relative}: {finding}" for finding in path_findings(relative))
        if not path.is_file():
            findings.append(f"{relative}: tracked path is missing from the worktree")
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        for label, pattern in CONTENT_PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{relative}:{line}: {label}")
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Git worktree to scan")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    paths = tracked_files(root)
    findings = scan_paths(root, paths)
    if findings:
        print("Public-tree boundary and sensitive-data scan: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Public-tree boundary and sensitive-data scan: PASS")
    print(f"- scanned {len(paths)} Git-tracked paths")
    print("- every root file and top-level directory is explicitly approved")
    print("- no generated output, archives, local telemetry, or review evidence found")
    print("- no high-confidence private keys, service tokens, or local user paths found")
    print("Employer-confidentiality review: PASS")
    print("- no employer-specific URLs or email-address markers found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
