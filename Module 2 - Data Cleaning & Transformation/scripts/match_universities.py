import pandas as pd
import re
import unicodedata
from pathlib import Path
from rapidfuzz import fuzz, process


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

QS_FILE = OUTPUT_DIR / "qs_cleaned_encoding_fixed.csv"
THE_FILE = OUTPUT_DIR / "the_cleaned_encoding_fixed.csv"

MATCHED_OUTPUT = OUTPUT_DIR / "university_matched_data_v2.csv"
UNMATCHED_OUTPUT = OUTPUT_DIR / "unmatched_qs_universities_v3.csv"
REVIEW_OUTPUT = OUTPUT_DIR / "matches_needing_review_v2.csv"
DETAILS_OUTPUT = OUTPUT_DIR / "match_details_v2.csv"


# ============================================================
# SETTINGS
# ============================================================

HIGH_THRESHOLD = 92
MEDIUM_THRESHOLD = 88


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(value):
    """
    Normalize university text for matching.
    """

    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    # Fix common mojibake
    try:
        if any(x in value for x in ["Ã", "Â", "â", "Å", "Ä"]):
            value = value.encode("latin1").decode("utf-8").lower()
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # Unicode normalization
    value = unicodedata.normalize("NFKD", value)

    # Remove accents
    value = "".join(
        c for c in value
        if not unicodedata.combining(c)
    )

    # & -> and
    value = value.replace("&", " and ")

    # Remove bracket contents
    value = re.sub(r"\([^)]*\)", " ", value)

    # Normalize university words
    value = re.sub(
        r"\b(university|universite|universität|universidad)\b",
        " university ",
        value
    )

    # Remove punctuation
    value = re.sub(r"[^a-z0-9\s]", " ", value)

    # Normalize spaces
    value = re.sub(r"\s+", " ", value).strip()

    return value


def normalize_name(value):
    """
    Create normalized university name.
    """

    value = normalize_text(value)

    value = re.sub(
        r"\s+",
        " ",
        value
    ).strip()

    return value


def normalize_country(value):
    """
    Standardize country names between QS and THE.
    """

    if pd.isna(value):
        return ""

    value = str(value).strip()

    replacements = {
        "United States": "United States of America",
        "United States of America": "United States of America",

        "China": "China (Mainland)",
        "China (Mainland)": "China (Mainland)",

        "South Korea": "Republic of Korea",
        "Korea, Republic of": "Republic of Korea",
        "Republic of Korea": "Republic of Korea",

        "Russia": "Russian Federation",
        "Russian Federation": "Russian Federation",

        "Czech Republic": "Czechia",
        "Czechia": "Czechia",
    }

    return replacements.get(
        value,
        value
    )


# ============================================================
# KNOWN FALSE POSITIVE PAIRS
# ============================================================

FORBIDDEN_MATCHES = {
    (
        normalize_name("University of South Alabama (USA)"),
        normalize_name("The University of Alabama")
    )
}


# ============================================================
# LOAD DATASETS
# ============================================================

print("=" * 70)
print("LOADING CLEANED DATASETS")
print("=" * 70)

qs = pd.read_csv(
    QS_FILE,
    encoding="utf-8-sig"
)

the = pd.read_csv(
    THE_FILE,
    encoding="utf-8-sig"
)

print(f"QS shape : {qs.shape}")
print(f"THE shape: {the.shape}")


# ============================================================
# VERIFY REQUIRED COLUMNS
# ============================================================

required_qs = [
    "Institution Name",
    "Country/Territory",
    "university_key"
]

required_the = [
    "Name",
    "Country",
    "university_key"
]

missing_qs = [
    col
    for col in required_qs
    if col not in qs.columns
]

missing_the = [
    col
    for col in required_the
    if col not in the.columns
]

if missing_qs:

    print("\nERROR: Missing QS columns:")
    print(missing_qs)

    print("\nAvailable QS columns:")
    print(qs.columns.tolist())

    raise KeyError(
        f"Missing QS columns: {missing_qs}"
    )


if missing_the:

    print("\nERROR: Missing THE columns:")
    print(missing_the)

    print("\nAvailable THE columns:")
    print(the.columns.tolist())

    raise KeyError(
        f"Missing THE columns: {missing_the}"
    )


# ============================================================
# CREATE MATCHING FIELDS
# ============================================================

qs["match_name"] = qs[
    "Institution Name"
].apply(normalize_name)

the["match_name"] = the[
    "Name"
].apply(normalize_name)

qs["match_country"] = qs[
    "Country/Territory"
].apply(normalize_country)

the["match_country"] = the[
    "Country"
].apply(normalize_country)


# ============================================================
# CHECK MATCHING KEYS
# ============================================================

print("\n" + "=" * 70)
print("CHECKING MATCHING KEYS")
print("=" * 70)

print("\nQS university keys:")
print(
    qs["match_name"]
    .head()
    .to_string(index=False)
)

print("\nTHE university keys:")
print(
    the["match_name"]
    .head()
    .to_string(index=False)
)


# ============================================================
# LEVEL 1
# EXACT NAME + SAME COUNTRY
# ============================================================

print("\n" + "=" * 70)
print("LEVEL 1 - EXACT NAME + SAME COUNTRY")
print("=" * 70)


the_lookup = {}

for idx, row in the.iterrows():

    key = (
        row["match_name"],
        row["match_country"]
    )

    if key not in the_lookup:
        the_lookup[key] = idx


matched_records = []

used_the_indices = set()

exact_matches = 0


for qs_idx, qs_row in qs.iterrows():

    key = (
        qs_row["match_name"],
        qs_row["match_country"]
    )

    if key not in the_lookup:
        continue

    the_idx = the_lookup[key]

    if the_idx in used_the_indices:
        continue

    the_row = the.loc[the_idx]

    pair = (
        qs_row["match_name"],
        the_row["match_name"]
    )

    # Safety check
    if pair in FORBIDDEN_MATCHES:
        continue

    matched_records.append({
        "qs_index": qs_idx,
        "the_index": the_idx,
        "qs_university": qs_row["Institution Name"],
        "the_university": the_row["Name"],
        "qs_country": qs_row["Country/Territory"],
        "the_country": the_row["Country"],
        "match_type": "exact_name_country",
        "similarity": 100.0,
        "country_match": True
    })

    used_the_indices.add(the_idx)

    exact_matches += 1


print(
    f"Exact same-country matches: {exact_matches}"
)


# ============================================================
# LEVEL 2
# CONTROLLED FUZZY MATCHING
# ============================================================

print("\n" + "=" * 70)
print("LEVEL 2 - CONTROLLED FUZZY MATCHING")
print("=" * 70)


# ------------------------------------------------------------
# Build country-specific THE candidates
# ------------------------------------------------------------

country_candidates = {}

for idx, row in the.iterrows():

    if idx in used_the_indices:
        continue

    country = row["match_country"]

    if country not in country_candidates:
        country_candidates[country] = []

    country_candidates[country].append(
        (
            idx,
            row["match_name"]
        )
    )


fuzzy_matches = []
review_candidates = []

matched_qs_indices = {
    record["qs_index"]
    for record in matched_records
}


# ============================================================
# PROCESS UNMATCHED QS UNIVERSITIES
# ============================================================

for qs_idx, qs_row in qs.iterrows():

    if qs_idx in matched_qs_indices:
        continue

    qs_name = qs_row["match_name"]
    qs_country = qs_row["match_country"]

    if not qs_name:
        continue

    candidates = country_candidates.get(
        qs_country,
        []
    )

    if not candidates:
        continue

    candidate_names = [
        name
        for _, name in candidates
    ]

    # --------------------------------------------------------
    # Get top 3 candidates
    # --------------------------------------------------------

    results = process.extract(
        qs_name,
        candidate_names,
        scorer=fuzz.token_sort_ratio,
        limit=3
    )

    if not results:
        continue

    best_match_name = results[0][0]
    similarity = float(results[0][1])

    # --------------------------------------------------------
    # Find THE index
    # --------------------------------------------------------

    best_the_idx = None

    for idx, name in candidates:

        if name == best_match_name:
            best_the_idx = idx
            break

    if best_the_idx is None:
        continue

    the_row = the.loc[best_the_idx]

    # --------------------------------------------------------
    # FALSE-POSITIVE PROTECTION
    # --------------------------------------------------------

    pair = (
        qs_name,
        the_row["match_name"]
    )

    if pair in FORBIDDEN_MATCHES:

        print("\nBlocked known false positive:")
        print(
            f"QS : {qs_row['Institution Name']}"
        )
        print(
            f"THE: {the_row['Name']}"
        )
        print(
            f"Similarity: {similarity:.2f}"
        )

        # IMPORTANT:
        # Do not try another candidate automatically.
        # This university remains unmatched.
        continue

    # --------------------------------------------------------
    # Build record
    # --------------------------------------------------------

    record = {
        "qs_index": qs_idx,
        "the_index": best_the_idx,
        "qs_university": qs_row["Institution Name"],
        "the_university": the_row["Name"],
        "qs_country": qs_row["Country/Territory"],
        "the_country": the_row["Country"],
        "similarity": round(similarity, 2),
        "country_match": (
            qs_country ==
            the_row["match_country"]
        )
    }

    # --------------------------------------------------------
    # HIGH CONFIDENCE
    # --------------------------------------------------------

    if similarity >= HIGH_THRESHOLD:

        record["match_type"] = "fuzzy_high"

        fuzzy_matches.append(record)

        used_the_indices.add(
            best_the_idx
        )

    # --------------------------------------------------------
    # REVIEW
    # --------------------------------------------------------

    elif similarity >= MEDIUM_THRESHOLD:

        record["match_type"] = "review"

        review_candidates.append(record)


# ============================================================
# ADD FUZZY MATCHES
# ============================================================

matched_records.extend(
    fuzzy_matches
)


# ============================================================
# MATCHING SUMMARY
# ============================================================

total_qs = len(qs)

total_matched = len(
    matched_records
)

total_unmatched = (
    total_qs -
    total_matched
)

match_rate = (
    total_matched /
    total_qs *
    100
)


print("\n" + "=" * 70)
print("MATCHING SUMMARY")
print("=" * 70)

print(
    f"Total QS universities: {total_qs}"
)

print(
    f"High-confidence matches: {total_matched}"
)

print(
    f"Unmatched: {total_unmatched}"
)

print(
    f"Match rate: {match_rate:.2f}%"
)

print(
    f"Potential matches requiring review: "
    f"{len(review_candidates)}"
)


# ============================================================
# MATCH TYPE SUMMARY
# ============================================================

if matched_records:

    match_type_counts = pd.Series(
        [
            record["match_type"]
            for record in matched_records
        ]
    ).value_counts()

    print("\nMatch types:")
    print(match_type_counts)

else:

    print("\nNo matches found.")


# ============================================================
# CREATE MATCH DETAILS
# ============================================================

match_details = pd.DataFrame(
    matched_records
)

if not match_details.empty:

    match_details = match_details[
        [
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
    ]


# ============================================================
# CREATE MATCHED DATASET
# ============================================================

print("\n" + "=" * 70)
print("CREATING MATCHED DATASET")
print("=" * 70)


matched_rows = []


for record in matched_records:

    qs_idx = record["qs_index"]
    the_idx = record["the_index"]

    qs_row = qs.loc[qs_idx]
    the_row = the.loc[the_idx]

    combined = {}

    # --------------------------------------------------------
    # QS columns
    # --------------------------------------------------------

    for col in qs.columns:

        if col not in [
            "match_name",
            "match_country"
        ]:

            combined[
                f"qs_{col}"
            ] = qs_row[col]

    # --------------------------------------------------------
    # THE columns
    # --------------------------------------------------------

    for col in the.columns:

        if col not in [
            "match_name",
            "match_country"
        ]:

            combined[
                f"the_{col}"
            ] = the_row[col]

    # --------------------------------------------------------
    # Match metadata
    # --------------------------------------------------------

    combined["match_type"] = record[
        "match_type"
    ]

    combined["match_similarity"] = record[
        "similarity"
    ]

    combined["country_match"] = record[
        "country_match"
    ]

    matched_rows.append(
        combined
    )


matched_df = pd.DataFrame(
    matched_rows
)


# ============================================================
# CREATE UNMATCHED QS DATASET
# ============================================================

matched_qs_indices = {
    record["qs_index"]
    for record in matched_records
}


unmatched_qs = qs[
    ~qs.index.isin(
        matched_qs_indices
    )
].copy()


# ============================================================
# SAVE OUTPUTS
# ============================================================

matched_df.to_csv(
    MATCHED_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

unmatched_qs.to_csv(
    UNMATCHED_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

pd.DataFrame(
    review_candidates
).to_csv(
    REVIEW_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

match_details.to_csv(
    DETAILS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("MATCHING COMPLETED")
print("=" * 70)

print(
    f"High-confidence matches: "
    f"{total_matched}"
)

print(
    f"Unmatched: "
    f"{total_unmatched}"
)

print(
    f"Match rate: "
    f"{match_rate:.2f}%"
)

print(
    f"Manual review candidates: "
    f"{len(review_candidates)}"
)

print("\nCreated files:")

print(MATCHED_OUTPUT)
print(UNMATCHED_OUTPUT)
print(REVIEW_OUTPUT)
print(DETAILS_OUTPUT)