import pandas as pd
import numpy as np
from pathlib import Path

# Module 2 - Data Cleaning and Transformation

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "Data" / "Processed Data"
CLEANED_DIR = BASE_DIR / "Data" / "Cleaned Data"
DOCS_DIR = BASE_DIR / "docs"

CLEANED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = PROCESSED_DIR / "university_raw_data.csv"

CLEANED_FILE = CLEANED_DIR / "university_cleaned.csv"
TABLEAU_FILE = CLEANED_DIR / "university_tableau_ready.csv"
REPORT_FILE = DOCS_DIR / "data_cleaning_report.txt"

print("Module 2 - Data Cleaning and Transformation")

if not INPUT_FILE.exists():
    print("Input dataset not found:")
    print(INPUT_FILE)
    raise SystemExit

# Load integrated dataset
df = pd.read_csv(INPUT_FILE)

print("\nInput file:", INPUT_FILE)
print("Original rows:", len(df))
print("Original columns:", len(df.columns))

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"_+", "_", regex=True)
)

# Standardize text fields
text_columns = [
    "university_name",
    "country",
    "ranking_source"
]

for column in text_columns:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )

# Standardize university names
df["university_name_std"] = (
    df["university_name"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Standardize country names
df["country_std"] = (
    df["country"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Preserve original ranking values
df["rank_original"] = df["rank"]
df["score_original"] = df["score"]

# Convert ranking ranges
def convert_rank(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if "-" in value:

        parts = value.split("-")

        try:
            lower = float(parts[0])
            upper = float(parts[1])

            return (lower + upper) / 2

        except ValueError:
            return np.nan

    try:
        return float(value)

    except ValueError:
        return np.nan


df["rank"] = df["rank"].apply(convert_rank)

# Convert score values
df["score"] = pd.to_numeric(
    df["score"],
    errors="coerce"
)

# Normalize ranking score
def normalize_rank(group):

    minimum = group["rank"].min()
    maximum = group["rank"].max()

    if maximum == minimum:
        return pd.Series(
            100,
            index=group.index
        )

    return (
        (maximum - group["rank"])
        /
        (maximum - minimum)
    ) * 100


df["rank_normalized"] = (
    df.groupby("ranking_source", group_keys=False)
    .apply(
        normalize_rank,
        include_groups=False
    )
    .sort_index()
)

# Normalize score
def normalize_score(group):

    minimum = group["score"].min()
    maximum = group["score"].max()

    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(
            np.nan,
            index=group.index
        )

    if maximum == minimum:
        return pd.Series(
            100,
            index=group.index
        )

    return (
        (group["score"] - minimum)
        /
        (maximum - minimum)
    ) * 100


df["score_normalized"] = (
    df.groupby("ranking_source", group_keys=False)
    .apply(
        normalize_score,
        include_groups=False
    )
    .sort_index()
)

# Remove exact duplicates
before_duplicates = len(df)

df = df.drop_duplicates()

exact_duplicates_removed = (
    before_duplicates - len(df)
)

# Check duplicate university-source records
duplicate_mask = df.duplicated(
    subset=[
        "university_name_std",
        "country_std",
        "ranking_source"
    ],
    keep="first"
)

duplicate_university_source_count = (
    duplicate_mask.sum()
)

# Remove duplicate university-source records
df = df.loc[
    ~duplicate_mask
].copy()

# Missing-value report before Tableau filtering
missing_before = df.isna().sum()

# Create Tableau-ready dataset
# Records without an Overall Score are excluded from
# the analysis-ready dataset rather than assigning
# artificial values.

tableau_df = df.dropna(
    subset=[
        "university_name_std",
        "country_std",
        "year",
        "ranking_source",
        "rank",
        "score"
    ]
).copy()

# Calculate Tableau-ready missing percentage
required_columns = [
    "university_name_std",
    "country_std",
    "year",
    "ranking_source",
    "rank",
    "score",
    "rank_normalized",
    "score_normalized"
]

total_cells = (
    len(tableau_df) *
    len(required_columns)
)

missing_cells = (
    tableau_df[required_columns]
    .isna()
    .sum()
    .sum()
)

if total_cells > 0:

    tableau_missing_percentage = (
        missing_cells / total_cells
    ) * 100

else:

    tableau_missing_percentage = 100

# Save cleaned dataset
df.to_csv(
    CLEANED_FILE,
    index=False
)

# Save Tableau-ready dataset
tableau_df.to_csv(
    TABLEAU_FILE,
    index=False
)

# Print results
print("\nStandardized columns:")
for column in df.columns:
    print("-", column)

print("\nExact duplicates removed:",
      exact_duplicates_removed)

print(
    "Duplicate university-source records removed:",
    duplicate_university_source_count
)

print("\nMissing-value report before Tableau filtering:")

for column, count in missing_before.items():

    percentage = (
        count / len(df)
    ) * 100

    print(
        f"{column}: "
        f"{count} "
        f"({percentage:.2f}%)"
    )

print("\nRanking source distribution:")
print(
    df["ranking_source"].value_counts()
)

print("\nFinal cleaned dataset rows:",
      len(df))

print(
    "Tableau-ready dataset rows:",
    len(tableau_df)
)

print(
    "Tableau-ready missing percentage:",
    round(
        tableau_missing_percentage,
        2
    ),
    "%"
)

print("\nOutput files:")
print(CLEANED_FILE)
print(TABLEAU_FILE)

# Create cleaning report
with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "MODULE 2 - DATA CLEANING AND TRANSFORMATION\n"
    )

    report.write(
        "============================================\n\n"
    )

    report.write(
        f"Original rows: {before_duplicates}\n"
    )

    report.write(
        f"Rows after cleaning: {len(df)}\n"
    )

    report.write(
        f"Exact duplicates removed: "
        f"{exact_duplicates_removed}\n"
    )

    report.write(
        f"Duplicate university-source records removed: "
        f"{duplicate_university_source_count}\n\n"
    )

    report.write(
        "Transformations performed:\n"
    )

    report.write(
        "- Standardized university names\n"
    )

    report.write(
        "- Standardized country names\n"
    )

    report.write(
        "- Converted ranking ranges to numeric midpoint values\n"
    )

    report.write(
        "- Converted ranking scores to numeric values\n"
    )

    report.write(
        "- Created normalized ranking scores\n"
    )

    report.write(
        "- Created normalized overall scores\n"
    )

    report.write(
        "- Preserved original ranking and score fields\n"
    )

    report.write(
        "- Removed duplicate university-source records\n"
    )

    report.write(
        "- Created Tableau-ready complete-case dataset\n\n"
    )

    report.write(
        "Missing score handling:\n"
    )

    report.write(
        "QS records containing '-' for Overall Score were "
        "treated as unavailable rather than assigning artificial values.\n"
    )

    report.write(
        f"\nTableau-ready rows: {len(tableau_df)}\n"
    )

    report.write(
        f"Tableau-ready missing percentage: "
        f"{tableau_missing_percentage:.2f}%\n"
    )

    report.write(
        f"\nCleaned dataset: {CLEANED_FILE}\n"
    )

    report.write(
        f"Tableau-ready dataset: {TABLEAU_FILE}\n"
    )

print("\nModule 2 completed successfully.")