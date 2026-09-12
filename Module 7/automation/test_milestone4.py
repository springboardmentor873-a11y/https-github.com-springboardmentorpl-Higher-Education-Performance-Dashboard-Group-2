#!/usr/bin/env python3
"""Regression suite for the EduVision Milestone 4 approved release."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from validate_milestone4 import run  # noqa: E402


class Milestone4ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run(include_deliverables=False)

    def test_release_is_approved(self) -> None:
        self.assertEqual(self.result["summary"]["release_status"], "APPROVED")
        self.assertEqual(self.result["summary"]["failed_tests"], 0)

    def test_dataset_scope_is_exact(self) -> None:
        data = self.result["data"]
        self.assertEqual(data["rows"], 1120)
        self.assertEqual(data["countries"], 93)
        self.assertEqual(data["regions"], 5)
        self.assertEqual(data["reporting_years"], [2026])

    def test_source_and_cleaning_quality_gates(self) -> None:
        data = self.result["data"]
        self.assertGreater(data["raw_completeness_pct"], 95)
        self.assertLess(data["cleaned_missing_pct"], 2)
        self.assertEqual(data["duplicate_keys"], 0)

    def test_every_kpi_reconciles(self) -> None:
        self.assertEqual(self.result["data"]["kpi_accuracy_pct"], 100.0)
        self.assertEqual(len(self.result["data"]["kpi_results"]), 6)
        self.assertTrue(all(item["status"] == "PASS" for item in self.result["data"]["kpi_results"]))
        self.assertTrue(all(item["rows_checked"] == 1120 for item in self.result["data"]["kpi_results"]))

    def test_dashboard_page_order(self) -> None:
        self.assertEqual(
            self.result["dashboard"]["page_order"],
            [
                "University Overview",
                "Research Analytics",
                "Student Analytics",
                "Country Comparison",
                "Executive Command Center",
            ],
        )

    def test_dashboard_inventory(self) -> None:
        report = self.result["dashboard"]
        self.assertEqual(report["visual_count"], 110)
        self.assertEqual(report["data_visual_count"], 95)
        self.assertEqual(report["measure_count"], 35)
        self.assertEqual(report["column_count"], 35)

    def test_page_control_contract(self) -> None:
        report = self.result["dashboard"]
        self.assertEqual(report["slicers"], 30)
        self.assertEqual(report["kpi_cards"], 22)
        self.assertEqual(report["navigators"], 5)
        self.assertEqual(report["maps"], 5)

    def test_visual_bindings_are_active(self) -> None:
        report = self.result["dashboard"]
        self.assertEqual(report["active_projections"], 310)
        self.assertEqual(report["inactive_projections"], 0)

    def test_model_is_portable(self) -> None:
        report = self.result["dashboard"]
        self.assertTrue(report["embedded_import_model"])
        self.assertFalse(report["machine_specific_path"])

    def test_standard_maps_replace_azure_maps(self) -> None:
        visual_types = self.result["dashboard"]["visual_types"]
        self.assertEqual(visual_types.get("map"), 5)
        self.assertEqual(visual_types.get("azureMap", 0), 0)

    def test_approved_zip_checksum(self) -> None:
        self.assertEqual(
            self.result["release"]["sha256"],
            "98dd2ed7bdae98fabe661d68af729c3cdb8c3f1d5ae097d94492813ba1593a12",
        )

    def test_machine_readable_evidence_exists(self) -> None:
        evidence = HERE.parent / "evidence"
        self.assertTrue((evidence / "module7_validation.json").is_file())
        self.assertTrue((evidence / "test_results.csv").is_file())
        self.assertTrue((evidence / "dashboard_inventory.json").is_file())
        parsed = json.loads((evidence / "module7_validation.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(parsed["summary"]["total_tests"], 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
