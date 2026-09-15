import pandas as pd
from pathlib import Path

# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "university_cleaned.csv"

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Loading Clean Dataset...")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print("\nDataset Shape")
print(df.shape)

print("\nColumn Names")
print(df.columns.tolist())

print("\nFirst 5 Rows")
print(df.head())

print("\nData Types")
print(df.dtypes)

# =====================================================
# Step 2: General Statistics
# =====================================================

print("\n" + "=" * 60)
print("Step 2: General Statistics")
print("=" * 60)

# Number of universities
print("\nTotal Universities:")
print(df["University"].nunique())

# Number of countries
print("\nTotal Countries:")
print(df["Country"].nunique())

# Average Scores
print("\nAverage QS Overall Score:")
print(round(df["Overall_QS"].mean(), 2))

print("\nAverage THE Overall Score:")
print(round(df["Overall_THE"].mean(), 2))

# Highest Scores
print("\nHighest QS Overall Score:")
print(df["Overall_QS"].max())

print("\nHighest THE Overall Score:")
print(df["Overall_THE"].max())

# Lowest Scores
print("\nLowest QS Overall Score:")
print(df["Overall_QS"].min())

print("\nLowest THE Overall Score:")
print(df["Overall_THE"].min())

# Average Rank
print("\nAverage QS Rank:")
print(round(df["Rank_QS"].mean(), 2))

print("\nAverage THE Rank:")
print(round(df["Rank_THE"].mean(), 2))

# =====================================================
# Step 3: Missing Value Analysis
# =====================================================

print("\n" + "=" * 60)
print("Step 3: Missing Value Analysis")
print("=" * 60)

missing = df.isnull().sum()

missing_percent = (
    missing / len(df) * 100
).round(2)

missing_summary = pd.DataFrame({
    "Missing Values": missing,
    "Percentage": missing_percent
})

missing_summary = (
    missing_summary
    .sort_values(
        by="Missing Values",
        ascending=False
    )
)

print(missing_summary)

# Only show columns having missing values

print("\nColumns having Missing Values\n")

print(
    missing_summary[
        missing_summary["Missing Values"] > 0
    ]
)

# =====================================================
# Step 4: Top Universities
# =====================================================

print("\n" + "=" * 60)
print("Step 4: Top Universities")
print("=" * 60)

# ------------------------------
# Top 10 QS Universities
# ------------------------------

top_qs = (
    df[
        ["University", "Country", "Rank_QS", "Overall_QS"]
    ]
    .dropna(subset=["Rank_QS"])
    .sort_values("Rank_QS")
    .head(10)
)

print("\nTop 10 Universities (QS)")
print(top_qs)

# ------------------------------
# Top 10 THE Universities
# ------------------------------

top_the = (
    df[
        ["University", "Country", "Rank_THE", "Overall_THE"]
    ]
    .dropna(subset=["Rank_THE"])
    .sort_values("Rank_THE")
    .head(10)
)

print("\nTop 10 Universities (THE)")
print(top_the)

# =====================================================
# Step 5: Country-wise Analysis
# =====================================================

print("\n" + "=" * 60)
print("Step 5: Country-wise Analysis")
print("=" * 60)

# -----------------------------------------------------
# 5.1 Number of Universities per Country
# -----------------------------------------------------

universities_by_country = (
    df.groupby("Country")["University"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nTop 10 Countries by Number of Universities")

print(
    universities_by_country
    .head(10)
)

# -----------------------------------------------------
# 5.2 Average QS Score by Country
# -----------------------------------------------------

qs_by_country = (
    df.dropna(subset=["Overall_QS"])
    .groupby("Country")
    .agg(
        Universities=("University", "nunique"),
        Average_QS_Score=("Overall_QS", "mean")
    )
    .sort_values(
        "Average_QS_Score",
        ascending=False
    )
)

print("\nTop 10 Countries by Average QS Score")

print(
    qs_by_country
    .head(10)
)

# -----------------------------------------------------
# 5.3 Average THE Score by Country
# -----------------------------------------------------

the_by_country = (
    df.dropna(subset=["Overall_THE"])
    .groupby("Country")
    .agg(
        Universities=("University", "nunique"),
        Average_THE_Score=("Overall_THE", "mean")
    )
    .sort_values(
        "Average_THE_Score",
        ascending=False
    )
)

print("\nTop 10 Countries by Average THE Score")

print(
    the_by_country
    .head(10)
)