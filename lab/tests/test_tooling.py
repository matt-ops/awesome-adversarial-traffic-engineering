from __future__ import annotations

import asyncio
import unittest
from unittest.mock import patch

from lab.tooling.client import fetch_with_retry, summarize


class ToolingExerciseTests(unittest.TestCase):
    def test_summary_counts_labels_and_preserves_limitations(self) -> None:
        result = summarize(
            [
                {"population": "headed", "is_abuse": False},
                {"population": "headed", "is_abuse": True},
                {"population": "manual", "is_abuse": False},
            ]
        )
        self.assertEqual(result["records"], 3)
        self.assertEqual(result["populations"], {"headed": 2, "manual": 1})
        self.assertEqual(result["labels"], {"abuse": 1, "benign": 2})
        self.assertTrue(result["limitations"])

    def test_retry_stops_after_success_and_records_budget(self) -> None:
        responses = [
            {"ok": False, "status": 503, "elapsed_ms": 1.0},
            {"ok": True, "status": 200, "elapsed_ms": 1.0},
        ]
        with (
            patch("lab.tooling.client.fetch_once", side_effect=responses),
            patch("lab.tooling.client.asyncio.sleep", return_value=None),
        ):
            events = asyncio.run(
                fetch_with_retry("http://localhost:8080/health", base_delay_seconds=0)
            )
        self.assertEqual([event["status"] for event in events], [503, 200])
        self.assertEqual([event["attempt"] for event in events], [1, 2])

    def test_retry_rejects_unbounded_attempt_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "attempts must be 1..3"):
            asyncio.run(fetch_with_retry("http://localhost:8080/health", attempts=4))


if __name__ == "__main__":
    unittest.main()
