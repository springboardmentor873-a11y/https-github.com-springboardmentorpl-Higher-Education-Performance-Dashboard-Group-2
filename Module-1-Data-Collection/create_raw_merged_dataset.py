import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

FINAL_MATCHED_FILE = (
    OUTPUT_DIR / "university_matched_data_final.csv"
)

RAW_MERGED_OUTPUT = (
    OUTPUT_DIR / "university_raw_merged_data.csv"
)


# ============================================================
# LOAD FINAL APPROVED MATCHES
# ============================================================

print("=" * 70)
print("CREATING RAW MERGED DATASET")
print("=" * 70)

df = pd.read_csv(
    FINAL_MATCHED_FILE,
    encoding="utf-8-sig"
)

print("\nLoaded final matched dataset")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATING APPROVED MATCHES")
print("=" * 70)

required_columns = [
    "qs_Institution Name",
    "qs_Country/Territory",
    "the_Name",
    "the_Country",
    "match_type",
    "match_similarity",
    "country_match"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise KeyError(
        f"Required columns missing: {missing_columns}"
    )


# ============================================================
# CHECK ROW COUNT
# ============================================================

if len(df) != 1008:
    raise ValueError(
        f"Expected 1008 approved matches, "
        f"but found {len(df)}."
    )


# ============================================================
# CHECK DUPLICATES
# ============================================================

duplicate_qs = (
    df["qs_Institution Name"]
    .duplicated()
    .sum()
)

duplicate_the = (
    df["the_Name"]
    .duplicated()
    .sum()
)

print(
    "\nDuplicate QS universities:",
    duplicate_qs
)

print(
    "Duplicate THE universities:",
    duplicate_the
)


if duplicate_qs != 0:
    raise ValueError(
        "Duplicate QS universities detected."
    )

if duplicate_the != 0:
    raise ValueError(
        "Duplicate THE universities detected."
    )


# ============================================================
# COUNTRY VALIDATION
# ============================================================

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


if country_mismatches != 0:
    raise ValueError(
        "Country mismatches detected."
    )


# ============================================================
# MISSING UNIVERSITY NAMES
# ============================================================

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


if missing_qs_names != 0:
    raise ValueError(
        "Missing QS university names detected."
    )

if missing_the_names != 0:
    raise ValueError(
        "Missing THE university names detected."
    )


# ============================================================
# MATCH TYPE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MATCH TYPE SUMMARY")
print("=" * 70)

print(
    df["match_type"]
    .value_counts()
)


# ============================================================
# CREATE RAW MERGED DATASET
# ============================================================

print("\n" + "=" * 70)
print("SAVING RAW MERGED DATASET")
print("=" * 70)

df.to_csv(
    RAW_MERGED_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# FINAL CHECK
# ============================================================

check_df = pd.read_csv(
    RAW_MERGED_OUTPUT,
    encoding="utf-8-sig"
)

print("\nSaved successfully.")

print(
    "Raw merged rows:",
    len(check_df)
)

print(
    "Raw merged columns:",
    len(check_df.columns)
)

print(
    "Output:",
    RAW_MERGED_OUTPUT
)


# ============================================================
# FINAL STATUS
# ============================================================

if len(check_df) == 1008:

    print("\n" + "=" * 70)
    print("RAW MERGED DATASET CREATED SUCCESSFULLY")
    print("=" * 70)

    print("\nRows:", len(check_df))
    print("Columns:", len(check_df.columns))

else:

    raise ValueError(
        "Final row count changed after saving."
    )