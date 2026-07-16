"""Synthetic local commerce API for authorized AATE experiments."""

from __future__ import annotations

import hashlib
import time
import uuid
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Query, Request
from pydantic import BaseModel, Field
from starlette.responses import HTMLResponse, PlainTextResponse, Response

app = FastAPI(title="AATE Local App", version="0.1.0")
EVENTS: list[dict[str, Any]] = []
INVENTORY = defaultdict(lambda: 5, {"demo-1": 5, "demo-2": 3})
PROMOTIONS: set[tuple[str, str]] = set()
LAB_USERS = {"alice": "wonderland", "bob": "builder", "carol": "sunrise"}
CREATED_USERS: dict[str, str] = {}
LOGIN_ATTEMPTS: list[dict[str, Any]] = []
CHALLENGE_TOKENS: set[str] = set()
LIMITED_REPORT_CALLS: defaultdict[str, int] = defaultdict(int)
CONTROL_NONCES: set[str] = set()
CONTROL_TOKENS: set[str] = set()
CACHEABLE_REPORTS: dict[str, str] = {}
UNSTABLE_CALLS: defaultdict[str, int] = defaultdict(int)


class Event(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    event_type: str = Field(min_length=1, max_length=64)
    attributes: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class IdentityRequest(BaseModel):
    identity: str = Field(min_length=1, max_length=64)


class ReserveRequest(IdentityRequest):
    product_id: str = Field(min_length=1, max_length=64)
    quantity: int = Field(ge=1, le=2)


class PromotionRequest(IdentityRequest):
    code: str = Field(min_length=1, max_length=32)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)
    session_id: str = Field(min_length=1, max_length=64)


class AccountRequest(LoginRequest):
    pass


class ChallengeRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    answer: str = Field(min_length=1, max_length=32)


class ContextObservation(BaseModel):
    language: str = Field(min_length=1, max_length=32)
    platform: str = Field(min_length=1, max_length=64)


class ControlEvaluationRequest(BaseModel):
    trial_id: str = Field(min_length=1, max_length=64)
    population: str = Field(min_length=1, max_length=64)
    nonce: str = Field(min_length=8, max_length=128)
    captured_at_ms: int = Field(gt=0)
    webdriver: bool
    user_agent: str = Field(min_length=1, max_length=512)
    timezone: str = Field(min_length=1, max_length=64)
    viewport_width: int = Field(gt=0, le=10000)
    screen_width: int = Field(gt=0, le=10000)
    page: ContextObservation
    frame: ContextObservation
    worker: ContextObservation


@app.middleware("http")
async def request_context(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    started = time.perf_counter()
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))[:128]
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-aate-latency-ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
    return response


@app.get("/")
def root() -> dict[str, str]:
    return {"project": "AATE", "scope": "synthetic local lab"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aate-local-app"}


@app.get("/control-lab", response_class=HTMLResponse)
def control_lab() -> str:
    """Serve three same-origin execution contexts for local signal collection."""
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>AATE control lab</title></head>
<body><h1>AATE control lab</h1><p id="status">ready</p>
<iframe title="sensor frame" src="/control-frame"></iframe>
<script>
window.aateWorkerReady = new Promise((resolve, reject) => {
  const worker = new Worker('/control-worker.js');
  worker.onmessage = (event) => resolve(event.data);
  worker.onerror = reject;
});
</script></body></html>"""


@app.get("/control-frame", response_class=HTMLResponse)
def control_frame() -> str:
    return "<!doctype html><html lang='en'><body><p>sensor frame ready</p></body></html>"


@app.get("/control-worker.js", response_class=PlainTextResponse)
def control_worker() -> str:
    return "postMessage({language: navigator.language, platform: navigator.platform || 'worker-unavailable'});"


@app.post("/api/control/evaluate")
def evaluate_control(payload: ControlEvaluationRequest) -> dict[str, Any]:
    """Evaluate transparent toy rules and issue a single-use local action token."""
    if payload.nonce in CONTROL_NONCES:
        raise HTTPException(status_code=409, detail="synthetic sensor nonce replayed")
    CONTROL_NONCES.add(payload.nonce)

    reasons: list[str] = []
    if payload.webdriver:
        reasons.append("top_page_webdriver")
    languages = {payload.page.language, payload.frame.language, payload.worker.language}
    if len(languages) != 1:
        reasons.append("cross_context_language_mismatch")
    if payload.viewport_width > payload.screen_width:
        reasons.append("viewport_exceeds_screen")

    decision = "challenge" if reasons else "allow"
    token: str | None = None
    if decision == "allow":
        token = hashlib.sha256(f"{payload.trial_id}:{payload.nonce}:aate-control".encode()).hexdigest()[:24]
        CONTROL_TOKENS.add(token)
    return {
        "trial_id": payload.trial_id,
        "population": payload.population,
        "decision": decision,
        "reasons": reasons,
        "action_token": token,
        "limitations": "transparent synthetic rules; not a production bot-control model",
    }


@app.post("/api/control/protected")
def control_protected(
    session_id: str = Query(min_length=1, max_length=64),
    x_aate_control: str | None = Header(default=None),
) -> dict[str, Any]:
    """Perform the toy protected action once for an allowed evaluation token."""
    if x_aate_control not in CONTROL_TOKENS:
        raise HTTPException(status_code=403, detail="synthetic control authorization required")
    CONTROL_TOKENS.remove(x_aate_control)
    return {"accepted": True, "session_id": session_id, "action": "synthetic-report-created"}


@app.get("/api/search")
def search(q: str = Query(default="demo", max_length=64)) -> dict[str, Any]:
    products = [
        {"id": "demo-1", "name": "Synthetic Widget"},
        {"id": "demo-2", "name": "Synthetic Kit"},
    ]
    needle = q.casefold()
    return {"query": q, "results": [item for item in products if needle in item["name"].casefold() or needle == "demo"]}


@app.get("/api/protocol/observe")
def protocol_observe(request: Request) -> dict[str, Any]:
    """Return server-visible HTTP metadata for the fixed local comparison."""
    return {
        "http_version": request.scope.get("http_version", "unknown"),
        "method": request.method,
        "path": request.url.path,
        "host": request.headers.get("host", ""),
        "user_agent": request.headers.get("user-agent", ""),
        "accept": request.headers.get("accept", ""),
        "accept_language": request.headers.get("accept-language", ""),
    }


@app.post("/api/auth/login")
def login(payload: LoginRequest) -> dict[str, Any]:
    expected = CREATED_USERS.get(payload.username, LAB_USERS.get(payload.username))
    success = expected is not None and payload.password == expected
    LOGIN_ATTEMPTS.append(
        {
            "username": payload.username,
            "session_id": payload.session_id,
            "success": success,
            "attempt": len(LOGIN_ATTEMPTS) + 1,
        }
    )
    if not success:
        raise HTTPException(status_code=401, detail="synthetic credentials rejected")
    token = hashlib.sha256(f"{payload.username}:{payload.session_id}".encode()).hexdigest()[:16]
    return {"authenticated": True, "username": payload.username, "lab_token": token}


@app.post("/api/accounts/create", status_code=201)
def create_account(payload: AccountRequest) -> dict[str, Any]:
    if payload.username in LAB_USERS or payload.username in CREATED_USERS:
        raise HTTPException(status_code=409, detail="synthetic account already exists")
    CREATED_USERS[payload.username] = payload.password
    return {"created": True, "username": payload.username, "session_id": payload.session_id}


@app.get("/api/auth/attempts")
def auth_attempts() -> dict[str, Any]:
    return {
        "attempts": len(LOGIN_ATTEMPTS),
        "failures": sum(not attempt["success"] for attempt in LOGIN_ATTEMPTS),
        "distinct_users": len({attempt["username"] for attempt in LOGIN_ATTEMPTS}),
        "distinct_sessions": len({attempt["session_id"] for attempt in LOGIN_ATTEMPTS}),
    }


@app.post("/api/challenge")
def challenge(payload: ChallengeRequest) -> dict[str, Any]:
    # Deliberately flawed local control: the answer and returned token are fixed, and
    # the token is not bound to a session, action, expiry, or one-time use.
    if payload.answer.strip().casefold() != "aate":
        raise HTTPException(status_code=403, detail="synthetic challenge failed")
    token = hashlib.sha256(b"aate-replayable-challenge").hexdigest()[:16]
    CHALLENGE_TOKENS.add(token)
    return {"passed": True, "session_id": payload.session_id, "lab_token": token}


@app.get("/api/products/{product_id}")
def product(product_id: str) -> dict[str, Any]:
    if product_id not in {"demo-1", "demo-2"}:
        raise HTTPException(status_code=404, detail="synthetic product not found")
    return {"id": product_id, "available": INVENTORY[product_id]}


@app.post("/api/cart/reserve")
def reserve(payload: ReserveRequest) -> dict[str, Any]:
    if payload.product_id not in {"demo-1", "demo-2"}:
        raise HTTPException(status_code=404, detail="synthetic product not found")
    if INVENTORY[payload.product_id] < payload.quantity:
        raise HTTPException(status_code=409, detail="synthetic inventory unavailable")
    INVENTORY[payload.product_id] -= payload.quantity
    return {"reserved": payload.quantity, "remaining": INVENTORY[payload.product_id]}


@app.post("/api/promotions/redeem")
def redeem(payload: PromotionRequest) -> dict[str, Any]:
    key = (payload.identity, payload.code)
    if key in PROMOTIONS:
        raise HTTPException(status_code=409, detail="synthetic promotion already redeemed")
    PROMOTIONS.add(key)
    return {"redeemed": True, "identity": payload.identity, "code": payload.code}


@app.get("/api/reports/expensive")
def expensive(work: int = Query(default=25, ge=1, le=100)) -> dict[str, Any]:
    # Bounded, deterministic CPU work. The route models relative cost, not production load.
    digest = b"aate-synthetic"
    for _ in range(work * 200):
        digest = hashlib.sha256(digest).digest()
    return {"work": work, "digest_prefix": digest.hex()[:12]}


@app.get("/api/reports/cacheable")
def cacheable_report(
    cache_key: str = Query(min_length=1, max_length=64), bypass: bool = Query(default=False)
) -> dict[str, Any]:
    """Model cached versus cache-bypass application work with bounded CPU."""
    if not bypass and cache_key in CACHEABLE_REPORTS:
        return {"cache_key": cache_key, "cache_hit": True, "digest_prefix": CACHEABLE_REPORTS[cache_key]}
    digest = b"aate-cacheable-synthetic"
    for _ in range(100 * 200):
        digest = hashlib.sha256(digest).digest()
    prefix = digest.hex()[:12]
    if not bypass:
        CACHEABLE_REPORTS[cache_key] = prefix
    return {"cache_key": cache_key, "cache_hit": False, "digest_prefix": prefix}


@app.get("/api/reports/unstable")
def unstable_report(operation_id: str = Query(min_length=1, max_length=64)) -> dict[str, Any]:
    """Fail once per operation so bounded retry amplification can be measured."""
    UNSTABLE_CALLS[operation_id] += 1
    if UNSTABLE_CALLS[operation_id] == 1:
        raise HTTPException(status_code=503, detail="synthetic first-attempt failure")
    return {"accepted": True, "operation_id": operation_id, "attempt": UNSTABLE_CALLS[operation_id]}


@app.get("/api/reports/protected")
def protected_report(
    session_id: str = Query(min_length=1, max_length=64),
    work: int = Query(default=10, ge=1, le=25),
    x_lab_challenge: str | None = Header(default=None),
) -> dict[str, Any]:
    """Intentionally replayable challenge gate for the local bypass lab."""
    if x_lab_challenge not in CHALLENGE_TOKENS:
        raise HTTPException(status_code=403, detail="synthetic challenge required")
    digest = b"aate-protected-synthetic"
    for _ in range(work * 100):
        digest = hashlib.sha256(digest).digest()
    return {"authorized": True, "session_id": session_id, "work": work, "digest_prefix": digest.hex()[:12]}


@app.get("/api/reports/limited")
def limited_report(
    session_id: str = Query(min_length=1, max_length=64),
    work: int = Query(default=10, ge=1, le=25),
) -> dict[str, Any]:
    """Intentionally weak per-session limit for the local key-rotation lab."""
    LIMITED_REPORT_CALLS[session_id] += 1
    if LIMITED_REPORT_CALLS[session_id] > 2:
        raise HTTPException(status_code=429, detail="synthetic per-session limit reached")
    digest = b"aate-limited-synthetic"
    for _ in range(work * 100):
        digest = hashlib.sha256(digest).digest()
    return {
        "accepted": True,
        "session_id": session_id,
        "session_count": LIMITED_REPORT_CALLS[session_id],
        "work": work,
        "digest_prefix": digest.hex()[:12],
    }


@app.post("/telemetry/events", status_code=202)
def record_event(event: Event, x_request_id: str | None = Header(default=None)) -> dict[str, Any]:
    stored = event.model_dump()
    stored["request_id"] = (x_request_id or str(uuid.uuid4()))[:128]
    EVENTS.append(stored)
    return {"accepted": True, "event_count": len(EVENTS)}


@app.get("/api/session/{session_id}/summary")
def session_summary(session_id: str) -> dict[str, Any]:
    matches = [event for event in EVENTS if event["session_id"] == session_id]
    return {
        "session_id": session_id,
        "event_count": len(matches),
        "event_types": [event["event_type"] for event in matches],
    }


@app.post("/api/reset")
def reset() -> dict[str, bool]:
    # The application is reachable only through the edge port bound to 127.0.0.1
    # or from the Compose-internal network. Do not publish the app service itself.
    EVENTS.clear()
    INVENTORY.clear()
    INVENTORY.update({"demo-1": 5, "demo-2": 3})
    PROMOTIONS.clear()
    CREATED_USERS.clear()
    LOGIN_ATTEMPTS.clear()
    CHALLENGE_TOKENS.clear()
    LIMITED_REPORT_CALLS.clear()
    CONTROL_NONCES.clear()
    CONTROL_TOKENS.clear()
    CACHEABLE_REPORTS.clear()
    UNSTABLE_CALLS.clear()
    return {"reset": True}
