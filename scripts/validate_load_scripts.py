"""Statically enforce non-negotiable safety controls in every k6 course script."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOAD_ROOT = ROOT / "lab" / "load"
REQUIRED = (
    "ALLOWED_TARGETS",
    "AATE_DRY_RUN",
    "DURATION_SECONDS > 15",
    "RATE * 2 > 10",
    "MAX_VUS > 5",
    "100-request ceiling",
    "abortOnFail: true",
    "http_req_duration",
    "http_req_failed",
    "teardown",
    'http.get(`${TARGET}/health`)',
)


def main() -> int:
    errors: list[str] = []
    scripts = sorted(LOAD_ROOT.glob("*.js"))
    if not scripts:
        errors.append("no k6 scripts found")
    for script in scripts:
        text = script.read_text(encoding="utf-8")
        for marker in REQUIRED:
            if marker not in text:
                errors.append(f"{script.relative_to(ROOT)}: missing safety marker {marker!r}")
        if "http://" in text and "localhost:8080" not in text and "127.0.0.1:8080" not in text:
            errors.append(f"{script.relative_to(ROOT)}: unexpected HTTP target")
    if errors:
        print("Load-script validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Load-script validation: PASS")
    print(
        f"- {len(scripts)} script(s) contain target, duration, VU, rate, total, "
        "threshold, abort, dry-run, and recovery controls"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
