import pandas as pd
from pathlib import Path

# Module 2 - Data Cleaning and Transformation

# Get the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Define folders
PROCESSED_DIR = BASE_DIR / "Data" / "Processed Data"
CLEANED_DIR = BASE_DIR / "Data" / "Cleaned Data"
DOCS_DIR = BASE_DIR / "docs"

# Create required folders
CLEANED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Define input and output files
INPUT_FILE = PROCESSED_DIR / "university_raw_data.csv"
OUTPUT_FILE = CLEANED_DIR / "university_cleaned.csv"
REPORT_FILE = DOCS_DIR / "data_cleaning_report.txt"

print("Module 2 - Data Cleaning and Transformation")

# Check input file
if not INPUT_FILE.exists():
    print("Input file not found:")
    print(INPUT_FILE)
    raise SystemExit

# Load the Module 1 dataset
df = pd.read_csv(INPUT_FILE)

print("Input file:", INPUT_FILE)
print("Original rows:", len(df))
print("Original columns:", len(df.columns))

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nStandardized columns:")
for column in df.columns:
    print("-", column)

# Check required columns
required_columns = [
    "university_name",
    "country",
    "year",
    "ranking_source",
    "rank",
    "score"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nMissing required columns:")
    print(missing_columns)
    raise SystemExit

# Clean text fields
df["university_name"] = (
    df["university_name"]
    .astype("string")
    .str.strip()
)

df["country"] = (
    df["country"]
    .astype("string")
    .str.strip()
)

df["ranking_source"] = (
    df["ranking_source"]
    .astype("string")
    .str.strip()
)

# Remove exact duplicate rows
exact_duplicates = df.duplicated().sum()

df = df.drop_duplicates().copy()

print("\nExact duplicates removed:", exact_duplicates)

# Create a standardized university name
df["university_name_std"] = (
    df["university_name"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Create a standardized country name
df["country_std"] = (
    df["country"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Preserve the original ranking representation
df["rank_original"] = df["rank"].astype("string").str.strip()

# Convert ranking values to numeric values
# Numeric ranks remain unchanged.
# Ranking ranges are converted to their midpoint.
def convert_rank_to_numeric(value):

    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    if value == "" or value.lower() in ["nan", "na", "n/a", "-"]:
        return pd.NA

    # Handle ranking ranges such as 1201-1400
    if "-" in value:

        parts = value.split("-")

        if len(parts) == 2:

            try:
                lower = float(parts[0].strip())
                upper = float(parts[1].strip())

                return (lower + upper) / 2

            except ValueError:
                return pd.NA

    # Handle normal numeric ranking
    try:
        return float(value)

    except ValueError:
        return pd.NA


df["rank_numeric"] = df["rank_original"].apply(
    convert_rank_to_numeric
)

# Convert scores to numeric values
# A '-' means that the score was not provided.
df["score_original"] = df["score"].astype("string").str.strip()

df["score_numeric"] = pd.to_numeric(
    df["score_original"].replace("-", pd.NA),
    errors="coerce"
)

# Keep the original rank and score fields
# Replace them with cleaned numeric fields for analysis.
df["rank"] = df["rank_numeric"]
df["score"] = df["score_numeric"]

# Detect duplicate university-source records
duplicate_source_mask = df.duplicated(
    subset=[
        "university_name_std",
        "country_std",
        "ranking_source"
    ],
    keep=False
)

duplicate_source_count = duplicate_source_mask.sum()

print(
    "Duplicate university-source records found:",
    duplicate_source_count
)

# Normalize ranking values to a 0-100 scale
# Higher rank means a better position, so the rank scale is inverted.
def normalize_rank(series):

    numeric = pd.to_numeric(series, errors="coerce")

    minimum = numeric.min()
    maximum = numeric.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return numeric

    if maximum == minimum:
        return pd.Series(
            100.0,
            index=series.index
        )

    return (
        (maximum - numeric) /
        (maximum - minimum)
    ) * 100


# Normalize score values to a 0-100 scale
def normalize_score(series):

    numeric = pd.to_numeric(
        series,
        errors="coerce"
    )

    minimum = numeric.min()
    maximum = numeric.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return numeric

    if maximum == minimum:
        return pd.Series(
            100.0,
            index=series.index
        )

    return (
        (numeric - minimum) /
        (maximum - minimum)
    ) * 100


df["rank_normalized"] = normalize_rank(
    df["rank"]
)

df["score_normalized"] = normalize_score(
    df["score"]
)

# Create the missing-value report
missing_columns = [
    "university_name",
    "country",
    "year",
    "ranking_source",
    "rank",
    "score",
    "rank_normalized",
    "score_normalized"
]

missing_report = df[missing_columns].isna().sum()

print("\nMissing-value report:")

for column, count in missing_report.items():

    percentage = (
        count / len(df)
    ) * 100

    print(
        f"{column}: {count} "
        f"({percentage:.2f}%)"
    )

# Check ranking source distribution
print("\nRanking source distribution:")

print(
    df["ranking_source"].value_counts()
)

# Check rank ranges that were successfully converted
range_count = (
    df["rank_original"]
    .str.contains("-", na=False)
    .sum()
)

print(
    "\nRanking ranges detected:",
    range_count
)

# Save cleaned dataset
df.to_csv(
    OUTPUT_FILE,
    index=False
)

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
        f"Original rows: {len(pd.read_csv(INPUT_FILE))}\n"
    )

    report.write(
        f"Final rows: {len(df)}\n"
    )

    report.write(
        f"Original columns: {len(pd.read_csv(INPUT_FILE).columns)}\n"
    )

    report.write(
        f"Final columns: {len(df.columns)}\n\n"
    )

    report.write(
        f"Exact duplicates removed: "
        f"{exact_duplicates}\n"
    )

    report.write(
        f"Duplicate university-source records: "
        f"{duplicate_source_count}\n"
    )

    report.write(
        f"Ranking ranges detected: "
        f"{range_count}\n\n"
    )

    report.write(
        "Missing-value report:\n"
    )

    for column, count in missing_report.items():

        percentage = (
            count / len(df)
        ) * 100

        report.write(
            f"{column}: {count} "
            f"({percentage:.2f}%)\n"
        )

    report.write(
        "\nRanking source distribution:\n"
    )

    report.write(
        df["ranking_source"]
        .value_counts()
        .to_string()
    )

print("\nModule 2 completed successfully.")

print(
    "Cleaned dataset:",
    OUTPUT_FILE
)

print(
    "Cleaning report:",
    REPORT_FILE
)