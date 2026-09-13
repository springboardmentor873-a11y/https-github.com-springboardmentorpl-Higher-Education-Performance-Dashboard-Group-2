import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "output"
    / "university_cleaned_merged_data.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "output"
    / "university_kpi_dataset.csv"
)

SUMMARY_FILE = (
    BASE_DIR
    / "output"
    / "kpi_summary.csv"
)


# ============================================================
# SETTINGS
# ============================================================

print("=" * 70)
print("EDUCATION KPI ENGINEERING")
print("=" * 70)


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading cleaned merged dataset...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )

df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8-sig"
)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "qs_2026_rank",
    "qs_AR SCORE",
    "qs_CPF SCORE",
    "qs_IRN SCORE",
    "the_Rank",
    "the_Students to Staff Ratio",
    "the_International Students",
    "the_Research Environment",
    "the_Research Quality",
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print("\nMissing required columns:")

    for column in missing_columns:
        print(f"- {column}")

    raise KeyError(
        "Required KPI source columns are missing."
    )


print("\nAll required KPI source columns found.")


# ============================================================
# CONVERT NUMERIC FIELDS
# ============================================================

numeric_columns = [
    "qs_2026_rank",
    "qs_AR SCORE",
    "qs_CPF SCORE",
    "qs_IRN SCORE",
    "the_Rank",
    "the_Students to Staff Ratio",
    "the_International Students",
    "the_Research Environment",
    "the_Research Quality",
]


for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# KPI 1 — ACADEMIC REPUTATION SCORE
# ============================================================

print("\nCalculating Academic Reputation Score...")

df["academic_reputation_score"] = (
    df["qs_AR SCORE"]
)


# ============================================================
# KPI 2 — INTERNATIONAL STUDENT PERCENTAGE
# ============================================================

print("Calculating International Student Percentage...")

df["international_student_percentage"] = (
    df["the_International Students"] * 100
)


# ============================================================
# KPI 3 — FACULTY-TO-STUDENT RATIO
# ============================================================

print("Calculating Faculty-to-Student Ratio...")

df["faculty_to_student_ratio"] = np.where(
    df["the_Students to Staff Ratio"] > 0,
    1 / df["the_Students to Staff Ratio"],
    np.nan
)


# ============================================================
# KPI 4 — RESEARCH IMPACT SCORE
# ============================================================

print("Calculating Research Impact Score...")

research_impact_columns = [
    "qs_CPF SCORE",
    "qs_IRN SCORE",
    "the_Research Quality",
    "the_Research Environment",
]

df["research_impact_score"] = (
    df[research_impact_columns]
    .mean(axis=1)
)


# ============================================================
# KPI 5 — RESEARCH PRODUCTIVITY INDEX
# ============================================================

print("Calculating Research Productivity Index...")

df["research_productivity_index"] = (
    0.40 * df["qs_CPF SCORE"]
    + 0.20 * df["qs_IRN SCORE"]
    + 0.20 * df["the_Research Quality"]
    + 0.20 * df["the_Research Environment"]
)


# ============================================================
# KPI 6 — GLOBAL RANKING SCORE
# ============================================================

print("Calculating Global Ranking Score...")


# Rank percentile:
# rank 1 = strongest
# higher rank number = weaker

qs_rank_score = (
    1
    - (
        df["qs_2026_rank"] - 1
    )
    / (
        df["qs_2026_rank"].max() - 1
    )
) * 100


the_rank_score = (
    1
    - (
        df["the_Rank"] - 1
    )
    / (
        df["the_Rank"].max() - 1
    )
) * 100


df["global_ranking_score"] = (
    qs_rank_score + the_rank_score
) / 2


# ============================================================
# ROUND KPI VALUES
# ============================================================

kpi_columns = [
    "global_ranking_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index",
]


for column in kpi_columns:

    df[column] = df[column].round(2)


# ============================================================
# KPI VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("KPI VALIDATION")
print("=" * 70)


# ------------------------------------------------------------
# Score-based KPIs
# ------------------------------------------------------------

score_kpis = [
    "global_ranking_score",
    "research_impact_score",
    "academic_reputation_score",
    "research_productivity_index",
]


for column in score_kpis:

    below_zero = (
        df[column] < 0
    ).sum()

    above_100 = (
        df[column] > 100
    ).sum()

    missing = (
        df[column].isna()
    ).sum()

    print(
        f"\n{column}"
    )

    print(
        f"  Missing     : {missing}"
    )

    print(
        f"  Minimum     : {df[column].min()}"
    )

    print(
        f"  Maximum     : {df[column].max()}"
    )

    print(
        f"  Below 0     : {below_zero}"
    )

    print(
        f"  Above 100   : {above_100}"
    )

    if below_zero > 0 or above_100 > 0:

        raise ValueError(
            f"Invalid range detected in {column}"
        )


# ------------------------------------------------------------
# International student percentage
# ------------------------------------------------------------

international_missing = (
    df["international_student_percentage"]
    .isna()
    .sum()
)

international_below_zero = (
    df["international_student_percentage"] < 0
).sum()

international_above_100 = (
    df["international_student_percentage"] > 100
).sum()


print(
    "\nInternational Student Percentage"
)

print(
    f"  Missing     : {international_missing}"
)

print(
    f"  Minimum     : "
    f"{df['international_student_percentage'].min()}"
)

print(
    f"  Maximum     : "
    f"{df['international_student_percentage'].max()}"
)

print(
    f"  Below 0     : {international_below_zero}"
)

print(
    f"  Above 100   : {international_above_100}"
)


if (
    international_below_zero > 0
    or international_above_100 > 0
):

    raise ValueError(
        "Invalid International Student Percentage."
    )


# ------------------------------------------------------------
# Faculty-to-student ratio
# ------------------------------------------------------------

ratio_missing = (
    df["faculty_to_student_ratio"]
    .isna()
    .sum()
)

ratio_invalid = (
    df["faculty_to_student_ratio"] <= 0
).sum()


print(
    "\nFaculty-to-Student Ratio"
)

print(
    f"  Missing     : {ratio_missing}"
)

print(
    f"  Minimum     : "
    f"{df['faculty_to_student_ratio'].min()}"
)

print(
    f"  Maximum     : "
    f"{df['faculty_to_student_ratio'].max()}"
)

print(
    f"  Invalid <=0 : {ratio_invalid}"
)


if ratio_invalid > 0:

    raise ValueError(
        "Invalid Faculty-to-Student Ratio detected."
    )


# ============================================================
# KPI SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CREATING KPI SUMMARY")
print("=" * 70)


summary_rows = []


for column in kpi_columns:

    summary_rows.append({

        "KPI": column,

        "Minimum": round(
            df[column].min(),
            2
        ),

        "Maximum": round(
            df[column].max(),
            2
        ),

        "Mean": round(
            df[column].mean(),
            2
        ),

        "Median": round(
            df[column].median(),
            2
        ),

        "Missing": int(
            df[column].isna().sum()
        ),

        "Available": int(
            df[column].notna().sum()
        ),

    })


summary_df = pd.DataFrame(
    summary_rows
)


# ============================================================
# SAVE KPI DATASET
# ============================================================

print("\n" + "=" * 70)
print("SAVING KPI DATASET")
print("=" * 70)


df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


summary_df.to_csv(
    SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"\nKPI dataset saved:"
)

print(
    OUTPUT_FILE
)


print(
    f"\nKPI summary saved:"
)

print(
    SUMMARY_FILE
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("KPI ENGINEERING COMPLETED")
print("=" * 70)

print(
    f"\nFinal rows    : {len(df)}"
)

print(
    f"Final columns : {len(df.columns)}"
)

print("\nCreated KPIs:")

for column in kpi_columns:

    print(
        f"  ✓ {column}"
    )


print("\nKPI engineering completed successfully.")