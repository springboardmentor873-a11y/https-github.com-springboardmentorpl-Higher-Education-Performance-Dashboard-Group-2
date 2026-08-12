import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

QS_FILE = OUTPUT_DIR / "qs_cleaned_encoding_fixed.csv"
THE_FILE = OUTPUT_DIR / "the_cleaned_encoding_fixed.csv"

MATCHED_FILE = OUTPUT_DIR / "university_matched_data_v2.csv"
MATCH_DETAILS_FILE = OUTPUT_DIR / "match_details_v2.csv"
REVIEW_FILE = OUTPUT_DIR / "matches_needing_review_v2.csv"

FINAL_MATCHED_FILE = OUTPUT_DIR / "university_matched_data_final.csv"
FINAL_REVIEW_FILE = OUTPUT_DIR / "manual_review_decisions.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("BUILDING FINAL MATCHED DATASET")
print("=" * 70)

qs = pd.read_csv(
    QS_FILE,
    encoding="utf-8-sig"
)

the = pd.read_csv(
    THE_FILE,
    encoding="utf-8-sig"
)

matched = pd.read_csv(
    MATCHED_FILE,
    encoding="utf-8-sig"
)

match_details = pd.read_csv(
    MATCH_DETAILS_FILE,
    encoding="utf-8-sig"
)

review = pd.read_csv(
    REVIEW_FILE,
    encoding="utf-8-sig"
)


print(f"\nQS rows: {len(qs)}")
print(f"THE rows: {len(the)}")
print(f"Existing approved matches: {len(matched)}")
print(f"Match details: {len(match_details)}")
print(f"Review candidates: {len(review)}")


# ============================================================
# MANUAL REVIEW DECISIONS
# ============================================================

# These 9 are confirmed false matches.
# They must remain unmatched.

rejected_pairs = [

    (
        "Indian Institute of Technology Kanpur (IITK)",
        "Indian Institute of Technology Mandi"
    ),

    (
        "Indian Institute of Technology Roorkee (IITR)",
        "Indian Institute of Technology Ropar"
    ),

    (
        "Zhengzhou University",
        "Wenzhou University"
    ),

    (
        "Oregon State University",
        "Morgan State University"
    ),

    (
        "Lanzhou University",
        "Changzhou University"
    ),

    (
        "Wuhan University of Technology",
        "Zhejiang University of Technology"
    ),

    (
        "University of Massachusetts - Boston",
        "University of Massachusetts"
    ),

    (
        "Universidade Federal do Ceará (UFC)",
        "Universidade Federal do ABC (UFABC)"
    ),

    (
        "Soka University",
        "Shizuoka University"
    )
]


# ============================================================
# APPLY DECISIONS
# ============================================================

review["decision"] = "ACCEPT"

for qs_name, the_name in rejected_pairs:

    mask = (
        (review["qs_university"] == qs_name)
        &
        (review["the_university"] == the_name)
    )

    review.loc[mask, "decision"] = "REJECT"


# ============================================================
# VALIDATE MANUAL DECISIONS
# ============================================================

print("\n" + "=" * 70)
print("MANUAL REVIEW SUMMARY")
print("=" * 70)

print(
    review["decision"].value_counts()
)


accepted_review = review[
    review["decision"] == "ACCEPT"
].copy()

rejected_review = review[
    review["decision"] == "REJECT"
].copy()


if len(accepted_review) != 68:
    raise ValueError(
        f"Expected 68 accepted review matches, "
        f"but found {len(accepted_review)}."
    )


if len(rejected_review) != 9:
    raise ValueError(
        f"Expected 9 rejected review matches, "
        f"but found {len(rejected_review)}."
    )


# ============================================================
# CHECK REQUIRED INDEX COLUMNS
# ============================================================

required_columns = [
    "qs_index",
    "the_index",
    "qs_university",
    "the_university",
    "qs_country",
    "the_country",
    "similarity",
    "country_match"
]

for column in required_columns:

    if column not in review.columns:
        raise KeyError(
            f"Missing required column in review file: {column}"
        )


# ============================================================
# CHECK INDICES
# ============================================================

print("\n" + "=" * 70)
print("CHECKING REVIEW INDICES")
print("=" * 70)

for _, row in accepted_review.iterrows():

    qs_index = int(row["qs_index"])
    the_index = int(row["the_index"])

    if qs_index not in qs.index:
        raise ValueError(
            f"QS index {qs_index} not found."
        )

    if the_index not in the.index:
        raise ValueError(
            f"THE index {the_index} not found."
        )


print("All accepted QS/THE indices are valid.")


# ============================================================
# CHECK THAT ACCEPTED REVIEW MATCHES ARE NOT ALREADY
# IN THE EXISTING MATCHED DATASET
# ============================================================

existing_qs_names = set(
    matched["qs_Institution Name"]
    .astype(str)
)

duplicate_review_matches = accepted_review[
    accepted_review["qs_university"].astype(str).isin(
        existing_qs_names
    )
]

if len(duplicate_review_matches) > 0:

    print("\nDuplicate review matches detected:")

    print(
        duplicate_review_matches[
            [
                "qs_university",
                "the_university",
                "similarity"
            ]
        ].to_string(index=False)
    )

    raise ValueError(
        "Some accepted review matches already exist "
        "in the approved dataset."
    )


print(
    "No accepted review matches are already present."
)


# ============================================================
# PREPARE QS DATA FOR MERGING
# ============================================================

def prefix_columns(df, prefix):
    """
    Add dataset prefix to every column.
    """
    return df.rename(
        columns={
            col: f"{prefix}_{col}"
            for col in df.columns
        }
    )


qs_prefixed = prefix_columns(
    qs.copy(),
    "qs"
)

the_prefixed = prefix_columns(
    the.copy(),
    "the"
)


# ============================================================
# CREATE 68 ACCEPTED MATCHES
# ============================================================

print("\n" + "=" * 70)
print("ADDING ACCEPTED MANUAL MATCHES")
print("=" * 70)

accepted_rows = []


for _, review_row in accepted_review.iterrows():

    qs_index = int(review_row["qs_index"])
    the_index = int(review_row["the_index"])

    qs_row = qs_prefixed.loc[
        qs_index
    ].to_dict()

    the_row = the_prefixed.loc[
        the_index
    ].to_dict()

    # --------------------------------------------------------
    # Combine QS + THE
    # --------------------------------------------------------

    combined = {}

    combined.update(qs_row)
    combined.update(the_row)

    # --------------------------------------------------------
    # Add matching metadata
    # --------------------------------------------------------

    combined["match_type"] = "manual_review_approved"

    combined["match_similarity"] = float(
        review_row["similarity"]
    )

    combined["country_match"] = bool(
        review_row["country_match"]
    )

    accepted_rows.append(
        combined
    )


accepted_matches = pd.DataFrame(
    accepted_rows
)


print(
    f"Accepted manual matches created: "
    f"{len(accepted_matches)}"
)


# ============================================================
# ALIGN COLUMNS
# ============================================================

# Existing matched dataset and newly created rows
# must have exactly the same columns.

existing_columns = list(
    matched.columns
)

accepted_matches = accepted_matches.reindex(
    columns=existing_columns
)


# ============================================================
# COMBINE EXISTING + MANUAL MATCHES
# ============================================================

final_matched = pd.concat(
    [
        matched,
        accepted_matches
    ],
    ignore_index=True
)


# ============================================================
# DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("FINAL MATCH CHECK")
print("=" * 70)

duplicate_qs = final_matched[
    "qs_Institution Name"
].duplicated().sum()

duplicate_the = final_matched[
    "the_Name"
].duplicated().sum()


print(
    f"Duplicate QS universities: {duplicate_qs}"
)

print(
    f"Duplicate THE universities: {duplicate_the}"
)


if duplicate_qs > 0:
    raise ValueError(
        "Duplicate QS universities detected."
    )


# ============================================================
# COUNTRY VALIDATION
# ============================================================

country_column_qs = "qs_Country/Territory"
country_column_the = "the_Country"

country_mismatches = (
    final_matched[country_column_qs].astype(str)
    !=
    final_matched[country_column_the].astype(str)
).sum()


print(
    f"Country mismatches: {country_mismatches}"
)


if country_mismatches > 0:

    print("\nCountry mismatch examples:")

    print(
        final_matched[
            final_matched[country_column_qs].astype(str)
            !=
            final_matched[country_column_the].astype(str)
        ][
            [
                "qs_Institution Name",
                "the_Name",
                country_column_qs,
                country_column_the
            ]
        ].head(20).to_string(index=False)
    )

    raise ValueError(
        "Country mismatches detected."
    )


# ============================================================
# EXPECTED FINAL COUNT
# ============================================================

expected_final_matches = (
    len(matched) + len(accepted_review)
)

actual_final_matches = len(
    final_matched
)


print(
    f"\nExpected final matches: "
    f"{expected_final_matches}"
)

print(
    f"Actual final matches: "
    f"{actual_final_matches}"
)


if actual_final_matches != expected_final_matches:

    raise ValueError(
        "Final match count does not match expected count."
    )


# ============================================================
# SAVE FINAL MATCHED DATA
# ============================================================

final_matched.to_csv(
    FINAL_MATCHED_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# SAVE REVIEW DECISIONS
# ============================================================

review.to_csv(
    FINAL_REVIEW_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL MATCHING COMPLETED")
print("=" * 70)

print(
    f"\nOriginal high-confidence matches: "
    f"{len(matched)}"
)

print(
    f"Accepted manual-review matches: "
    f"{len(accepted_review)}"
)

print(
    f"Rejected manual-review candidates: "
    f"{len(rejected_review)}"
)

print(
    f"FINAL APPROVED MATCHES: "
    f"{len(final_matched)}"
)

print(
    f"TOTAL QS UNIVERSITIES: "
    f"{len(qs)}"
)

print(
    f"FINAL UNMATCHED QS: "
    f"{len(qs) - len(final_matched)}"
)

print(
    f"FINAL MATCH RATE: "
    f"{len(final_matched) / len(qs) * 100:.2f}%"
)

print("\nCreated:")

print(FINAL_MATCHED_FILE)
print(FINAL_REVIEW_FILE)

print("\n" + "=" * 70)
print("NEXT STEP")
print("=" * 70)

print(
    "\nRun final validation before creating "
    "the raw merged dataset."
)