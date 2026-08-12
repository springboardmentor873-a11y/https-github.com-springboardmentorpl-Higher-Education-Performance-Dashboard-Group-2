import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. Load QS dataset
# --------------------------------------------------

qs_file = DATA_DIR / "2026 QS World University Rankings.csv"

qs = pd.read_csv(qs_file)

print("\nQS DATASET")
print("-" * 50)
print("Rows:", len(qs))
print("Columns:", len(qs.columns))
print("\nColumns:")
print(qs.columns.tolist())


# --------------------------------------------------
# 3. Load THE dataset
# --------------------------------------------------

the_file = DATA_DIR / "THE World University Rankings 2026.xlsx"

the = pd.read_excel(the_file)

print("\nTHE DATASET")
print("-" * 50)
print("Rows:", len(the))
print("Columns:", len(the.columns))
print("\nColumns:")
print(the.columns.tolist())


# --------------------------------------------------
# 4. Basic duplicate check
# --------------------------------------------------

print("\nDUPLICATE CHECK")
print("-" * 50)

print("QS duplicate rows:", qs.duplicated().sum())
print("THE duplicate rows:", the.duplicated().sum())


# --------------------------------------------------
# 5. Basic missing-value check
# --------------------------------------------------

print("\nMISSING VALUES — QS")
print("-" * 50)
print(qs.isna().sum())


print("\nMISSING VALUES — THE")
print("-" * 50)
print(the.isna().sum())


# --------------------------------------------------
# 6. Save combined raw datasets
# --------------------------------------------------

qs["Source"] = "QS"
the["Source"] = "THE"

# Put both datasets into one raw file.
# Since their columns are different, pandas will preserve
# all columns and fill unavailable fields with NaN.

raw_data = pd.concat(
    [qs, the],
    ignore_index=True,
    sort=False
)

raw_file = OUTPUT_DIR / "university_raw_data.csv"

raw_data.to_csv(raw_file, index=False)

print("\nRAW DATA CREATED")
print("-" * 50)
print("File:", raw_file)
print("Rows:", len(raw_data))
print("Columns:", len(raw_data.columns))

# --------------------------------------------------
# 7. Inspect university and country fields
# --------------------------------------------------

print("\nQS UNIVERSITY / COUNTRY SAMPLE")
print("-" * 50)
print(qs[["Institution Name", "Country/Territory"]].head(20).to_string(index=False))

print("\nTHE UNIVERSITY / COUNTRY SAMPLE")
print("-" * 50)
print(the[["Name", "Country"]].head(20).to_string(index=False))


# --------------------------------------------------
# 8. Check unique countries
# --------------------------------------------------

print("\nQS COUNTRIES")
print("-" * 50)
print(sorted(qs["Country/Territory"].dropna().unique()))

print("\nTHE COUNTRIES")
print("-" * 50)
print(sorted(the["Country"].dropna().unique()))

# --------------------------------------------------
# 9. Compare country names between QS and THE
# --------------------------------------------------

qs_countries = set(qs["Country/Territory"].dropna().unique())
the_countries = set(the["Country"].dropna().unique())

print("\nCOUNTRIES ONLY IN QS")
print("-" * 50)

print(sorted(qs_countries - the_countries))


print("\nCOUNTRIES ONLY IN THE")
print("-" * 50)

print(sorted(the_countries - qs_countries))


print("\nCOUNTRY MATCH SUMMARY")
print("-" * 50)

print("QS unique countries:", len(qs_countries))
print("THE unique countries:", len(the_countries))
print("Common countries:", len(qs_countries & the_countries))

# --------------------------------------------------
# 10. Standardize country names
# --------------------------------------------------

country_mapping = {
    # QS -> common standardized name
    "China (Mainland)": "China",
    "Hong Kong SAR, China": "Hong Kong",
    "Iran (Islamic Republic of)": "Iran",
    "Macao SAR, China": "Macao",
    "Republic of Korea": "South Korea",
    "Syrian Arab Republic": "Syria",
    "Türkiye": "Turkey",
    "United States of America": "United States",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Viet Nam": "Vietnam",

    # Other standardized spellings
    "United States": "United States",
    "South Korea": "South Korea",
    "China": "China",
    "Iran": "Iran",
    "Syria": "Syria",
    "Turkey": "Turkey",
    "Vietnam": "Vietnam",
}


# Apply mapping
qs["Standard Country"] = (
    qs["Country/Territory"]
    .replace(country_mapping)
)

the["Standard Country"] = (
    the["Country"]
    .replace(country_mapping)
)


# --------------------------------------------------
# 11. Validate country standardization
# --------------------------------------------------

qs_standard_countries = set(qs["Standard Country"].dropna().unique())
the_standard_countries = set(the["Standard Country"].dropna().unique())

print("\nSTANDARDIZED COUNTRY CHECK")
print("-" * 50)

print("QS unique countries:", len(qs_standard_countries))
print("THE unique countries:", len(the_standard_countries))

print("\nCountries still different between datasets:")

print(
    sorted(
        qs_standard_countries - the_standard_countries
    )
)

print("\nCountries only in THE:")

print(
    sorted(
        the_standard_countries - qs_standard_countries
    )
)

# --------------------------------------------------
# 12. Normalize university names
# --------------------------------------------------

import re


def normalize_university_name(name):
    """
    Normalize university names for matching.

    This does NOT change the original university name.
    It creates a separate matching key.
    """

    if pd.isna(name):
        return ""

    name = str(name).strip().lower()

    # Remove text inside parentheses
    name = re.sub(r"\([^)]*\)", "", name)

    # Remove common leading article
    name = re.sub(r"^the\s+", "", name)

    # Replace ampersand with 'and'
    name = name.replace("&", "and")

    # Remove punctuation
    name = re.sub(r"[^\w\s]", " ", name)

    # Normalize whitespace
    name = re.sub(r"\s+", " ", name).strip()

    return name


qs["University Match Name"] = (
    qs["Institution Name"]
    .apply(normalize_university_name)
)

the["University Match Name"] = (
    the["Name"]
    .apply(normalize_university_name)
)


# --------------------------------------------------
# 13. Measure university-name matches
# --------------------------------------------------

qs_names = set(qs["University Match Name"])
the_names = set(the["University Match Name"])

common_names = qs_names & the_names

print("\nUNIVERSITY NAME MATCHING")
print("-" * 50)

print("QS universities:", len(qs_names))
print("THE universities:", len(the_names))
print("Normalized exact matches:", len(common_names))

print(
    "QS match percentage:",
    round(len(common_names) / len(qs_names) * 100, 2),
    "%"
)

print(
    "THE match percentage:",
    round(len(common_names) / len(the_names) * 100, 2),
    "%"
)

# --------------------------------------------------
# 14. Merge QS and THE using INNER JOIN
# --------------------------------------------------

matched_data = pd.merge(
    qs,
    the,
    on=["University Match Name", "Standard Country"],
    how="inner",
    suffixes=("_QS", "_THE")
)


# --------------------------------------------------
# 15. Create Tableau-ready column structure
# --------------------------------------------------

final_data = pd.DataFrame({
    # University information
    "University Name": matched_data["Institution Name"],
    "Country": matched_data["Standard Country"],
    "Region": matched_data["Region"],

    # QS ranking information
    "QS Rank": matched_data["2026 Rank"],
    "QS Previous Rank": matched_data["Previous Rank"],
    "QS Overall Score": matched_data["Overall SCORE"],

    "QS Academic Reputation Score": matched_data["AR SCORE"],
    "QS Academic Reputation Rank": matched_data["AR RANK"],

    "QS Employer Reputation Score": matched_data["ER SCORE"],
    "QS Employer Reputation Rank": matched_data["ER RANK"],

    "QS Faculty Student Ratio Score": matched_data["FSR SCORE"],
    "QS Faculty Student Ratio Rank": matched_data["FSR RANK"],

    "QS Citations per Faculty Score": matched_data["CPF SCORE"],
    "QS Citations per Faculty Rank": matched_data["CPF RANK"],

    "QS International Faculty Ratio Score": matched_data["IFR SCORE"],
    "QS International Faculty Ratio Rank": matched_data["IFR RANK"],

    "QS International Student Ratio Score": matched_data["ISR SCORE"],
    "QS International Student Ratio Rank": matched_data["ISR RANK"],

    "QS International Student Diversity Score": matched_data["ISD SCORE"],
    "QS International Student Diversity Rank": matched_data["ISD RANK"],

    "QS International Research Network Score": matched_data["IRN SCORE"],
    "QS International Research Network Rank": matched_data["IRN RANK"],

    "QS Employment Outcomes Score": matched_data["EO SCORE"],
    "QS Employment Outcomes Rank": matched_data["EO RANK"],

    "QS Sustainability Score": matched_data["SUS SCORE"],
    "QS Sustainability Rank": matched_data["SUS RANK"],

    # THE ranking information
    "THE Rank": matched_data["Rank"],
    "THE Overall Score": matched_data["Overall Score"],

    "THE Student Population": matched_data["Student Population"],
    "THE Students to Staff Ratio": matched_data["Students to Staff Ratio"],
    "THE International Students": matched_data["International Students"],
    "THE Female to Male Ratio": matched_data["Female to Male Ratio"],

    "THE Teaching Score": matched_data["Teaching"],
    "THE Research Environment Score": matched_data["Research Environment"],
    "THE Research Quality Score": matched_data["Research Quality"],
    "THE Industry Impact Score": matched_data["Industry Impact"],
    "THE International Outlook Score": matched_data["International Outlook"],

    "Ranking Year": matched_data["Year"]
})


# --------------------------------------------------
# 16. Remove duplicate universities
# --------------------------------------------------

final_data = final_data.drop_duplicates(
    subset=["University Name", "Country"]
)


# --------------------------------------------------
# 17. Sort by QS ranking
# --------------------------------------------------

final_data = final_data.sort_values(
    by="QS Rank",
    ascending=True
).reset_index(drop=True)


# --------------------------------------------------
# 18. Save Tableau-ready dataset
# --------------------------------------------------

cleaned_file = OUTPUT_DIR / "university_cleaned.csv"

final_data.to_csv(
    cleaned_file,
    index=False
)


# --------------------------------------------------
# 19. Final validation
# --------------------------------------------------

print("\nFINAL DATASET")
print("-" * 50)

print("Rows:", len(final_data))
print("Columns:", len(final_data.columns))

print("\nDuplicate rows:", final_data.duplicated().sum())

print("\nMissing values:")

missing_values = final_data.isna().sum()

print(
    missing_values[
        missing_values > 0
    ].sort_values(ascending=False)
)

total_cells = final_data.shape[0] * final_data.shape[1]
missing_cells = final_data.isna().sum().sum()

missing_percentage = (
    missing_cells / total_cells
) * 100

print(
    "\nOverall missing-value percentage:",
    round(missing_percentage, 2),
    "%"
)

print("\nFINAL COLUMNS")
print("-" * 50)

print(final_data.columns.tolist())

print("\nCLEANED DATASET CREATED")
print("-" * 50)

print("File:", cleaned_file)