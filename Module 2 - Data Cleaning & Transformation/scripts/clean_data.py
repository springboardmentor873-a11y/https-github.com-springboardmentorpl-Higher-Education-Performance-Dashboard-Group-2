import pandas as pd
import numpy as np
import re
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

QS_FILE = DATA_DIR / "2026 QS World University Rankings.csv"
THE_FILE = DATA_DIR / "THE World University Rankings 2026.xlsx"

QS_OUTPUT = OUTPUT_DIR / "qs_cleaned_encoding_fixed.csv"
THE_OUTPUT = OUTPUT_DIR / "the_cleaned_encoding_fixed.csv"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def fix_encoding(value):
    """
    Fix common UTF-8 / Latin-1 mojibake while preserving
    legitimate text.
    """
    if pd.isna(value):
        return value

    value = str(value)

    try:
        if any(x in value for x in ["Ã", "Â", "â", "Å", "Ä"]):
            return value.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    return value


def clean_text(value):
    """
    Standardize text without destroying Unicode characters.
    """
    if pd.isna(value):
        return value

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)

    return value


def standardize_country(value):
    """
    Standardize country names only where necessary.
    """
    if pd.isna(value):
        return value

    value = clean_text(value)

    replacements = {
        "United States": "United States of America",
        "United States of America": "United States of America",
        "China": "China (Mainland)",
        "South Korea": "Republic of Korea",
        "Korea, Republic of": "Republic of Korea",
        "Russia": "Russian Federation",
        "Czech Republic": "Czechia",
    }

    return replacements.get(value, value)


# ============================================================
# QS RANK PARSER
# ============================================================

def parse_qs_rank(value):
    """
    Convert QS rank into numeric lower-bound rank.

    Examples:
        1         -> 1
        17        -> 17
        '101-150' -> 101
        '1401+'    -> 1401
        '-'       -> NaN
    """

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if value in {"-", "", "nan", "NaN"}:
        return np.nan

    # --------------------------------------------------------
    # 1401+
    # --------------------------------------------------------

    match = re.match(r"^(\d+)\+$", value)

    if match:
        return float(match.group(1))

    # --------------------------------------------------------
    # 101-150
    # --------------------------------------------------------

    match = re.match(r"^(\d+)\s*-\s*(\d+)$", value)

    if match:
        return float(match.group(1))

    # --------------------------------------------------------
    # Normal number
    # --------------------------------------------------------

    match = re.match(r"^(\d+(?:\.\d+)?)$", value)

    if match:
        return float(match.group(1))

    return np.nan


# ============================================================
# NUMERIC PARSER
# ============================================================

def parse_numeric(value):
    """
    Safely convert numeric values.

    '-' and empty values become NaN.
    """

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if value in {"", "-", "—", "nan", "NaN"}:
        return np.nan

    value = value.replace(",", "")

    try:
        return float(value)

    except (ValueError, TypeError):
        return np.nan


# ============================================================
# FEMALE / MALE RATIO PARSER
# ============================================================

def parse_ratio(value):
    """
    Convert THE Female to Male Ratio into numeric female percentage.

    Handles normal strings:

        '33 : 67' -> 33.0
        '39 : 61' -> 39.0
        '37 : 63' -> 37.0

    Also handles Excel/pandas timedelta values.

    Examples:

        1 day, 19:57:00 -> 43.0
        2 days, 00:52:00 -> 48.0
        2 days, 04:48:00 -> 52.0
        2 days, 05:47:00 -> 53.0

    Invalid or genuinely missing values become NaN.
    """

    # --------------------------------------------------------
    # Missing value
    # --------------------------------------------------------

    if pd.isna(value):
        return np.nan

    # ========================================================
    # CASE 1: pandas Timedelta
    # ========================================================

    if isinstance(value, pd.Timedelta):

        total_seconds = value.total_seconds()

        # Convert timedelta into total hours and minutes.
        #
        # Example:
        #
        # 1 day, 19:57:00
        #
        # 24 hours + 19 hours = 43
        # remaining minutes = 57
        #
        # Therefore:
        # 43 : 57
        #
        # Female percentage = 43

        total_hours = int(total_seconds // 3600)

        remaining_seconds = total_seconds % 3600

        minutes = int(round(remaining_seconds / 60))

        # Handle possible rounding to 60 minutes
        if minutes == 60:
            total_hours += 1
            minutes = 0

        # Validate that it represents a ratio adding to 100
        if (
            0 <= total_hours <= 100
            and 0 <= minutes <= 100
            and total_hours + minutes == 100
        ):
            return float(total_hours)

        return np.nan

    # ========================================================
    # CASE 2: Normal string ratio
    # ========================================================

    value_str = str(value).strip()

    match = re.match(
        r"^\s*(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\s*$",
        value_str
    )

    if match:

        female = float(match.group(1))
        male = float(match.group(2))

        # Validate ratio
        if (
            0 <= female <= 100
            and 0 <= male <= 100
            and abs((female + male) - 100) < 0.01
        ):
            return female

        return np.nan

    # ========================================================
    # CASE 3: String representation of timedelta
    # ========================================================

    if "day" in value_str:

        try:

            td = pd.to_timedelta(value_str)

            total_seconds = td.total_seconds()

            total_hours = int(total_seconds // 3600)

            remaining_seconds = total_seconds % 3600

            minutes = int(round(remaining_seconds / 60))

            if minutes == 60:
                total_hours += 1
                minutes = 0

            if (
                0 <= total_hours <= 100
                and 0 <= minutes <= 100
                and total_hours + minutes == 100
            ):
                return float(total_hours)

        except (ValueError, TypeError):
            pass

    return np.nan


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD ORIGINAL DATASETS
# ============================================================

print("=" * 70)
print("LOADING ORIGINAL DATASETS")
print("=" * 70)

qs = pd.read_csv(
    QS_FILE,
    encoding="utf-8-sig"
)

the = pd.read_excel(
    THE_FILE
)

print(f"QS shape: {qs.shape}")
print(f"THE shape: {the.shape}")


# ============================================================
# FIX TEXT ENCODING
# ============================================================

print("\nFixing text encoding...")

for col in qs.select_dtypes(
    include=["object", "string"]
).columns:

    qs[col] = qs[col].map(fix_encoding)


for col in the.select_dtypes(
    include=["object", "string"]
).columns:

    the[col] = the[col].map(fix_encoding)


# ============================================================
# CLEAN TEXT COLUMNS
# ============================================================

for col in qs.select_dtypes(
    include=["object", "string"]
).columns:

    qs[col] = qs[col].map(clean_text)


for col in the.select_dtypes(
    include=["object", "string"]
).columns:

    the[col] = the[col].map(clean_text)


# ============================================================
# QS RANKING COLUMNS
# ============================================================

print("\nProcessing QS ranking columns...")


# ------------------------------------------------------------
# Preserve original QS rank
# ------------------------------------------------------------

qs["2026_rank_original"] = qs["2026 Rank"]


# ------------------------------------------------------------
# Numeric rank for analysis
# ------------------------------------------------------------

qs["2026_rank"] = qs["2026 Rank"].apply(
    parse_qs_rank
)


# ------------------------------------------------------------
# Preserve display version
# ------------------------------------------------------------

qs["2026_rank_display"] = (
    qs["2026 Rank"].astype("string")
)


# ------------------------------------------------------------
# Convert Overall SCORE
# ------------------------------------------------------------

qs["overall_score"] = (
    qs["Overall SCORE"].apply(parse_numeric)
)


# ------------------------------------------------------------
# Flag whether QS score was actually published
# ------------------------------------------------------------

qs["overall_score_available"] = (
    qs["Overall SCORE"].apply(
        lambda x:
        False
        if pd.isna(x)
        or str(x).strip() in {"-", "—", ""}
        else True
    )
)


# ------------------------------------------------------------
# Convert other QS numeric columns
# ------------------------------------------------------------

qs_numeric_columns = [

    "Previous Rank",

    "AR SCORE",
    "AR RANK",

    "ER SCORE",
    "ER RANK",

    "FSR SCORE",
    "FSR RANK",

    "CPF SCORE",
    "CPF RANK",

    "IFR SCORE",
    "IFR RANK",

    "ISR SCORE",
    "ISR RANK",

    "ISD SCORE",
    "ISD RANK",

    "IRN SCORE",
    "IRN RANK",

    "EO SCORE",
    "EO RANK",

    "SUS SCORE",
    "SUS RANK",
]


for col in qs_numeric_columns:

    if col in qs.columns:

        qs[col] = qs[col].apply(
            parse_numeric
        )


# ============================================================
# QS COUNTRY
# ============================================================

if "Country/Territory" in qs.columns:

    qs["Country/Territory"] = (
        qs["Country/Territory"]
        .map(standardize_country)
    )


# ============================================================
# QS UNIVERSITY KEY
# ============================================================

qs["university_key"] = (
    qs["Institution Name"]
    .astype("string")
    .str.lower()
    .str.replace(
        r"\([^)]*\)",
        "",
        regex=True
    )
    .str.replace(
        "&",
        "and"
    )
    .str.replace(
        r"[^a-z0-9\s]",
        " ",
        regex=True
    )
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# THE RANK
# ============================================================

print("\nProcessing THE ranking columns...")

the["rank"] = (
    the["Rank"].apply(parse_qs_rank)
)


# ============================================================
# THE NUMERIC COLUMNS
# ============================================================

the_numeric_columns = [

    "Student Population",

    "Students to Staff Ratio",

    "Overall Score",

    "Teaching",

    "Research Environment",

    "Research Quality",

    "Industry Impact",

    "International Outlook",
]


for col in the_numeric_columns:

    if col in the.columns:

        the[col] = (
            the[col].apply(parse_numeric)
        )


# ============================================================
# THE FEMALE / MALE RATIO
# ============================================================

print("\nProcessing Female to Male Ratio...")


if "Female to Male Ratio" in the.columns:

    the["female_to_male_ratio_clean"] = (
        the["Female to Male Ratio"]
        .apply(parse_ratio)
    )

    # Keep original ratio as text
    the["female_to_male_ratio_original"] = (
        the["Female to Male Ratio"]
    )


# ============================================================
# THE COUNTRY
# ============================================================

if "Country" in the.columns:

    the["Country"] = (
        the["Country"]
        .map(standardize_country)
    )


# ============================================================
# THE UNIVERSITY KEY
# ============================================================

the["university_key"] = (
    the["Name"]
    .astype("string")
    .str.lower()
    .str.replace(
        r"\([^)]*\)",
        "",
        regex=True
    )
    .str.replace(
        "&",
        "and"
    )
    .str.replace(
        r"[^a-z0-9\s]",
        " ",
        regex=True
    )
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

print("\nDuplicate removal:")

qs_before = len(qs)
the_before = len(the)


qs = qs.drop_duplicates(
    subset=["university_key"],
    keep="first"
)


the = the.drop_duplicates(
    subset=["university_key"],
    keep="first"
)


print(
    f"QS removed: {qs_before - len(qs)}"
)

print(
    f"THE removed: {the_before - len(the)}"
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)


# ------------------------------------------------------------
# QS validation
# ------------------------------------------------------------

print(
    "\nQS rank missing:",
    qs["2026_rank"].isna().sum()
)


print(
    "QS overall score missing:",
    qs["overall_score"].isna().sum()
)


print(
    "QS overall score available:",
    qs["overall_score"].notna().sum()
)


print(
    "\nQS score availability flag:"
)

print(
    qs["overall_score_available"]
    .value_counts()
)


# ------------------------------------------------------------
# THE validation
# ------------------------------------------------------------

print(
    "\nTHE rank missing:",
    the["rank"].isna().sum()
)


if "female_to_male_ratio_clean" in the.columns:

    print(
        "THE female/male ratio missing:",
        the["female_to_male_ratio_clean"]
        .isna()
        .sum()
    )

    print(
        "THE female/male ratio available:",
        the["female_to_male_ratio_clean"]
        .notna()
        .sum()
    )


# ============================================================
# SAVE CLEANED DATASETS
# ============================================================

qs.to_csv(
    QS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


the.to_csv(
    THE_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CLEANING COMPLETED")
print("=" * 70)


print(
    f"\nQS final shape: {qs.shape}"
)


print(
    f"THE final shape: {the.shape}"
)


print("\nCreated:")

print(QS_OUTPUT)

print(THE_OUTPUT)


print("\nImportant:")

print(
    "QS '-' Overall SCORE values were preserved as NaN."
)

print(
    "QS rank values such as 1401+ were converted to numeric 1401"
)

print(
    "while the original/display rank is preserved."
)

print(
    "No missing QS scores were artificially imputed."
)

print(
    "THE Excel timedelta Female/Male ratios were converted "
    "back to their female percentage."
)

print("\nStage 2 completed successfully.")