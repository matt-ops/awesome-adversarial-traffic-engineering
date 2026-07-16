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

    def test_control_requires_consistent_non_automated_observation_and_single_use(self) -> None:
        baseline = {
            "trial_id": "baseline",
            "population": "stock-headless",
            "nonce": "baseline-nonce-0001",
            "captured_at_ms": 1,
            "webdriver": True,
            "user_agent": "Synthetic Chrome",
            "timezone": "America/Chicago",
            "viewport_width": 1280,
            "screen_width": 1280,
            "page": {"language": "en-US", "platform": "Win32"},
            "frame": {"language": "en-US", "platform": "Win32"},
            "worker": {"language": "en-US", "platform": "Win32"},
        }
        challenged = self.client.post("/api/control/evaluate", json=baseline)
        self.assertEqual(challenged.status_code, 200)
        self.assertEqual(challenged.json()["decision"], "challenge")
        self.assertIsNone(challenged.json()["action_token"])

        changed = {**baseline, "trial_id": "one-variable", "nonce": "changed-nonce-0001", "webdriver": False}
        allowed = self.client.post("/api/control/evaluate", json=changed)
        self.assertEqual(allowed.json()["decision"], "allow")
        token = allowed.json()["action_token"]
        protected = self.client.post(
            "/api/control/protected", params={"session_id": "one-variable"}, headers={"X-AATE-Control": token}
        )
        self.assertEqual(protected.status_code, 200)
        replay = self.client.post(
            "/api/control/protected", params={"session_id": "replay"}, headers={"X-AATE-Control": token}
        )
        self.assertEqual(replay.status_code, 403)
        nonce_replay = self.client.post("/api/control/evaluate", json=changed)
        self.assertEqual(nonce_replay.status_code, 409)

    def test_control_rejects_cross_context_mismatch(self) -> None:
        payload = {
            "trial_id": "mismatch",
            "population": "patched-page-only",
            "nonce": "mismatch-nonce-0001",
            "captured_at_ms": 1,
            "webdriver": False,
            "user_agent": "Synthetic Chrome",
            "timezone": "UTC",
            "viewport_width": 800,
            "screen_width": 800,
            "page": {"language": "en-US", "platform": "Win32"},
            "frame": {"language": "en-US", "platform": "Win32"},
            "worker": {"language": "fr-FR", "platform": "Win32"},
        }
        response = self.client.post("/api/control/evaluate", json=payload)
        self.assertEqual(response.json()["decision"], "challenge")
        self.assertIn("cross_context_language_mismatch", response.json()["reasons"])


if __name__ == "__main__":
    unittest.main()
