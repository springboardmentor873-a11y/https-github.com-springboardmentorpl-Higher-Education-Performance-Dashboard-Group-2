from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "dashboard" / "eduvision_prototype.twbx"
DATASET = ROOT / "data" / "processed" / "university_final_dataset_all_kpis.xlsx"
CHECKLIST = ROOT / "dashboard" / "module7_qa_checklist.md"
REPORT = ROOT / "dashboard" / "module7_dashboard_testing_report.md"
MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS = {"x": MAIN}


def cell_text(cell, shared):
    if cell is None:
        return ""
    if cell.attrib.get("t") == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(f"{{{MAIN}}}t"))
    value = cell.find("x:v", NS)
    if value is None:
        return ""
    return shared[int(value.text)] if cell.attrib.get("t") == "s" else value.text


def read_data():
    with ZipFile(DATASET) as package:
        shared = []
        if "xl/sharedStrings.xml" in package.namelist():
            root = ET.fromstring(package.read("xl/sharedStrings.xml"))
            shared = ["".join(node.text or "" for node in item.iter(f"{{{MAIN}}}t")) for item in root.findall("x:si", NS)]
        rows = ET.fromstring(package.read("xl/worksheets/sheet1.xml")).findall(".//x:row", NS)
    headers = {"".join(ch for ch in c.attrib["r"] if ch.isalpha()): cell_text(c, shared) for c in rows[0].findall("x:c", NS)}
    records = []
    for row in rows[1:]:
        record = {}
        for cell in row.findall("x:c", NS):
            column = "".join(ch for ch in cell.attrib["r"] if ch.isalpha())
            record[headers[column]] = cell_text(cell, shared)
        records.append(record)
    return headers, records


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def average(records, field):
    values = [number(row.get(field)) for row in records]
    values = [value for value in values if value is not None]
    return sum(values) / len(values) if values else None


def direct_sort(records, field, limit):
    values = [(row.get("University"), number(row.get(field))) for row in records]
    values = [(name, value) for name, value in values if name and value is not None]
    return sorted(values, key=lambda item: (-item[1], item[0]))[:limit]


def run():
    headers, records = read_data()
    with ZipFile(WORKBOOK) as package:
        root = ET.fromstring(package.read("eduvision_prototype.twb"))
    worksheets = {node.attrib["name"]: node for node in root.findall("./worksheets/worksheet")}
    dashboards = {node.attrib["name"]: node for node in root.findall("./dashboards/dashboard")}
    checks = []
    checks.append(("TWBX XML parse", True, "The packaged workbook XML is well-formed."))
    checks.append(("Tableau engine open/render", False, "Tableau Desktop/Public is unavailable; engine-level opening and rendering remain unverified."))
    checks.append(("Dashboard and worksheet inventory", set(dashboards) == {"University Overview", "Research Analytics", "Student Analytics", "Country Comparison"} and len(worksheets) == 36, f"Found {len(dashboards)} dashboards and {len(worksheets)} worksheets."))

    zones = [zone for dashboard in dashboards.values() for zone in dashboard.findall("./zones/zone")]
    kpi_zones = [zone for zone in zones if " - KPI - " in zone.attrib.get("name", "")]
    checks.append(("16 KPI worksheet zones", len(kpi_zones) == 16 and all(zone.attrib.get("type-v2") == "worksheet" and zone.attrib.get("name") in worksheets for zone in kpi_zones), "KPI zones use the repaired dashboard/zones schema."))

    expected_kpis = {
        "University Overview - KPI - Total Universities": ("COUNTD", "University"),
        "University Overview - KPI - Average Global Score": ("AVG", "Global_Ranking_Score"),
        "University Overview - KPI - Countries Represented": ("COUNTD", "Country"),
        "University Overview - KPI - Region Coverage": (None, "Region Coverage"),
        "Research Analytics - KPI - Research Impact": ("AVG", "Research_Impact_Score"),
        "Research Analytics - KPI - Productivity Index": ("AVG", "Research_Productivity_Index"),
        "Research Analytics - KPI - Citations": ("AVG", "scores_citations"),
        "Research Analytics - KPI - Research Score": ("AVG", "scores_research"),
        "Student Analytics - KPI - Average International Students": ("AVG", "International_Student_Percentage"),
        "Student Analytics - KPI - Average Faculty-to-Student Ratio": ("AVG", "Faculty_to_Student_Ratio"),
        "Student Analytics - KPI - Total Enrolled Students": ("SUM", "stats_number_students"),
        "Student Analytics - KPI - Universities with Enrollment": ("COUNT", "stats_number_students"),
        "Country Comparison - KPI - Total Countries": ("COUNTD", "Country"),
        "Country Comparison - KPI - Top Country by Global Score": ("ATTR", "Top Country by Average Global Score"),
        "Country Comparison - KPI - Average Global Score": ("AVG", "Global_Ranking_Score"),
        "Country Comparison - KPI - Average Research Impact": ("AVG", "Research_Impact_Score"),
    }
    kpi_pass = []
    for name, (aggregation, field) in expected_kpis.items():
        column = worksheets[name].find("./table/cols/column")
        expected_name = f"[none:{field}:{'nk' if field in {'University', 'Country'} else 'qk'}]"
        kpi_pass.append(column is not None and column.attrib.get("name") == expected_name and column.attrib.get("aggregation", "").upper() == (aggregation or ""))
    checks.append(("KPI aggregation bindings", all(kpi_pass), f"Validated {len(kpi_pass)} live KPI worksheet bindings."))

    formula_node = root.find(".//column[@name='[Enrollment Bin Label]']/calculation")
    formula = formula_node.attrib.get("formula", "") if formula_node is not None else ""
    checks.append(("Enrollment log labels", "[stats_number_students (log)]" in formula and all(f"LOG({n})" in formula for n in (10000, 25000, 50000, 100000)), formula))
    checks.append(("No orphan enrollment bin", not root.findall(".//bin") and not root.findall(".//column[@name='[stats_number_students (log bin)]']"), "No unsupported enrollment bin element remains."))

    ranking_specs = [("Top 10 universities", "Global_Ranking_Score", 10), ("Top research institutions", "Research_Impact_Score", 10), ("Citations by institution", "scores_citations", 15)]
    ranking_report = []
    ranking_pass = []
    for title, field, limit in ranking_specs:
        prefix = "University Overview" if title == "Top 10 universities" else "Research Analytics"
        worksheet = worksheets[f"{prefix} - {title}"]
        view = worksheet.find("./table/view")
        sort = view.find("./sort")
        top_filter = view.find("./filter[@column='[none:University:nk]']")
        members = top_filter.findall("./groupfilter/groupfilter") if top_filter is not None else []
        actual = [name for name, _ in direct_sort(records, field, limit)]
        surfaced = [member.attrib.get("member") for member in members]
        expected_sort = f"[none:{field}:qk]"
        passed = sort is not None and sort.attrib.get("column") == expected_sort and sort.attrib.get("direction") == "desc" and len(surfaced) == limit and surfaced == actual
        ranking_pass.append(passed)
        ranking_report.append((title, field, actual, surfaced, expected_sort, sort.attrib.get("column") if sort is not None else None, passed))
    checks.append(("Top-N filters and exact ordering", all(ranking_pass), "Validated categorical member filters and descending sort fields for Top 10, Top 10, and Top 15."))

    actions = root.findall("./actions/action")
    action_pass = []
    for action in actions:
        source = action.find("./source")
        target = action.find("./target")
        column = action.findtext("./column", default="")
        field = re.search(r":([^:\]]+):[a-z]+\]", column)
        action_pass.append(source is not None and target is not None and source.attrib.get("worksheet") in worksheets and target.attrib.get("worksheet") in worksheets and field and field.group(1) in headers.values())
    checks.append(("Dashboard action resolution", False, f"The invalid hand-authored action XML was removed to make the workbook loadable; the generator still contains the 50-action source/target matrix, but no actions are serialized in this package."))

    range_pass = []
    for row in records:
        for field in ("International_Student_Percentage", "female_percentage", "male_percentage"):
            value = number(row.get(field))
            if value is not None: range_pass.append(0 <= value <= 100)
        for field in ("Faculty_to_Student_Ratio", "stats_student_staff_ratio"):
            value = number(row.get(field))
            if value is not None: range_pass.append(value > 0)
    checks.append(("Educational metric ranges", bool(range_pass) and all(range_pass), "Percentage values are 0-100 and staffing ratios are positive."))

    checklist = ["# Module 7 QA Checklist", "", "| Check | Result | Evidence |", "|---|---|---|"]
    for name, passed, evidence in checks:
        checklist.append(f"| {name} | {'PASS' if passed else 'FAIL / LIMITATION'} | {evidence} |")
    checklist.append("\nTableau engine validation remains unavailable because Tableau Desktop/Public is not installed.")
    CHECKLIST.write_text("\n".join(checklist) + "\n", encoding="utf-8")

    report = ["# Module 7 Dashboard Testing Report", "", "## Engine Availability", "", "Tableau Desktop/Public was not available. The workbook has now been rewritten to the expected Tableau XML hierarchy, but it still requires a real Tableau engine check for repair prompts and rendering.", "", "## Top-N Validation", ""]
    for title, field, actual, surfaced, expected_sort, actual_sort, passed in ranking_report:
        report.append(f"- **{title}**: `{field}` raw field maps to expected sort `{expected_sort}`; actual sort `{actual_sort}`; identity/order result: {'PASS' if passed else 'FAIL' }.")
        report.append(f"  Direct sort: {', '.join(actual)}")
        report.append(f"  Categorical filter members: {', '.join(surfaced)}")
    report.extend(["", "## Structural Result", "", f"- Worksheets: {len(worksheets)}; dashboards: {len(dashboards)}; KPI zones: {len(kpi_zones)}; serialized actions: {len(actions)}.", "- The generator retains the verified 50-action source/target matrix, but invalid hand-authored action XML was removed from the package because it caused Tableau schema errors.", "- Unsupported custom `<bin>`, `class='top'`, dashboard `<layout>`, storyboard, and invalid action structures were removed.", "- Residual limitation: no real Tableau engine/rendering check was possible; dashboard action wiring must be recreated or validated in Tableau."])
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Wrote {CHECKLIST}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    run()
