#!/usr/bin/env python3
"""Generate an auditable field-level data dictionary for the final dataset."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "REFERENCE_DATA" / "university_final_dataset.csv"
OUTPUT = ROOT / "MODULE_07_QA_TESTING" / "evidence" / "data_dictionary.json"

DEFINITIONS = {
    "Name": "Standardized university name used as the institutional label.",
    "Country": "Standardized country assigned to the university.",
    "Region": "Geographic region used for dashboard grouping.",
    "Year": "Reporting year. The delivered scope contains 2026 only.",
    "Size": "Institution size category from the supplied source.",
    "Focus": "Institutional subject-focus category from the supplied source.",
    "Research": "Research-activity category from the supplied source.",
    "Status": "Institution ownership/status category from the supplied source.",
    "QS_Rank_Normalized": "QS rank transformed to a 0-100 score where a higher score indicates a stronger rank.",
    "THE_Rank_Normalized": "THE rank transformed to a 0-100 score where a higher score indicates a stronger rank.",
    "KPI_Global_Ranking_Score": "Average of the normalized QS and THE ranking scores.",
    "KPI_Research_Impact_Score": "Weighted score using citations, research quality and industry impact.",
    "KPI_Faculty_to_Student_Ratio": "Reciprocal of students per staff member; higher values indicate more staff availability.",
    "KPI_International_Student_Percentage": "International-student share expressed in percentage points.",
    "KPI_Academic_Reputation_Score": "Supplied academic-reputation score retained as an auditable KPI.",
    "KPI_Research_Productivity_Index": "Weighted proxy based on research quality, environment, citations, network and industry impact; not a publication-count measure.",
}


def describe_column(frame: pd.DataFrame, column: str) -> dict:
    series = frame[column]
    non_null = int(series.notna().sum())
    missing = int(series.isna().sum())
    examples = [str(value) for value in series.dropna().drop_duplicates().head(3).tolist()]
    item = {
        "field": column,
        "data_type": str(series.dtype),
        "non_null_count": non_null,
        "missing_count": missing,
        "missing_pct": round(missing / len(frame) * 100, 4),
        "unique_values": int(series.nunique(dropna=True)),
        "minimum": "",
        "maximum": "",
        "examples": "; ".join(examples),
        "definition": DEFINITIONS.get(column, column.replace("_", " ").replace("QS", "QS").replace("THE", "THE") + " from the supplied QS/THE dataset."),
        "role": "Derived KPI" if column.startswith("KPI_") else ("Derived normalized field" if column.endswith("_Normalized") else "Source field"),
    }
    if pd.api.types.is_numeric_dtype(series):
        item["minimum"] = "" if series.dropna().empty else round(float(series.min()), 4)
        item["maximum"] = "" if series.dropna().empty else round(float(series.max()), 4)
    return item


def main() -> None:
    frame = pd.read_csv(SOURCE, low_memory=False)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "dataset": SOURCE.name,
        "rows": len(frame),
        "columns": len(frame.columns),
        "reporting_year": 2026,
        "fields": [describe_column(frame, column) for column in frame.columns],
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "fields": len(output["fields"])}, indent=2))


if __name__ == "__main__":
    main()
