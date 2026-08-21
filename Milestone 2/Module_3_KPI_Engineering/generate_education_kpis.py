"""
EduVision_DV - Milestone 2 / Module 3: Education KPI Engineering

Input:
    university_cleaned.csv

Output:
    university_final_dataset.xlsx

KPIs:
    1. Global Ranking Score
    2. Research Impact Score
    3. Faculty-to-Student Ratio
    4. International Student Percentage
    5. Academic Reputation Score
    6. Research Productivity Index
"""

from pathlib import Path
import pandas as pd
import numpy as np
import re


# =========================================================
# 1. FILE PATHS
# =========================================================

BASE = Path(__file__).resolve().parent

INPUT = BASE / "university_cleaned.csv"
OUTPUT = BASE / "university_final_dataset.xlsx"


# =========================================================
# 2. HELPER FUNCTIONS
# =========================================================

def to_num(series):
    """Convert values to numeric. Invalid values become NaN."""
    return pd.to_numeric(series, errors="coerce")


def normalize_rank(series):
    """
    Converts ranking values into numeric values.

    Examples:
        1          -> 1
        741-750    -> 745.5
        1401+      -> 1401
        Missing    -> NaN
    """

    def one(value):

        if pd.isna(value):
            return np.nan

        text = str(value).strip().replace(",", "")

        # Ranking range, e.g. 741-750
        match = re.fullmatch(
            r"(\d+)\s*-\s*(\d+)",
            text
        )

        if match:
            return (
                float(match.group(1))
                + float(match.group(2))
            ) / 2

        # Ranking with +, e.g. 1401+
        match = re.fullmatch(
            r"(\d+)\+",
            text
        )

        if match:
            return float(match.group(1))

        # Normal numeric ranking
        match = re.search(
            r"\d+(?:\.\d+)?",
            text
        )

        return float(match.group()) if match else np.nan

    return series.map(one)


def inverse_rank_score(series):
    """
    Converts ranking position into a 0-100 score.

    Lower ranking number = better score.

    Missing values remain NaN.
    """

    valid = series.dropna()

    if valid.empty:
        return pd.Series(
            index=series.index,
            dtype=float
        )

    minimum = valid.min()
    maximum = valid.max()

    if maximum == minimum:
        return pd.Series(
            100.0,
            index=series.index
        )

    return (
        (maximum - series)
        / (maximum - minimum)
        * 100
    ).clip(0, 100)


def minmax_100(series):
    """
    Converts a numeric series into a 0-100 scale.

    Missing values remain NaN.
    """

    valid = series.dropna()

    if valid.empty:
        return pd.Series(
            index=series.index,
            dtype=float
        )

    minimum = valid.min()
    maximum = valid.max()

    if maximum == minimum:
        return pd.Series(
            100.0,
            index=series.index
        )

    return (
        (series - minimum)
        / (maximum - minimum)
        * 100
    ).clip(0, 100)


# =========================================================
# 3. LOAD DATA
# =========================================================

if not INPUT.exists():

    raise FileNotFoundError(
        f"Could not find:\n{INPUT}\n\n"
        "Make sure university_cleaned.csv is in the "
        "same folder as this Python script."
    )


df = pd.read_csv(INPUT)  #Here is loading the data


print("=" * 65)
print("EDUVISION_DV - MODULE 3 KPI ENGINEERING")
print("=" * 65)

print(f"Input file: {INPUT}")
print(
    f"Input rows before filtering: "
    f"{len(df):,}"
)


# =========================================================
# 4. HANDLE MISSING VALUES
# =========================================================

# IMPORTANT:
#
# -1 is NOT an actual KPI value.
# It represents missing/unavailable data.
#
# Therefore:
# -1 → NaN
#
# NaN will appear as a blank cell in Excel
# and as Null in Tableau.

df = df.replace(
    [-1, "-1"],
    np.nan
)


# =========================================================
# 5. KEEP ONLY 2026 DATA
# =========================================================

if "Year" in df.columns:

    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )

    df = df[
        df["Year"] == 2026
    ].copy()


print(
    f"Rows after 2026 filtering: "
    f"{len(df):,}"
)


# =========================================================
# 6. CONVERT SOURCE FIELDS TO NUMERIC
# =========================================================

df["QS_Rank_Num"] = normalize_rank(
    df["QS_Rank"]
)

df["THE_Rank_Num"] = to_num(
    df["THE_Rank"]
)

df[
    "QS_Academic_Reputation_Score_Num"
] = to_num(
    df["QS_Academic_Reputation_Score"]
)

df[
    "THE_Research_Quality_Num"
] = to_num(
    df["THE_Research_Quality"]
)

df[
    "THE_Research_Environment_Num"
] = to_num(
    df["THE_Research_Environment"]
)

df[
    "THE_Students_to_Staff_Ratio_Num"
] = to_num(
    df["THE_Students_to_Staff_Ratio"]
)

df[
    "THE_International_Students_Pct_Num"
] = to_num(
    df["THE_International_Students_Pct"]
)


# =========================================================
# 7. KPI 1 — GLOBAL RANKING SCORE
# =========================================================

df["QS_Rank_Score"] = inverse_rank_score(
    df["QS_Rank_Num"]
)

df["THE_Rank_Score"] = inverse_rank_score(
    df["THE_Rank_Num"]
)


# Average the available QS and THE scores.
#
# If both are available:
#     average of QS + THE
#
# If only one is available:
#     use the available score
#
# If neither is available:
#     result is NaN

df["Global_Ranking_Score"] = df[
    [
        "QS_Rank_Score",
        "THE_Rank_Score"
    ]
].mean(
    axis=1,
    skipna=True
)


# =========================================================
# 8. KPI 2 — RESEARCH IMPACT SCORE
# =========================================================

# Project-defined formula:
#
# Research Impact Score =
#
# 60% Research Quality
# +
# 40% Research Environment

df["Research_Impact_Score"] = (
    0.60
    * df["THE_Research_Quality_Num"]
    +
    0.40
    * df["THE_Research_Environment_Num"]
)


# =========================================================
# 9. KPI 3 — FACULTY-TO-STUDENT RATIO
# =========================================================

# Source:
#
# Students-to-Staff Ratio
#
# Conversion:
#
# Faculty-to-Student Ratio =
# 1 / Students-to-Staff Ratio
#
# Missing or invalid values remain NaN.

df["Faculty_to_Student_Ratio"] = np.where(

    df[
        "THE_Students_to_Staff_Ratio_Num"
    ] > 0,

    1
    / df[
        "THE_Students_to_Staff_Ratio_Num"
    ],

    np.nan
)


# =========================================================
# 10. KPI 4 — INTERNATIONAL STUDENT PERCENTAGE
# =========================================================

df[
    "International_Student_Percentage"
] = df[
    "THE_International_Students_Pct_Num"
]


# =========================================================
# 11. KPI 5 — ACADEMIC REPUTATION SCORE
# =========================================================

df[
    "Academic_Reputation_Score"
] = df[
    "QS_Academic_Reputation_Score_Num"
]


# =========================================================
# 12. KPI 6 — RESEARCH PRODUCTIVITY INDEX
# =========================================================

# Normalize Research Quality to 0-100

df[
    "Research_Quality_Score_100"
] = minmax_100(
    df["THE_Research_Quality_Num"]
)


# Normalize Research Environment to 0-100

df[
    "Research_Environment_Score_100"
] = minmax_100(
    df["THE_Research_Environment_Num"]
)


# Project-defined formula:
#
# Research Productivity Index =
#
# 50% Research Quality
# +
# 50% Research Environment

df[
    "Research_Productivity_Index"
] = (

    0.50
    * df[
        "Research_Quality_Score_100"
    ]

    +

    0.50
    * df[
        "Research_Environment_Score_100"
    ]
)


# =========================================================
# 13. FINAL DATASET COLUMNS
# =========================================================

base_columns = [

    "University_Name",
    "Country",
    "Year",

    "QS_Rank",
    "QS_Previous_Rank",
    "QS_Academic_Reputation_Score",

    "QS_Region",
    "QS_Size",
    "QS_Focus",
    "QS_Research_Level",
    "QS_Status",

    "THE_Rank",
    "THE_Student_Population",
    "THE_Students_to_Staff_Ratio",
    "THE_International_Students",
    "THE_Female_to_Male_Ratio",

    "THE_Overall_Score",
    "THE_Teaching",
    "THE_Research_Environment",
    "THE_Research_Quality",
    "THE_Industry_Impact",
    "THE_International_Outlook",

    "THE_Year",

    "Data_Source",
    "QS_THE_Match_Status",

    "THE_International_Students_Pct",

    "THE_Female_Ratio",
    "THE_Male_Ratio",

    "QS_Data_Available",
    "THE_Data_Available"
]


# =========================================================
# KPI COLUMNS
# =========================================================

kpi_columns = [

    "QS_Rank_Score",

    "THE_Rank_Score",

    "Global_Ranking_Score",

    "Research_Impact_Score",

    "Faculty_to_Student_Ratio",

    "International_Student_Percentage",

    "Academic_Reputation_Score",

    "Research_Productivity_Index"
]


# =========================================================
# 14. CREATE FINAL DATAFRAME
# =========================================================

columns = [

    column

    for column
    in base_columns + kpi_columns

    if column in df.columns
]


final_df = df[
    columns
].copy()


# =========================================================
# 15. FINAL -1 SAFETY CHECK
# =========================================================

# Make absolutely sure no -1 placeholder remains.

final_df = final_df.replace(
    [-1, "-1"],
    np.nan
)


# =========================================================
# 16. ROUND KPI VALUES
# =========================================================

for column in kpi_columns:

    if column in final_df.columns:

        final_df[column] = (
            final_df[column]
            .round(4)
        )


# =========================================================
# 17. VALIDATION — DUPLICATES
# =========================================================

duplicate_count = final_df.duplicated(

    subset=[
        "University_Name",
        "Country",
        "Year"
    ]

).sum()


assert duplicate_count == 0, (

    "Duplicate university-country-year "
    f"records found: {duplicate_count}"

)


# =========================================================
# 18. VALIDATION — YEAR
# =========================================================

assert set(

    final_df[
        "Year"
    ].dropna().unique()

) == {2026}, (

    "Dataset contains a year "
    "other than 2026."

)


# =========================================================
# 19. VALIDATION — NO -1 VALUES
# =========================================================

remaining_minus_one = (

    final_df == -1

).sum().sum()


assert remaining_minus_one == 0, (

    "Some -1 placeholder values "
    "still remain."

)


# =========================================================
# 20. KPI COVERAGE
# =========================================================

print("\nKPI COVERAGE")
print("-" * 65)


for column in [

    "Global_Ranking_Score",

    "Research_Impact_Score",

    "Faculty_to_Student_Ratio",

    "International_Student_Percentage",

    "Academic_Reputation_Score",

    "Research_Productivity_Index"

]:

    count = (

        final_df[
            column
        ].notna().sum()

    )

    coverage = (

        count
        / len(final_df)
        * 100

    )

    print(

        f"{column}: "
        f"{count:,} "
        f"({coverage:.2f}%)"

    )


# =========================================================
# 21. FINAL VALIDATION INFORMATION
# =========================================================

print("\nVALIDATION")
print("-" * 65)

print(
    f"Input rows: "
    f"{len(df):,}"
)

print(
    f"Output rows: "
    f"{len(final_df):,}"
)

print(
    f"Output columns: "
    f"{len(final_df.columns)}"
)

print(
    f"Duplicate records: "
    f"{duplicate_count}"
)

print(
    f"Remaining -1 values: "
    f"{remaining_minus_one}"
)

print(
    "Years included:",
    sorted(
        final_df[
            "Year"
        ]
        .dropna()
        .unique()
        .tolist()
    )
)


# =========================================================
# 22. SAVE FINAL DATASET
# =========================================================

final_df.to_excel(

    OUTPUT,

    sheet_name="Final Dataset",

    index=False

)


# =========================================================
# 23. SUCCESS MESSAGE
# =========================================================

print("\n" + "=" * 65)

print(
    "KPI ENGINEERING COMPLETED SUCCESSFULLY"
)

print("=" * 65)

print(
    f"Created: {OUTPUT}"
)

print(
    "Missing/unavailable values are stored "
    "as blank/NaN"
)