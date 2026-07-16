from __future__ import annotations

import unittest

from lab.protocol.compare import client_hello, compare_client_hellos, summarize_client_hello


class ProtocolFixtureTests(unittest.TestCase):
    def test_generated_bytes_are_tls_clienthello(self) -> None:
        summary = summarize_client_hello(client_hello(), "test")
        self.assertEqual(summary["record_type"], 22)
        self.assertEqual(summary["handshake_type"], 1)
        self.assertGreater(summary["record_length"], 100)

    def test_alpn_configuration_changes_generated_bytes(self) -> None:
        comparison = compare_client_hellos()
        self.assertTrue(comparison["bytes_differ"])
        self.assertNotEqual(
            comparison["default"]["sha256_prefix"], comparison["with_alpn"]["sha256_prefix"]
        )


if __name__ == "__main__":
    unittest.main()
