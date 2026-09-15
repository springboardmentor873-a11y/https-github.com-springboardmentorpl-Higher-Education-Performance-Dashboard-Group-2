from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "processed" / "university_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "university_final_dataset_all_kpis.xlsx"
LEGACY_OUTPUT_FILE = OUTPUT_DIR / "university_final_dataset.xlsx"


def row_average(frame, columns):
    """Match the shipped KPI rule: skip missing inputs, then round to 2 places."""
    return frame[columns].apply(pd.to_numeric, errors="coerce").mean(axis=1).round(2)


def build_dataset():
    df = pd.read_csv(INPUT_FILE)

    df["Overall_QS"] = pd.to_numeric(df["Overall_QS"], errors="coerce")
    df["Overall_THE"] = pd.to_numeric(df["Overall_THE"], errors="coerce")

    df["Global_Ranking_Score"] = row_average(df, ["Overall_QS", "Overall_THE"])
    df["Academic_Excellence_Score"] = row_average(
        df,
        [
            "Academic Reputation Score",
            "Faculty Student Score",
            "Citations per Faculty Score",
            "scores_teaching",
            "scores_research",
            "scores_citations",
        ],
    )
    df["Research_Impact_Score"] = row_average(
        df,
        [
            "scores_citations",
            "Citations per Faculty Score",
            "International Research Network Score",
        ],
    )
    df["Faculty_to_Student_Ratio"] = pd.to_numeric(
        df["stats_student_staff_ratio"], errors="coerce"
    )
    df["International_Student_Percentage"] = pd.to_numeric(
        df["stats_pc_intl_students"], errors="coerce"
    )
    df["Academic_Reputation_KPI"] = pd.to_numeric(
        df["Academic Reputation Score"], errors="coerce"
    )
    df["Research_Productivity_Index"] = row_average(
        df,
        [
            "scores_research",
            "Citations per Faculty Score",
            "International Research Network Score",
        ],
    )

    return df


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = build_dataset()
    df.to_excel(OUTPUT_FILE, index=False)
    # Keep the earlier filename available for scripts that still reference it.
    df.to_excel(LEGACY_OUTPUT_FILE, index=False)
    print(f"Wrote {OUTPUT_FILE}")
    print(f"Wrote {LEGACY_OUTPUT_FILE}")
    print(f"Rows: {len(df)}; columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
