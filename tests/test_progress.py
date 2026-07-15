from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.progress import gate_status, load_progress, recommended_tasks, render_report, validate_progress

ROOT = Path(__file__).resolve().parents[1]


class ProgressTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load_progress(ROOT / "curriculum" / "progress.yaml")

    def test_default_schema_is_valid(self) -> None:
        self.assertEqual(validate_progress(self.data), [])
        report = render_report(self.data)
        self.assertIn("Current checkpoint: Foundation in progress", report)
        self.assertIn("Completed modules at current level: 0/9", report)
        self.assertIn("not a hiring prediction", report)

    def test_recommends_canonical_first_three_modules(self) -> None:
        tasks = recommended_tasks(self.data, gate_status(self.data))
        self.assertIn("Safety and red-team engagement discipline", tasks[0])
        self.assertIn("Web request path and network fundamentals", tasks[1])
        self.assertIn("Automated abuse and threat modeling", tasks[2])

    def test_foundation_gate_requires_modules_artifacts_and_evidence(self) -> None:
        data = copy.deepcopy(self.data)
        for module in data["modules"].values():
            module["level"] = 1
            module["artifacts"] = ["artifacts/example.md"]
        self.assertFalse(gate_status(data)["foundation"]["satisfied"])
        for field in data["gate_evidence"]["foundation"]:
            data["gate_evidence"]["foundation"][field] = True
        self.assertTrue(gate_status(data)["foundation"]["satisfied"])

    def test_rejects_non_integer_or_out_of_range_level(self) -> None:
        for invalid in (True, "1", -1, 5):
            with self.subTest(invalid=invalid):
                data = copy.deepcopy(self.data)
                data["modules"]["safety"]["level"] = invalid
                self.assertTrue(validate_progress(data))

    def test_progress_file_is_json_compatible_yaml(self) -> None:
        json.loads((ROOT / "curriculum" / "progress.yaml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

