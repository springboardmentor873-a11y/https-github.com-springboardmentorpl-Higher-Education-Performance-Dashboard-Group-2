import pandas as pd
import numpy as np
import re
import unicodedata
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

INPUT_FILE = (
    OUTPUT_DIR / "university_raw_merged_data.csv"
)

OUTPUT_FILE = (
    OUTPUT_DIR / "university_cleaned_merged_data.csv"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def fix_mojibake(value):
    """
    Fix common UTF-8/Latin-1 encoding corruption.
    """

    if pd.isna(value):
        return value

    value = str(value)

    # Try repeated correction where necessary
    for _ in range(2):

        if not any(
            x in value
            for x in ["Ã", "Â", "â", "Å", "Ä", "Æ"]
        ):
            break

        try:

            fixed = (
                value
                .encode("latin1")
                .decode("utf-8")
            )

            value = fixed

        except (
            UnicodeEncodeError,
            UnicodeDecodeError
        ):
            break

    return value


def clean_text(value):
    """
    Clean whitespace while preserving Unicode.
    """

    if pd.isna(value):
        return value

    value = fix_mojibake(value)

    value = str(value).strip()

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value


def normalize_country(value):
    """
    Standardize country names.
    """

    if pd.isna(value):
        return value

    value = clean_text(value)

    replacements = {

        "United States":
            "United States of America",

        "United States of America":
            "United States of America",

        "China":
            "China (Mainland)",

        "China (Mainland)":
            "China (Mainland)",

        "South Korea":
            "Republic of Korea",

        "Korea, Republic of":
            "Republic of Korea",

        "Republic of Korea":
            "Republic of Korea",

        "Russia":
            "Russian Federation",

        "Russian Federation":
            "Russian Federation",

        "Czech Republic":
            "Czechia",

        "Czechia":
            "Czechia",
    }

    return replacements.get(
        value,
        value
    )


def parse_numeric(value):
    """
    Safely convert numeric values.
    """

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if value in {
        "",
        "-",
        "—",
        "nan",
        "NaN",
        "None"
    }:
        return np.nan

    value = value.replace(
        ",",
        ""
    )

    try:
        return float(value)

    except (
        ValueError,
        TypeError
    ):
        return np.nan


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("FINAL CLEANING OF MERGED DATASET")
print("=" * 70)

df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8-sig"
)

print(
    f"\nInput shape: {df.shape}"
)


# ============================================================
# PRESERVE ORIGINAL UNIVERSITY NAMES
# ============================================================

print("\nPreserving original university names...")

df["qs_Institution Name_original"] = (
    df["qs_Institution Name"]
)

df["the_Name_original"] = (
    df["the_Name"]
)


# ============================================================
# CLEAN TEXT COLUMNS
# ============================================================

print("\nCleaning text columns...")

text_columns = df.select_dtypes(
    include=[
        "object",
        "string"
    ]
).columns

for col in text_columns:

    df[col] = df[col].map(
        clean_text
    )


# ============================================================
# STANDARDIZE COUNTRIES
# ============================================================

print("\nStandardizing countries...")

country_columns = [
    "qs_Country/Territory",
    "the_Country"
]

for col in country_columns:

    if col in df.columns:

        df[col] = df[col].map(
            normalize_country
        )


# ============================================================
# NUMERIC COLUMNS
# ============================================================

print("\nProcessing numeric columns...")


numeric_columns = [

    # QS
    "qs_2026 Rank",
    "qs_Previous Rank",

    "qs_AR SCORE",
    "qs_AR RANK",

    "qs_ER SCORE",
    "qs_ER RANK",

    "qs_FSR SCORE",
    "qs_FSR RANK",

    "qs_CPF SCORE",
    "qs_CPF RANK",

    "qs_IFR SCORE",
    "qs_IFR RANK",

    "qs_ISR SCORE",
    "qs_ISR RANK",

    "qs_ISD SCORE",
    "qs_ISD RANK",

    "qs_IRN SCORE",
    "qs_IRN RANK",

    "qs_EO SCORE",
    "qs_EO RANK",

    "qs_SUS SCORE",
    "qs_SUS RANK",

    "qs_2026_rank",

    "qs_overall_score",

    # THE
    "the_Rank",
    "the_Student Population",
    "the_Students to Staff Ratio",
    "the_Overall Score",
    "the_Teaching",
    "the_Research Environment",
    "the_Research Quality",
    "the_Industry Impact",
    "the_International Outlook",
    "the_Year",

    "the_rank",

    "the_female_to_male_ratio_clean",

    # Matching
    "match_similarity"
]


for col in numeric_columns:

    if col in df.columns:

        df[col] = df[col].apply(
            parse_numeric
        )


# ============================================================
# SCORE AVAILABILITY FLAG
# ============================================================

if "qs_overall_score" in df.columns:

    df["qs_overall_score_available"] = (
        df["qs_overall_score"]
        .notna()
    )


# ============================================================
# CLEAN FEMALE/Male RATIO
# ============================================================

print("\nValidating female-to-male ratio...")

if "the_female_to_male_ratio_clean" in df.columns:

    ratio = df[
        "the_female_to_male_ratio_clean"
    ]

    invalid_ratio = (
        (ratio < 0)
        |
        (ratio > 100)
    )

    df.loc[
        invalid_ratio,
        "the_female_to_male_ratio_clean"
    ] = np.nan


# ============================================================
# RECREATE UNIVERSITY KEYS
# ============================================================

print("\nCreating standardized university keys...")


def create_university_key(value):

    if pd.isna(value):
        return ""

    value = str(value).lower()

    value = unicodedata.normalize(
        "NFKD",
        value
    )

    value = "".join(
        c
        for c in value
        if not unicodedata.combining(c)
    )

    value = re.sub(
        r"\([^)]*\)",
        " ",
        value
    )

    value = value.replace(
        "&",
        "and"
    )

    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


df["qs_university_key_clean"] = (
    df["qs_Institution Name"]
    .apply(create_university_key)
)

df["the_university_key_clean"] = (
    df["the_Name"]
    .apply(create_university_key)
)


# ============================================================
# REMOVE UNNECESSARY MATCHING HELPER COLUMNS
# ============================================================

drop_columns = [
    "qs_match_name",
    "qs_match_country",
    "the_match_name",
    "the_match_country"
]

existing_drop_columns = [
    col
    for col in drop_columns
    if col in df.columns
]

if existing_drop_columns:

    df.drop(
        columns=existing_drop_columns,
        inplace=True
    )


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATASET VALIDATION")
print("=" * 70)


print(
    "\nRows:",
    len(df)
)

print(
    "Columns:",
    len(df.columns)
)


# ------------------------------------------------------------
# Duplicate QS
# ------------------------------------------------------------

duplicate_qs = (
    df["qs_Institution Name"]
    .duplicated()
    .sum()
)

print(
    "Duplicate QS universities:",
    duplicate_qs
)


# ------------------------------------------------------------
# Duplicate THE
# ------------------------------------------------------------

duplicate_the = (
    df["the_Name"]
    .duplicated()
    .sum()
)

print(
    "Duplicate THE universities:",
    duplicate_the
)


# ------------------------------------------------------------
# Country mismatches
# ------------------------------------------------------------

country_match = (
    df["qs_Country/Territory"]
    .astype(str)
    .str.strip()
    ==
    df["the_Country"]
    .astype(str)
    .str.strip()
)

country_mismatches = (
    ~country_match
).sum()

print(
    "Country mismatches:",
    country_mismatches
)


# ------------------------------------------------------------
# Missing names
# ------------------------------------------------------------

missing_qs_names = (
    df["qs_Institution Name"]
    .isna()
    .sum()
)

missing_the_names = (
    df["the_Name"]
    .isna()
    .sum()
)

print(
    "Missing QS names:",
    missing_qs_names
)

print(
    "Missing THE names:",
    missing_the_names
)


# ============================================================
# MISSING VALUE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE SUMMARY")
print("=" * 70)

missing_summary = (
    df.isna()
    .sum()
    .sort_values(
        ascending=False
    )
)

print(
    missing_summary[
        missing_summary > 0
    ].to_string()
)


# ============================================================
# SAVE
# ============================================================

print("\n" + "=" * 70)
print("SAVING CLEANED DATASET")
print("=" * 70)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# RELOAD CHECK
# ============================================================

check_df = pd.read_csv(
    OUTPUT_FILE,
    encoding="utf-8-sig"
)

print(
    "\nSaved dataset shape:",
    check_df.shape
)

print(
    "Output:",
    OUTPUT_FILE
)


# ============================================================
# FINAL STATUS
# ============================================================

if (
    len(check_df) == 1008
    and
    duplicate_qs == 0
    and
    duplicate_the == 0
    and
    country_mismatches == 0
    and
    missing_qs_names == 0
    and
    missing_the_names == 0
):

    print("\n" + "=" * 70)
    print("FINAL CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        "\nDashboard-ready dataset created:"
    )

    print(
        OUTPUT_FILE
    )

else:

    print("\n" + "=" * 70)
    print("WARNING - VALIDATION ISSUES FOUND")
    print("=" * 70)

    print(
        "\nReview the validation output before proceeding."
    )
    