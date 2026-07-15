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

    def test_challenge_token_is_intentionally_replayable_across_sessions(self) -> None:
        denied = self.client.get("/api/reports/protected", params={"session_id": "replay-session"})
        self.assertEqual(denied.status_code, 403)
        solved = self.client.post("/api/challenge", json={"session_id": "solver-session", "answer": "AATE"})
        token = solved.json()["lab_token"]
        replayed = self.client.get(
            "/api/reports/protected",
            params={"session_id": "replay-session"},
            headers={"X-Lab-Challenge": token},
        )
        self.assertEqual(replayed.status_code, 200)
        self.assertEqual(replayed.json()["session_id"], "replay-session")

    def test_per_session_limit_is_intentionally_bypassable_by_key_rotation(self) -> None:
        fixed = [self.client.get("/api/reports/limited", params={"session_id": "fixed"}).status_code for _ in range(3)]
        rotated = [
            self.client.get("/api/reports/limited", params={"session_id": f"rotated-{number}"}).status_code
            for number in range(1, 4)
        ]
        self.assertEqual(fixed, [200, 200, 429])
        self.assertEqual(rotated, [200, 200, 200])


if __name__ == "__main__":
    unittest.main()
