import pandas as pd
import numpy as np
df = pd.read_csv(r"C:\Users\pujit\Downloads\EduVision\output\university_cleaned.csv")
df.columns = df.columns.str.strip()
print(df.shape)
print(df.columns.tolist())
print(df[["QS Rank", "THE Rank"]].dtypes)
print(df["QS Rank"].unique()[:50])
print(df["QS Rank"].value_counts().head(30))
def convert_qs_rank(value):
    value = str(value).strip()
    
    if "-" in value:
        start, end = value.split("-")
        return (float(start) + float(end)) / 2
    else:
        return float(value)
df["QS Rank Numeric"] = df["QS Rank"].apply(convert_qs_rank)
print(df[["QS Rank", "QS Rank Numeric"]].tail(50))
print(df["QS Rank Numeric"].dtype)
df["Global Ranking Score"] = (
    df["QS Overall Score"] +
    df["THE Overall Score"]
) / 2
print(
    df[
        [
            "Name",
            "QS Overall Score",
            "THE Overall Score",
            "Global Ranking Score"
        ]
    ].head(10)
)
research_cols = [
    "Citations per Faculty SCORE",
    "International Research Network SCORE",
    "THE Research Quality",
    "THE Research Environment"
]

print(df[research_cols].head())
print()
print(df[research_cols].dtypes)
df["Research Impact Score"] = (
    df["Citations per Faculty SCORE"]
    + df["International Research Network SCORE"]
    + df["THE Research Quality"]
    + df["THE Research Environment"]
) / 4
print(
    df[
        [
            "Name",
            "Citations per Faculty SCORE",
            "International Research Network SCORE",
            "THE Research Quality",
            "THE Research Environment",
            "Research Impact Score"
        ]
    ].head(10)
)
print(df["THE Student Staff Ratio"].head(10))
df["Faculty-to-Student Ratio"] = df["THE Student Staff Ratio"]
print(
    df[
        [
            "Name",
            "THE Student Staff Ratio",
            "Faculty-to-Student Ratio"
        ]
    ].head(10)
)
df["International Student Percentage"] = (
    df["THE International Students"]
    .str.replace("%", "", regex=False)
    .astype(float)
)
print(
    df[
        [
            "Name",
            "THE International Students",
            "International Student Percentage"
        ]
    ].head(10)
)
print(df["Academic Reputation SCORE"].head(10))
print(df["Academic Reputation SCORE"].dtype)
df["Academic Reputation Score"] = df["Academic Reputation SCORE"]
print(
    df[
        [
            "Name",
            "Academic Reputation Score"
        ]
    ].head(10)
)
df["Research Productivity Index"] = (
    df["Citations per Faculty SCORE"]
    + df["THE Research Quality"]
    + df["THE Research Environment"]
) / 3
print(
    df[
        [
            "Name",
            "Research Productivity Index"
        ]
    ].head(10)
)
kpi_columns = [
    "Global Ranking Score",
    "Research Impact Score",
    "Faculty-to-Student Ratio",
    "International Student Percentage",
    "Academic Reputation Score",
    "Research Productivity Index"
]

print(df[kpi_columns].head())
print(df[kpi_columns].isnull().sum())
df.to_excel(r"C:\Users\pujit\Downloads\EduVision\output\university_final_dataset.xlsx", index=False)
