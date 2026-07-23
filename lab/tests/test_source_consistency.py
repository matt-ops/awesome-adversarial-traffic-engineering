from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any

from scripts.validate_sources import (
    STRICT_SOURCE_CONSISTENCY,
    strict_source_consistency_errors,
)


class SourceConsistencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.by_id: dict[str, dict[str, Any]] = {
            "first-cti-source-evaluation": {
                "source_type": "OFFICIAL_DOCUMENTATION",
                "url": "https://www.first.org/global/sigs/cti/curriculum/source-evaluation",
            },
            "oasis-stix-21": {
                "source_type": "STANDARD",
                "url": "https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html",
            },
        }
        self.ids = ["first-cti-source-evaluation", "oasis-stix-21"]
        self.rows = [
            [
                "OFFICIAL_DOCUMENTATION",
                "[FIRST](https://www.first.org/global/sigs/cti/curriculum/source-evaluation)",
                "Source reliability; Information reliability",
                "ratings",
                "not probability",
            ],
            [
                "STANDARD",
                "[STIX](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)",
                "4.7 Indicator; 4.14 Observed Data",
                "objects",
                "not truth validation",
            ],
        ]

    def _errors(self, text: str, rows: list[list[str]] | None = None) -> list[str]:
        return strict_source_consistency_errors(
            Path("fixture.md"),
            f"{STRICT_SOURCE_CONSISTENCY}\n{text}",
            self.ids,
            self.rows if rows is None else rows,
            self.by_id,
        )

    def test_canonical_sources_pass(self) -> None:
        text = (
            "**Direct link:** [FIRST]"
            "(https://www.first.org/global/sigs/cti/curriculum/source-evaluation)\n"
            "**Direct link:** [STIX](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)"
        )
        self.assertEqual(self._errors(text), [])

    def test_obsolete_first_and_stix_urls_fail(self) -> None:
        text = (
            "https://www.first.org/global/sigs/cti/curriculum/cti-source-evaluation\n"
            "https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html"
        )
        errors = self._errors(text)
        self.assertEqual(sum("obsolete URL" in error for error in errors), 2)

    def test_visible_type_mismatch_fails(self) -> None:
        rows = [list(row) for row in self.rows]
        rows[0][0] = "STANDARD"
        self.assertTrue(any("differs from" in error for error in self._errors("", rows)))

    def test_stale_stix_section_label_fails(self) -> None:
        self.assertTrue(any("stale source label" in error for error in self._errors("4.13 Observed Data")))

    def test_undeclared_direct_link_fails(self) -> None:
        errors = self._errors("**Direct link:** [Other](https://example.com/undeclared)")
        self.assertTrue(any("does not correspond" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
