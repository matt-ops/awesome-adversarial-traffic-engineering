"""Statically enforce non-negotiable safety controls in every k6 course script."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOAD_ROOT = ROOT / "lab" / "load"
CONFIG_REQUIRED = (
    "ALLOWED_TARGETS",
    '"endpoint-cost-observation"',
    '"workflow-sequence-observation"',
    "AATE_DRY_RUN",
    '"AATE_DURATION", 1, 15',
    '"AATE_RATE", 1, 5',
    '"AATE_MAX_VUS", 1, 5',
    "rate * 2 > 10",
    "worstCaseRequests > 100",
    "100-request ceiling",
    "abortOnFail: true",
    "http_req_duration",
    "http_req_failed",
)
SCRIPT_REQUIRED = (
    'from "./config.mjs"',
    "parseLoadConfiguration(__ENV)",
    "teardown",
    'http.get(`${TARGET}/health`)',
    "cheap-expensive: expensive request took longer",
    "cache-bypass: fixed key is a cache hit",
    "cache-bypass: bypass path performs fresh work",
    "identity-key: pre-seeded fixed key is rejected",
    "identity-key: rotated caller key is accepted",
    "endpoint-cost-observation: higher work took longer",
    "workflow-sequence-observation: search exposes demo-1",
    "workflow-sequence-observation: product step resolves demo-1",
    "retry-amplification: exactly one retry is attempt two",
    "recovery health returned within 1000ms",
)
PROHIBITED = (
    '"endpoint-specific"',
    '"workflow-aware"',
)


def main() -> int:
    errors: list[str] = []
    scripts = sorted(LOAD_ROOT.glob("*.js"))
    config_path = LOAD_ROOT / "config.mjs"
    config_text = config_path.read_text(encoding="utf-8") if config_path.is_file() else ""
    if not config_text:
        errors.append("lab/load/config.mjs: missing pure load-configuration module")
    for marker in CONFIG_REQUIRED:
        if marker not in config_text:
            errors.append(f"lab/load/config.mjs: missing safety marker {marker!r}")
    for marker in PROHIBITED:
        if marker in config_text:
            errors.append(f"lab/load/config.mjs: obsolete scenario name {marker!r}")
    if not scripts:
        errors.append("no k6 scripts found")
    for script in scripts:
        text = script.read_text(encoding="utf-8")
        for marker in SCRIPT_REQUIRED:
            if marker not in text:
                errors.append(f"{script.relative_to(ROOT)}: missing safety marker {marker!r}")
        for marker in PROHIBITED:
            if marker in text:
                errors.append(f"{script.relative_to(ROOT)}: obsolete scenario name {marker!r}")
        if "http://" in text and "localhost:8080" not in text and "127.0.0.1:8080" not in text:
            errors.append(f"{script.relative_to(ROOT)}: unexpected HTTP target")
    if errors:
        print("Load-script validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Load-script validation: PASS")
    print(
        f"- {len(scripts)} script(s) use the tested pure target, duration, VU, rate, total, "
        "threshold, abort, and dry-run configuration"
    )
    print(
        "- recovery, truthful scenario names, and deterministic outcome assertions remain in the executable script"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
