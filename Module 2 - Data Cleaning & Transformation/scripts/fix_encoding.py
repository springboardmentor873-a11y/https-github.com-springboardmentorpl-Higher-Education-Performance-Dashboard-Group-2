import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"


# ============================================================
# FUNCTION TO FIX MOJIBAKE
# ============================================================

def fix_encoding(value):

    if pd.isna(value):
        return value

    value = str(value)

    # Common UTF-8 decoded as Latin-1/Windows-1252
    if any(
        bad in value
        for bad in [
            "Ã",
            "Â",
            "Å",
            "â",
            "ð"
        ]
    ):

        try:
            value = value.encode(
                "latin1"
            ).decode(
                "utf-8"
            )

        except (
            UnicodeEncodeError,
            UnicodeDecodeError
        ):
            pass

    return value


# ============================================================
# LOAD DATA
# ============================================================

qs = pd.read_csv(
    OUTPUT_DIR /
    "qs_cleaned.csv"
)

the = pd.read_csv(
    OUTPUT_DIR /
    "the_cleaned.csv"
)


# ============================================================
# FIX TEXT COLUMNS
# ============================================================

qs_text_columns = [
    "institution_name",
    "country_territory",
    "region",
    "size",
    "focus",
    "research",
    "status"
]


the_text_columns = [
    "name",
    "country"
]


for column in qs_text_columns:

    if column in qs.columns:

        qs[column] = qs[
            column
        ].apply(fix_encoding)


for column in the_text_columns:

    if column in the.columns:

        the[column] = the[
            column
        ].apply(fix_encoding)


# ============================================================
# SAVE FIXED DATA
# ============================================================

qs.to_csv(
    OUTPUT_DIR /
    "qs_cleaned_encoding_fixed.csv",
    index=False,
    encoding="utf-8-sig"
)

the.to_csv(
    OUTPUT_DIR /
    "the_cleaned_encoding_fixed.csv",
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# DISPLAY EXAMPLES
# ============================================================

print("=" * 70)
print("ENCODING CORRECTION COMPLETED")
print("=" * 70)

print("\nQS examples:")

print(
    qs[
        ["institution_name"]
    ].head(10).to_string(
        index=False
    )
)

print("\nTHE examples:")

print(
    the[
        ["name"]
    ].head(10).to_string(
        index=False
    )
)

print("\nCreated:")

print(
    OUTPUT_DIR /
    "qs_cleaned_encoding_fixed.csv"
)

print(
    OUTPUT_DIR /
    "the_cleaned_encoding_fixed.csv"
)
