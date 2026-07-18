from __future__ import annotations

import unittest

from scripts.check_external_links import classify_http_status, valid_http_url


class ExternalLinkClassificationTests(unittest.TestCase):
    def test_http_status_categories_are_distinct(self) -> None:
        self.assertEqual(classify_http_status(200), "successful_response")
        self.assertEqual(classify_http_status(301), "redirect")
        self.assertEqual(classify_http_status(404), "permanent_not_found")
        self.assertEqual(classify_http_status(429), "temporary_server_error")
        self.assertEqual(classify_http_status(503), "temporary_server_error")
        self.assertEqual(classify_http_status(403), "client_error")

    def test_url_validation_rejects_malformed_and_credential_bearing_urls(self) -> None:
        self.assertTrue(valid_http_url("https://example.com/docs"))
        self.assertFalse(valid_http_url("not a URL"))
        self.assertFalse(valid_http_url("ftp://example.com/file"))
        self.assertFalse(valid_http_url("https://user:password@example.com/private"))
