from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from lab.app.main import app


class SyntheticAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_search_and_bounded_expensive_route(self) -> None:
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json(), {"status": "ok", "service": "aate-local-app"})
        self.assertIn("x-request-id", health.headers)

        search = self.client.get("/api/search", params={"q": "demo"})
        self.assertEqual(len(search.json()["results"]), 2)

        self.assertEqual(self.client.get("/api/reports/expensive", params={"work": 1}).status_code, 200)
        self.assertEqual(self.client.get("/api/reports/expensive", params={"work": 101}).status_code, 422)

    def test_event_validation_and_session_summary(self) -> None:
        accepted = self.client.post(
            "/telemetry/events",
            json={"session_id": "test-session", "event_type": "synthetic_click", "attributes": {"sequence": 1}},
        )
        self.assertEqual(accepted.status_code, 202)
        summary = self.client.get("/api/session/test-session/summary")
        self.assertGreaterEqual(summary.json()["event_count"], 1)
        invalid = self.client.post("/telemetry/events", json={"session_id": "", "event_type": "x"})
        self.assertEqual(invalid.status_code, 422)


if __name__ == "__main__":
    unittest.main()
