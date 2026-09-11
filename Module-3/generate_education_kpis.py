import pandas as pd
import numpy as np

# Load cleaned dataset
df = pd.read_csv("university_cleaned.csv")

# -----------------------------------
# 1. Global Ranking Score
# -----------------------------------

if "normalized_ranking_score" in df.columns:
    df["global_ranking_score"] = df["global_ranking_score"].fillna(
        df["normalized_ranking_score"]
    )

# -----------------------------------
# 2. Research Impact Score
# -----------------------------------

df["research_impact_score"] = (
    df["citations_score"] * 0.6 +
    df["research_score"] * 0.4
)

# -----------------------------------
# 3. Faculty-to-Student Ratio
# -----------------------------------

df["faculty_to_student_ratio"] = df["faculty_to_student_ratio"].fillna(
    df["student_staff_ratio"]
    if "student_staff_ratio" in df.columns
    else np.nan
)

# -----------------------------------
# 4. International Student Percentage
# -----------------------------------

df["international_student_percentage"] = (
    df["international_student_percentage"]
)

# -----------------------------------
# 5. Academic Reputation Score
# -----------------------------------

df["academic_reputation_score"] = (
    df["academic_reputation_score"].fillna(
        df["academic_reputation"]
    )
)

# -----------------------------------
# 6. Research Productivity Index
# -----------------------------------

df["research_productivity_index"] = (
    df["research_score"] * 0.5 +
    df["citations_score"] * 0.5
)

# -----------------------------------
# Select KPI columns
# -----------------------------------

kpi_columns = [
    "university_name",
    "country",
    "region",
    "global_ranking_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index"
]

kpi_df = df[kpi_columns]

# Display
print(kpi_df.head())

# Save KPI dataset
kpi_df.to_csv("university_kpis.csv", index=False)

print("KPI dataset created successfully!")