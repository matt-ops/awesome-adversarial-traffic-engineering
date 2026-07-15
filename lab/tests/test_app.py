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

    def test_synthetic_login_and_attempt_summary(self) -> None:
        rejected = self.client.post(
            "/api/auth/login",
            json={"username": "alice", "password": "wrong", "session_id": "s-login"},
        )
        self.assertEqual(rejected.status_code, 401)
        accepted = self.client.post(
            "/api/auth/login",
            json={"username": "alice", "password": "wonderland", "session_id": "s-login"},
        )
        self.assertEqual(accepted.status_code, 200)
        summary = self.client.get("/api/auth/attempts").json()
        self.assertEqual(summary["attempts"], 2)
        self.assertEqual(summary["failures"], 1)

    def test_synthetic_account_and_challenge(self) -> None:
        created = self.client.post(
            "/api/accounts/create",
            json={"username": "student-1", "password": "lab-only", "session_id": "s-create"},
        )
        self.assertEqual(created.status_code, 201)
        passed = self.client.post("/api/challenge", json={"session_id": "s-create", "answer": "AATE"})
        self.assertEqual(passed.status_code, 200)


if __name__ == "__main__":
    unittest.main()
