"""
Module 3: Education KPI Engineering
--------------------------------------
Builds the 25-column Tableau-ready KPI schema from the cleaned dataset
and filters down to the top 50 universities by composite performance.

KPI formulas:
    Global Ranking Score   = provided per-university composite rank score
    Research Impact Score  = provided per-university research composite
    Teaching Quality Score = average(Teaching, Faculty_Student_Ratio)
    Ranking KPI            = Global Ranking Score
    Research KPI           = Research Impact Score
    Teaching KPI            = round(Teaching Quality Score)
    Overall KPI Score       = 0.4*Ranking KPI + 0.3*Research KPI + 0.3*Teaching KPI
    Performance Category    = Excellent (>=90) / Very Good (>=75) /
                               Good (>=60) / Average (<60)

Input:
    university_cleaned.csv

Output:
    university_final_dataset_top50.csv
"""

import pandas as pd

INPUT_PATH = "university_cleaned.csv"
OUTPUT_PATH = "university_final_dataset_top50.csv"
TOP_N = 50


def categorize(score: float) -> str:
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Very Good"
    elif score >= 60:
        return "Good"
    else:
        return "Average"


def build_kpi_table(df: pd.DataFrame) -> pd.DataFrame:
    kpi = pd.DataFrame()

    kpi["University"] = df["Name_QS"]
    kpi["Country"] = df["Country/Territory"].fillna(df["Country"])
    kpi["QS_Rank"] = df["QS_Rank_Numeric"]
    kpi["Overall_Score_QS"] = pd.to_numeric(df["Overall SCORE"], errors="coerce")
    kpi["Academic_Reputation"] = df["Academic Reputation SCORE"]
    kpi["Employer_Reputation"] = df["Employer Reputation SCORE"]
    kpi["Citations_per_Faculty"] = df["Citations per Faculty SCORE"]
    kpi["Faculty_Student_Ratio"] = df["Faculty Student Ratio SCORE"]
    kpi["International_Students"] = df["International Students"] * 100
    kpi["THE_Rank"] = df["THE_Rank_Numeric"]
    kpi["Overall_Score"] = df["Overall Score"]
    kpi["Teaching"] = df["Teaching"]
    kpi["Research"] = df["Research Environment"]
    kpi["Citations"] = df["Research Quality"]
    kpi["Industry_Income"] = df["Industry Impact"]
    kpi["International_Outlook"] = df["International Outlook"]

    # Composite scores: average QS + THE rank-based scores as the "global" score
    qs_norm = 100 - (kpi["QS_Rank"] / kpi["QS_Rank"].max() * 100)
    the_norm = 100 - (kpi["THE_Rank"] / kpi["THE_Rank"].max() * 100)
    kpi["Global Ranking Score"] = ((qs_norm + the_norm) / 2).round(2)

    kpi["Research Impact Score"] = (
        (kpi["Citations_per_Faculty"] + kpi["Citations"] + kpi["Research"]) / 3
    ).round(2)

    kpi["Teaching Quality Score"] = (
        (kpi["Teaching"] + kpi["Faculty_Student_Ratio"]) / 2
    ).round(2)

    kpi["Ranking KPI"] = kpi["Global Ranking Score"]
    kpi["Research KPI"] = kpi["Research Impact Score"]
    kpi["Teaching KPI"] = kpi["Teaching Quality Score"].round(0)

    kpi["Overall KPI Score"] = (
        0.4 * kpi["Ranking KPI"] + 0.3 * kpi["Research KPI"] + 0.3 * kpi["Teaching KPI"]
    ).round(2)

    return kpi


def main():
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded cleaned dataset: {df.shape}")

    kpi = build_kpi_table(df)
    kpi = kpi.dropna(subset=["Overall KPI Score"])

    # Keep top N universities by Overall KPI Score
    kpi = kpi.sort_values("Overall KPI Score", ascending=False).head(TOP_N).reset_index(drop=True)
    kpi["KPI Rank"] = kpi["Overall KPI Score"].rank(ascending=False, method="min").astype(int)
    kpi["Performance Category"] = kpi["Overall KPI Score"].apply(categorize)

    final_cols = [
        "University", "Country", "QS_Rank", "Overall_Score_QS", "Academic_Reputation",
        "Employer_Reputation", "Citations_per_Faculty", "Faculty_Student_Ratio",
        "International_Students", "THE_Rank", "Overall_Score", "Teaching", "Research",
        "Citations", "Industry_Income", "International_Outlook", "Global Ranking Score",
        "Research Impact Score", "Teaching Quality Score", "Ranking KPI", "Research KPI",
        "Teaching KPI", "Overall KPI Score", "KPI Rank", "Performance Category",
    ]
    kpi = kpi[final_cols]

    print(f"Final KPI dataset (Top {TOP_N}): {kpi.shape}")
    kpi.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
