"""Scan the Git release tree for private artifacts, high-confidence secrets, and local identity paths."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROHIBITED_PATHS = (
    re.compile(r"(^|/)(archive|artifacts|audit-evidence|fix-evidence)(/|$)", re.IGNORECASE),
    re.compile(r"(^|/)(AATE-CODEX|REMEDIATION_|REWRITE_|FIX_STATUS)", re.IGNORECASE),
    re.compile(r"\.zip$", re.IGNORECASE),
    re.compile(r"(^|/)\.env$", re.IGNORECASE),
)
LOCAL_USER_PATH_PATTERN = re.compile(
    r"(?:[A-Z]:\\Users\\|" + "/" + "Users/|" + "/" + r"home/)[^/\\\s]+",
    re.IGNORECASE,
)
CONTENT_PATTERNS = {
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
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Git worktree to scan")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    paths = tracked_files(root)
    findings: list[str] = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        for pattern in PROHIBITED_PATHS:
            if pattern.search(relative):
                findings.append(f"{relative}: prohibited private-development path")
        if path.is_file():
            data = path.read_bytes()
            if b"\0" not in data:
                text = data.decode("utf-8", errors="replace")
                for label, pattern in CONTENT_PATTERNS.items():
                    for match in pattern.finditer(text):
                        line = text.count("\n", 0, match.start()) + 1
                        findings.append(f"{relative}:{line}: {label}")
    if findings:
        print("Public-tree secret and privacy scan: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Public-tree secret and privacy scan: PASS")
    print(f"- scanned {len(paths)} Git-tracked paths")
    print("- no high-confidence private keys, service tokens, local user paths, or private-development paths found")
    print("Employer-confidentiality review: PASS")
    print("- no employer-specific URLs or email-address markers found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
