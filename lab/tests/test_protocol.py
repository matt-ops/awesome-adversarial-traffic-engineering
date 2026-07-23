from __future__ import annotations

import io
import socket
import subprocess
import sys
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from typing import Any
from unittest import mock

import lab.protocol.compare as protocol_compare
from lab.protocol.compare import (
    AUTOMATED_WALL_TIMEOUT_SECONDS,
    HOST,
    MAX_CONNECTIONS,
    ProtocolDeadlineExceeded,
    ProtocolSafetyError,
    RawClientHelloObserver,
    _capture_trigger,
    _join_client_results,
    _python_tls_trigger,
    assert_no_non_loopback_page_requests,
    client_hello,
    compare_client_hellos,
    ephemeral_certificate,
    main,
    observe_http2,
    parse_client_hello,
    remaining_seconds,
    require_loopback_host,
    require_loopback_url,
    run_automated_comparison,
    validate_cap,
)


class FakeObserverProcess:
    def __init__(
        self,
        command: list[str],
        *,
        ready_line: str = '{"status":"ready","port":443}\n',
        output_text: str = '{"status":"observed","bind":"127.0.0.1","sessions":[]}',
        wait_failures: int = 0,
    ) -> None:
        output_index = command.index("--output") + 1
        self.output_path = Path(command[output_index])
        self.ready_line = ready_line
        self.output_text = output_text
        self.wait_failures = wait_failures
        self.wait_calls = 0
        self.stdin = io.StringIO()
        self.stdout = io.StringIO(ready_line)
        self.stderr = io.StringIO("")
        self.returncode: int | None = None
        self.terminated = False
        self.killed = False

    def poll(self) -> int | None:
        return self.returncode

    def wait(self, timeout: float | None = None) -> int:
        self.wait_calls += 1
        if self.wait_calls <= self.wait_failures:
            raise subprocess.TimeoutExpired(["fake-observer"], timeout or 0.0)
        if not self.output_path.exists():
            self.output_path.write_text(self.output_text, encoding="utf-8")
        self.returncode = -9 if self.killed else 0
        return self.returncode

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True


class ProtocolParserTests(unittest.TestCase):
    def test_generated_clienthello_exposes_real_fields(self) -> None:
        summary = parse_client_hello(client_hello(("h2", "http/1.1")), "test", "generated")
        self.assertEqual(summary["record_type"], 22)
        self.assertEqual(summary["clienthello_legacy_version"], "0x0303")
        self.assertGreater(len(summary["cipher_suite_ids"]), 5)
        self.assertIn(16, summary["extension_ids"])
        self.assertEqual(summary["alpn_offers"], ["h2", "http/1.1"])
        self.assertTrue(summary["sni_present"])

    def test_alpn_configuration_changes_parsed_fields(self) -> None:
        comparison = compare_client_hellos()
        self.assertTrue(comparison["bytes_differ"])
        self.assertEqual(comparison["default"]["alpn_offers"], [])
        self.assertEqual(comparison["with_alpn"]["alpn_offers"], ["h2", "http/1.1"])

    def test_malformed_and_truncated_records_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "truncated"):
            parse_client_hello(b"\x16\x03\x01", "bad", "fixture")
        generated = client_hello()
        with self.assertRaisesRegex(ValueError, "truncated or trailing"):
            parse_client_hello(generated[:-1], "bad", "fixture")
        with self.assertRaisesRegex(ValueError, "record type"):
            parse_client_hello(b"\x17" + generated[1:], "bad", "fixture")

    def test_digest_is_explicitly_not_ja4_or_identity(self) -> None:
        summary = parse_client_hello(client_hello(), "test", "generated")
        self.assertEqual(summary["digest_label"], "not JA4; not identity proof")
        self.assertEqual(len(summary["comparison_digest"]), 16)


class ProtocolSafetyTests(unittest.TestCase):
    def test_loopback_enforcement(self) -> None:
        self.assertEqual(require_loopback_host("127.0.0.1"), "127.0.0.1")
        self.assertEqual(require_loopback_url("https://localhost:8443/path"), "https://localhost:8443/path")
        with self.assertRaisesRegex(ValueError, "loopback"):
            require_loopback_host("192.0.2.10")
        with self.assertRaisesRegex(ValueError, "loopback"):
            require_loopback_url("https://example.com/")

    def test_simulated_non_loopback_page_request_fails(self) -> None:
        self.assertEqual(
            assert_no_non_loopback_page_requests(
                [{"client": "browser", "non_loopback_page_requests_observed": []}]
            ),
            [],
        )
        with self.assertRaisesRegex(ProtocolSafetyError, "non-loopback page requests"):
            assert_no_non_loopback_page_requests(
                [
                    {
                        "client": "browser",
                        "non_loopback_page_requests_observed": ["https://example.com/background"],
                    }
                ]
            )

    def test_structured_output_does_not_claim_hard_coded_zero_external_requests(self) -> None:
        source = Path(protocol_compare.__file__).read_text(encoding="utf-8")
        self.assertNotIn('"external_requests": 0', source)
        self.assertIn('"packet_level_external_traffic": "not measured"', source)

    def test_connection_cap_is_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "between 1"):
            validate_cap(MAX_CONNECTIONS + 1, MAX_CONNECTIONS, "connection cap")
        observer = RawClientHelloObserver(max_connections=1)
        observer.start()
        with socket.create_connection((HOST, observer.port), timeout=2) as connection:
            connection.sendall(client_hello())
        captured = observer.result()
        observer.close()
        self.assertEqual(observer.connection_count, 1)
        self.assertEqual(parse_client_hello(captured, "cap-test", "generated")["record_type"], 22)

    def test_ephemeral_certificate_cleanup(self) -> None:
        with ephemeral_certificate() as paths:
            directory = paths.directory
            certificate = paths.certificate
            private_key = paths.private_key
            self.assertTrue(certificate.is_file())
            self.assertTrue(private_key.is_file())
        self.assertFalse(directory.exists())
        self.assertFalse(certificate.exists())
        self.assertFalse(private_key.exists())


class ProtocolIntegrationTests(unittest.TestCase):
    def test_python_openssl_capture(self) -> None:
        observation = _capture_trigger("python-openssl", "unavailable", _python_tls_trigger)
        self.assertEqual(observation["status"], "observed")
        self.assertGreater(observation["total_bytes"], 100)
        self.assertIn("OpenSSL", observation["runtime_version"])

    def test_local_http2_observer_and_unsupported_handling(self) -> None:
        result = observe_http2()
        self.assertEqual(result["status"], "observed")
        self.assertEqual(result["bind"], HOST)
        node = next(client for client in result["clients"] if client.get("client") == "node-http2")
        self.assertEqual(node["status"], "observed")
        node_session = next(session for session in result["sessions"] if "node-http2" in session["clients"])
        self.assertEqual(node_session["negotiated_alpn"], "h2")
        self.assertEqual(node_session["stream_count"], 2)
        self.assertTrue(node_session["remote_settings"])
        self.assertIn("temporary certificate", result["cleanup"])

        rows = _join_client_results(
            [{"client": "curl", "status": "unsupported", "runtime_version": "fixture"}],
            {
                "clients": [
                    {
                        "client": "curl-http2",
                        "status": "unsupported",
                        "runtime_version": "fixture",
                        "reason": "no HTTP2 feature",
                    }
                ],
                "sessions": [],
            },
        )
        curl_row = next(row for row in rows if row["client"] == "curl")
        self.assertEqual(curl_row["negotiated_protocol"], "unsupported")
        self.assertIn("HTTP/2 remote settings and reuse not observed", curl_row["unsupported_or_missing_fields"])


class ProtocolFailureCleanupTests(unittest.TestCase):
    def _observe_with_fake(
        self,
        *,
        ready_line: str = '{"status":"ready","port":443}\n',
        output_text: str = '{"status":"observed","bind":"127.0.0.1","sessions":[]}',
        wait_failures: int = 0,
        client_side_effect: Any = None,
    ) -> tuple[BaseException | None, FakeObserverProcess]:
        created: list[FakeObserverProcess] = []

        def factory(command: list[str], **_: Any) -> FakeObserverProcess:
            process = FakeObserverProcess(
                command,
                ready_line=ready_line,
                output_text=output_text,
                wait_failures=wait_failures,
            )
            created.append(process)
            return process

        default_client = {
            "client": "fixture",
            "status": "observed",
            "runtime_version": "fixture",
            "non_loopback_page_requests_observed": [],
        }
        error: BaseException | None = None
        with (
            mock.patch("lab.protocol.compare._npx_command", return_value="npx"),
            mock.patch("lab.protocol.compare.subprocess.Popen", side_effect=factory),
            mock.patch(
                "lab.protocol.compare._run_protocol_client",
                side_effect=client_side_effect,
                return_value=default_client,
            ),
            mock.patch(
                "lab.protocol.compare._curl_supports_http2",
                return_value=(False, "fixture curl without HTTP2", "curl"),
            ),
        ):
            try:
                observe_http2(time.monotonic() + 2)
            except BaseException as exc:  # noqa: BLE001 - tests inspect injected failures.
                error = exc
        self.assertEqual(len(created), 1)
        return error, created[0]

    def _assert_cleaned(self, process: FakeObserverProcess) -> None:
        self.assertIsNotNone(process.returncode)
        self.assertTrue(process.stdin.closed)
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)
        self.assertFalse(process.output_path.parent.exists())

    def test_malformed_ready_output_stops_child_and_removes_key_material(self) -> None:
        error, process = self._observe_with_fake(ready_line="not-json\n")
        self.assertIsInstance(error, RuntimeError)
        self.assertIn("malformed ready JSON", str(error))
        self._assert_cleaned(process)

    def test_client_exception_after_startup_stops_child(self) -> None:
        error, process = self._observe_with_fake(client_side_effect=RuntimeError("injected client failure"))
        self.assertIsInstance(error, RuntimeError)
        self.assertIn("injected client failure", str(error))
        self._assert_cleaned(process)

    def test_output_json_parse_failure_stops_child(self) -> None:
        error, process = self._observe_with_fake(output_text="{not-json")
        self.assertIsInstance(error, ValueError)
        self._assert_cleaned(process)

    def test_global_timeout_stops_child(self) -> None:
        created: list[FakeObserverProcess] = []

        def factory(command: list[str], **_: Any) -> FakeObserverProcess:
            process = FakeObserverProcess(command)
            created.append(process)
            return process

        with (
            mock.patch("lab.protocol.compare._npx_command", return_value="npx"),
            mock.patch("lab.protocol.compare.subprocess.Popen", side_effect=factory),
            mock.patch(
                "lab.protocol.compare._readline_with_deadline",
                side_effect=ProtocolDeadlineExceeded("injected global timeout"),
            ),
        ):
            with self.assertRaises(ProtocolDeadlineExceeded):
                observe_http2(time.monotonic() + 2)
        self._assert_cleaned(created[0])

    def test_page_request_violation_stops_child(self) -> None:
        client = {
            "client": "playwright-chromium",
            "status": "failed",
            "runtime_version": "fixture",
            "non_loopback_page_requests_observed": ["https://example.com/blocked"],
        }
        error, process = self._observe_with_fake(client_side_effect=[client, client])
        self.assertIsInstance(error, ProtocolSafetyError)
        self._assert_cleaned(process)

    def test_failed_graceful_stop_escalates_to_terminate_and_kill(self) -> None:
        error, process = self._observe_with_fake(ready_line="not-json\n", wait_failures=2)
        self.assertIsInstance(error, RuntimeError)
        self.assertTrue(process.terminated)
        self.assertTrue(process.killed)
        self._assert_cleaned(process)


class ProtocolDeadlineTests(unittest.TestCase):
    def test_delayed_dependency_enforces_global_deadline_and_skips_next_observer(self) -> None:
        observer_called = False

        def delayed_capture(deadline: float) -> list[dict[str, Any]]:
            time.sleep(0.03)
            remaining_seconds(deadline, "injected delayed dependency")
            return []

        def observer(_: float) -> dict[str, Any]:
            nonlocal observer_called
            observer_called = True
            return {}

        with self.assertRaises(ProtocolDeadlineExceeded):
            run_automated_comparison(0.01, delayed_capture, observer)
        self.assertFalse(observer_called)

    def test_timeout_command_returns_nonzero_with_clear_error(self) -> None:
        def delayed_capture(deadline: float) -> list[dict[str, Any]]:
            time.sleep(0.03)
            remaining_seconds(deadline, "injected command dependency")
            return []

        def delayed_run() -> dict[str, Any]:
            return run_automated_comparison(
                0.01,
                delayed_capture,
                lambda _: {},
            )

        stderr = io.StringIO()
        with (
            mock.patch.object(sys, "argv", ["compare", "automated"]),
            mock.patch("lab.protocol.compare.run_automated_comparison", side_effect=delayed_run),
            redirect_stderr(stderr),
        ):
            exit_code = main()
        self.assertNotEqual(exit_code, 0)
        self.assertIn("Protocol comparison timeout", stderr.getvalue())

    def test_configured_deadline_never_exceeds_45_seconds(self) -> None:
        self.assertEqual(AUTOMATED_WALL_TIMEOUT_SECONDS, 45)
        with self.assertRaises(ValueError):
            run_automated_comparison(46)


if __name__ == "__main__":
    unittest.main()
