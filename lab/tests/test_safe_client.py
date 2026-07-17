from __future__ import annotations

import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, ClassVar, cast
from unittest.mock import patch

from lab.clients.safe_client import DURATION_BUDGET_ERROR, fetch_once, run
from lab.safety import LoadEnvelope, SafetyError


class _LocalServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _Handler)
        self.request_paths: list[str] = []


class _Handler(BaseHTTPRequestHandler):
    REDIRECTS = {
        "/external": "https://example.invalid/not-contacted",
        "/public-ip": "http://8.8.8.8/not-contacted",
        "/private-ip": "http://192.168.1.5/not-contacted",
        "/scheme": "file:///not-contacted",
        "/loop": "/loop",
        "/local": "/ok",
        "/port": "http://127.0.0.1:1/not-contacted",
    }

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        server = cast(_LocalServer, self.server)
        server.request_paths.append(self.path)
        if self.path in self.REDIRECTS:
            self.send_response(302)
            self.send_header("Location", self.REDIRECTS[self.path])
            self.end_headers()
            return
        if self.path == "/slow":
            time.sleep(2)
        body = b'{"status":"ok"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, format: str, *args: Any) -> None:
        del format, args


class SafeClientBoundaryTests(unittest.TestCase):
    server: ClassVar[_LocalServer]
    port: ClassVar[int]
    origin: ClassVar[str]
    thread: ClassVar[threading.Thread]

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _LocalServer()
        cls.port = int(cls.server.server_address[1])
        cls.origin = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self) -> None:
        self.server.request_paths.clear()

    def _approved_test_origin(self) -> Any:
        return patch("lab.safety.APPROVED_COURSE_ORIGINS", frozenset({("http", "127.0.0.1", self.port)}))

    def test_approved_local_url_without_redirect_succeeds(self) -> None:
        with self._approved_test_origin():
            result = fetch_once(f"{self.origin}/ok")
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], 200)
        self.assertEqual(self.server.request_paths, ["/ok"])

    def test_redirect_to_external_hostname_is_rejected(self) -> None:
        self._assert_redirect_rejected("/external")

    def test_redirect_to_public_ip_is_rejected(self) -> None:
        self._assert_redirect_rejected("/public-ip")

    def test_redirect_to_private_network_ip_is_rejected(self) -> None:
        self._assert_redirect_rejected("/private-ip")

    def test_redirect_to_unapproved_scheme_is_rejected(self) -> None:
        self._assert_redirect_rejected("/scheme")

    def test_redirect_loop_is_rejected_on_first_hop(self) -> None:
        self._assert_redirect_rejected("/loop")

    def test_approved_local_to_local_redirect_is_explicitly_rejected(self) -> None:
        self._assert_redirect_rejected("/local")

    def test_redirect_cannot_bypass_port_restriction(self) -> None:
        self._assert_redirect_rejected("/port")

    def _assert_redirect_rejected(self, path: str) -> None:
        with self._approved_test_origin(), self.assertRaisesRegex(SafetyError, "redirects are not allowed"):
            fetch_once(f"{self.origin}{path}")
        self.assertEqual(self.server.request_paths, [path])

    def test_slow_response_hits_real_wall_clock_budget(self) -> None:
        envelope = LoadEnvelope(duration_seconds=1, requests_per_second=1, total_requests=1)
        started = time.monotonic()
        with self._approved_test_origin():
            results = run(f"{self.origin}/slow", envelope, dry_run=False)
        elapsed = time.monotonic() - started
        self.assertLess(elapsed, 1.75)
        self.assertEqual(results[-1]["error"], DURATION_BUDGET_ERROR)
        self.assertTrue(results[-1]["duration_budget_exceeded"])

    def test_no_new_request_starts_after_deadline(self) -> None:
        envelope = LoadEnvelope(duration_seconds=1, requests_per_second=2, total_requests=2)
        with (
            patch("lab.clients.safe_client.time.monotonic", side_effect=[0.0, 0.0, 0.4, 1.0]),
            patch("lab.clients.safe_client.time.sleep", return_value=None),
            patch("lab.clients.safe_client.fetch_once", return_value={"ok": True, "status": 200}) as mocked_fetch,
        ):
            results = run("http://localhost:8080/health", envelope, dry_run=False)
        self.assertEqual(mocked_fetch.call_count, 1)
        self.assertFalse(results[-1]["request_started"])
        self.assertEqual(results[-1]["error"], DURATION_BUDGET_ERROR)

    def test_request_timeout_is_bounded_by_remaining_duration(self) -> None:
        envelope = LoadEnvelope(duration_seconds=1, requests_per_second=1, total_requests=1)
        with (
            patch("lab.clients.safe_client.time.monotonic", side_effect=[10.0, 10.25, 10.5]),
            patch("lab.clients.safe_client.fetch_once", return_value={"ok": True, "status": 200}) as mocked_fetch,
        ):
            run("http://localhost:8080/health", envelope, dry_run=False)
        self.assertEqual(mocked_fetch.call_args.kwargs["timeout_seconds"], 0.75)

    def test_total_request_ceiling_still_applies(self) -> None:
        envelope = LoadEnvelope(duration_seconds=15, requests_per_second=10, total_requests=101)
        with patch("lab.clients.safe_client.fetch_once") as mocked_fetch, self.assertRaises(SafetyError):
            run("http://localhost:8080/health", envelope, dry_run=False)
        mocked_fetch.assert_not_called()

    def test_request_rate_ceiling_still_applies(self) -> None:
        envelope = LoadEnvelope(duration_seconds=2, requests_per_second=2, total_requests=2)
        with (
            patch("lab.clients.safe_client.time.monotonic", side_effect=[0.0, 0.0, 0.1, 0.7, 0.8]),
            patch("lab.clients.safe_client.time.sleep", return_value=None) as mocked_sleep,
            patch("lab.clients.safe_client.fetch_once", return_value={"ok": True, "status": 200}),
        ):
            run("http://localhost:8080/health", envelope, dry_run=False)
        delay = float(mocked_sleep.call_args.args[0])
        self.assertGreaterEqual(delay, 0.5)
        self.assertLessEqual(delay, 0.55)

    def test_normal_local_run_succeeds(self) -> None:
        envelope = LoadEnvelope(duration_seconds=2, requests_per_second=1, total_requests=1)
        with self._approved_test_origin():
            results = run(f"{self.origin}/ok", envelope, dry_run=False)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]["ok"])

    def test_invalid_direct_timeout_is_rejected(self) -> None:
        invalid: tuple[Any, ...] = (0, -1, 2.01, float("nan"), float("inf"), True, "1")
        with self._approved_test_origin():
            for timeout in invalid:
                with self.subTest(timeout=timeout), self.assertRaises(SafetyError):
                    fetch_once(f"{self.origin}/ok", timeout_seconds=timeout)


if __name__ == "__main__":
    unittest.main()
