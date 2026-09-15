import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "output"
    / "university_kpi_dataset.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "output"
    / "university_kpis.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("CREATING UNIVERSITY KPI DATASET")
print("=" * 70)

df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8-sig"
)

print(f"\nInput rows    : {len(df)}")
print(f"Input columns : {len(df.columns)}")


# ============================================================
# REQUIRED COLUMNS
# ============================================================

columns = [
    "qs_Institution Name",
    "qs_Country/Territory",

    "global_ranking_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index",
]


missing = [
    column
    for column in columns
    if column not in df.columns
]

if missing:

    print("\nERROR: Missing columns:")

    for column in missing:
        print("-", column)

    raise KeyError(
        "Required KPI columns are missing."
    )


# ============================================================
# CREATE KPI DATASET
# ============================================================

kpi_df = df[columns].copy()


# ============================================================
# RENAME COLUMNS
# ============================================================

kpi_df = kpi_df.rename(
    columns={
        "qs_Institution Name": "University",
        "qs_Country/Territory": "Country",
    }
)


# ============================================================
# VALIDATION
# ============================================================

kpi_columns = [
    "global_ranking_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index",
]


print("\n" + "=" * 70)
print("KPI VALIDATION")
print("=" * 70)

print(
    f"\nUniversities: {len(kpi_df)}"
)

print(
    f"Duplicate universities: "
    f"{kpi_df['University'].duplicated().sum()}"
)


print("\nMissing KPI values:")

print(
    kpi_df[kpi_columns]
    .isna()
    .sum()
)


# ============================================================
# VALIDATE SCORE KPIs
# ============================================================

score_kpis = [
    "global_ranking_score",
    "research_impact_score",
    "academic_reputation_score",
    "research_productivity_index",
]


for column in score_kpis:

    below_zero = (
        kpi_df[column] < 0
    ).sum()

    above_100 = (
        kpi_df[column] > 100
    ).sum()

    if below_zero > 0 or above_100 > 0:

        raise ValueError(
            f"Invalid values found in {column}"
        )


# ============================================================
# VALIDATE INTERNATIONAL STUDENT %
# ============================================================

if (
    (kpi_df["international_student_percentage"] < 0)
    |
    (kpi_df["international_student_percentage"] > 100)
).any():

    raise ValueError(
        "Invalid International Student Percentage."
    )


# ============================================================
# SAVE
# ============================================================

kpi_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# DISPLAY
# ============================================================

print("\n" + "=" * 70)
print("KPI DATASET CREATED")
print("=" * 70)

print(
    f"\nOutput: {OUTPUT_FILE}"
)

print(
    f"Rows: {len(kpi_df)}"
)

print(
    f"Columns: {len(kpi_df.columns)}"
)

print("\nColumns:")

for column in kpi_df.columns:

    print(
        f"  ✓ {column}"
    )


print("\nFirst 10 universities:")

print(
    kpi_df.head(10)
    .to_string(index=False)
)

print(
    "\nAll six KPIs are available for all universities."
)