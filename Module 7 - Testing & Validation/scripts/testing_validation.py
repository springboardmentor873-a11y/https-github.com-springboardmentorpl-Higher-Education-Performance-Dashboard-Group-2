import csv
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

KPI_FILE = BASE_DIR / "Module 3 - Education KPI Engineering" / "output" / "university_kpis.csv"
FULL_KPI_FILE = BASE_DIR / "Module 3 - Education KPI Engineering" / "output" / "university_kpi_dataset.csv"
TABLEAU_FILE = BASE_DIR / "output" / "EduVision.twb"

EXPECTED_ROWS = 1008

KPI_RANGES = {
    "global_ranking_score": (0, 100),
    "research_impact_score": (0, 100),
    "faculty_to_student_ratio": (0, 1),
    "international_student_percentage": (0, 100),
    "academic_reputation_score": (0, 100),
    "research_productivity_index": (0, 100),
}

EXPECTED_DASHBOARDS = {
    "Comparison Dashboard",
    "Overview Dashboard",
    "Research Dashboard",
    "Student analysis Dashboard",
}

results = []


def record(test, status, details):
    results.append((test, status, details))


print("=" * 70)
print("EDUVISION - MODULE 7 TESTING & VALIDATION")
print("=" * 70)


# ---------------------------------------------------------
# 1. Final KPI dataset existence
# ---------------------------------------------------------
if KPI_FILE.exists():
    record(
        "Final KPI dataset exists",
        "PASS",
        f"{KPI_FILE.name} found."
    )
else:
    record(
        "Final KPI dataset exists",
        "FAIL",
        f"Missing file: {KPI_FILE}"
    )


# ---------------------------------------------------------
# 2. Final KPI dataset row count and duplicates
# ---------------------------------------------------------
if KPI_FILE.exists():
    with KPI_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames or []

    row_count = len(rows)

    if row_count == EXPECTED_ROWS:
        record(
            "Final KPI dataset row count",
            "PASS",
            f"{row_count} rows found; expected {EXPECTED_ROWS}."
        )
    else:
        record(
            "Final KPI dataset row count",
            "FAIL",
            f"{row_count} rows found; expected {EXPECTED_ROWS}."
        )

    university_col = next(
        (c for c in columns if c.strip().lower() == "university"),
        None
    )

    if university_col:
        names = [
            (row.get(university_col) or "").strip()
            for row in rows
        ]
        names = [n for n in names if n]

        duplicate_count = len(names) - len(set(names))

        if duplicate_count == 0:
            record(
                "University duplicate check",
                "PASS",
                "No duplicate university names detected."
            )
        else:
            record(
                "University duplicate check",
                "FAIL",
                f"{duplicate_count} duplicate university names detected."
            )
    else:
        record(
            "University duplicate check",
            "FAIL",
            "University Name column not found."
        )


# ---------------------------------------------------------
# 3. Required KPI columns
# ---------------------------------------------------------
if KPI_FILE.exists():
    missing_columns = [
        kpi for kpi in KPI_RANGES
        if kpi not in columns
    ]

    if not missing_columns:
        record(
            "Required KPI columns",
            "PASS",
            "All six required KPI columns are present."
        )
    else:
        record(
            "Required KPI columns",
            "FAIL",
            "Missing: " + ", ".join(missing_columns)
        )


# ---------------------------------------------------------
# 4. KPI completeness, numeric validity and ranges
# ---------------------------------------------------------
if KPI_FILE.exists():
    for kpi, (lower, upper) in KPI_RANGES.items():

        if kpi not in columns:
            continue

        missing = 0
        invalid = 0
        out_of_range = 0

        for row in rows:
            value = (row.get(kpi) or "").strip()

            if value == "":
                missing += 1
                continue

            try:
                number = float(value)
            except ValueError:
                invalid += 1
                continue

            if number < lower or number > upper:
                out_of_range += 1

        if missing == 0 and invalid == 0 and out_of_range == 0:
            record(
                f"KPI validation - {kpi}",
                "PASS",
                "No missing, non-numeric, or out-of-range values."
            )
        else:
            record(
                f"KPI validation - {kpi}",
                "FAIL",
                f"Missing={missing}, invalid={invalid}, out_of_range={out_of_range}"
            )


# ---------------------------------------------------------
# 5. Ranking-related field inspection
# ---------------------------------------------------------
if FULL_KPI_FILE.exists():
    with FULL_KPI_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        full_columns = reader.fieldnames or []

    ranking_columns = [
        c for c in full_columns
        if "rank" in c.lower()
    ]

    if ranking_columns:
        record(
            "Ranking fields available for validation",
            "PASS",
            "Ranking-related fields found: " + ", ".join(ranking_columns)
        )
    else:
        record(
            "Ranking fields available for validation",
            "INFO",
            "No ranking-related columns detected in the final KPI dataset."
        )
else:
    record(
        "Ranking fields available for validation",
        "INFO",
        "Full KPI dataset not found; ranking-field inspection skipped."
    )


# ---------------------------------------------------------
# 6. Tableau workbook existence
# ---------------------------------------------------------
if TABLEAU_FILE.exists():
    record(
        "Integrated Tableau workbook exists",
        "PASS",
        f"{TABLEAU_FILE.name} found."
    )
else:
    record(
        "Integrated Tableau workbook exists",
        "FAIL",
        f"Missing file: {TABLEAU_FILE}"
    )


# ---------------------------------------------------------
# 7. Tableau dashboard structure
# ---------------------------------------------------------
if TABLEAU_FILE.exists():
    try:
        tree = ET.parse(TABLEAU_FILE)
        root = tree.getroot()

        dashboard_names = {
            element.get("name")
            for element in root.iter("dashboard")
            if element.get("name")
        }

        missing_dashboards = EXPECTED_DASHBOARDS - dashboard_names

        if not missing_dashboards:
            record(
                "Integrated dashboard structure",
                "PASS",
                "All four expected dashboards are present."
            )
        else:
            record(
                "Integrated dashboard structure",
                "FAIL",
                "Missing dashboards: " + ", ".join(sorted(missing_dashboards))
            )

        print("\nDashboards detected:")
        for name in sorted(dashboard_names):
            print(f"  - {name}")

    except Exception as exc:
        record(
            "Integrated dashboard structure",
            "FAIL",
            f"Unable to parse Tableau workbook XML: {exc}"
        )


# ---------------------------------------------------------
# Final summary
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("TEST RESULTS")
print("=" * 70)

for test, status, details in results:
    print(f"[{status}] {test}")
    print(f"       {details}")

pass_count = sum(1 for _, status, _ in results if status == "PASS")
fail_count = sum(1 for _, status, _ in results if status == "FAIL")
info_count = sum(1 for _, status, _ in results if status == "INFO")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"PASS : {pass_count}")
print(f"FAIL : {fail_count}")
print(f"INFO : {info_count}")

if fail_count == 0:
    print("\nAUTOMATED VALIDATION STATUS: PASS")
else:
    print("\nAUTOMATED VALIDATION STATUS: REVIEW REQUIRED")

print("=" * 70)

