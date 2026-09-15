import pandas as pd
import numpy as np
import re
import unicodedata
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"


# ============================================================
# LOAD RAW DATA
# ============================================================

print("=" * 70)
print("FINAL DATA CLEANING")
print("=" * 70)

input_file = OUTPUT_DIR / "university_raw_data.csv"

df = pd.read_csv(
    input_file,
    encoding="utf-8-sig"
)

print("\nInput shape:", df.shape)


# ============================================================
# 1. FIX TEXT ENCODING / MOJIBAKE
# ============================================================

def fix_encoding(value):

    if pd.isna(value):
        return value

    value = str(value)

    # Try repeatedly because some values can be
    # encoded incorrectly more than once.
    for _ in range(2):

        if any(
            bad in value
            for bad in [
                "Ã",
                "Â",
                "Å",
                "â",
                "ð",
                "Ä"
            ]
        ):

            try:

                value = value.encode(
                    "latin1"
                ).decode(
                    "utf-8"
                )

            except (
                UnicodeEncodeError,
                UnicodeDecodeError
            ):
                break

    return value


# Apply only to object/string columns

text_columns = df.select_dtypes(
    include=["object"]
).columns


for column in text_columns:

    df[column] = df[
        column
    ].apply(fix_encoding)


# ============================================================
# 2. STANDARDIZE UNIVERSITY NAME
# ============================================================

def clean_university_name(name):

    if pd.isna(name):
        return np.nan

    name = str(name).strip()

    # Normalize spaces
    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name


df["university_name"] = df[
    "institution_name"
].apply(
    clean_university_name
)


# ============================================================
# 3. STANDARDIZE COUNTRY
# ============================================================

def standardize_country(country):

    if pd.isna(country):
        return np.nan

    country = str(country).strip()

    aliases = {

        "United States of America":
            "United States",

        "USA":
            "United States",

        "US":
            "United States",

        "United Kingdom":
            "United Kingdom",

        "UK":
            "United Kingdom",

        "Republic of Korea":
            "South Korea",

        "Korea, Republic of":
            "South Korea",

        "China (Mainland)":
            "China",

        "Hong Kong SAR, China":
            "Hong Kong",

        "Macao SAR, China":
            "Macau",

        "Russian Federation":
            "Russia",

        "UAE":
            "United Arab Emirates",

        "Czechia":
            "Czech Republic"
    }

    return aliases.get(
        country,
        country
    )


df["country"] = df[
    "country_territory"
].apply(
    standardize_country
)


# ============================================================
# 4. NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "2026_rank",
    "previous_rank",
    "overall_score",
    "the_rank",
    "the_overall_score",

    "the_student_population",
    "the_students_to_staff_ratio",
    "the_international_students",
    "the_female_to_male_ratio",

    "the_teaching",
    "the_research_environment",
    "the_research_quality",
    "the_industry_impact",
    "the_international_outlook"
]


# QS indicator scores/ranks
for column in df.columns:

    if column.endswith("_score") or column.endswith("_rank"):

        numeric_columns.append(
            column
        )


numeric_columns = list(
    set(numeric_columns)
)


for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# 5. NORMALIZE QS RANK
# ============================================================

# Ranking numbers: smaller rank = better.
#
# We use min-max normalization:
#
# normalized =
# 100 * (max_rank - rank)
# / (max_rank - min_rank)
#
# Rank 1 therefore gets the highest normalized score.

qs_rank_max = df[
    "2026_rank"
].max()

qs_rank_min = df[
    "2026_rank"
].min()


df["qs_rank_normalized"] = (
    100
    *
    (
        qs_rank_max
        -
        df["2026_rank"]
    )
    /
    (
        qs_rank_max
        -
        qs_rank_min
    )
)


# ============================================================
# 6. NORMALIZE THE RANK
# ============================================================

the_rank_max = df[
    "the_rank"
].max()

the_rank_min = df[
    "the_rank"
].min()


df["the_rank_normalized"] = (
    100
    *
    (
        the_rank_max
        -
        df["the_rank"]
    )
    /
    (
        the_rank_max
        -
        the_rank_min
    )
)


# ============================================================
# 7. NORMALIZE OVERALL SCORES
# ============================================================

def min_max_normalize(series):

    minimum = series.min()
    maximum = series.max()

    if pd.isna(minimum) or pd.isna(maximum):

        return series

    if maximum == minimum:

        return pd.Series(
            100,
            index=series.index
        )

    return (
        100
        *
        (series - minimum)
        /
        (maximum - minimum)
    )


df["qs_score_normalized"] = (
    min_max_normalize(
        df["overall_score"]
    )
)


df["the_score_normalized"] = (
    min_max_normalize(
        df["the_overall_score"]
    )
)


# ============================================================
# 8. COMBINED RANKING SCORE
# ============================================================

# Average only available ranking scores.
#
# If only QS is available:
# combined score = QS normalized score
#
# If only THE is available:
# combined score = THE normalized score
#
# If both are available:
# combined score = average of both.

df["combined_ranking_score"] = (
    df[
        [
            "qs_rank_normalized",
            "the_rank_normalized"
        ]
    ].mean(
        axis=1,
        skipna=True
    )
)


# ============================================================
# 9. MATCH STATUS
# ============================================================

df["match_status"] = np.where(
    df["the_rank"].notna(),
    "Matched",
    "QS Only"
)


# ============================================================
# 10. REMOVE UNNECESSARY COLUMNS
# ============================================================

columns_to_remove = [

    "institution_name",

    "country_territory",

    "qs_index",

    "the_index",

    "match_name",

    "match_country",

    "country_match",

    "similarity",

    "university_key"
]


df = df.drop(
    columns=[
        column
        for column in columns_to_remove
        if column in df.columns
    ]
)


# ============================================================
# 11. REMOVE DUPLICATES
# ============================================================

before_duplicates = len(df)

df = df.drop_duplicates(
    subset=[
        "university_name",
        "country"
    ]
)

after_duplicates = len(df)

duplicates_removed = (
    before_duplicates
    -
    after_duplicates
)


# ============================================================
# 12. REORDER IMPORTANT COLUMNS
# ============================================================

priority_columns = [

    "university_name",
    "country",
    "region",

    "2026_rank",
    "overall_score",

    "the_rank",
    "the_name",
    "the_country",
    "the_overall_score",

    "qs_rank_normalized",
    "the_rank_normalized",

    "qs_score_normalized",
    "the_score_normalized",

    "combined_ranking_score",

    "match_status"
]


priority_columns = [
    column
    for column in priority_columns
    if column in df.columns
]


remaining_columns = [
    column
    for column in df.columns
    if column not in priority_columns
]


df = df[
    priority_columns
    +
    remaining_columns
]


# ============================================================
# 13. MISSING VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)


missing_count = df.isna().sum()

missing_percentage = (
    df.isna().mean()
    * 100
)


missing_report = pd.DataFrame({

    "missing_count":
        missing_count,

    "missing_percentage":
        missing_percentage

})


missing_report = missing_report[
    missing_report[
        "missing_count"
    ] > 0
].sort_values(
    "missing_percentage",
    ascending=False
)


print(
    missing_report.to_string()
)


# ============================================================
# 14. OVERALL COMPLETENESS
# ============================================================

total_cells = (
    df.shape[0]
    *
    df.shape[1]
)

missing_cells = (
    df.isna().sum().sum()
)

completeness = (
    1
    -
    missing_cells
    /
    total_cells
) * 100

missing_percentage_overall = (
    missing_cells
    /
    total_cells
) * 100


print("\n" + "=" * 70)
print("DATASET QUALITY")
print("=" * 70)

print(
    f"Rows: {df.shape[0]}"
)

print(
    f"Columns: {df.shape[1]}"
)

print(
    f"Total cells: {total_cells}"
)

print(
    f"Missing cells: {missing_cells}"
)

print(
    f"Overall completeness: {completeness:.2f}%"
)

print(
    f"Overall missing percentage: "
    f"{missing_percentage_overall:.2f}%"
)


# ============================================================
# 15. DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE CHECK")
print("=" * 70)

print(
    "Duplicates removed:",
    duplicates_removed
)

print(
    "Remaining duplicate rows:",
    df.duplicated().sum()
)


# ============================================================
# 16. SAVE FINAL DATASET
# ============================================================

output_file = (
    OUTPUT_DIR /
    "university_cleaned.csv"
)


df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 17. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL CLEANING COMPLETED")
print("=" * 70)

print(
    "Final shape:",
    df.shape
)

print(
    "Created:"
)

print(
    output_file
)

print("\nData source distribution:")

print(
    df["match_status"]
    .value_counts()
)


# ============================================================
# 18. TARGET CHECK
# ============================================================

print("\n" + "=" * 70)
print("INTERNSHIP QUALITY TARGET")
print("=" * 70)

if completeness >= 95:

    print(
        "PASS: Completeness is above 95%."
    )

else:

    print(
        "WARNING: Completeness is below 95%."
    )


if missing_percentage_overall < 2:

    print(
        "PASS: Overall missing values are below 2%."
    )

else:

    print(
        "WARNING: Overall missing values exceed 2%."
    )