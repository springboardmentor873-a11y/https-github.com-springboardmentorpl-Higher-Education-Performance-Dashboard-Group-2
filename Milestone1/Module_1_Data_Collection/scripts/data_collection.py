"""
EduVision_DV - Module 1: Education Data Collection
Purpose:
    1. Load QS and THE source files.
    2. Keep only 2026 data.
    3. Standardize university/country matching keys.
    4. Merge QS + THE using normalized university name + country.
    5. Export university_raw_data.csv.

Expected input files:
    raw_data/QS_2026.csv
    raw_data/THE_2026.csv

Run:
    python data_collection.py
"""

from pathlib import Path
import pandas as pd
import re
import unicodedata

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "raw_data"
OUT = BASE / "processed_data"
OUT.mkdir(exist_ok=True)

QS_FILE = RAW / "QS_2026.csv"
THE_FILE = RAW / "THE_2026.csv"

def normalize_name(value):
    s = "" if pd.isna(value) else str(value)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()
    s = s.replace("&", " and ")
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\bthe\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def normalize_country(value):
    s = "" if pd.isna(value) else str(value).strip().lower()
    aliases = {
        "united states of america": "United States",
        "united states": "United States",
        "usa": "United States",
        "us": "United States",
        "united kingdom": "United Kingdom",
        "uk": "United Kingdom",
        "england": "United Kingdom",
    }
    return aliases.get(s, str(value).strip() if not pd.isna(value) else "")

qs = pd.read_csv(QS_FILE)
the = pd.read_csv(THE_FILE)

# Safety check: only THE 2026 records are allowed into the integrated dataset.
the = the[the["Year"].astype(str).str.strip() == "2026"].copy()

qs["University_Key"] = qs["Institution Name"].map(normalize_name)
the["University_Key"] = the["Name"].map(normalize_name)
qs["Country_Standardized"] = qs["Country/Territory"].map(normalize_country)
the["Country_Standardized"] = the["Country"].map(normalize_country)

qs = qs.rename(columns={
    "2026 Rank": "QS_Rank",
    "Previous Rank": "QS_Previous_Rank",
    "Institution Name": "QS_University_Name",
    "Country/Territory": "QS_Country",
    "Region": "QS_Region",
    "Size": "QS_Size",
    "Focus": "QS_Focus",
    "Research": "QS_Research_Level",
    "Status": "QS_Status",
    "AR SCORE": "QS_Academic_Reputation_Score",
})

the = the.rename(columns={
    "Rank": "THE_Rank",
    "Name": "THE_University_Name",
    "Country": "THE_Country",
    "Student Population": "THE_Student_Population",
    "Students to Staff Ratio": "THE_Students_to_Staff_Ratio",
    "International Students": "THE_International_Students",
    "Female to Male Ratio": "THE_Female_to_Male_Ratio",
    "Overall Score": "THE_Overall_Score",
    "Teaching": "THE_Teaching",
    "Research Environment": "THE_Research_Environment",
    "Research Quality": "THE_Research_Quality",
    "Industry Impact": "THE_Industry_Impact",
    "International Outlook": "THE_International_Outlook",
    "Year": "THE_Year",
})

merged = qs.merge(
    the,
    on=["University_Key", "Country_Standardized"],
    how="outer",
    indicator=True,
)

merged["University_Name"] = merged["QS_University_Name"].fillna(merged["THE_University_Name"])
merged["Country"] = merged["Country_Standardized"]
merged["Year"] = 2026
merged["Data_Source"] = merged["_merge"].map({
    "both": "QS + THE",
    "left_only": "QS only",
    "right_only": "THE only"
})
merged["QS_THE_Match_Status"] = merged["_merge"].map({
    "both": "Matched",
    "left_only": "QS record not matched in THE",
    "right_only": "THE record not matched in QS"
})

# Drop technical merge keys from the final deliverable.
drop_cols = ["University_Key", "Country_Standardized", "_merge"]
result = merged.drop(columns=drop_cols, errors="ignore")

result.to_csv(OUT / "university_raw_data.csv", index=False)
print(f"Created: {OUT / 'university_raw_data.csv'}")
print(f"Rows: {len(result):,}")
print("THE years included:", sorted(result["THE_Year"].dropna().unique().tolist()))
