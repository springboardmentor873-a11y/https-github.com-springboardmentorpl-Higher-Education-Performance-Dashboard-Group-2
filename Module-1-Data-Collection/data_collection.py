import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. INPUT FILES
# ============================================================

QS_FILE = DATA_DIR / "2026 QS World University Rankings.csv"
THE_FILE = DATA_DIR / "THE World University Rankings 2026.xlsx"


# ============================================================
# 3. CHECK FILES
# ============================================================

print("=" * 70)
print("CHECKING INPUT FILES")
print("=" * 70)

if not QS_FILE.exists():
    raise FileNotFoundError(f"QS file not found: {QS_FILE}")

if not THE_FILE.exists():
    raise FileNotFoundError(f"THE file not found: {THE_FILE}")

print("QS file found:", QS_FILE.name)
print("THE file found:", THE_FILE.name)


# ============================================================
# 4. LOAD DATASETS
# ============================================================

print("\n" + "=" * 70)
print("LOADING DATASETS")
print("=" * 70)

qs = pd.read_csv(QS_FILE)
the = pd.read_excel(THE_FILE)

print("QS dataset loaded successfully.")
print("THE dataset loaded successfully.")


# ============================================================
# 5. DATASET SIZE
# ============================================================

print("\n" + "=" * 70)
print("DATASET SIZE")
print("=" * 70)

print(f"QS rows    : {qs.shape[0]}")
print(f"QS columns : {qs.shape[1]}")

print(f"THE rows    : {the.shape[0]}")
print(f"THE columns : {the.shape[1]}")


# ============================================================
# 6. DISPLAY COLUMN NAMES
# ============================================================

print("\n" + "=" * 70)
print("QS COLUMN NAMES")
print("=" * 70)

for i, column in enumerate(qs.columns, start=1):
    print(f"{i}. {column}")


print("\n" + "=" * 70)
print("THE COLUMN NAMES")
print("=" * 70)

for i, column in enumerate(the.columns, start=1):
    print(f"{i}. {column}")


# ============================================================
# 7. MISSING VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUES - QS")
print("=" * 70)

qs_missing = qs.isnull().sum()
qs_missing = qs_missing[qs_missing > 0]

if len(qs_missing) == 0:
    print("No missing values found.")
else:
    print(qs_missing)


print("\n" + "=" * 70)
print("MISSING VALUES - THE")
print("=" * 70)

the_missing = the.isnull().sum()
the_missing = the_missing[the_missing > 0]

if len(the_missing) == 0:
    print("No missing values found.")
else:
    print(the_missing)


# ============================================================
# 8. DUPLICATE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS")
print("=" * 70)

print("QS duplicate rows :", qs.duplicated().sum())
print("THE duplicate rows:", the.duplicated().sum())


# ============================================================
# 9. UNIVERSITY NAME CHECK
# ============================================================

print("\n" + "=" * 70)
print("UNIVERSITY NAME CHECK")
print("=" * 70)

qs_name_column = "Institution Name"
the_name_column = "Name"

print("QS university column:", qs_name_column)
print("THE university column:", the_name_column)

print("\nFirst 10 QS universities:")
print(qs[qs_name_column].head(10).to_string(index=False))

print("\nFirst 10 THE universities:")
print(the[the_name_column].head(10).to_string(index=False))


# ============================================================
# 10. COUNTRY CHECK
# ============================================================

print("\n" + "=" * 70)
print("COUNTRY CHECK")
print("=" * 70)

print("QS country column: Country/Territory")
print("THE country column: Country")

print("\nNumber of QS countries:",
      qs["Country/Territory"].nunique())

print("Number of THE countries:",
      the["Country"].nunique())


# ============================================================
# 11. SAVE RAW COPIES
# ============================================================

qs.to_csv(
    OUTPUT_DIR / "qs_raw.csv",
    index=False
)

the.to_csv(
    OUTPUT_DIR / "the_raw.csv",
    index=False
)

print("\n" + "=" * 70)
print("RAW DATA SAVED")
print("=" * 70)

print("Created:")
print(OUTPUT_DIR / "qs_raw.csv")
print(OUTPUT_DIR / "the_raw.csv")

print("\nData collection and initial inspection completed.")