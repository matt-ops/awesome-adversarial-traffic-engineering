"""Transparent non-production scoring rules for deterministic fixtures."""

from __future__ import annotations

from typing import Any

WEIGHTS = {
    "automation_property": 2,
    "missing_browser_headers": 1,
    "ua_platform_mismatch": 2,
    "rapid_navigation": 1,
    "expensive_workflow_burst": 2,
}


def score_event(event: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if event.get("webdriver") is True:
        reasons.append("automation_property")
    if not event.get("accept_language") or not event.get("sec_fetch_site"):
        reasons.append("missing_browser_headers")
    user_agent = str(event.get("user_agent", ""))
    platform = str(event.get("platform", ""))
    if ("Windows" in user_agent and "Linux" in platform) or ("Linux" in user_agent and "Win" in platform):
        reasons.append("ua_platform_mismatch")
    if float(event.get("inter_arrival_ms", 1000)) < 100:
        reasons.append("rapid_navigation")
    if event.get("path") == "/api/reports/expensive" and int(event.get("session_expensive_count", 0)) >= 3:
        reasons.append("expensive_workflow_burst")
    score = sum(WEIGHTS[reason] for reason in reasons)
    return {"score": score, "decision": "challenge" if score >= 3 else "allow", "reasons": reasons}
