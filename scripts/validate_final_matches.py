import pandas as pd
from pathlib import Path


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

FINAL_FILE = OUTPUT_DIR / "university_matched_data_final.csv"


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("FINAL MATCH VALIDATION")
print("=" * 70)

df = pd.read_csv(
    FINAL_FILE,
    encoding="utf-8-sig"
)

print(f"\nFinal dataset shape: {df.shape}")


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("BASIC VALIDATION")
print("=" * 70)

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# DUPLICATES
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE VALIDATION")
print("=" * 70)

duplicate_qs = df[
    df["qs_Institution Name"].duplicated(keep=False)
]

duplicate_the = df[
    df["the_Name"].duplicated(keep=False)
]

print(
    "Duplicate QS universities:",
    df["qs_Institution Name"].duplicated().sum()
)

print(
    "Duplicate THE universities:",
    df["the_Name"].duplicated().sum()
)


if not duplicate_qs.empty:

    print("\nDuplicate QS universities:")
    print(
        duplicate_qs[
            [
                "qs_Institution Name",
                "the_Name"
            ]
        ].to_string(index=False)
    )


if not duplicate_the.empty:

    print("\nDuplicate THE universities:")
    print(
        duplicate_the[
            [
                "qs_Institution Name",
                "the_Name"
            ]
        ].to_string(index=False)
    )


# ============================================================
# COUNTRY VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("COUNTRY VALIDATION")
print("=" * 70)

country_mismatch = (
    df["qs_Country/Territory"].astype(str).str.strip()
    !=
    df["the_Country"].astype(str).str.strip()
)

print(
    "Country mismatches:",
    country_mismatch.sum()
)

if country_mismatch.sum() > 0:

    print("\nCountry mismatches:")
    print(
        df.loc[
            country_mismatch,
            [
                "qs_Institution Name",
                "the_Name",
                "qs_Country/Territory",
                "the_Country"
            ]
        ].to_string(index=False)
    )


# ============================================================
# MISSING UNIVERSITY NAMES
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE VALIDATION")
print("=" * 70)

print(
    "Missing QS university names:",
    df["qs_Institution Name"].isna().sum()
)

print(
    "Missing THE university names:",
    df["the_Name"].isna().sum()
)


# ============================================================
# MATCH TYPE
# ============================================================

print("\n" + "=" * 70)
print("MATCH TYPE SUMMARY")
print("=" * 70)

print(
    df["match_type"].value_counts()
)


# ============================================================
# SIMILARITY
# ============================================================

print("\n" + "=" * 70)
print("SIMILARITY SUMMARY")
print("=" * 70)

print(
    df["match_similarity"].describe()
)


# ============================================================
# LOW SIMILARITY MATCHES
# ============================================================

print("\n" + "=" * 70)
print("LOWEST SIMILARITY MATCHES")
print("=" * 70)

low_similarity = (
    df.sort_values(
        "match_similarity"
    )
    .head(20)
)

print(
    low_similarity[
        [
            "qs_Institution Name",
            "the_Name",
            "qs_Country/Territory",
            "the_Country",
            "match_type",
            "match_similarity"
        ]
    ].to_string(index=False)
)


# ============================================================
# SOUTH ALABAMA SAFETY CHECK
# ============================================================

print("\n" + "=" * 70)
print("FALSE-POSITIVE SAFETY CHECK")
print("=" * 70)

south_alabama = df[
    df["qs_Institution Name"]
    .astype(str)
    .str.contains(
        "South Alabama",
        case=False,
        na=False
    )
]

print(
    south_alabama[
        [
            "qs_Institution Name",
            "the_Name",
            "match_type",
            "match_similarity"
        ]
    ].to_string(index=False)
)


# ============================================================
# FINAL PASS/FAIL
# ============================================================

duplicate_qs_count = (
    df["qs_Institution Name"].duplicated().sum()
)

duplicate_the_count = (
    df["the_Name"].duplicated().sum()
)

country_mismatch_count = (
    country_mismatch.sum()
)

missing_qs_count = (
    df["qs_Institution Name"].isna().sum()
)

missing_the_count = (
    df["the_Name"].isna().sum()
)


print("\n" + "=" * 70)
print("FINAL VALIDATION RESULT")
print("=" * 70)


if (
    duplicate_qs_count == 0
    and
    duplicate_the_count == 0
    and
    country_mismatch_count == 0
    and
    missing_qs_count == 0
    and
    missing_the_count == 0
):

    print("\nPASS - FINAL MATCHED DATASET IS VALID")
    print("\nSafe to proceed to raw merged dataset creation.")

else:

    print("\nFAIL - VALIDATION ISSUES FOUND")
    print("\nDo NOT create the merged dataset yet.")


print("\nFinal rows:", len(df))
print("=" * 70)