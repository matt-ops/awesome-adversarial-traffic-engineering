from __future__ import annotations

import socket
import unittest

from lab.protocol.compare import (
    HOST,
    MAX_CONNECTIONS,
    RawClientHelloObserver,
    _capture_trigger,
    _join_client_results,
    _python_tls_trigger,
    client_hello,
    compare_client_hellos,
    ephemeral_certificate,
    observe_http2,
    parse_client_hello,
    require_loopback_host,
    require_loopback_url,
    validate_cap,
)


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


if __name__ == "__main__":
    unittest.main()
