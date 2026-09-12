"""
EduVision KPI Engineering Script
--------------------------------
This script takes the merged QS + THE 2026 dataset and creates six KPI fields:

1. KPI_Global_Ranking_Score
2. KPI_Research_Impact_Score
3. KPI_Faculty_to_Student_Ratio
4. KPI_International_Student_Percentage
5. KPI_Academic_Reputation_Score
6. KPI_Research_Productivity_Index

Input:
    EduVision_Merged_2026_Selected_Columns.xlsx

Output:
    EduVision_Merged_2026_With_KPIs.xlsx
"""

import re
import pandas as pd
import numpy as np


INPUT_FILE = "EduVision_Merged_2026_Selected_Columns.xlsx"
OUTPUT_FILE = "EduVision_Merged_2026_With_KPIs.xlsx"


def to_numeric_safe(series: pd.Series) -> pd.Series:
    """
    Converts a column into numeric values after removing commas and percentage signs.
    Invalid values are converted into NaN instead of throwing errors.
    """
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


def extract_rank_number(value):
    """
    Extracts the first numeric part from rank values such as:
    '1', '7=', '801-850', '1401+', etc.
    This is useful because ranking columns are sometimes stored as text/ranges.
    """
    match = re.search(r"\d+(\.\d+)?", str(value))
    return float(match.group(0)) if match else np.nan


def inverse_minmax_rank(rank_series: pd.Series) -> pd.Series:
    """
    Converts ordinal rank values into a 0-100 normalized score.
    Since lower rank means better performance, inverse min-max scaling is used:

        normalized_score = ((max_rank - current_rank) / (max_rank - min_rank)) * 100

    Higher normalized score = better ranking performance.
    """
    rank_series = rank_series.astype(float)
    min_rank = rank_series.min()
    max_rank = rank_series.max()

    if pd.isna(min_rank) or pd.isna(max_rank) or min_rank == max_rank:
        return pd.Series(np.nan, index=rank_series.index)

    return ((max_rank - rank_series) / (max_rank - min_rank)) * 100


# -------------------------------------------------------------------
# Step 1: Load merged dataset
# -------------------------------------------------------------------
df = pd.read_excel(INPUT_FILE, sheet_name="Merged_2026")

# -------------------------------------------------------------------
# Step 2: Ensure numerical fields are in correct data type
# -------------------------------------------------------------------
numeric_columns = [
    "Academic_Reputation_Score",
    "Citations_per_Faculty_Score",
    "International_Research_Network_Score",
    "Students_to_Staff_Ratio",
    "International_Students",
    "Research_Environment",
    "Research_Quality",
    "Industry_Impact",
    "QS_Rank_Normalized",
    "THE_Rank_Normalized"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = to_numeric_safe(df[col])

# -------------------------------------------------------------------
# Step 3: Create normalized rank fields if they are missing
# -------------------------------------------------------------------
if "QS_Rank_Normalized" not in df.columns:
    df["QS_Rank_Number"] = df["Rank_QS"].apply(extract_rank_number)
    df["QS_Rank_Normalized"] = inverse_minmax_rank(df["QS_Rank_Number"])

if "THE_Rank_Normalized" not in df.columns:
    df["THE_Rank_Number"] = df["Rank_THE"].apply(extract_rank_number)
    df["THE_Rank_Normalized"] = inverse_minmax_rank(df["THE_Rank_Number"])

# -------------------------------------------------------------------
# Step 4: KPI Engineering
# -------------------------------------------------------------------

# 1. Global Ranking Score
# Combines normalized QS and THE rank performance into one rank-based score.
df["KPI_Global_Ranking_Score"] = (
    df[["QS_Rank_Normalized", "THE_Rank_Normalized"]].mean(axis=1)
)

# 2. Research Impact Score
# Gives higher weight to THE Research Quality, followed by QS Citations per Faculty
# and THE Industry Impact.
df["KPI_Research_Impact_Score"] = (
    0.35 * df["Citations_per_Faculty_Score"] +
    0.45 * df["Research_Quality"] +
    0.20 * df["Industry_Impact"]
)

# 3. Faculty-to-Student Ratio
# THE gives Students-to-Staff Ratio. To convert it into Faculty-to-Student Ratio,
# we take the inverse.
df["KPI_Faculty_to_Student_Ratio"] = (
    1 / df["Students_to_Staff_Ratio"]
)

# 4. International Student Percentage
# The source field is stored as a decimal, so it is multiplied by 100.
df["KPI_International_Student_Percentage"] = (
    df["International_Students"] * 100
)

# 5. Academic Reputation Score
# Directly taken from QS Academic Reputation Score.
df["KPI_Academic_Reputation_Score"] = (
    df["Academic_Reputation_Score"]
)

# 6. Research Productivity Index
# Composite index based on research quality, research environment, citations,
# international research collaboration and industry impact.
df["KPI_Research_Productivity_Index"] = (
    0.30 * df["Research_Quality"] +
    0.25 * df["Research_Environment"] +
    0.20 * df["Citations_per_Faculty_Score"] +
    0.15 * df["International_Research_Network_Score"] +
    0.10 * df["Industry_Impact"]
)

# -------------------------------------------------------------------
# Step 5: Validation checks
# -------------------------------------------------------------------
required_kpis = [
    "KPI_Global_Ranking_Score",
    "KPI_Research_Impact_Score",
    "KPI_Faculty_to_Student_Ratio",
    "KPI_International_Student_Percentage",
    "KPI_Academic_Reputation_Score",
    "KPI_Research_Productivity_Index"
]

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("\nMissing values in KPI columns:")
print(df[required_kpis].isna().sum())

print("\nDuplicate university-country records:")
print(df.duplicated(subset=["Name", "Country"]).sum())

# -------------------------------------------------------------------
# Step 6: Export final file
# -------------------------------------------------------------------
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Merged_2026_KPIs")

print("\nKPI dataset created successfully:", OUTPUT_FILE)
