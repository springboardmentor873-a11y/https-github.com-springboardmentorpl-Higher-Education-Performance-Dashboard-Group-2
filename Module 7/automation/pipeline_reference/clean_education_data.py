#!/usr/bin/env python3
"""Module 2: clean, standardize and normalize the consolidated ranking data."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from project_config import COUNTRY_ALIASES, DATA_DIR, REPORTING_YEAR, TEXT_COLUMNS


def extract_rank(value: object) -> float:
    """Convert labels such as 1401+ or =120 into comparable numeric ranks."""
    if pd.isna(value):
        return np.nan
    match = re.search(r"\d+", str(value).replace(",", ""))
    return float(match.group(0)) if match else np.nan


def normalize_rank(rank_series: pd.Series) -> pd.Series:
    """Use inverse min-max scaling; rank 1 receives the highest score."""
    numeric = rank_series.map(extract_rank)
    minimum = numeric.min()
    maximum = numeric.max()
    if pd.isna(minimum) or pd.isna(maximum):
        raise ValueError("Ranking data contains no usable numeric values.")
    if maximum == minimum:
        return pd.Series(100.0, index=rank_series.index)
    return ((maximum - numeric) / (maximum - minimum) * 100).round(2)


def clean_dataset(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    cleaned = frame.copy()
    input_rows = len(cleaned)

    for column in TEXT_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip().str.replace(
                r"\s+", " ", regex=True
            )

    cleaned["Country"] = cleaned["Country"].replace(COUNTRY_ALIASES)
    cleaned = cleaned.drop_duplicates(subset=["Name", "Country", "Year"], keep="first")
    cleaned = cleaned.loc[cleaned["Year"].eq(REPORTING_YEAR)].copy()

    # Categorical metadata may be labelled; unavailable numerical observations
    # must remain empty so scores and historical ranks are never fabricated.
    if "Status" in cleaned.columns:
        cleaned["Status"] = cleaned["Status"].fillna("Not reported")
    if "Female_to_Male_Ratio" in cleaned.columns:
        cleaned["Female_to_Male_Ratio"] = cleaned["Female_to_Male_Ratio"].fillna("Not reported")

    cleaned["QS_Rank_Normalized"] = normalize_rank(cleaned["Rank_QS"])
    cleaned["THE_Rank_Normalized"] = normalize_rank(cleaned["Rank_THE"])

    missing_rate = float(cleaned.isna().sum().sum() / cleaned.size * 100)
    audit = {
        "input_rows": int(input_rows),
        "output_rows": int(len(cleaned)),
        "duplicates_removed": int(input_rows - len(cleaned)),
        "missing_cells": int(cleaned.isna().sum().sum()),
        "missing_pct": round(missing_rate, 4),
        "completeness_pct": round(100 - missing_rate, 4),
        "years": sorted(int(value) for value in cleaned["Year"].unique()),
        "normalization": "Inverse min-max rank normalization, rounded to 2 decimals.",
        "numeric_missing_policy": "Retained as missing; no scores, ranks or publication counts invented.",
    }
    return cleaned, audit


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DATA_DIR / "university_raw_data.csv")
    parser.add_argument("--output", type=Path, default=DATA_DIR / "university_cleaned.csv")
    parser.add_argument("--audit-output", type=Path, default=DATA_DIR / "cleaning_audit.json")
    args = parser.parse_args()

    frame = pd.read_csv(args.input, low_memory=False)
    cleaned, audit = clean_dataset(frame)
    if audit["missing_pct"] >= 2:
        raise ValueError(f"Clean dataset missingness exceeds the 2% target: {audit['missing_pct']}%")
    cleaned.to_csv(args.output, index=False, encoding="utf-8-sig")
    args.audit_output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
