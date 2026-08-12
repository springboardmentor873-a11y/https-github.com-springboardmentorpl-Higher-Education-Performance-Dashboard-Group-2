import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("CREATING RAW MERGED DATASET")
print("=" * 70)

qs = pd.read_csv(
    OUTPUT_DIR /
    "qs_cleaned_encoding_fixed.csv"
)

the = pd.read_csv(
    OUTPUT_DIR /
    "the_cleaned_encoding_fixed.csv"
)

matches = pd.read_csv(
    OUTPUT_DIR /
    "match_details_v2.csv"
)


print("\nQS shape:", qs.shape)
print("THE shape:", the.shape)
print("Matches:", matches.shape)


# ============================================================
# SELECT MATCHED QS/THE RECORDS
# ============================================================

match_map = matches[
    [
        "qs_index",
        "the_index",
        "match_type",
        "similarity",
        "country_match"
    ]
].copy()


match_map["qs_index"] = (
    match_map["qs_index"]
    .astype(int)
)

match_map["the_index"] = (
    match_map["the_index"]
    .astype(int)
)


# ============================================================
# ADD MATCH INFORMATION TO QS
# ============================================================

qs = qs.copy()

qs["qs_index"] = qs.index


qs = qs.merge(
    match_map,
    on="qs_index",
    how="left"
)


# ============================================================
# ADD THE DATA
# ============================================================

the = the.copy()

the["the_index"] = the.index


# Remove helper columns from THE
the_columns = [
    column
    for column in the.columns
    if column not in [
        "match_name",
        "match_country"
    ]
]


the_subset = the[
    the_columns
].copy()


# Rename THE columns
rename_the = {}

for column in the_subset.columns:

    if column != "the_index":

        rename_the[column] = (
            "the_" + column
        )


the_subset = the_subset.rename(
    columns=rename_the
)


# ============================================================
# MERGE QS + THE
# ============================================================

raw = qs.merge(
    the_subset,
    left_on="the_index",
    right_on="the_index",
    how="left"
)


# ============================================================
# CLEAN HELPER COLUMNS
# ============================================================

helper_columns = [
    "qs_index",
    "the_index",
    "match_name",
    "match_country"
]


raw = raw.drop(
    columns=[
        column
        for column in helper_columns
        if column in raw.columns
    ]
)


# ============================================================
# CREATE STANDARD SOURCE COLUMN
# ============================================================

def determine_source(row):

    if pd.notna(
        row.get("the_rank")
    ):

        return "QS + THE"

    return "QS only"


raw["data_source"] = raw.apply(
    determine_source,
    axis=1
)


# ============================================================
# REORDER IMPORTANT COLUMNS
# ============================================================

priority_columns = [
    "institution_name",
    "country_territory",
    "region",
    "2026_rank",
    "overall_score",
    "the_rank",
    "the_name",
    "the_country",
    "the_overall_score",
    "data_source",
    "match_type",
    "similarity",
    "country_match"
]


existing_priority = [
    column
    for column in priority_columns
    if column in raw.columns
]


remaining_columns = [
    column
    for column in raw.columns
    if column not in existing_priority
]


raw = raw[
    existing_priority +
    remaining_columns
]


# ============================================================
# SAVE
# ============================================================

output_file = (
    OUTPUT_DIR /
    "university_raw_data.csv"
)


raw.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("RAW DATASET CREATED")
print("=" * 70)

print(
    "Rows:",
    len(raw)
)

print(
    "Columns:",
    len(raw.columns)
)

print(
    "Matched QS + THE:",
    (
        raw["data_source"]
        == "QS + THE"
    ).sum()
)

print(
    "QS only:",
    (
        raw["data_source"]
        == "QS only"
    ).sum()
)

print(
    "\nMissing THE rank:",
    raw["the_rank"].isna().sum()
)

print(
    "\nCreated:"
)

print(
    output_file
)