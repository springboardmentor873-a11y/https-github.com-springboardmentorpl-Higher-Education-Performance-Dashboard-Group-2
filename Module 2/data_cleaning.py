"""
Module 2: Data Cleaning & Transformation
------------------------------------------
Cleans the raw merged QS + THE dataset:
  - Removes duplicate university rows
  - Standardizes university and country name formatting
  - Resolves QS "band" ranks (e.g. "601-650") into numeric mid-point ranks
  - Normalizes core ranking metrics for downstream KPI engineering

Input:
    university_raw_data.csv

Output:
    university_cleaned.csv
"""

import re
import pandas as pd

INPUT_PATH = "university_raw_data.csv"
OUTPUT_PATH = "university_cleaned.csv"


def resolve_band_rank(value) -> float:
    """Convert a rank value that may be a single number or a
    'start-end' band (e.g. '601-650') into a numeric midpoint."""
    if pd.isna(value):
        return None
    text = str(value).strip().replace("=", "")
    if "-" in text or "–" in text:
        parts = re.split(r"[-–]", text)
        try:
            nums = [float(p) for p in parts if p.strip()]
            return sum(nums) / len(nums)
        except ValueError:
            return None
    try:
        return float(text)
    except ValueError:
        return None


def standardize_text(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["Name_QS"]).copy()
    removed = before - len(df)
    print(f"Duplicate rows removed: {removed}")

    df["Name_QS"] = standardize_text(df["Name_QS"])
    df["Country/Territory"] = standardize_text(df["Country/Territory"])
    df["Country"] = standardize_text(df["Country"])

    # Resolve QS/THE ranks that may be given as bands into numeric ranks
    df["QS_Rank_Numeric"] = df["Rank_QS"].apply(resolve_band_rank)
    df["THE_Rank_Numeric"] = df["Rank_THE"].apply(resolve_band_rank)

    # Drop rows with no resolvable rank on either side (unusable for KPIs)
    before_rank_filter = len(df)
    df = df.dropna(subset=["QS_Rank_Numeric", "THE_Rank_Numeric"])
    print(f"Rows dropped for missing rank data: {before_rank_filter - len(df)}")

    completeness = 100 * (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1]))
    print(f"Dataset completeness after cleaning: {completeness:.2f}%")

    return df.reset_index(drop=True)


def main():
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded raw dataset: {df.shape}")

    cleaned = clean(df)
    print(f"Cleaned dataset: {cleaned.shape}")

    cleaned.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved cleaned dataset -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
