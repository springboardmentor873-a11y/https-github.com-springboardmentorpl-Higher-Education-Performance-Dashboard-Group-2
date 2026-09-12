#!/usr/bin/env python3
"""Module 3: generate the six original, source-faithful education KPIs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from project_config import COUNTRY_ALIASES, DATA_DIR, KPI_COLUMNS


def calculate_kpis(cleaned: pd.DataFrame) -> pd.DataFrame:
    frame = cleaned.copy()

    frame["KPI_Global_Ranking_Score"] = (
        frame["QS_Rank_Normalized"] + frame["THE_Rank_Normalized"]
    ) / 2

    frame["KPI_Research_Impact_Score"] = (
        0.35 * frame["Citations_per_Faculty_Score"]
        + 0.45 * frame["Research_Quality"]
        + 0.20 * frame["Industry_Impact"]
    )

    staff_ratio = pd.to_numeric(frame["Students_to_Staff_Ratio"], errors="coerce")
    if (staff_ratio <= 0).any():
        raise ValueError("Students_to_Staff_Ratio must be positive for every university.")
    frame["KPI_Faculty_to_Student_Ratio"] = 1 / staff_ratio

    frame["KPI_International_Student_Percentage"] = frame["International_Students"] * 100
    frame["KPI_Academic_Reputation_Score"] = frame["Academic_Reputation_Score"]

    frame["KPI_Research_Productivity_Index"] = (
        0.30 * frame["Research_Quality"]
        + 0.25 * frame["Research_Environment"]
        + 0.20 * frame["Citations_per_Faculty_Score"]
        + 0.15 * frame["International_Research_Network_Score"]
        + 0.10 * frame["Industry_Impact"]
    )
    return frame


def compare_with_reference(generated: pd.DataFrame, reference: pd.DataFrame) -> dict:
    reference = reference.copy()
    for key in ["Name", "Country"]:
        reference[key] = reference[key].astype("string").str.strip().str.replace(
            r"\s+", " ", regex=True
        )
    reference["Country"] = reference["Country"].replace(COUNTRY_ALIASES)
    aligned = generated.merge(
        reference[["Name", "Country", *KPI_COLUMNS]],
        on=["Name", "Country"],
        how="inner",
        suffixes=("_generated", "_reference"),
    )
    if len(aligned) != len(generated):
        raise ValueError(
            f"Reference comparison matched {len(aligned)} of {len(generated)} universities."
        )
    results = []
    for column in KPI_COLUMNS:
        observed = aligned[f"{column}_generated"].to_numpy(dtype=float)
        expected = aligned[f"{column}_reference"].to_numpy(dtype=float)
        matched = np.isclose(observed, expected, rtol=1e-10, atol=1e-8, equal_nan=True)
        differences = np.abs(observed - expected)
        results.append(
            {
                "kpi": column,
                "rows_checked": int(len(aligned)),
                "matching_rows": int(matched.sum()),
                "accuracy_pct": round(float(matched.mean() * 100), 4),
                "max_absolute_difference": float(np.nanmax(differences)),
                "status": "PASS" if matched.all() else "FAIL",
            }
        )
    return {
        "matched_universities": int(len(aligned)),
        "kpi_count": len(KPI_COLUMNS),
        "overall_accuracy_pct": round(float(np.mean([row["accuracy_pct"] for row in results])), 4),
        "results": results,
        "publication_count_limitation": "The source does not contain publication totals; the research-productivity KPI is a weighted indicator proxy.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DATA_DIR / "university_cleaned.csv")
    parser.add_argument("--output", type=Path, default=DATA_DIR / "university_final_dataset.csv")
    parser.add_argument(
        "--reference",
        type=Path,
        default=DATA_DIR / "EduVision_Source_2026_With_KPIs.xlsx",
    )
    parser.add_argument("--audit-output", type=Path, default=DATA_DIR / "kpi_validation.json")
    args = parser.parse_args()

    cleaned = pd.read_csv(args.input, low_memory=False)
    final = calculate_kpis(cleaned)
    final.to_csv(args.output, index=False, encoding="utf-8-sig")

    reference = pd.read_excel(args.reference, sheet_name="Merged_2026")
    audit = compare_with_reference(final, reference)
    args.audit_output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    if audit["overall_accuracy_pct"] < 95:
        raise ValueError("KPI accuracy is below the 95% project requirement.")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
