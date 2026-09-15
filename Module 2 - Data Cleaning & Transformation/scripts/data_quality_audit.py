import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

INPUT_FILE = OUTPUT_DIR / "university_cleaned_merged_data.csv"
REPORT_FILE = OUTPUT_DIR / "data_quality_audit_report.txt"


# ============================================================
# HELPER
# ============================================================

def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# START
# ============================================================

print("=" * 70)
print("DATA QUALITY AUDIT")
print("=" * 70)

print("\nScript location:")
print(Path(__file__).resolve())

print("\nInput file:")
print(INPUT_FILE)

print("\nChecking input file...")


# ============================================================
# CHECK FILE
# ============================================================

if not INPUT_FILE.exists():
    print("\nERROR: Input dataset was not found.")
    print(f"Expected location: {INPUT_FILE}")
    raise FileNotFoundError(INPUT_FILE)

print("Input file found successfully.")


# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8-sig"
)

print("Dataset loaded successfully.")


# ============================================================
# BASIC INFORMATION
# ============================================================

print_section("1. BASIC DATASET INFORMATION")

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print("\nColumn names:")
for i, col in enumerate(df.columns, start=1):
    print(f"{i:3}. {col}")


# ============================================================
# DATA TYPES
# ============================================================

print_section("2. DATA TYPES")

dtype_summary = pd.DataFrame({
    "column": df.columns,
    "dtype": df.dtypes.astype(str).values,
    "missing": df.isna().sum().values,
    "missing_percent": (
        df.isna().mean().values * 100
    ).round(2)
})

print(dtype_summary.to_string(index=False))


# ============================================================
# DUPLICATE VALIDATION
# ============================================================

print_section("3. DUPLICATE VALIDATION")

if "qs_Institution Name" in df.columns:

    print(
        "Duplicate QS universities:",
        df["qs_Institution Name"].duplicated().sum()
    )

if "the_Name" in df.columns:

    print(
        "Duplicate THE universities:",
        df["the_Name"].duplicated().sum()
    )

print(
    "Duplicate complete rows:",
    df.duplicated().sum()
)


# ============================================================
# UNIVERSITY NAME VALIDATION
# ============================================================

print_section("4. UNIVERSITY NAME VALIDATION")

if "qs_Institution Name" in df.columns:

    print(
        "Missing QS university names:",
        df["qs_Institution Name"].isna().sum()
    )

if "the_Name" in df.columns:

    print(
        "Missing THE university names:",
        df["the_Name"].isna().sum()
    )


# ============================================================
# COUNTRY VALIDATION
# ============================================================

print_section("5. COUNTRY VALIDATION")

if (
    "qs_Country/Territory" in df.columns
    and "the_Country" in df.columns
):

    qs_country = (
        df["qs_Country/Territory"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    the_country = (
        df["the_Country"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    country_mismatch = (
        qs_country != the_country
    )

    print(
        "Country mismatches:",
        country_mismatch.sum()
    )

    if country_mismatch.sum() > 0:

        print("\nCountry mismatch examples:")

        print(
            df.loc[
                country_mismatch,
                [
                    "qs_Institution Name",
                    "the_Name",
                    "qs_Country/Territory",
                    "the_Country"
                ]
            ]
            .head(20)
            .to_string(index=False)
        )


# ============================================================
# MATCH QUALITY
# ============================================================

print_section("6. MATCH QUALITY")

if "match_type" in df.columns:

    print(
        df["match_type"]
        .value_counts(dropna=False)
        .to_string()
    )

if "match_similarity" in df.columns:

    similarity = pd.to_numeric(
        df["match_similarity"],
        errors="coerce"
    )

    print("\nSimilarity statistics:")

    print(
        similarity.describe()
        .to_string()
    )

    print(
        "\nSimilarity below 90:",
        (similarity < 90).sum()
    )

    print(
        "Similarity below 92:",
        (similarity < 92).sum()
    )

    print(
        "Similarity equal to 100:",
        (similarity == 100).sum()
    )


# ============================================================
# QS RANK VALIDATION
# ============================================================

print_section("7. QS RANK VALIDATION")

qs_rank_columns = [
    "qs_2026_rank",
    "qs_2026_rank_display",
    "qs_2026_rank_original"
]

for col in qs_rank_columns:

    if col in df.columns:

        print(f"\n{col}")

        if col == "qs_2026_rank":

            values = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            print("Missing:", values.isna().sum())

            if values.notna().any():

                print("Minimum:", values.min())
                print("Maximum:", values.max())

                print(
                    "Values <= 0:",
                    (values <= 0).sum()
                )


# ============================================================
# QS OVERALL SCORE
# ============================================================

print_section("8. QS OVERALL SCORE")

if "qs_overall_score" in df.columns:

    qs_score = pd.to_numeric(
        df["qs_overall_score"],
        errors="coerce"
    )

    print("Available:", qs_score.notna().sum())
    print("Missing:", qs_score.isna().sum())

    if qs_score.notna().any():

        print("Minimum:", qs_score.min())
        print("Maximum:", qs_score.max())

        print(
            "Below 0:",
            (qs_score < 0).sum()
        )

        print(
            "Above 100:",
            (qs_score > 100).sum()
        )

        print("\nScore statistics:")

        print(
            qs_score.describe()
            .to_string()
        )


# ============================================================
# QS SCORE AVAILABILITY
# ============================================================

print_section("9. QS SCORE AVAILABILITY")

if "qs_overall_score_available" in df.columns:

    print(
        df["qs_overall_score_available"]
        .value_counts(dropna=False)
        .to_string()
    )


# ============================================================
# THE OVERALL SCORE
# ============================================================

print_section("10. THE OVERALL SCORE")

if "the_Overall Score" in df.columns:

    the_score = pd.to_numeric(
        df["the_Overall Score"],
        errors="coerce"
    )

    print("Available:", the_score.notna().sum())
    print("Missing:", the_score.isna().sum())

    if the_score.notna().any():

        print("Minimum:", the_score.min())
        print("Maximum:", the_score.max())

        print(
            "Below 0:",
            (the_score < 0).sum()
        )

        print(
            "Above 100:",
            (the_score > 100).sum()
        )

        print("\nScore statistics:")

        print(
            the_score.describe()
            .to_string()
        )


# ============================================================
# FEMALE / MALE RATIO
# ============================================================

print_section("11. FEMALE-TO-MALE RATIO")

ratio_columns = [
    "the_female_to_male_ratio_clean",
    "the_female_to_male_ratio_original",
    "the_Female to Male Ratio"
]

if "the_female_to_male_ratio_clean" in df.columns:

    ratio = pd.to_numeric(
        df["the_female_to_male_ratio_clean"],
        errors="coerce"
    )

    print(
        "Available:",
        ratio.notna().sum()
    )

    print(
        "Missing:",
        ratio.isna().sum()
    )

    if ratio.notna().any():

        print(
            "Minimum:",
            ratio.min()
        )

        print(
            "Maximum:",
            ratio.max()
        )

        print(
            "Below 0:",
            (ratio < 0).sum()
        )

        print(
            "Above 100:",
            (ratio > 100).sum()
        )

        print("\nRatio statistics:")

        print(
            ratio.describe()
            .to_string()
        )


# ============================================================
# STUDENT POPULATION
# ============================================================

print_section("12. STUDENT POPULATION")

if "the_Student Population" in df.columns:

    population = pd.to_numeric(
        df["the_Student Population"],
        errors="coerce"
    )

    print(
        "Available:",
        population.notna().sum()
    )

    print(
        "Missing:",
        population.isna().sum()
    )

    if population.notna().any():

        print(
            "Minimum:",
            population.min()
        )

        print(
            "Maximum:",
            population.max()
        )

        print(
            "Values below 0:",
            (population < 0).sum()
        )

        print("\nPopulation statistics:")

        print(
            population.describe()
            .to_string()
        )


# ============================================================
# STUDENT / STAFF RATIO
# ============================================================

print_section("13. STUDENT-TO-STAFF RATIO")

if "the_Students to Staff Ratio" in df.columns:

    ratio = pd.to_numeric(
        df["the_Students to Staff Ratio"],
        errors="coerce"
    )

    print(
        "Available:",
        ratio.notna().sum()
    )

    print(
        "Missing:",
        ratio.isna().sum()
    )

    if ratio.notna().any():

        print(
            "Minimum:",
            ratio.min()
        )

        print(
            "Maximum:",
            ratio.max()
        )

        print(
            "Values below 0:",
            (ratio < 0).sum()
        )


# ============================================================
# QS SCORE COLUMNS
# ============================================================

print_section("14. QS SCORE RANGE CHECK")

qs_score_columns = [
    col
    for col in df.columns
    if col.startswith("qs_")
    and "SCORE" in col.upper()
    and "overall" not in col.lower()
]

for col in qs_score_columns:

    values = pd.to_numeric(
        df[col],
        errors="coerce"
    )

    if values.notna().any():

        below_zero = (
            values < 0
        ).sum()

        above_100 = (
            values > 100
        ).sum()

        print(
            f"{col:30} "
            f"min={values.min():8.2f} "
            f"max={values.max():8.2f} "
            f"missing={values.isna().sum():4} "
            f"<0={below_zero:3} "
            f">100={above_100:3}"
        )


# ============================================================
# MISSING VALUE SUMMARY
# ============================================================

print_section("15. MISSING VALUE SUMMARY")

missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

missing = missing[
    missing > 0
]

if len(missing) == 0:

    print("No missing values.")

else:

    missing_summary = pd.DataFrame({
        "missing_count": missing,
        "missing_percent": (
            missing / len(df) * 100
        ).round(2)
    })

    print(
        missing_summary.to_string()
    )


# ============================================================
# FINAL STATUS
# ============================================================

print_section("16. FINAL AUDIT STATUS")

issues = []

# Duplicate checks
if "qs_Institution Name" in df.columns:
    if df["qs_Institution Name"].duplicated().sum() > 0:
        issues.append("Duplicate QS universities")

if "the_Name" in df.columns:
    if df["the_Name"].duplicated().sum() > 0:
        issues.append("Duplicate THE universities")

# Country check
if (
    "qs_Country/Territory" in df.columns
    and "the_Country" in df.columns
):

    if country_mismatch.sum() > 0:
        issues.append("Country mismatches")

# QS score check
if "qs_overall_score" in df.columns:

    if (
        (qs_score < 0).sum()
        + (qs_score > 100).sum()
    ) > 0:

        issues.append(
            "Invalid QS overall scores"
        )

# THE score check
if "the_Overall Score" in df.columns:

    if (
        (the_score < 0).sum()
        + (the_score > 100).sum()
    ) > 0:

        issues.append(
            "Invalid THE overall scores"
        )

# Female ratio
if "the_female_to_male_ratio_clean" in df.columns:

    if (
        (ratio < 0).sum()
        + (ratio > 100).sum()
    ) > 0:

        issues.append(
            "Invalid female-to-male ratios"
        )


if len(issues) == 0:

    print("PASS - No critical data-quality issues detected.")

else:

    print("REVIEW REQUIRED")

    print("\nIssues found:")

    for issue in issues:
        print(f"- {issue}")


# ============================================================
# SAVE AUDIT REPORT
# ============================================================

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "DATA QUALITY AUDIT COMPLETED\n"
    )

    f.write(
        f"Rows: {len(df)}\n"
    )

    f.write(
        f"Columns: {len(df.columns)}\n"
    )

    f.write(
        f"Duplicate rows: {df.duplicated().sum()}\n"
    )

    f.write(
        "\nMissing values:\n"
    )

    f.write(
        missing_summary.to_string()
        if len(missing) > 0
        else "None"
    )

    f.write(
        "\n\nFinal status:\n"
    )

    if len(issues) == 0:
        f.write(
            "PASS - No critical data-quality issues detected.\n"
        )
    else:
        f.write(
            "REVIEW REQUIRED\n"
        )

        for issue in issues:
            f.write(
                f"- {issue}\n"
            )


print("\n" + "=" * 70)
print("AUDIT COMPLETED")
print("=" * 70)

print("\nAudit report created:")
print(REPORT_FILE)