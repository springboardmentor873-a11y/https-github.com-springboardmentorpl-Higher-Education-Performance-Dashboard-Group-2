"""
Module 2: Education Data Cleaning & Transformation
---------------------------------------------------
Completes the Module 2 cleaning workflow for EduVision.

Input:
    university_raw_data.csv

Outputs:
    university_cleaned.csv
    cleaning_summary.json

Key operations required by the project:
    * remove duplicate universities
    * standardize university/country text
    * resolve QS/THE rank bands to numeric midpoints
    * normalize numeric ranking fields
    * validate missingness and duplicate rates
    * produce a Tableau-ready cleaned dataset
"""

from pathlib import Path
import re
import json
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "university_raw_data.csv"
OUTPUT_PATH = BASE_DIR / "data" / "university_cleaned.csv"
SUMMARY_PATH = BASE_DIR / "docs" / "cleaning_summary.json"


def resolve_band_rank(value):
    """Convert 1, 2=, 601-650 or 601–650 to a numeric rank."""
    if pd.isna(value):
        return np.nan
    text = str(value).strip().replace("=", "")
    if not text or text.lower() in {"nan", "none"}:
        return np.nan
    parts = re.split(r"[-–]", text)
    try:
        nums = [float(p.strip()) for p in parts if p.strip()]
        return float(sum(nums) / len(nums))
    except (ValueError, TypeError):
        return np.nan


def standardize_text(series):
    return (
        series.astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def clean(df):
    df = df.copy()

    # Standardize names and country fields.
    for col in ["Name_QS", "Name_THE", "Country/Territory", "Country", "Region"]:
        if col in df.columns:
            df[col] = standardize_text(df[col])

    # Remove duplicate universities using the primary QS name.
    before = len(df)
    df = df.drop_duplicates(subset=["Name_QS"], keep="first").copy()
    duplicates_removed = before - len(df)

    # Resolve ranking bands.
    df["QS_Rank_Numeric"] = df["Rank_QS"].apply(resolve_band_rank)
    df["THE_Rank_Numeric"] = df["Rank_THE"].apply(resolve_band_rank)

    # Normalize common numeric columns when present.
    numeric_candidates = [
        "Academic Reputation SCORE", "Employer Reputation SCORE",
        "Faculty Student Ratio SCORE", "Citations per Faculty SCORE",
        "International Faculty  SCORE", "International Student SCORE",
        "International Students Diversity SCORE",
        "International Research Network SCORE", "Employment Outcomes SCORE",
        "Sustainability SCORE", "Overall SCORE", "Student Population",
        "Students to Staff Ratio", "International Students", "Overall Score",
        "Teaching", "Research Environment", "Research Quality",
        "Industry Impact", "International Outlook"
    ]
    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Use the QS country as the preferred canonical country when available.
    if "Country/Territory" in df.columns and "Country" in df.columns:
        df["Country"] = df["Country/Territory"].fillna(df["Country"])

    # Rows without either ranking cannot support the ranking KPIs.
    usable = df["QS_Rank_Numeric"].notna() & df["THE_Rank_Numeric"].notna()
    rows_dropped_missing_rank = int((~usable).sum())
    df = df.loc[usable].reset_index(drop=True)

    return df, {
        "rows_before": int(before),
        "duplicates_removed": int(duplicates_removed),
        "rows_dropped_missing_rank": rows_dropped_missing_rank,
        "rows_after": int(len(df)),
    }


def main():
    df = pd.read_csv(INPUT_PATH)
    cleaned, stats = clean(df)

    missing_cells = int(cleaned.isna().sum().sum())
    total_cells = int(cleaned.shape[0] * cleaned.shape[1])
    completeness = 100 * (1 - missing_cells / total_cells) if total_cells else 0
    missing_rate = 100 - completeness

    # Module 2 target: less than 2% missing values.
    stats.update({
        "columns_after": int(cleaned.shape[1]),
        "missing_cells": missing_cells,
        "missing_rate_percent": round(missing_rate, 4),
        "completeness_percent": round(completeness, 4),
        "module_2_target_met": bool(missing_rate < 2.0),
        "duplicate_name_count_after": int(cleaned["Name_QS"].duplicated().sum()),
    })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_PATH, index=False)
    SUMMARY_PATH.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    print(json.dumps(stats, indent=2))
    print(f"Saved cleaned dataset -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
