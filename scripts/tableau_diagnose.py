from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import difflib
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "tableau_diagnostic"
PACKAGE = ROOT / "dashboard" / "eduvision_prototype.twbx"
EXTRACTED = DIAGNOSTIC / "original_extracted"
TWB_NAME = "eduvision_prototype.twb"
DATASET_NAME = "university_final_dataset_all_kpis.xlsx"
FIELD_PATTERN = re.compile(r"\[([^\]]+)\]")


def children(node):
    return [child.tag for child in list(node)] if node is not None else []


def element_text(node):
    return "" if node is None else "".join(node.itertext()).strip()


def field_name(token):
    parts = token.split(":")
    if len(parts) == 3 and parts[0] == "none":
        return parts[1]
    return token


def load_twb(package_path):
    with ZipFile(package_path) as package:
        raw = package.read(TWB_NAME)
        names = package.namelist()
    return ET.fromstring(raw), names, raw


def attrs(node):
    return " ".join(f"{key}={value!r}" for key, value in sorted(node.attrib.items()))


def field_references(root):
    references = []
    for node in root.iter():
        for key, value in node.attrib.items():
            if key in {"name", "caption", "id", "path"}:
                continue
            for field in FIELD_PATTERN.findall(value):
                references.append((node.tag, key, field_name(field), value))
        if node.tag in {"rows", "cols"} and element_text(node):
            for field in FIELD_PATTERN.findall(element_text(node)):
                references.append((node.tag, "text", field_name(field), element_text(node)))
        if node.tag == "calculation":
            for field in FIELD_PATTERN.findall(node.attrib.get("formula", "")):
                references.append((node.tag, "formula", field_name(field), node.attrib.get("formula", "")))
    return references


def inventory(root, names):
    worksheets = root.findall("./worksheets/worksheet")
    dashboards = root.findall("./dashboards/dashboard")
    datasource = root.find("./datasources/datasource")
    lines = ["# Workbook Inventory", "", "## Package", "", f"- package entries: {len(names)}", f"- TWB present: {TWB_NAME in names}", f"- Excel datasource present: {DATASET_NAME in names}", "", "## Workbook", "", f"- root attributes: {attrs(root)}", f"- child order: {', '.join(children(root))}", ""]
    manifest = root.find("./document-format-change-manifest")
    lines += [f"- manifest: {'missing' if manifest is None else (element_text(manifest) or 'empty')}", f"- repository-location: {attrs(root.find('./repository-location'))}", ""]

    lines += ["## Datasources", ""]
    for source in root.findall("./datasources/datasource"):
        connection = source.find("./connection")
        lines.append(f"- {source.attrib.get('name')} caption={source.attrib.get('caption')!r} version={source.attrib.get('version')!r} inline={source.attrib.get('inline')!r}")
        lines.append(f"  - connection: {attrs(connection)}")
        lines.append(f"  - relation: {attrs(source.find('./connection/relation'))}")
        for column in source.findall("./column"):
            calculation = column.find("./calculation")
            suffix = f" calculation={calculation.attrib.get('formula')!r}" if calculation is not None else ""
            lines.append(f"  - field {column.attrib.get('name')}: {attrs(column)}{suffix}")

    lines += ["", "## Worksheets", ""]
    for worksheet in worksheets:
        table = worksheet.find("./table")
        view = table.find("./view") if table is not None else None
        panes = table.find("./panes") if table is not None else None
        pane = panes.find("./pane") if panes is not None else None
        lines.append(f"- {worksheet.attrib.get('name')}")
        lines.append(f"  - worksheet attrs: {attrs(worksheet)}")
        lines.append(f"  - table order: {', '.join(children(table))}")
        lines.append(f"  - view order: {', '.join(children(view))}")
        lines.append(f"  - pane order: {', '.join(children(pane))}")
        lines.append(f"  - rows={element_text(table.find('./rows')) if table is not None else ''!r} cols={element_text(table.find('./cols')) if table is not None else ''!r}")
        lines.append(f"  - marks={[node.attrib for node in worksheet.findall('./table/panes/pane/mark')]}")
        lines.append(f"  - filters={len(worksheet.findall('.//filter'))} sorts={len(worksheet.findall('.//sort'))} calculations={len(worksheet.findall('.//calculation'))} encodings={len(worksheet.findall('.//encoding'))}")

    lines += ["", "## Dashboards", ""]
    for dashboard in dashboards:
        zones = dashboard.findall("./zones/zone")
        lines.append(f"- {dashboard.attrib.get('name')}: child order={','.join(children(dashboard))} zones={len(zones)}")
        for zone in zones:
            lines.append(f"  - zone {attrs(zone)}")

    windows = root.find("./windows")
    lines += ["", "## Other Structures", "", f"- windows: {attrs(windows)} children={children(windows)}", f"- window count: {len(root.findall('./windows/window')) if windows is not None else 0}", f"- actions: {len(root.findall('./actions/action'))}", f"- stories: {len(root.findall('./stories/story')) + len(root.findall('./storyboards/storyboard'))}", f"- parameters: {len(root.findall('.//parameter'))}", f"- sets: {len(root.findall('.//set'))}", f"- bins: {len(root.findall('.//bin'))}", f"- aliases: {len(root.findall('.//alias'))}", f"- simple-id elements: {len(root.findall('.//simple-id'))}", "", "## Element Counts", ""]
    for tag, count in sorted(Counter(node.tag for node in root.iter()).items()):
        lines.append(f"- {tag}: {count}")
    return "\n".join(lines) + "\n"


def field_report(root):
    datasource_fields = {column.attrib.get("name", "").strip("[]") for column in root.findall("./datasources/datasource/column")}
    refs = field_references(root)
    counts = Counter(field for _, _, field, _ in refs if field != "University_Data$")
    lines = ["# Field Reference Report", "", f"Datasource fields: {len(datasource_fields)}", ""]
    for field, count in sorted(counts.items()):
        status = "OK" if field in datasource_fields else "MISSING"
        lines.append(f"- {status}: [{field}] ({count} references)")
    missing = sorted(set(counts) - datasource_fields)
    lines += ["", f"Missing referenced fields: {len(missing)}", "", "## Reference Samples", ""]
    for tag, key, field, value in refs:
        if field in missing:
            lines.append(f"- {tag} @{key}: [{field}] in {value!r}")
    return "\n".join(lines) + "\n"


def dashboard_report(root):
    worksheet_names = {node.attrib.get("name") for node in root.findall("./worksheets/worksheet")}
    lines = ["# Dashboard Reference Report", ""]
    for dashboard in root.findall("./dashboards/dashboard"):
        name = dashboard.attrib.get("name")
        zones = dashboard.findall("./zones/zone")
        lines.append(f"## {name}")
        for zone in zones:
            target = zone.attrib.get("name")
            status = "OK" if target in worksheet_names else "MISSING"
            lines.append(f"- {status}: zone {zone.attrib.get('id')} -> {target!r}; x={zone.attrib.get('x')} y={zone.attrib.get('y')} w={zone.attrib.get('w')} h={zone.attrib.get('h')}")
        lines.append("")
    return "\n".join(lines)


def previous_repairs_report(root, raw):
    original = DIAGNOSTIC / "eduvision_prototype.original.twbx"
    lines = ["# Previous Repairs Report", ""]
    if not original.exists():
        return "\n".join(lines + ["No preserved original package was found."]) + "\n"
    with ZipFile(original) as package:
        original_raw = package.read(TWB_NAME)
    if original_raw == raw:
        lines += ["The preserved package and the current workbook are byte-identical.", "No prior XML modifications are observable in this workspace.", ""]
        lines.append("The user-supplied fixed_final and other repair variants are absent, so their changes cannot be reconstructed.")
        return "\n".join(lines) + "\n"
    diff = list(difflib.unified_diff(original_raw.decode("utf-8").splitlines(), raw.decode("utf-8").splitlines(), fromfile="original", tofile="current", lineterm=""))
    lines += [f"Observed diff lines: {len(diff)}", "", "```diff", *diff[:400], "```"]
    return "\n".join(lines) + "\n"


def root_cause_report(root):
    version = root.attrib.get("version")
    worksheets = root.findall("./worksheets/worksheet")
    dashboards = root.findall("./dashboards/dashboard")
    missing_fields = sorted(set(field for _, _, field, _ in field_references(root) if field != "University_Data$") - {column.attrib.get("name", "").strip("[]") for column in root.findall('./datasources/datasource/column')})
    lines = ["# Root Cause", "", "## Root Cause", "", "The package is a hand-authored legacy TWB whose worksheet and dashboard document structures do not conform to the official 2026.2 workbook schema. The rejection is structural and cascades from malformed parent content models; changing isolated attributes such as simple-id, pane class, mark class, or aggregation cannot repair it.", "", "## Evidence", "", f"- Workbook reports version={version!r}, original-version={root.attrib.get('original-version')!r}, source-build={root.attrib.get('source-build')!r}; these values are not, by themselves, evidence that version 18.1 must be changed.", f"- All {len(worksheets)} worksheets contain a direct table body with child order `view, style, panes, rows, cols`, but the official 2026.2 schema requires each workbook worksheet wrapper to contain a repository location, a visual specification, and a required `simple-id`.", f"- The worksheet visual specification requires `view` to contain an `aggregation` element after its view specification. This package has {len(root.findall('./worksheets/worksheet/table/view/aggregation'))} worksheet-level aggregation elements for {len(worksheets)} worksheets.", f"- Every pane uses `<mark class=...>` and `<encoding attr=... field=...>`, while the official 2026.2 pane model requires the mark and uses named mark-encoding elements such as `<color column=...>`.", f"- Each dashboard uses child order `repository-location, style, size, zones`, while the official dashboard model requires a size/options element, optional datasource/dependencies, zones, and a required dashboard `simple-id`.", f"- The package contains {len(root.findall('./windows/window'))} window and its child is `cards`; the official dashboard window model requires `viewpoints`, `active`, optional preview settings, grid options, and optional simple-id.", f"- The document-format-change-manifest is empty. The official guidance recommends `<ManifestByVersion />` for direct authoring, but an empty manifest is secondary to the malformed worksheet/dashboard content models.", "", "## Secondary Problems", "", f"- {len(missing_fields)} referenced field names are not declared as datasource columns: {', '.join(missing_fields) if missing_fields else 'none'}.", f"- The package has {len(root.findall('./actions/action'))} root-level action nodes, but the 2026.2 action content model expects an `actions` wrapper and nested legacy action structure.", "- The generated datasource omits the metadata records and other structures normally emitted by Tableau, so XSD compliance alone would not establish semantic loadability.", "", "## Cascading Errors", "", "Errors such as `no declaration found for element rows`, `cols`, and `mark`, plus missing `class`, `revision`, or `aggregation`, are expected consequences when Tableau enters the wrong content model after the malformed worksheet parent. Treating them as independent repairs explains why earlier attribute-level changes did not converge.", "", "## Previous Repair Mistakes", "", "- The visible workspace contains only `dashboard/eduvision_prototype.twbx`; the requested fixed_final and other repair variants are absent, so their exact edits cannot be audited.", "- Existing project documentation says invalid action XML, bins, layout, and storyboard structures were removed without a Tableau engine check. Those removals may reduce individual errors but cannot turn a hand-authored legacy worksheet body into a valid 2026.2 document model.", "", "## Recommended Repair", "", "Do not patch the current TWB element-by-element. Recreate a minimal workbook in Tableau 2026.2.2 (or obtain a genuine 2026.2 TWB), then transplant datasource fields and worksheet/dashboard definitions using that workbook's exact wrapper, child order, identifiers, and action syntax. Until such a reference workbook is available, a full repair preserving all 36 worksheets and 4 dashboards would be speculative.", "", "## Validation Boundary", "", "Tableau Desktop/Public is not installed in this environment, and no fixed_final package was supplied. This report is static diagnosis only; it does not claim that the current or any repaired package opens in Tableau."]
    return "\n".join(lines) + "\n"


def main():
    DIAGNOSTIC.mkdir(exist_ok=True)
    root, names, raw = load_twb(PACKAGE)
    (DIAGNOSTIC / "workbook_inventory.txt").write_text(inventory(root, names), encoding="utf-8")
    (DIAGNOSTIC / "field_reference_report.txt").write_text(field_report(root), encoding="utf-8")
    (DIAGNOSTIC / "dashboard_reference_report.txt").write_text(dashboard_report(root), encoding="utf-8")
    (DIAGNOSTIC / "previous_repairs_report.txt").write_text(previous_repairs_report(root, raw), encoding="utf-8")
    (DIAGNOSTIC / "ROOT_CAUSE.md").write_text(root_cause_report(root), encoding="utf-8")
    print(f"Wrote diagnostics to {DIAGNOSTIC}")


if __name__ == "__main__":
    main()