from __future__ import annotations

import unittest

from lab.safety import LoadEnvelope, SafetyError, validate_course_client_url, validate_local_url


class TargetSafetyTests(unittest.TestCase):
    def test_approved_local_targets(self) -> None:
        for target in ("http://localhost:8080/health", "http://127.0.0.1/", "https://[::1]/", "http://app:8000/health"):
            self.assertEqual(validate_local_url(target), target)

    def test_rejects_public_private_and_arbitrary_targets(self) -> None:
        rejected = (
            "https://example.com/",
            "http://8.8.8.8/",
            "http://10.0.0.1/",
            "http://192.168.1.5/",
            "ftp://localhost/file",
            "http://localhost.example.com/",
            "http://user:pass@localhost/",
        )
        for target in rejected:
            with self.subTest(target=target), self.assertRaises(SafetyError):
                validate_local_url(target)

    def test_course_client_uses_exact_approved_origins(self) -> None:
        approved = (
            "http://localhost:8080/health",
            "http://127.0.0.1:8080/",
            "http://app:8000/health",
            "http://edge:8080/control-lab",
        )
        rejected = (
            "http://localhost:8081/health",
            "https://localhost:8080/health",
            "http://127.0.0.1/health",
            "http://aate-app:8000/health",
            "http://10.0.0.1:8080/health",
        )
        for target in approved:
            with self.subTest(target=target):
                self.assertEqual(validate_course_client_url(target), target)
        for target in rejected:
            with self.subTest(target=target), self.assertRaises(SafetyError):
                validate_course_client_url(target)


class LoadEnvelopeTests(unittest.TestCase):
    def test_accepts_conservative_envelope(self) -> None:
        envelope = LoadEnvelope(
            duration_seconds=5,
            concurrency=2,
            requests_per_second=2,
            total_requests=10,
            expensive_requests=2,
        )
        self.assertIs(envelope.validate(), envelope)

    def test_rejects_each_excessive_parameter(self) -> None:
        invalid = (
            LoadEnvelope(duration_seconds=16),
            LoadEnvelope(concurrency=6),
            LoadEnvelope(requests_per_second=11),
            LoadEnvelope(total_requests=101, duration_seconds=15, requests_per_second=10),
            LoadEnvelope(expensive_requests=21, total_requests=25, duration_seconds=5, requests_per_second=5),
        )
        for envelope in invalid:
            with self.subTest(envelope=envelope), self.assertRaises(SafetyError):
                envelope.validate()


if __name__ == "__main__":
    unittest.main()
