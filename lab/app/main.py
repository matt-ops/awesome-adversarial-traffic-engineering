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
from starlette.responses import Response

app = FastAPI(title="AATE Local App", version="0.1.0")
EVENTS: list[dict[str, Any]] = []
INVENTORY = defaultdict(lambda: 5, {"demo-1": 5, "demo-2": 3})
PROMOTIONS: set[tuple[str, str]] = set()


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


@app.get("/api/search")
def search(q: str = Query(default="demo", max_length=64)) -> dict[str, Any]:
    products = [
        {"id": "demo-1", "name": "Synthetic Widget"},
        {"id": "demo-2", "name": "Synthetic Kit"},
    ]
    needle = q.casefold()
    return {"query": q, "results": [item for item in products if needle in item["name"].casefold() or needle == "demo"]}


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
def reset(request: Request) -> dict[str, bool]:
    if request.client is None or request.client.host not in {"127.0.0.1", "::1", "app", "edge"}:
        raise HTTPException(status_code=403, detail="reset is local-only")
    EVENTS.clear()
    INVENTORY.clear()
    INVENTORY.update({"demo-1": 5, "demo-2": 3})
    PROMOTIONS.clear()
    return {"reset": True}
