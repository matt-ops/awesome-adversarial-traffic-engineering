from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from lab.app.main import app


class SyntheticAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.assertEqual(self.client.post("/api/reset").status_code, 200)

    def test_health_search_and_bounded_expensive_route(self) -> None:
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json(), {"status": "ok", "service": "aate-local-app"})
        self.assertIn("x-request-id", health.headers)

        search = self.client.get("/api/search", params={"q": "demo"})
        self.assertEqual(len(search.json()["results"]), 2)

        self.assertEqual(self.client.get("/api/reports/expensive", params={"work": 1}).status_code, 200)
        self.assertEqual(self.client.get("/api/reports/expensive", params={"work": 101}).status_code, 422)

        protocol = self.client.get("/api/protocol/observe", headers={"User-Agent": "test-protocol"})
        self.assertEqual(protocol.json()["method"], "GET")
        self.assertEqual(protocol.json()["path"], "/api/protocol/observe")
        self.assertEqual(protocol.json()["user_agent"], "test-protocol")

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
        replayed = [
            self.client.get(
                "/api/reports/protected",
                params={"session_id": "replay-session"},
                headers={"X-Lab-Challenge": token},
            )
            for _ in range(2)
        ]
        self.assertEqual([response.status_code for response in replayed], [200, 200])
        self.assertEqual([response.json()["session_id"] for response in replayed], ["replay-session"] * 2)

    def test_challenge_browser_surface_is_provider_neutral_and_local(self) -> None:
        page = self.client.get("/challenge-lab")
        script = self.client.get("/challenge-lab.js")
        self.assertEqual((page.status_code, script.status_code), (200, 200))
        self.assertIn("no visual CAPTCHA widget or iframe", page.text)
        self.assertIn('src="/challenge-lab.js"', page.text)
        self.assertIn("/api/challenge", script.text)
        self.assertIn("/api/reports/protected", script.text)
        self.assertNotIn("recaptcha", (page.text + script.text).casefold())

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

    def test_cache_and_retry_fixtures_are_bounded_and_deterministic(self) -> None:
        first = self.client.get("/api/reports/cacheable", params={"cache_key": "fixed"})
        second = self.client.get("/api/reports/cacheable", params={"cache_key": "fixed"})
        bypass = self.client.get("/api/reports/cacheable", params={"cache_key": "fixed", "bypass": True})
        self.assertFalse(first.json()["cache_hit"])
        self.assertTrue(second.json()["cache_hit"])
        self.assertFalse(bypass.json()["cache_hit"])

        failed = self.client.get("/api/reports/unstable", params={"operation_id": "bounded"})
        retried = self.client.get("/api/reports/unstable", params={"operation_id": "bounded"})
        self.assertEqual(failed.status_code, 503)
        self.assertEqual(retried.status_code, 200)
        self.assertEqual(retried.json()["attempt"], 2)

    def test_load_scenario_fixture_assertions_match_application_behavior(self) -> None:
        self.assertEqual(self.client.post("/api/reset").status_code, 200)

        low_work = self.client.get("/api/reports/expensive", params={"work": 1})
        high_work = self.client.get("/api/reports/expensive", params={"work": 100})
        self.assertEqual((low_work.json()["work"], high_work.json()["work"]), (1, 100))

        prime = self.client.get("/api/reports/cacheable", params={"cache_key": "fixed"})
        cached = self.client.get("/api/reports/cacheable", params={"cache_key": "fixed"})
        bypass = self.client.get(
            "/api/reports/cacheable", params={"cache_key": "unique", "bypass": True}
        )
        self.assertFalse(prime.json()["cache_hit"])
        self.assertTrue(cached.json()["cache_hit"])
        self.assertFalse(bypass.json()["cache_hit"])
        self.assertEqual(cached.json()["digest_prefix"], bypass.json()["digest_prefix"])

        seeded = [
            self.client.get("/api/reports/limited", params={"session_id": "fixed"}).status_code
            for _ in range(2)
        ]
        rejected = self.client.get("/api/reports/limited", params={"session_id": "fixed"})
        rotated = self.client.get("/api/reports/limited", params={"session_id": "rotated"})
        self.assertEqual(seeded, [200, 200])
        self.assertEqual(rejected.status_code, 429)
        self.assertEqual(rotated.status_code, 200)
        self.assertEqual(rotated.json()["session_count"], 1)

        search = self.client.get("/api/search", params={"q": "demo"}).json()
        product = self.client.get("/api/products/demo-1").json()
        self.assertIn("demo-1", {item["id"] for item in search["results"]})
        self.assertEqual(product["id"], "demo-1")

        failed = self.client.get("/api/reports/unstable", params={"operation_id": "scenario"})
        retried = self.client.get("/api/reports/unstable", params={"operation_id": "scenario"})
        self.assertEqual((failed.status_code, retried.status_code), (503, 200))
        self.assertEqual(retried.json()["attempt"], 2)
        self.assertEqual(self.client.get("/health").status_code, 200)


if __name__ == "__main__":
    unittest.main()
