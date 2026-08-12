from pathlib import Path
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA = BASE_DIR / "data" / "processed"

INPUT_FILE = RAW_DATA / "university_raw_data.csv"

# Create processed folder if it doesn't exist
PROCESSED_DATA.mkdir(exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Loading Raw Dataset...")
print("=" * 60)

df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")

# =====================================================
# Basic Information
# =====================================================

print("\nDataset Shape")
print(df.shape)

print("\nColumn Names")
print(df.columns.tolist())

print("\nData Types")
print(df.dtypes)

print("\nDataset Info")
df.info()

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nFirst 5 Rows")
print(df.head())

# =====================================================
# Step 2: Basic Cleaning
# =====================================================

print("\n" + "=" * 60)
print("Step 2: Basic Data Cleaning")
print("=" * 60)

# Remove duplicate rows
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)

print(f"Duplicate rows removed: {before - after}")

# Clean text columns
text_columns = ["University", "Country"]

for col in text_columns:
    df[col] = (
        df[col]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

print("\nMissing values after text cleaning:")
print(df[text_columns].isnull().sum())

# Display rows with missing Country
missing_country = df[df["Country"].isna()]

print("\nRows with missing Country:")
print(missing_country[["University", "Country"]])

# =====================================================
# Step 3: Clean Ranking Columns
# =====================================================

print("\n" + "=" * 60)
print("Step 3: Cleaning Ranking Columns")
print("=" * 60)

import numpy as np

def clean_rank(rank):
    """
    Convert ranking values to numeric.
    Examples:
    =336      -> 336
    681-690   -> 685.5
    201–250   -> 225.5
    1501+     -> 1501
    Reporter  -> NaN
    """

    if pd.isna(rank):
        return np.nan

    rank = str(rank).strip()

    # Reporter
    if rank.lower() == "reporter":
        return np.nan

    # Remove "="
    rank = rank.replace("=", "")

    # Handle 1501+
    if rank.endswith("+"):
        return float(rank[:-1])

    # Support both hyphen (-) and en dash (–)
    if "-" in rank or "–" in rank:
        separator = "–" if "–" in rank else "-"

        try:
            low, high = rank.split(separator)
            return (float(low) + float(high)) / 2
        except:
            return np.nan

    try:
        return float(rank)
    except:
        return np.nan


# Apply cleaning
df["Rank_QS"] = df["Rank_QS"].apply(clean_rank)
df["Rank_THE"] = df["Rank_THE"].apply(clean_rank)

print("\nRank_QS Data Type:", df["Rank_QS"].dtype)
print("Rank_THE Data Type:", df["Rank_THE"].dtype)

print("\nSample QS Ranks")
print(df["Rank_QS"].dropna().head(10))

print("\nSample THE Ranks")
print(df["Rank_THE"].dropna().head(10))

# =====================================================
# Step 4: Clean Overall Score Columns
# =====================================================

print("\n" + "=" * 60)
print("Step 4: Cleaning Overall Score Columns")
print("=" * 60)


def clean_score(score):
    """
    Convert score values to numeric.
    Examples:
    98.5 -> 98.5
    55.9–58.6 -> 57.25
    """
    if pd.isna(score):
        return np.nan

    score = str(score).strip()

    # Handle ranges
    if "–" in score or "-" in score:
        separator = "–" if "–" in score else "-"

        try:
            low, high = score.split(separator)
            return (float(low) + float(high)) / 2
        except:
            return np.nan

    try:
        return float(score)
    except:
        return np.nan


# Apply cleaning
df["Overall_QS"] = df["Overall_QS"].apply(clean_score)
df["Overall_THE"] = df["Overall_THE"].apply(clean_score)

print("\nOverall_QS Data Type:", df["Overall_QS"].dtype)
print("Overall_THE Data Type:", df["Overall_THE"].dtype)

print("\nSample Overall_QS")
print(df["Overall_QS"].dropna().head(10))

print("\nSample Overall_THE")
print(df["Overall_THE"].dropna().head(10))

# =====================================================
# Step 5: Clean Student Statistics
# =====================================================

print("\n" + "=" * 60)
print("Step 5: Cleaning Student Statistics")
print("=" * 60)

# -----------------------------------------------------
# Number of Students
# -----------------------------------------------------

df["stats_number_students"] = (
    df["stats_number_students"]
    .astype("string")
    .str.replace(",", "", regex=False)
)

df["stats_number_students"] = pd.to_numeric(
    df["stats_number_students"],
    errors="coerce"
)

# -----------------------------------------------------
# International Students Percentage
# -----------------------------------------------------

df["stats_pc_intl_students"] = (
    df["stats_pc_intl_students"]
    .astype("string")
    .str.replace("%", "", regex=False)
)

df["stats_pc_intl_students"] = pd.to_numeric(
    df["stats_pc_intl_students"],
    errors="coerce"
)

# -----------------------------------------------------
# Female : Male Ratio
# -----------------------------------------------------

ratio = (
    df["stats_female_male_ratio"]
    .astype("string")
    .str.split(":", expand=True)
)

df["female_percentage"] = pd.to_numeric(
    ratio[0].str.strip(),
    errors="coerce"
)

df["male_percentage"] = pd.to_numeric(
    ratio[1].str.strip(),
    errors="coerce"
)

# Remove old column
df.drop(columns=["stats_female_male_ratio"], inplace=True)

print("\nStudent Statistics Cleaned Successfully!")

print("\nData Types")
print(df[
    [
        "stats_number_students",
        "stats_pc_intl_students",
        "female_percentage",
        "male_percentage"
    ]
].dtypes)

print("\nSample Student Statistics")
print(
    df[
        [
            "stats_number_students",
            "stats_pc_intl_students",
            "female_percentage",
            "male_percentage"
        ]
    ].head(10)
)

# =====================================================
# Step 6: Final Validation
# =====================================================

print("\n" + "=" * 60)
print("Step 6: Final Dataset Validation")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nSummary Statistics:")
print(df.describe(include="all"))

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# =====================================================
# Step 7: Save Cleaned Dataset
# =====================================================

OUTPUT_FILE = PROCESSED_DATA / "university_cleaned.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 60)
print("Module 2 Completed Successfully!")
print("=" * 60)

print(f"\nCleaned dataset saved to:\n{OUTPUT_FILE}")