"""Run the course's small, bounded local exercises.

Every exercise is hard-coded to localhost and keeps totals below the safety envelope.
Start the lab first with: docker compose -f lab/docker-compose.yml up --build -d
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from typing import Any

from lab.detectors.rules import score_event

BASE_URL = "http://localhost:8080"


def request(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, Any], float]:
    if not path.startswith("/") or "://" in path:
        raise ValueError("exercise paths must be local relative paths")
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": "aate-course-lab/1.0"}
    if extra_headers:
        headers.update(extra_headers)
    http_request = urllib.request.Request(  # noqa: S310 - fixed localhost base URL and relative-path check above.
        BASE_URL + path, data=body, headers=headers, method=method
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(http_request, timeout=3) as response:  # noqa: S310 - fixed localhost base URL.
            status = response.status
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        status = exc.code
        data = json.loads(exc.read().decode("utf-8"))
    return status, data, round((time.perf_counter() - started) * 1000, 2)


def reset() -> None:
    status, _, _ = request("POST", "/api/reset")
    if status != 200:
        raise RuntimeError("local reset failed")


def credential_demo() -> None:
    reset()
    attempts = [
        ("alice", "wrong-1", "spray-a"),
        ("bob", "wrong-1", "spray-a"),
        ("carol", "wrong-1", "spray-a"),
        ("alice", "wonderland", "stuff-b"),
        ("bob", "not-builder", "stuff-b"),
    ]
    for username, password, session_id in attempts:
        status, _, elapsed = request(
            "POST",
            "/api/auth/login",
            {"username": username, "password": password, "session_id": session_id},
        )
        print(json.dumps({"username": username, "session_id": session_id, "status": status, "elapsed_ms": elapsed}))
        time.sleep(0.1)
    _, summary, _ = request("GET", "/api/auth/attempts")
    print(json.dumps({"summary": summary}, sort_keys=True))


def workflow_demo() -> None:
    reset()
    steps = [
        ("POST", "/api/accounts/create", {"username": "student-1", "password": "lab-only", "session_id": "agent-1"}),
        ("POST", "/api/auth/login", {"username": "student-1", "password": "lab-only", "session_id": "agent-1"}),
        ("GET", "/api/search?q=demo", None),
        ("GET", "/api/products/demo-1", None),
        ("POST", "/api/cart/reserve", {"identity": "student-1", "product_id": "demo-1", "quantity": 1}),
        ("POST", "/api/promotions/redeem", {"identity": "student-1", "code": "LABONLY"}),
        ("POST", "/api/challenge", {"session_id": "agent-1", "answer": "AATE"}),
    ]
    for number, (method, path, payload) in enumerate(steps, start=1):
        status, body, elapsed = request(method, path, payload)
        print(
            json.dumps(
                {
                    "step": number,
                    "action": f"{method} {path}",
                    "status": status,
                    "elapsed_ms": elapsed,
                    "observation": body,
                }
            )
        )
        if status >= 400:
            print(json.dumps({"agent": "stopped", "reason": "unexpected response"}))
            return
    print(json.dumps({"agent": "finished", "steps": len(steps), "policy": "fixed local workflow"}))


def resilience_demo() -> None:
    reset()
    samples: dict[str, list[float]] = {"cheap": [], "expensive": []}
    for _ in range(5):
        for label, path in (("cheap", "/health"), ("expensive", "/api/reports/expensive?work=100")):
            status, _, elapsed = request("GET", path)
            if status != 200:
                raise RuntimeError(f"unexpected {status} from {path}")
            samples[label].append(elapsed)
            time.sleep(0.1)
    for label, values in samples.items():
        print(
            json.dumps(
                {
                    "endpoint": label,
                    "requests": len(values),
                    "median_ms": round(statistics.median(values), 2),
                    "max_ms": max(values),
                }
            )
        )
    ratio = statistics.median(samples["expensive"]) / max(statistics.median(samples["cheap"]), 0.01)
    print(json.dumps({"expensive_to_cheap_median_ratio": round(ratio, 2), "claim": "local relative cost only"}))


def evasion_demo() -> None:
    baseline = {
        "webdriver": True,
        "accept_language": "",
        "sec_fetch_site": "",
        "user_agent": "Chrome Windows",
        "platform": "Win32",
        "inter_arrival_ms": 350,
        "path": "/api/cart/reserve",
        "session_expensive_count": 0,
    }
    evaded = {**baseline, "webdriver": False}
    baseline_result = score_event(baseline)
    evaded_result = score_event(evaded)
    if baseline_result["decision"] != "challenge" or evaded_result["decision"] != "allow":
        raise RuntimeError("detector fixture no longer demonstrates the expected one-signal bypass")
    print(json.dumps({"phase": "baseline", "event": baseline, **baseline_result}, sort_keys=True))
    print(
        json.dumps(
            {"phase": "bypass", "changed": "webdriver true -> false", "event": evaded, **evaded_result},
            sort_keys=True,
        )
    )
    print(json.dumps({"result": "control bypassed", "protected_workflow": "/api/cart/reserve"}))


def bypass_demo() -> None:
    reset()
    denied_status, _, _ = request("GET", "/api/reports/protected?session_id=attacker-copy&work=10")
    challenge_status, challenge_body, _ = request(
        "POST", "/api/challenge", {"session_id": "solver-session", "answer": "AATE"}
    )
    token = str(challenge_body.get("lab_token", ""))
    replay_status, replay_body, _ = request(
        "GET",
        "/api/reports/protected?session_id=attacker-copy&work=10",
        extra_headers={"X-Lab-Challenge": token},
    )
    if (denied_status, challenge_status, replay_status) != (403, 200, 200):
        raise RuntimeError("challenge replay did not produce the expected local bypass")
    print(json.dumps({"phase": "baseline", "without_token_status": denied_status}))
    print(json.dumps({"phase": "capture", "solver_session": "solver-session", "token": token}))
    print(
        json.dumps(
            {
                "phase": "bypass",
                "replayed_as_session": "attacker-copy",
                "status": replay_status,
                "observation": replay_body,
            }
        )
    )
    print(json.dumps({"result": "control bypassed", "weakness": "token not bound to session, action, expiry, or use"}))


def ratelimit_demo() -> None:
    reset()
    fixed_statuses = [request("GET", "/api/reports/limited?session_id=fixed&work=10")[0] for _ in range(3)]
    rotated_statuses = [
        request("GET", f"/api/reports/limited?session_id=rotated-{number}&work=10")[0] for number in range(1, 4)
    ]
    if fixed_statuses != [200, 200, 429] or rotated_statuses != [200, 200, 200]:
        raise RuntimeError("per-session limit no longer demonstrates the expected key-rotation bypass")
    print(json.dumps({"phase": "baseline", "session": "fixed", "statuses": fixed_statuses}))
    print(
        json.dumps(
            {"phase": "bypass", "mutation": "rotate caller-supplied session_id", "statuses": rotated_statuses}
        )
    )
    print(json.dumps({"result": "control bypassed", "weakness": "rate limit trusts one attacker-controlled key"}))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exercise", choices=("credential", "workflow", "evasion", "bypass", "ratelimit", "resilience"))
    args = parser.parse_args()
    try:
        {
            "credential": credential_demo,
            "workflow": workflow_demo,
            "evasion": evasion_demo,
            "bypass": bypass_demo,
            "ratelimit": ratelimit_demo,
            "resilience": resilience_demo,
        }[args.exercise]()
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "hint": "start the local Docker lab first"}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
