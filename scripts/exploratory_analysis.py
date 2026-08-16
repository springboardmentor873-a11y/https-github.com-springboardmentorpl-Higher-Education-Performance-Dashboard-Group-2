import pandas as pd
from pathlib import Path

# Module 3 - Exploratory Data Analysis

# Get the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Define folders
RAW_DIR = BASE_DIR / "Data" / "Raw Data"
CLEANED_DIR = BASE_DIR / "Data" / "Cleaned Data"
PROCESSED_DIR = BASE_DIR / "Data" / "Processed Data"
DOCS_DIR = BASE_DIR / "docs"

# Create required folders
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Define input files
QS_FILE = RAW_DIR / "2026_QS_World University_Rankings.csv"
THE_FILE = RAW_DIR / "THE World University Rankings 2026.xlsx"
CLEANED_FILE = CLEANED_DIR / "university_cleaned.csv"

# Define output files
QS_OUTPUT = PROCESSED_DIR / "qs_eda_summary.csv"
THE_OUTPUT = PROCESSED_DIR / "the_eda_summary.csv"
COUNTRY_OUTPUT = PROCESSED_DIR / "country_ranking_summary.csv"
REPORT_FILE = DOCS_DIR / "module_03_eda_report.txt"

print("Module 3 - Exploratory Data Analysis")

# Check input files
if not QS_FILE.exists():
    print("QS dataset not found:")
    print(QS_FILE)
    raise SystemExit

if not THE_FILE.exists():
    print("THE dataset not found:")
    print(THE_FILE)
    raise SystemExit

if not CLEANED_FILE.exists():
    print("Cleaned dataset not found:")
    print(CLEANED_FILE)
    raise SystemExit

# Load datasets
print("\nLoading QS dataset...")
qs = pd.read_csv(QS_FILE)

print("QS rows:", len(qs))
print("QS columns:", len(qs.columns))

print("\nLoading THE dataset...")
the = pd.read_excel(THE_FILE)

print("THE rows:", len(the))
print("THE columns:", len(the.columns))

print("\nLoading cleaned common dataset...")
cleaned = pd.read_csv(CLEANED_FILE)

print("Cleaned rows:", len(cleaned))

# Standardize column names
# Standardize QS column names
qs.columns = (
    qs.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"_+", "_", regex=True)
)

# Standardize THE column names
the.columns = (
    the.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"_+", "_", regex=True)
)

# Convert important QS numeric columns
qs_numeric_columns = [
    "rank",
    "academic_reputation_score",
    "employer_reputation_score",
    "faculty_student_ratio_score",
    "citations_per_faculty_score",
    "international_faculty_score",
    "international_student_score",
    "international_students_diversity_score",
    "international_research_network_score",
    "employment_outcomes_score",
    "sustainability_score",
    "overall_score"
]

for column in qs_numeric_columns:

    if column in qs.columns:
        qs[column] = pd.to_numeric(
            qs[column],
            errors="coerce"
        )

# Convert important THE numeric columns
the_numeric_columns = [
    "rank",
    "student_population",
    "students_to_staff_ratio",
    "overall_score",
    "teaching",
    "research_environment",
    "research_quality",
    "industry_impact",
    "international_outlook"
]

for column in the_numeric_columns:

    if column in the.columns:
        the[column] = pd.to_numeric(
            the[column],
            errors="coerce"
        )

# QS analysis
print("\nQS Analysis")

qs_summary = pd.DataFrame({
    "metric": [
        "Total Universities",
        "Average Rank",
        "Median Rank",
        "Best Rank",
        "Average Overall Score",
        "Median Overall Score",
        "Average Academic Reputation",
        "Average Employer Reputation",
        "Average Faculty Student Ratio",
        "Average Citations per Faculty",
        "Average International Faculty",
        "Average International Student",
        "Average Employment Outcomes",
        "Average Sustainability"
    ],
    "value": [
        len(qs),
        qs["rank"].mean(),
        qs["rank"].median(),
        qs["rank"].min(),
        qs["overall_score"].mean(),
        qs["overall_score"].median(),
        qs["academic_reputation_score"].mean(),
        qs["employer_reputation_score"].mean(),
        qs["faculty_student_ratio_score"].mean(),
        qs["citations_per_faculty_score"].mean(),
        qs["international_faculty_score"].mean(),
        qs["international_student_score"].mean(),
        qs["employment_outcomes_score"].mean(),
        qs["sustainability_score"].mean()
    ]
})

print(qs_summary.to_string(index=False))

# THE analysis
print("\nTHE Analysis")

the_summary = pd.DataFrame({
    "metric": [
        "Total Universities",
        "Average Rank",
        "Median Rank",
        "Best Rank",
        "Average Overall Score",
        "Median Overall Score",
        "Average Teaching",
        "Average Research Environment",
        "Average Research Quality",
        "Average Industry Impact",
        "Average International Outlook",
        "Average Students to Staff Ratio"
    ],
    "value": [
        len(the),
        the["rank"].mean(),
        the["rank"].median(),
        the["rank"].min(),
        the["overall_score"].mean(),
        the["overall_score"].median(),
        the["teaching"].mean(),
        the["research_environment"].mean(),
        the["research_quality"].mean(),
        the["industry_impact"].mean(),
        the["international_outlook"].mean(),
        the["students_to_staff_ratio"].mean()
    ]
})

print(the_summary.to_string(index=False))

# QS country analysis
qs_country = (
    qs.groupby("country/territory")
    .agg(
        university_count=("name", "count"),
        average_rank=("rank", "mean"),
        average_score=("overall_score", "mean")
    )
    .reset_index()
    .sort_values(
        "average_rank"
    )
)

qs_country["ranking_source"] = "QS"

# THE country analysis
the_country = (
    the.groupby("country")
    .agg(
        university_count=("name", "count"),
        average_rank=("rank", "mean"),
        average_score=("overall_score", "mean")
    )
    .reset_index()
    .sort_values(
        "average_rank"
    )
)

the_country["ranking_source"] = "THE"

# Standardize country column
qs_country = qs_country.rename(
    columns={
        "country/territory": "country"
    }
)

# Combine country analysis
country_summary = pd.concat(
    [
        qs_country,
        the_country
    ],
    ignore_index=True
)

# Save outputs
qs_summary.to_csv(
    QS_OUTPUT,
    index=False
)

the_summary.to_csv(
    THE_OUTPUT,
    index=False
)

country_summary.to_csv(
    COUNTRY_OUTPUT,
    index=False
)

# Create report
with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "MODULE 3 - EXPLORATORY DATA ANALYSIS\n"
    )

    report.write(
        "====================================\n\n"
    )

    report.write(
        "QS DATASET\n"
    )

    report.write(
        f"Universities: {len(qs)}\n"
    )

    report.write(
        f"Average Rank: {qs['rank'].mean():.2f}\n"
    )

    report.write(
        f"Median Rank: {qs['rank'].median():.2f}\n"
    )

    report.write(
        f"Best Rank: {qs['rank'].min():.2f}\n"
    )

    report.write(
        f"Average Overall Score: "
        f"{qs['overall_score'].mean():.2f}\n\n"
    )

    report.write(
        "THE DATASET\n"
    )

    report.write(
        f"Universities: {len(the)}\n"
    )

    report.write(
        f"Average Rank: {the['rank'].mean():.2f}\n"
    )

    report.write(
        f"Median Rank: {the['rank'].median():.2f}\n"
    )

    report.write(
        f"Best Rank: {the['rank'].min():.2f}\n"
    )

    report.write(
        f"Average Overall Score: "
        f"{the['overall_score'].mean():.2f}\n\n"
    )

    report.write(
        "OUTPUT FILES\n"
    )

    report.write(
        f"QS summary: {QS_OUTPUT}\n"
    )

    report.write(
        f"THE summary: {THE_OUTPUT}\n"
    )

    report.write(
        f"Country summary: {COUNTRY_OUTPUT}\n"
    )

print("\nModule 3 completed successfully.")

print("QS summary:")
print(QS_OUTPUT)

print("THE summary:")
print(THE_OUTPUT)

print("Country summary:")
print(COUNTRY_OUTPUT)

print("EDA report:")
print(REPORT_FILE)