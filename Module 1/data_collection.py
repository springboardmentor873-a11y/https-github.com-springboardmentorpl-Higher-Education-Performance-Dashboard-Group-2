"""
Module 1: University Data Collection
--------------------------------------
Loads the QS World University Rankings 2026 and THE World University
Rankings 2026 source files, matches universities across both rankings
by name, and produces a single merged "raw" dataset.

Input:
    2026_QS_World_University_Rankings.csv
    THE_World_University_Rankings_2026.xlsx

Output:
    university_raw_data.csv
"""

import pandas as pd

QS_PATH = "2026_QS_World_University_Rankings.csv"
THE_PATH = "THE_World_University_Rankings_2026.xlsx"
OUTPUT_PATH = "university_raw_data.csv"


def load_qs(path: str) -> pd.DataFrame:
    qs = pd.read_csv(path)
    qs["Name"] = qs["Name"].astype(str).str.strip()
    qs["match_key"] = qs["Name"].str.lower()
    return qs


def load_the(path: str) -> pd.DataFrame:
    the = pd.read_excel(path)
    the["Name"] = the["Name"].astype(str).str.strip()
    the["match_key"] = the["Name"].str.lower()
    return the


def merge_rankings(qs: pd.DataFrame, the: pd.DataFrame) -> pd.DataFrame:
    """Inner-join QS and THE rankings on normalized university name."""
    merged = pd.merge(
        qs,
        the,
        on="match_key",
        how="inner",
        suffixes=("_QS", "_THE"),
    )
    return merged


def main():
    qs = load_qs(QS_PATH)
    the = load_the(THE_PATH)

    print(f"QS Rankings loaded:  {len(qs)} universities")
    print(f"THE Rankings loaded: {len(the)} universities")

    merged = merge_rankings(qs, the)
    merged = merged.drop(columns=["match_key"])

    print(f"Matched universities (present in both rankings): {len(merged)}")

    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved raw merged dataset -> {OUTPUT_PATH}")
    print(f"Shape: {merged.shape}")


if __name__ == "__main__":
    main()
