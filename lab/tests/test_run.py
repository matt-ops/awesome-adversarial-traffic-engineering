from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from typing import Any
from unittest.mock import patch

from lab import run


class ReconRunnerTests(unittest.TestCase):
    def test_recon_maps_surface_and_produces_attack_hypotheses(self) -> None:
        specification: dict[str, Any] = {
            "paths": {
                "/health": {"get": {"responses": {"200": {}}}},
                "/api/cart/reserve": {
                    "post": {
                        "requestBody": {
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Reserve"}}}
                        },
                        "responses": {"200": {}, "422": {}},
                    }
                },
                "/api/reports/protected": {"get": {"responses": {"200": {}, "403": {}}}},
            },
            "components": {
                "schemas": {
                    "Reserve": {
                        "properties": {"identity": {}, "product_id": {}, "quantity": {}},
                        "required": ["identity", "product_id", "quantity"],
                    }
                }
            },
        }
        responses = [
            (200, specification, 1.0),
            (200, {"status": "ok"}, 1.0),
            (200, {"results": []}, 1.0),
            (404, {"detail": "not found"}, 1.0),
            (403, {"detail": "challenge required"}, 1.0),
            (200, {"result": 1}, 1.0),
        ]
        output = io.StringIO()
        with patch("lab.run.reset"), patch("lab.run.request", side_effect=responses), redirect_stdout(output):
            run.recon_demo()

        events = [json.loads(line) for line in output.getvalue().splitlines()]
        inventory = events[0]
        self.assertEqual(inventory["phase"], "surface-inventory")
        reserve = next(entry for entry in inventory["routes"] if entry["path"] == "/api/cart/reserve")
        self.assertEqual(reserve["method"], "POST")
        self.assertFalse(reserve["security_required"])
        self.assertIn({"location": "body", "name": "identity", "required": True}, reserve["inputs"])
        self.assertEqual(sum(event["phase"] == "bounded-probe" for event in events), 5)
        hypotheses = [event for event in events if event["phase"] == "attack-hypothesis"]
        self.assertEqual(len(hypotheses), 4)
        self.assertEqual(
            {event["control"] for event in hypotheses},
            {"workflow authorization", "challenge token", "rate limit", "resource protection"},
        )

    def test_bypass_records_cross_session_and_repeat_use_with_retest(self) -> None:
        responses = [
            (403, {"detail": "synthetic challenge required"}, 1.0),
            (200, {"passed": True, "session_id": "session-a", "lab_token": "proof"}, 1.0),
            (200, {"authorized": True, "session_id": "session-b"}, 1.0),
            (200, {"authorized": True, "session_id": "session-b"}, 1.0),
        ]
        output = io.StringIO()
        with patch("lab.run.reset"), patch("lab.run.request", side_effect=responses), redirect_stdout(output):
            run.bypass_demo()

        events = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(
            [event.get("phase") for event in events[:4]],
            ["blocked-baseline", "solve-session-a", "cross-session-first-use", "same-request-second-use"],
        )
        self.assertEqual(events[2]["response"]["session_id"], "session-b")
        self.assertEqual(events[3]["status"], 200)
        self.assertEqual(
            events[4]["absent_bindings"], ["session", "action", "origin", "nonce", "expiry", "one-use"]
        )
        self.assertIn("Session B receives 403", events[4]["negative_retest"])
        self.assertIn("Session A completes", events[4]["legitimate_positive_retest"])


if __name__ == "__main__":
    unittest.main()
