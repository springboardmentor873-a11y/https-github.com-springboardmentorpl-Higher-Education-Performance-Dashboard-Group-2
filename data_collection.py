import pandas as pd
import numpy as np
import re
from pathlib import Path

# ============================================================
# UNIVERSITY RANKING DATA COLLECTION
# QS + THE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# YOUR ACTUAL FILE NAMES
QS_FILE = BASE_DIR / "QS_Rankings.csv"
THE_FILE = BASE_DIR / "THE_Rankings.csv"

# OUTPUT
OUTPUT_FILE = BASE_DIR / "university_raw_data.csv"


# ============================================================
# 1. CHECK FILES
# ============================================================

print("=" * 70)
print("UNIVERSITY RANKING DATA COLLECTION")
print("=" * 70)

print("\nProject folder:")
print(BASE_DIR)

if not QS_FILE.exists():
    raise FileNotFoundError(
        f"\nQS file not found:\n{QS_FILE}\n\n"
        f"Make sure QS_Rankings.csv is inside:\n{BASE_DIR}"
    )

if not THE_FILE.exists():
    raise FileNotFoundError(
        f"\nTHE file not found:\n{THE_FILE}\n\n"
        f"Make sure THE_Rankings.csv is inside:\n{BASE_DIR}"
    )

print("\nQS file found:", QS_FILE.name)
print("THE file found:", THE_FILE.name)


# ============================================================
# 2. READ QS DATA
# ============================================================

print("\nReading QS dataset...")

qs = pd.read_csv(
    QS_FILE,
    encoding="latin1"
)

print("QS shape:", qs.shape)


# ============================================================
# 3. READ THE DATA
# ============================================================

print("\nReading THE dataset...")

the = pd.read_csv(
    THE_FILE,
    encoding="latin1"
)

print("THE shape:", the.shape)


# ============================================================
# 4. SHOW ORIGINAL COLUMNS
# ============================================================

print("\nQS columns:")
print(qs.columns.tolist())

print("\nTHE columns:")
print(the.columns.tolist())


# ============================================================
# 5. PROCESS QS DATA
# ============================================================

print("\nProcessing QS data...")

qs_data = pd.DataFrame()

# University name
qs_data["university_name"] = (
    qs["Institution_Name"]
    .astype(str)
    .str.strip()
)

# Country
qs_data["country"] = (
    qs["Location"]
    .astype(str)
    .str.strip()
)

# Region
qs_data["region"] = (
    qs["Region"]
    .astype(str)
    .str.strip()
)

# QS 2025 Rank
qs_data["rank"] = pd.to_numeric(
    qs["RANK_2025"],
    errors="coerce"
)

# QS 2024 Rank
qs_data["previous_rank"] = pd.to_numeric(
    qs["RANK_2024"],
    errors="coerce"
)

# Overall score
qs_data["overall_score"] = pd.to_numeric(
    qs["Overall_Score"],
    errors="coerce"
)

# Academic reputation
qs_data["academic_reputation_score"] = pd.to_numeric(
    qs["Academic_Reputation_Score"],
    errors="coerce"
)

# Employer reputation
qs_data["employer_reputation_score"] = pd.to_numeric(
    qs["Employer_Reputation_Score"],
    errors="coerce"
)

# Faculty/student
qs_data["faculty_student_score"] = pd.to_numeric(
    qs["Faculty_Student_Score"],
    errors="coerce"
)

# Citations
qs_data["citations_score"] = pd.to_numeric(
    qs["Citations_per_Faculty_Score"],
    errors="coerce"
)

# International faculty
qs_data["international_faculty_score"] = pd.to_numeric(
    qs["International_Faculty_Score"],
    errors="coerce"
)

# International students
qs_data["international_students_score"] = pd.to_numeric(
    qs["International_Students_Score"],
    errors="coerce"
)

# International research network
qs_data["international_research_network_score"] = pd.to_numeric(
    qs["International_Research_Network_Score"],
    errors="coerce"
)

# Employment outcomes
qs_data["employment_outcomes_score"] = pd.to_numeric(
    qs["Employment_Outcomes_Score"],
    errors="coerce"
)

# Sustainability
qs_data["sustainability_score"] = pd.to_numeric(
    qs["Sustainability_Score"],
    errors="coerce"
)

# Source
qs_data["source"] = "QS"


# ============================================================
# 6. PROCESS THE DATA
# ============================================================

print("Processing THE data...")

the_data = pd.DataFrame()

# University name
the_data["university_name"] = (
    the["name"]
    .astype(str)
    .str.strip()
)

# Country
the_data["country"] = (
    the["location"]
    .astype(str)
    .str.strip()
)

# Rank
the_data["rank"] = pd.to_numeric(
    the["rank"],
    errors="coerce"
)

# Overall score
the_data["overall_score"] = pd.to_numeric(
    the["scores_overall"],
    errors="coerce"
)

# Teaching score
the_data["teaching_score"] = pd.to_numeric(
    the["scores_teaching"],
    errors="coerce"
)

# Research score
the_data["research_score"] = pd.to_numeric(
    the["scores_research"],
    errors="coerce"
)

# Citations score
the_data["citations_score"] = pd.to_numeric(
    the["scores_citations"],
    errors="coerce"
)

# Industry income
the_data["industry_income_score"] = pd.to_numeric(
    the["scores_industry_income"],
    errors="coerce"
)

# International outlook
the_data["international_outlook_score"] = pd.to_numeric(
    the["scores_international_outlook"],
    errors="coerce"
)

# Number of students
the_data["number_of_students"] = pd.to_numeric(
    the["stats_number_students"],
    errors="coerce"
)

# Student staff ratio
the_data["student_staff_ratio"] = pd.to_numeric(
    the["stats_student_staff_ratio"],
    errors="coerce"
)

# International student percentage
the_data["international_student_percentage"] = (
    the["stats_pc_intl_students"]
    .astype(str)
    .str.strip()
    .str.replace("%", "", regex=False)
    .str.replace(",", "", regex=False)
)

the_data["international_student_percentage"] = pd.to_numeric(
    the_data["international_student_percentage"],
    errors="coerce"
)


# Female/male ratio
the_data["female_male_ratio"] = (
    the["stats_female_male_ratio"]
    .astype(str)
    .str.strip()
)

# Source
the_data["source"] = "THE"


# ============================================================
# 7. ADD MISSING QS/THE COLUMNS
# ============================================================

# Columns available in QS but not THE

the_data["region"] = np.nan
the_data["previous_rank"] = np.nan

the_data["academic_reputation_score"] = np.nan
the_data["employer_reputation_score"] = np.nan
the_data["faculty_student_score"] = np.nan
the_data["international_faculty_score"] = np.nan
the_data["international_students_score"] = np.nan
the_data["international_research_network_score"] = np.nan
the_data["employment_outcomes_score"] = np.nan
the_data["sustainability_score"] = np.nan


# Columns available in THE but not QS

qs_data["teaching_score"] = np.nan
qs_data["research_score"] = np.nan
qs_data["industry_income_score"] = np.nan
qs_data["international_outlook_score"] = np.nan
qs_data["number_of_students"] = np.nan
qs_data["student_staff_ratio"] = np.nan
qs_data["international_student_percentage"] = np.nan
qs_data["female_male_ratio"] = np.nan


# ============================================================
# 8. COMMON COLUMN STRUCTURE
# ============================================================

common_columns = [

    "university_name",
    "country",
    "region",
    "source",

    "rank",
    "previous_rank",
    "overall_score",

    "academic_reputation_score",
    "employer_reputation_score",
    "faculty_student_score",
    "citations_score",
    "international_faculty_score",
    "international_students_score",
    "international_research_network_score",
    "employment_outcomes_score",
    "sustainability_score",

    "teaching_score",
    "research_score",
    "industry_income_score",
    "international_outlook_score",

    "number_of_students",
    "student_staff_ratio",
    "international_student_percentage",
    "female_male_ratio"
]


qs_data = qs_data[common_columns]

the_data = the_data[common_columns]


# ============================================================
# 9. MERGE QS + THE
# ============================================================

print("\nMerging QS and THE datasets...")

university_raw_data = pd.concat(
    [
        qs_data,
        the_data
    ],
    ignore_index=True
)


# ============================================================
# 10. STANDARDIZE UNIVERSITY NAMES
# ============================================================

def clean_name(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value


university_raw_data["university_name"] = (
    university_raw_data["university_name"]
    .apply(clean_name)
)


# ============================================================
# 11. STANDARDIZE COUNTRY NAMES
# ============================================================

university_raw_data["country"] = (
    university_raw_data["country"]
    .astype(str)
    .str.strip()
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
)


country_mapping = {

    "USA": "United States",
    "US": "United States",
    "U.S.": "United States",
    "U.S.A.": "United States",

    "UK": "United Kingdom",
    "U.K.": "United Kingdom",

    "UAE": "United Arab Emirates",

    "Türkiye": "Turkey",
    "Turkiye": "Turkey",

    "Russian Federation": "Russia",

    "Czech Republic": "Czechia",

    "Republic of Korea": "South Korea"
}


university_raw_data["country"] = (
    university_raw_data["country"]
    .replace(country_mapping)
)


# ============================================================
# 12. REMOVE DUPLICATES
# ============================================================

duplicates_before = (
    university_raw_data
    .duplicated()
    .sum()
)

university_raw_data = (
    university_raw_data
    .drop_duplicates()
    .reset_index(drop=True)
)

duplicates_after = (
    university_raw_data
    .duplicated()
    .sum()
)

print(
    "\nDuplicates before:",
    duplicates_before
)

print(
    "Duplicates after:",
    duplicates_after
)


# ============================================================
# 13. NORMALIZE RANKING METRIC
# ============================================================

rank = pd.to_numeric(
    university_raw_data["rank"],
    errors="coerce"
)

max_rank = rank.max()

if pd.notna(max_rank) and max_rank > 0:

    university_raw_data["normalized_ranking_score"] = (
        (
            max_rank - rank + 1
        )
        /
        max_rank
    ) * 100

else:

    university_raw_data["normalized_ranking_score"] = np.nan


# ============================================================
# 14. CREATE UNIVERSITY ID
# ============================================================

university_raw_data.insert(
    0,
    "university_id",
    range(
        1,
        len(university_raw_data) + 1
    )
)


# ============================================================
# 15. DATA COMPLETENESS CHECK
# ============================================================

total_cells = (
    university_raw_data.shape[0]
    *
    university_raw_data.shape[1]
)

missing_cells = (
    university_raw_data.isna()
    .sum()
    .sum()
)

missing_percentage = (
    missing_cells
    /
    total_cells
) * 100

completeness = (
    100 - missing_percentage
)


# ============================================================
# 16. SAVE university_raw_data.csv
# ============================================================

university_raw_data.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# 17. FINAL REPORT
# ============================================================

print("\n")
print("=" * 70)
print("DATA COLLECTION COMPLETED")
print("=" * 70)

print(
    "QS records:",
    len(qs_data)
)

print(
    "THE records:",
    len(the_data)
)

print(
    "Merged records:",
    len(university_raw_data)
)

print(
    "Total columns:",
    len(university_raw_data.columns)
)

print(
    f"Missing data: {missing_percentage:.2f}%"
)

print(
    f"Completeness: {completeness:.2f}%"
)

print("\nSource distribution:")

print(
    university_raw_data["source"]
    .value_counts()
)

print("\nOutput file:")

print(OUTPUT_FILE)

print("\nFirst 5 records:")

print(
    university_raw_data.head()
)

print("=" * 70)

if completeness >= 95:

    print(
        "PASS: Dataset completeness is above 95%"
    )

else:

    print(
        "WARNING: Dataset completeness is below 95%"
    )