from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.scan_public_tree import scan_paths


class PublicTreeScannerTests(unittest.TestCase):
    def scan(self, files: dict[str, str | bytes]) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths: list[Path] = []
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(content, bytes):
                    path.write_bytes(content)
                else:
                    path.write_text(content, encoding="utf-8")
                paths.append(path)
            return scan_paths(root, paths)

    def test_allowed_public_tree_passes(self) -> None:
        findings = self.scan(
            {
                ".gitignore": "site/\n",
                "LICENSE": "MIT\n",
                "README.md": "# Course\n",
                ".github/workflows/pages.yml": "name: pages\n",
                "curriculum/manifest.yaml": "lessons: []\n",
                "docs/index.md": "# Course\n",
                "lab/run.py": "print('local lab')\n",
                "scripts/validate_lessons.py": "# validator\n",
                "sources/sources.yaml": "sources: []\n",
                "tests/javascript/quality.test.ts": "// test\n",
            }
        )
        self.assertEqual(findings, [])

    def test_unexpected_root_markdown_report_fails(self) -> None:
        findings = self.scan({"REVIEW_NOTES.md": "# Internal review\n"})
        self.assertTrue(any("unapproved root file" in finding for finding in findings))

    def test_unexpected_zip_fails(self) -> None:
        findings = self.scan({"docs/course-export.zip": b"PK\x03\x04"})
        self.assertTrue(any("ZIP archive" in finding for finding in findings))

    def test_unexpected_top_level_directory_fails(self) -> None:
        findings = self.scan({"private-work/file.txt": "scratch\n"})
        self.assertTrue(any("unapproved top-level directory" in finding for finding in findings))

    def test_secret_pattern_fails(self) -> None:
        token = "ghp_" + ("A" * 40)
        findings = self.scan({"docs/index.md": f"credential = {token}\n"})
        self.assertTrue(any("GitHub token" in finding for finding in findings))

    def test_local_user_path_fails(self) -> None:
        local_path = "C:" + "\\Users\\" + "example\\notes.txt"
        findings = self.scan({"docs/index.md": f"Generated at {local_path}\n"})
        self.assertTrue(any("local user path" in finding for finding in findings))

    def test_normal_lesson_and_source_files_pass(self) -> None:
        findings = self.scan(
            {
                "docs/modules/01-http-edge/01-http-request-response.md": "# HTTP request and response\n",
                "sources/README.md": "# Sources\n",
                "sources/sources.yaml": "sources: []\n",
            }
        )
        self.assertEqual(findings, [])

    def test_local_telemetry_fails(self) -> None:
        findings = self.scan({"lab/telemetry/run.json": "{}\n"})
        self.assertTrue(any("local telemetry output" in finding for finding in findings))

    def test_generated_site_output_fails(self) -> None:
        findings = self.scan({"site/index.html": "<h1>Generated</h1>\n"})
        self.assertTrue(any("generated site" in finding for finding in findings))

    def test_review_image_requires_learner_media_location(self) -> None:
        rejected = self.scan({"artifacts/screenshot.png": b"\x00PNG"})
        approved = self.scan({"docs/assets/course-diagram.png": b"\x00PNG"})
        self.assertTrue(any("image outside" in finding for finding in rejected))
        self.assertEqual(approved, [])


if __name__ == "__main__":
    unittest.main()
