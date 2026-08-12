import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

QS_FILE = OUTPUT_DIR / "qs_cleaned_encoding_fixed.csv"
THE_FILE = OUTPUT_DIR / "the_cleaned_encoding_fixed.csv"

MATCH_DETAILS_FILE = OUTPUT_DIR / "match_details_v2.csv"
REVIEW_FILE = OUTPUT_DIR / "university_match_review.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("MATCH VALIDATION")
print("=" * 70)

qs = pd.read_csv(
    QS_FILE,
    encoding="utf-8-sig"
)

the = pd.read_csv(
    THE_FILE,
    encoding="utf-8-sig"
)

matches = pd.read_csv(
    MATCH_DETAILS_FILE,
    encoding="utf-8-sig"
)


print(f"Total matches: {len(matches)}")


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_match_columns = [
    "qs_index",
    "the_index",
    "qs_university",
    "the_university",
    "qs_country",
    "the_country",
    "match_type",
    "similarity",
    "country_match"
]

missing = [
    col
    for col in required_match_columns
    if col not in matches.columns
]

if missing:
    print("\nERROR: Missing columns in match_details_v2.csv:")
    print(missing)
    print("\nAvailable columns:")
    print(matches.columns.tolist())
    raise KeyError(
        f"Missing match columns: {missing}"
    )


# ============================================================
# MATCH TYPE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MATCH TYPE SUMMARY")
print("=" * 70)

print(
    matches["match_type"].value_counts()
)


# ============================================================
# COUNTRY VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("COUNTRY VALIDATION")
print("=" * 70)


# Use the country values already recorded
# in match_details_v2.csv.

matches["country_match"] = (
    matches["qs_country"].fillna("").astype(str).str.strip()
    ==
    matches["the_country"].fillna("").astype(str).str.strip()
)

print(
    matches["country_match"].value_counts()
)

different_country_count = (
    (~matches["country_match"]).sum()
)

print(
    f"\nMatches with different countries: "
    f"{different_country_count}"
)


# ============================================================
# SHOW COUNTRY MISMATCHES
# ============================================================

if different_country_count > 0:

    print("\n" + "=" * 70)
    print("COUNTRY MISMATCHES")
    print("=" * 70)

    mismatches = matches[
        ~matches["country_match"]
    ][
        [
            "qs_university",
            "the_university",
            "qs_country",
            "the_country",
            "match_type",
            "similarity"
        ]
    ]

    print(
        mismatches.to_string(index=False)
    )


# ============================================================
# FUZZY MATCH STATISTICS
# ============================================================

fuzzy_matches = matches[
    matches["match_type"].str.contains(
        "fuzzy",
        case=False,
        na=False
    )
].copy()


print("\n" + "=" * 70)
print("FUZZY MATCH STATISTICS")
print("=" * 70)

print(
    f"Fuzzy matches: {len(fuzzy_matches)}"
)


if len(fuzzy_matches) > 0:

    print("\nSimilarity statistics:")

    print(
        fuzzy_matches["similarity"].describe()
    )


# ============================================================
# LOWEST SIMILARITY FUZZY MATCHES
# ============================================================

if len(fuzzy_matches) > 0:

    print("\n" + "=" * 70)
    print("LOWEST SIMILARITY FUZZY MATCHES")
    print("=" * 70)

    lowest = fuzzy_matches.sort_values(
        by="similarity",
        ascending=True
    ).head(30)

    print(
        lowest[
            [
                "qs_university",
                "the_university",
                "qs_country",
                "the_country",
                "match_type",
                "similarity",
                "country_match"
            ]
        ].to_string(index=False)
    )


# ============================================================
# HIGH-RISK FUZZY MATCHES
# ============================================================

high_risk = fuzzy_matches[
    fuzzy_matches["similarity"] < 94
].copy()


print("\n" + "=" * 70)
print("HIGH-RISK FUZZY MATCHES")
print("=" * 70)

print(
    f"Fuzzy matches below 94 similarity: "
    f"{len(high_risk)}"
)


if len(high_risk) > 0:

    print("\nThese should be manually reviewed:")

    print(
        high_risk[
            [
                "qs_university",
                "the_university",
                "qs_country",
                "the_country",
                "similarity"
            ]
        ].to_string(index=False)
    )


# ============================================================
# MATCH QUALITY SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MATCH QUALITY SUMMARY")
print("=" * 70)

total_matches = len(matches)

exact_matches = (
    matches["match_type"]
    .eq("exact_name_country")
    .sum()
)

fuzzy_count = (
    matches["match_type"]
    .str.contains(
        "fuzzy",
        case=False,
        na=False
    )
    .sum()
)

print(
    f"Total matches: {total_matches}"
)

print(
    f"Exact name + country: {exact_matches}"
)

print(
    f"Fuzzy high-confidence: {fuzzy_count}"
)

print(
    f"Country mismatches: {different_country_count}"
)


if fuzzy_count > 0:

    print(
        f"Average fuzzy similarity: "
        f"{fuzzy_matches['similarity'].mean():.2f}"
    )

    print(
        f"Minimum fuzzy similarity: "
        f"{fuzzy_matches['similarity'].min():.2f}"
    )


# ============================================================
# SAVE REVIEW FILE
# ============================================================

matches.to_csv(
    REVIEW_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)

print(
    f"Created: {REVIEW_FILE}"
)