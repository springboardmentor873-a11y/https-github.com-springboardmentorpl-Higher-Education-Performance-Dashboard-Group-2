import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FINAL_DATASET = (
    BASE_DIR
    / "data"
    / "processed"
    / "university_final_dataset.xlsx"
)

CLEAN_DATASET = (
    BASE_DIR
    / "data"
    / "processed"
    / "university_cleaned.csv"
)

INPUT_FILE = FINAL_DATASET if FINAL_DATASET.exists() else CLEAN_DATASET

OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "visualizations"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Load Dataset
# ============================================================

print("=" * 60)
print("Loading Final Dataset...")
print("=" * 60)

if INPUT_FILE.suffix == ".xlsx":
    df = pd.read_excel(INPUT_FILE)
else:
    df = pd.read_csv(INPUT_FILE)

if "Global_Ranking_Score" not in df.columns:
    df["Global_Ranking_Score"] = (
        df[["Overall_QS", "Overall_THE"]]
        .apply(pd.to_numeric, errors="coerce")
        .mean(axis=1, skipna=True)
        .round(2)
    )

print("\nDataset Shape:")
print(df.shape)


# ============================================================
# Visualization 1
# Top 10 Universities by Global Ranking Score
# ============================================================

print("\n" + "=" * 60)
print("Visualization 1: Top 10 Global Universities")
print("=" * 60)


top_10 = (
    df[
        [
            "University",
            "Country",
            "Global_Ranking_Score"
        ]
    ]
    .dropna(
        subset=["Global_Ranking_Score"]
    )
    .sort_values(
        by="Global_Ranking_Score",
        ascending=False
    )
    .head(10)
)


# Reverse order for horizontal bar chart

top_10 = top_10.sort_values(
    by="Global_Ranking_Score",
    ascending=True
)


# ============================================================
# Create Chart
# ============================================================

plt.figure(figsize=(12, 7))

plt.barh(
    top_10["University"],
    top_10["Global_Ranking_Score"]
)

plt.xlabel("Global Ranking Score")

plt.ylabel("University")

plt.title(
    "Top 10 Universities by Global Ranking Score",
    fontsize=16,
    fontweight="bold"
)

plt.xlim(
    0,
    105
)

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()


# ============================================================
# Save Visualization
# ============================================================

OUTPUT_FILE = (
    OUTPUT_DIR
    / "top_10_global_universities.png"
)

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nVisualization generated successfully!")

print("\nOutput:")
print(OUTPUT_FILE)

print("=" * 60)