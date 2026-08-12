from pathlib import Path
import pandas as pd
import re

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

QS_FILE = RAW_DATA / "qs_rankings_2024.csv"
THE_FILE = RAW_DATA / "the_rankings_2024.csv"
OUTPUT_FILE = RAW_DATA / "university_raw_data.csv"

# =====================================================
# Load Datasets
# =====================================================

print("=" * 60)
print("Loading datasets...")
print("=" * 60)

qs = pd.read_csv(QS_FILE)
the = pd.read_csv(THE_FILE)

print(f"QS Dataset Shape : {qs.shape}")
print(f"THE Dataset Shape: {the.shape}")

# =====================================================
# Remove Duplicate Header Row (if present)
# =====================================================

if str(qs.iloc[0]["2024 RANK"]).lower() == "rank display":
    qs = qs.iloc[1:].reset_index(drop=True)

# =====================================================
# Select Required Columns
# =====================================================

qs = qs[
    [
        "2024 RANK",
        "Institution Name",
        "Country",
        "Overall SCORE",
        "Academic Reputation Score",
        "Employer Reputation Score",
        "Faculty Student Score",
        "Citations per Faculty Score",
        "International Faculty Score",
        "International Students Score",
        "International Research Network Score",
        "Employment Outcomes Score",
        "Sustainability Score",
    ]
]

the = the[
    [
        "rank",
        "name",
        "location",
        "scores_overall",
        "scores_teaching",
        "scores_research",
        "scores_citations",
        "scores_industry_income",
        "scores_international_outlook",
        "stats_number_students",
        "stats_student_staff_ratio",
        "stats_pc_intl_students",
        "stats_female_male_ratio",
    ]
]

# =====================================================
# Rename Columns
# =====================================================

qs.rename(
    columns={
        "2024 RANK": "Rank_QS",
        "Institution Name": "University",
        "Overall SCORE": "Overall_QS",
    },
    inplace=True,
)

the.rename(
    columns={
        "rank": "Rank_THE",
        "name": "University",
        "location": "Country",
        "scores_overall": "Overall_THE",
    },
    inplace=True,
)

# =====================================================
# Clean University Names
# =====================================================

def clean_university(name):
    if pd.isna(name):
        return name

    name = str(name).lower().strip()

    # Remove text inside brackets
    name = re.sub(r"\(.*?\)", "", name)

    # Remove punctuation
    name = re.sub(r"[.,]", "", name)

    # Remove multiple spaces
    name = " ".join(name.split())

    return name

qs["University"] = qs["University"].apply(clean_university)
the["University"] = the["University"].apply(clean_university)

# =====================================================
# Clean Country Names
# =====================================================

qs["Country"] = qs["Country"].astype(str).str.lower().str.strip()
the["Country"] = the["Country"].astype(str).str.lower().str.strip()

# =====================================================
# Merge Datasets
# =====================================================

merged = pd.merge(
    qs,
    the,
    on=["University", "Country"],
    how="outer",
)

# =====================================================
# Summary
# =====================================================

print("\n" + "=" * 60)
print("Merge Summary")
print("=" * 60)

print(f"QS Universities      : {len(qs)}")
print(f"THE Universities     : {len(the)}")
print(f"Merged Universities  : {len(merged)}")

matched = merged["Rank_QS"].notna() & merged["Rank_THE"].notna()

print(f"Matched Universities : {matched.sum()}")

duplicates = merged.duplicated(
    subset=["University", "Country"]
).sum()

print(f"Duplicate Universities: {duplicates}")

print("\nMissing Values")
print(merged.isnull().sum())

# =====================================================
# Save Output
# =====================================================

merged.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)
print("\nMerged dataset saved successfully.")
print(f"Location: {OUTPUT_FILE}")