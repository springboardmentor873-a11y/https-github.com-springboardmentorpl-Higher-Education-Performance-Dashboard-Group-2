from pathlib import Path
from textwrap import wrap
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
DATASET = ROOT / "data" / "processed" / "university_final_dataset_all_kpis.xlsx"
PDF_FILE = DASHBOARD_DIR / "dashboard_storyboard.pdf"
TWBX_FILE = DASHBOARD_DIR / "eduvision_prototype.twbx"

NAVIGATION = [
    "University Overview",
    "Research Analytics",
    "Student Analytics",
    "Country Comparison",
]

FILTERS = ["Country"]
DIMENSION_FIELDS = {"University", "Country", "Enrollment Bin Label"}

KPI_WORKSHEETS = {
    ("University Overview", "Total Universities"): ("COUNTD", "University", "real"),
    ("University Overview", "Average Global Score"): ("AVG", "Global_Ranking_Score", "real"),
    ("University Overview", "Countries Represented"): ("COUNTD", "Country", "real"),
    ("University Overview", "Region Coverage"): (None, "Region Coverage", "string"),
    ("Research Analytics", "Research Impact"): ("AVG", "Research_Impact_Score", "real"),
    ("Research Analytics", "Productivity Index"): ("AVG", "Research_Productivity_Index", "real"),
    ("Research Analytics", "Citations"): ("AVG", "scores_citations", "real"),
    ("Research Analytics", "Research Score"): ("AVG", "scores_research", "real"),
    ("Student Analytics", "Average International Students"): ("AVG", "International_Student_Percentage", "real"),
    ("Student Analytics", "Average Faculty-to-Student Ratio"): ("AVG", "Faculty_to_Student_Ratio", "real"),
    ("Student Analytics", "Total Enrolled Students"): ("SUM", "stats_number_students", "real"),
    ("Student Analytics", "Universities with Enrollment"): ("COUNT", "stats_number_students", "real"),
    ("Country Comparison", "Total Countries"): ("COUNTD", "Country", "real"),
    ("Country Comparison", "Top Country by Global Score"): ("ATTR", "Top Country by Average Global Score", "string"),
    ("Country Comparison", "Average Global Score"): ("AVG", "Global_Ranking_Score", "real"),
    ("Country Comparison", "Average Research Impact"): ("AVG", "Research_Impact_Score", "real"),
}

DASHBOARDS = [
    {
        "name": "University Overview",
        "subtitle": "Rankings, reputation, and global context",
        "kpis": [
            ("Total Universities", "COUNTD(University)"),
            ("Average Global Score", "AVG(Global_Ranking_Score)"),
            ("Countries Represented", "COUNTD(Country)"),
            ("Region Coverage", "Not derivable: no Region column"),
        ],
        "visuals": [
            ("Top 10 universities", "Horizontal bar | University, Global_Ranking_Score"),
            ("Global score distribution", "Filled map or symbol map | Country, Global_Ranking_Score"),
            ("Reputation vs. ranking", "Scatter | Academic_Reputation_KPI, Global_Ranking_Score"),
            ("Global score histogram", "Histogram | Global_Ranking_Score"),
            ("University comparison", "Detail table | University + all KPI columns"),
        ],
        "action": "Click a country or university to filter comparison, research, and student views. Country is the available shared filter.",
    },
    {
        "name": "Research Analytics",
        "subtitle": "Research impact, citations, and productivity",
        "kpis": [
            ("Research Impact", "Research_Impact_Score"),
            ("Productivity Index", "Research_Productivity_Index"),
            ("Citations", "scores_citations"),
            ("Research Score", "scores_research"),
        ],
        "visuals": [
            ("Top research institutions", "Horizontal bar | University, Research_Impact_Score"),
            ("Productivity profile", "Scatter | Research_Productivity_Index, Research_Impact_Score"),
            ("Citations by institution", "Bar | University, scores_citations"),
            ("Research score distribution", "Histogram | scores_research"),
            ("Research benchmark table", "Table | Country, University, research KPIs"),
        ],
        "action": "Select a university to cross-filter the overview and country benchmark views. Country is the available shared filter.",
    },
    {
        "name": "Student Analytics",
        "subtitle": "International reach, enrollment, and faculty capacity",
        "kpis": [
            ("Average International Students", "AVG(International_Student_Percentage)"),
            ("Average Faculty-to-Student Ratio", "AVG(Faculty_to_Student_Ratio)"),
            ("Total Enrolled Students", "SUM(stats_number_students)"),
            ("Universities with Enrollment", "COUNT(stats_number_students)"),
        ],
        "visuals": [
            ("International student reach", "Country-level sorted bar | Country, AVG(International_Student_Percentage)"),
            ("Enrollment vs. faculty ratio", "Scatter | stats_number_students, Faculty_to_Student_Ratio"),
            ("Gender composition", "Country-level 100% stacked bar | Country, AVG female_percentage + AVG male_percentage"),
            ("Enrollment distribution", "Histogram | stats_number_students"),
            ("Student profile table", "Table | University, Country, student KPIs"),
        ],
        "action": "Click a country to synchronize the student profile and overview map selection. Country is the available shared filter.",
    },
    {
        "name": "Country Comparison",
        "subtitle": "Benchmark countries and regional patterns",
        "kpis": [
            ("Total Countries", "COUNTD(Country)"),
            ("Top Country by Global Score", "[Top Country by Average Global Score]"),
            ("Average Global Score", "AVG(Global_Ranking_Score)"),
            ("Average Research Impact", "AVG(Research_Impact_Score)"),
        ],
        "visuals": [
            ("Country ranking comparison", "Ranked bar | Country, AVG(Global_Ranking_Score)"),
            ("Benchmark profile", "Grouped bar | Country and selected KPI averages"),
            ("Country KPI comparison", "Grouped bar | Country, AVG(Global_Ranking_Score), AVG(Research_Impact_Score)"),
            ("Country distribution", "Map | Country, AVG(Research_Impact_Score)"),
            ("Benchmark detail", "Table | Country, institution count, KPI averages"),
        ],
        "action": "Click a country to apply a dashboard-wide Country filter; navigation preserves the selection.",
    },
]


def add_text(ax, x, y, text, size=9, color="#24313b", weight="normal", ha="left"):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=size, color=color,
            fontweight=weight, ha=ha, va="top", family="DejaVu Sans")


def panel(ax, x, y, w, h, title, body, accent="#1f6f78"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                transform=ax.transAxes, facecolor="#ffffff", edgecolor="#d5dee2", linewidth=1))
    ax.add_patch(Rectangle((x, y + h - 0.012), w, 0.012, transform=ax.transAxes,
                          facecolor=accent, edgecolor="none"))
    add_text(ax, x + 0.015, y + h - 0.028, title, size=8.5, weight="bold")
    lines = wrap(body, 36)
    for index, line in enumerate(lines[:5]):
        add_text(ax, x + 0.015, y + h - 0.064 - index * 0.038, line, size=7.2, color="#60727a")


def wireframe_page(pdf, dashboard):
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    fig.patch.set_facecolor("#eef3f1")
    ax.set_axis_off()
    add_text(ax, 0.045, 0.95, dashboard["name"], size=20, weight="bold", color="#173b45")
    add_text(ax, 0.045, 0.91, dashboard["subtitle"], size=9.5, color="#60727a")
    # Navigation strip
    for index, name in enumerate(NAVIGATION):
        x = 0.43 + index * 0.135
        active = name == dashboard["name"]
        ax.add_patch(FancyBboxPatch((x, 0.91), 0.125, 0.035, boxstyle="round,pad=0.004,rounding_size=0.008",
                                    transform=ax.transAxes, facecolor="#1f6f78" if active else "#dce7e5",
                                    edgecolor="none"))
        add_text(ax, x + 0.0625, 0.936, name.replace("University ", "Uni. "), size=6.5,
                 color="#ffffff" if active else "#35535a", weight="bold", ha="center")
    # Filter rail
    ax.add_patch(Rectangle((0.045, 0.815), 0.91, 0.055, transform=ax.transAxes, facecolor="#dce7e5", edgecolor="none"))
    add_text(ax, 0.06, 0.852, "FILTERS", size=7, weight="bold", color="#1f6f78")
    for index, item in enumerate(FILTERS):
        x = 0.15 + index * 0.19
        ax.add_patch(FancyBboxPatch((x, 0.827), 0.17, 0.029, boxstyle="round,pad=0.003,rounding_size=0.005",
                                    transform=ax.transAxes, facecolor="#ffffff", edgecolor="#c2d2d0"))
        add_text(ax, x + 0.085, 0.847, item, size=5.8, color="#50656a", ha="center")
    # KPI row
    for index, (label, field) in enumerate(dashboard["kpis"]):
        x = 0.045 + index * 0.228
        ax.add_patch(FancyBboxPatch((x, 0.70), 0.205, 0.085, boxstyle="round,pad=0.006,rounding_size=0.01",
                                    transform=ax.transAxes, facecolor="#ffffff", edgecolor="#d5dee2"))
        add_text(ax, x + 0.015, 0.765, label, size=7.2, color="#60727a")
        add_text(ax, x + 0.015, 0.735, "AVG / SELECTED", size=13, weight="bold", color="#173b45")
        add_text(ax, x + 0.015, 0.711, field, size=5.8, color="#1f6f78")
    # Main chart layout
    items = dashboard["visuals"]
    panel(ax, 0.045, 0.39, 0.43, 0.27, items[0][0], items[0][1])
    panel(ax, 0.525, 0.39, 0.43, 0.27, items[1][0], items[1][1], accent="#d87941")
    panel(ax, 0.045, 0.08, 0.27, 0.25, items[2][0], items[2][1], accent="#467c59")
    panel(ax, 0.365, 0.08, 0.27, 0.25, items[3][0], items[3][1], accent="#8b6f47")
    panel(ax, 0.685, 0.08, 0.27, 0.25, items[4][0], items[4][1], accent="#6c698d")
    add_text(ax, 0.045, 0.035, "Action: " + dashboard["action"], size=7.2, color="#35535a")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def make_storyboard():
    with PdfPages(PDF_FILE) as pdf:
        fig, ax = plt.subplots(figsize=(11.69, 8.27))
        fig.patch.set_facecolor("#173b45")
        ax.set_axis_off()
        add_text(ax, 0.08, 0.78, "EDUVISION", size=31, weight="bold", color="#e9f2ee")
        add_text(ax, 0.08, 0.70, "Module 6: Student & Country Dashboard Build", size=16, color="#c3d9d3")
        add_text(ax, 0.08, 0.61, "Storyboard and interaction specification", size=11, color="#f2c28f")
        add_text(ax, 0.08, 0.48, "Source: university_final_dataset_all_kpis.xlsx", size=9, color="#c3d9d3")
        add_text(ax, 0.08, 0.43, "4 dashboards | 20 realized visuals | shared dashboard navigation", size=9, color="#c3d9d3")
        add_text(ax, 0.08, 0.14, "Data note: Country is the only shared filter backed by a current workbook column. Year, Region, and Subject Area are omitted.", size=7.5, color="#e9f2ee")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        for dashboard in DASHBOARDS:
            wireframe_page(pdf, dashboard)


def twb_column(name, datatype):
    role = "measure" if datatype == "real" else "dimension"
    value = "quantitative" if datatype == "real" else "nominal"
    return f"<column datatype='{datatype}' datatype-customized='true' name='[{escape(name)}]' role='{role}' type='{value}' />"


def worksheet_fields(dashboard_name, title):
    bindings = {
        ("University Overview", "Top 10 universities"): ("University", "Global_Ranking_Score", ["Country"]),
        ("University Overview", "Global score distribution"): ("Country", "Global_Ranking_Score", ["Country"]),
        ("University Overview", "Reputation vs. ranking"): ("Academic_Reputation_KPI", "Global_Ranking_Score", ["Country"]),
        ("University Overview", "Global score histogram"): ("Global_Ranking_Score", "Global_Ranking_Score", ["Country"]),
        ("University Overview", "University comparison"): ("University", "Global_Ranking_Score", ["Country", "Academic_Excellence_Score", "Research_Impact_Score"]),
        ("Research Analytics", "Top research institutions"): ("University", "Research_Impact_Score", ["Country"]),
        ("Research Analytics", "Productivity profile"): ("Research_Productivity_Index", "Research_Impact_Score", ["Country"]),
        ("Research Analytics", "Citations by institution"): ("University", "scores_citations", ["Country"]),
        ("Research Analytics", "Research score distribution"): ("scores_research", "scores_research", ["Country"]),
        ("Research Analytics", "Research benchmark table"): ("Country", "Research_Impact_Score", ["University", "Research_Productivity_Index"]),
        ("Student Analytics", "International student reach"): ("Country", "International_Student_Percentage", ["Country"]),
        ("Student Analytics", "Enrollment vs. faculty ratio"): ("stats_number_students", "Faculty_to_Student_Ratio", ["Country"]),
        ("Student Analytics", "Gender composition"): ("Country", "female_percentage", ["Country", "male_percentage"]),
        ("Student Analytics", "Enrollment distribution"): ("stats_number_students", "stats_number_students", ["Country"]),
        ("Student Analytics", "Student profile table"): ("University", "International_Student_Percentage", ["Country", "Faculty_to_Student_Ratio", "stats_number_students"]),
        ("Country Comparison", "Country ranking comparison"): ("Country", "Global_Ranking_Score", ["University"]),
        ("Country Comparison", "Benchmark profile"): ("Country", "Global_Ranking_Score", ["Research_Impact_Score", "Academic_Reputation_KPI", "International_Student_Percentage"]),
        ("Country Comparison", "Country KPI comparison"): ("Country", "Global_Ranking_Score", ["Research_Impact_Score"]),
        ("Country Comparison", "Country distribution"): ("Country", "Research_Impact_Score", ["University"]),
        ("Country Comparison", "Benchmark detail"): ("Country", "Global_Ranking_Score", ["Research_Impact_Score", "Academic_Reputation_KPI", "International_Student_Percentage"]),
    }
    return bindings[(dashboard_name, title)]


def twb_field(name):
    datatype = "string" if name in DIMENSION_FIELDS else "real"
    suffix = "nk" if datatype == "string" else "qk"
    return f"[none:{escape(name)}:{suffix}]"


def chart_settings(dashboard_name, title, spec):
    settings = {
        "mark_class": "Bar",
        "sort_field": None,
        "sort_direction": None,
        "label_field": None,
        "detail_fields": [],
        "bin_size": None,
        "extra_filters": [],
        "aggregation": None,
        "stack_fields": [],
    }
    if "Scatter" in spec or title == "Reputation vs. ranking":
        settings["mark_class"] = "Circle"
    elif "Map" in spec:
        settings["mark_class"] = "Map"
    elif "Table" in spec:
        settings["mark_class"] = "Text"
    if title in {"Top 10 universities", "Top research institutions", "Citations by institution"}:
        settings["sort_field"] = "Global_Ranking_Score" if title == "Top 10 universities" else ("Research_Impact_Score" if title == "Top research institutions" else "scores_citations")
        settings["sort_direction"] = "DESC"
        settings["label_field"] = "University"
    if title == "International student reach":
        settings["sort_field"] = "International_Student_Percentage"
        settings["sort_direction"] = "DESC"
        settings["label_field"] = "Country"
    if title == "Top 10 universities":
        settings["extra_filters"].append(("top", "University", "10", "AVG([none:Global_Ranking_Score:qk])"))
    elif title == "Top research institutions":
        settings["extra_filters"].append(("top", "University", "10", "AVG([none:Research_Impact_Score:qk])"))
    elif title == "Citations by institution":
        settings["extra_filters"].append(("top", "University", "15", "AVG([none:scores_citations:qk])"))
    if title in {"Global score histogram", "Research score distribution", "Enrollment distribution"}:
        settings["bin_size"] = {"Global score histogram": "5", "Research score distribution": "5", "Enrollment distribution": None}[title]
    if title == "Reputation vs. ranking":
        settings["detail_fields"] = ["University"]
    if title == "Productivity profile":
        settings["detail_fields"] = ["University"]
    if title == "Enrollment vs. faculty ratio":
        settings["detail_fields"] = ["University"]
    if title == "Gender composition":
        settings["stack_fields"] = ["female_percentage", "male_percentage"]
        settings["aggregation"] = "AVG"
        settings["label_field"] = "Country"
    if title == "University comparison":
        settings["extra_filters"].append(("categorical", "University", "", ""))
    if dashboard_name == "Country Comparison":
        settings["aggregation"] = "AVG"
        settings["label_field"] = "Country"
        if title in {"Country ranking comparison", "Country KPI comparison", "Benchmark profile"}:
            settings["sort_field"] = "Global_Ranking_Score"
            settings["sort_direction"] = "DESC"
    return settings


def dashboard_actions(dashboard_name):
    actions = {
        "University Overview": [
            ("filter", "Top 10 universities", "University comparison", "University"),
            ("highlight", "Top 10 universities", "Reputation vs. ranking", "University"),
            ("filter", "Reputation vs. ranking", "University comparison", "University"),
            ("highlight", "Reputation vs. ranking", "Top 10 universities", "University"),
            ("filter", "Global score distribution", "University comparison", "Country"),
            ("filter", "Global score distribution", "Top 10 universities", "Country"),
            ("filter", "Global score distribution", "Reputation vs. ranking", "Country"),
            ("highlight", "University comparison", "Top 10 universities", "University"),
            ("highlight", "University comparison", "Reputation vs. ranking", "University"),
        ],
        "Research Analytics": [
            ("highlight", "Top research institutions", "Productivity profile", "University"),
            ("filter", "Top research institutions", "Citations by institution", "University"),
            ("filter", "Top research institutions", "Research benchmark table", "University"),
            ("highlight", "Citations by institution", "Productivity profile", "University"),
            ("filter", "Citations by institution", "Top research institutions", "University"),
            ("filter", "Citations by institution", "Research benchmark table", "University"),
            ("filter", "Productivity profile", "Citations by institution", "University"),
            ("filter", "Productivity profile", "Research benchmark table", "University"),
            ("highlight", "Productivity profile", "Top research institutions", "University"),
            ("filter", "Research benchmark table", "Top research institutions", "Country"),
            ("filter", "Research benchmark table", "Citations by institution", "Country"),
            ("filter", "Research benchmark table", "Productivity profile", "Country"),
        ],
        "Student Analytics": [
            ("filter", "International student reach", "Student profile table", "Country"),
            ("filter", "International student reach", "Gender composition", "Country"),
            ("highlight", "International student reach", "Enrollment vs. faculty ratio", "Country"),
            ("filter", "International student reach", "Enrollment distribution", "Country"),
            ("filter", "Enrollment vs. faculty ratio", "Student profile table", "University"),
            ("filter", "Enrollment vs. faculty ratio", "Gender composition", "Country"),
            ("highlight", "Gender composition", "Enrollment vs. faculty ratio", "Country"),
            ("filter", "Student profile table", "International student reach", "Country"),
            ("filter", "Student profile table", "Gender composition", "Country"),
        ],
        "Country Comparison": [
            ("filter", "Country ranking comparison", "Benchmark profile", "Country"),
            ("filter", "Country ranking comparison", "Country KPI comparison", "Country"),
            ("filter", "Country ranking comparison", "Country distribution", "Country"),
            ("filter", "Country ranking comparison", "Benchmark detail", "Country"),
            ("filter", "Benchmark profile", "Country ranking comparison", "Country"),
            ("filter", "Benchmark profile", "Country KPI comparison", "Country"),
            ("filter", "Benchmark profile", "Country distribution", "Country"),
            ("filter", "Benchmark profile", "Benchmark detail", "Country"),
            ("filter", "Country KPI comparison", "Country ranking comparison", "Country"),
            ("filter", "Country KPI comparison", "Benchmark profile", "Country"),
            ("filter", "Country KPI comparison", "Country distribution", "Country"),
            ("filter", "Country KPI comparison", "Benchmark detail", "Country"),
            ("filter", "Country distribution", "Country ranking comparison", "Country"),
            ("filter", "Country distribution", "Benchmark profile", "Country"),
            ("filter", "Country distribution", "Country KPI comparison", "Country"),
            ("filter", "Country distribution", "Benchmark detail", "Country"),
            ("filter", "Benchmark detail", "Country ranking comparison", "Country"),
            ("filter", "Benchmark detail", "Benchmark profile", "Country"),
            ("filter", "Benchmark detail", "Country KPI comparison", "Country"),
            ("filter", "Benchmark detail", "Country distribution", "Country"),
        ],
    }
    return actions.get(dashboard_name, [])


def make_twb():
    fields = [
        ("University", "string"), ("Country", "string"), ("Global_Ranking_Score", "real"),
        ("Academic_Excellence_Score", "real"), ("Research_Impact_Score", "real"),
        ("Faculty_to_Student_Ratio", "real"), ("International_Student_Percentage", "real"),
        ("Academic_Reputation_KPI", "real"), ("Research_Productivity_Index", "real"),
        ("scores_research", "real"), ("scores_citations", "real"),
        ("stats_number_students", "real"), ("female_percentage", "real"), ("male_percentage", "real"),
        ("Overall_QS", "real"), ("Overall_THE", "real"),
        ("Global_Ranking_Score (bin)", "real"), ("scores_research (bin)", "real"),
        ("Number of Records", "real"),
    ]
    datasource_id = "federated.0"
    source_df = pd.read_excel(DATASET)

    def top_filter_xml(field, count, expression):
        sort_field = next(
            candidate
            for candidate in fields
            if candidate[0] in expression
        )[0]
        universities = (
            source_df.dropna(subset=[field])
            .sort_values(by=[sort_field, "University"], ascending=[False, True])
            .head(int(count))["University"]
        )
        members = "".join(
            f"<groupfilter function='member' level='{twb_field(field)}' member='{escape(str(university))}' />"
            for university in universities
        )
        return f"<filter class='categorical' column='{twb_field('University')}'><groupfilter function='union'>{members}</groupfilter></filter>"
    worksheet_xml = []
    for dashboard in DASHBOARDS:
        for title, spec in dashboard["visuals"]:
            sheet_name = f"{dashboard['name']} - {title}"
            row_field, column_field, mark_fields = worksheet_fields(dashboard["name"], title)
            settings = chart_settings(dashboard["name"], title, spec)
            if title == "Global score histogram":
                row_field, column_field = "Global_Ranking_Score (bin)", "Number of Records"
            elif title == "Research score distribution":
                row_field, column_field = "scores_research (bin)", "Number of Records"
            elif title == "Enrollment distribution":
                row_field, column_field = "Enrollment Bin Label", "Number of Records"
            bound_fields = [row_field, column_field, *mark_fields]
            if title == "Enrollment distribution":
                bound_fields.append("stats_number_students (log)")
            dimension_fields = DIMENSION_FIELDS
            dependencies = "".join(
                f"<column datatype='{('string' if field in dimension_fields else 'real')}' name='{twb_field(field)}' role='{('dimension' if field in dimension_fields else 'measure')}' type='{('nominal' if field in dimension_fields else 'quantitative')}'{(' aggregation=' + chr(39) + settings['aggregation'] + chr(39)) if settings['aggregation'] and field not in dimension_fields else ''} />"
                for field in dict.fromkeys(bound_fields + ["Country"])
            )
            mark_encodings = "".join(
                f"<encoding attr='color' field='{twb_field(field)}' />" for field in mark_fields
            )
            detail_encodings = "".join(
                f"<encoding attr='detail' field='{twb_field(field)}' />" for field in settings["detail_fields"]
            )
            sort_xml = ""
            if settings["sort_field"]:
                sort_xml = f"<sort column='{twb_field(settings['sort_field'])}' direction='{settings['sort_direction']}' />"
            label_xml = ""
            if settings["label_field"]:
                label_xml = f"<label show='true' field='{twb_field(settings['label_field'])}' />"
            extra_filter = "".join(
                top_filter_xml(field, count, expression)
                if kind == "top" else
                f"<filter class='{kind}' column='{twb_field(field)}' />"
                for kind, field, count, expression in settings["extra_filters"]
            )
            row_aggregation = f" aggregation='{settings['aggregation']}'" if settings["aggregation"] and row_field not in dimension_fields else ""
            column_aggregation = f" aggregation='{settings['aggregation']}'" if settings["aggregation"] and column_field not in {"University", "Country"} else ""
            row_datatype = "string" if row_field in dimension_fields else "real"
            worksheet_xml.append(
                f"<worksheet name='{escape(sheet_name)}'><repository-location derived-from='http://localhost' id='{escape(sheet_name)}' path='/workbooks/EduVision/{escape(sheet_name)}' revision='1.0' /><table><view><datasources><datasource caption='University Data' name='{datasource_id}' /></datasources><datasource-dependencies datasource='{datasource_id}'>{dependencies}</datasource-dependencies><filter class='categorical' column='{twb_field('Country')}' />{extra_filter}{sort_xml}</view><style /><panes><pane class='0'><view><breakdown value='auto' /></view><mark class='{settings['mark_class']}' /><encodings>{mark_encodings}{detail_encodings}</encodings></pane></panes><rows>{twb_field(row_field)}</rows><cols>{twb_field(column_field)}</cols></table></worksheet>"
            )
    dashboard_xml = []
    action_xml = []
    kpi_worksheet_xml = []
    for (dashboard_name, label), (aggregation, field, datatype) in KPI_WORKSHEETS.items():
        sheet_name = f"{dashboard_name} - KPI - {label}"
        field_type = "nominal" if datatype == "string" else "quantitative"
        field_role = "dimension" if datatype == "string" else "measure"
        dependency = (
            f"<column datatype='{datatype}' name='{twb_field(field)}' role='{field_role}' type='{field_type}' />"
        )
        column_aggregation = f" aggregation='{aggregation}'" if aggregation else ""
        aggregation_xml = f"<aggregation value='{aggregation.lower()}' />" if aggregation else ""
        kpi_worksheet_xml.append(
            f"<worksheet name='{escape(sheet_name)}'><repository-location derived-from='http://localhost' id='{escape(sheet_name)}' path='/workbooks/EduVision/{escape(sheet_name)}' revision='1.0' /><table><view><datasources><datasource caption='University Data' name='{datasource_id}' /></datasources><datasource-dependencies datasource='{datasource_id}'>{dependency}</datasource-dependencies><filter class='categorical' column='{twb_field('Country')}' />{aggregation_xml}</view><style /><panes><pane class='0'><view><breakdown value='auto' /></view><mark class='Text' /><encodings><encoding attr='label' field='{twb_field(field)}' /></encodings></pane></panes><rows /><cols>{twb_field(field)}</cols></table></worksheet>"
        )
    for dashboard in DASHBOARDS:
        zones = []
        for index, (title, _) in enumerate(dashboard["visuals"]):
            sheet_name = f"{dashboard['name']} - {title}"
            x = 0 if index % 2 == 0 else 600
            y = 0 if index < 2 else 360 + ((index - 2) * 40)
            zones.append(f"<zone h='320' id='{index + 1}' name='{escape(sheet_name)}' show-title='true' type-v2='worksheet' w='580' x='{x}' y='{y}' />")
        if dashboard["name"] in {"University Overview", "Research Analytics", "Student Analytics", "Country Comparison"}:
            cards = "".join(
                f"<zone h='100' id='{100 + index}' name='{escape(dashboard['name'] + ' - KPI - ' + label)}' show-title='true' type-v2='worksheet' w='280' x='{index * 290}' y='-120' />"
                for index, (label, _) in enumerate(dashboard["kpis"])
            )
            zones.append(cards)
        action_xml = "".join(
            f"<action class='{kind}' name='{escape(source + ' to ' + target)}' source='{escape(dashboard['name'] + ' - ' + source)}' target='{escape(dashboard['name'] + ' - ' + target)}' field='{twb_field(field)}' />"
            for kind, source, target, field in dashboard_actions(dashboard["name"])
        )
        dashboard_xml.append(f"<dashboard name='{escape(dashboard['name'])}'><repository-location derived-from='http://localhost' id='{escape(dashboard['name'])}' path='/workbooks/EduVision/{escape(dashboard['name'])}' revision='1.0' /><style /><size /><zones>{''.join(zones)}</zones></dashboard>")
    calculated_fields = (
        "<column caption='Top Country by Average Global Score' datatype='string' name='[Top Country by Average Global Score]' role='dimension' type='nominal'><calculation class='tableau' formula='IF RANK(AVG([Global_Ranking_Score])) = 1 THEN [Country] END' /></column>"
        "<column caption='Region Coverage' datatype='string' name='[Region Coverage]' role='dimension' type='nominal'><calculation class='tableau' formula='&quot;N/A (no Region column)&quot;' /></column>"
        "<column caption='Log Enrollment' datatype='real' name='[stats_number_students (log)]' role='measure' type='quantitative'><calculation class='tableau' formula='LOG([stats_number_students])' /></column>"
        "<column caption='Enrollment Bin Label' datatype='string' name='[Enrollment Bin Label]' role='dimension' type='nominal'><calculation class='tableau' formula='IF [stats_number_students (log)] &lt; LOG(10000) THEN &quot;&lt; 10,000&quot; ELSEIF [stats_number_students (log)] &lt; LOG(25000) THEN &quot;10,000-25,000&quot; ELSEIF [stats_number_students (log)] &lt; LOG(50000) THEN &quot;25,000-50,000&quot; ELSEIF [stats_number_students (log)] &lt; LOG(100000) THEN &quot;50,000-100,000&quot; ELSE &quot;100,000+&quot; END' /></column>"
    )
    twb = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='2024.2' source-build='2024.2.0' source-platform='win' version='18.1' xml:base='http://tableau.com/xml/workbook'>
<document-format-change-manifest />
<repository-location derived-from='http://localhost' id='EduVision' path='/workbooks/EduVision' revision='1.0' />
<preferences />
<datasources>
<datasource caption='University Data' inline='true' name='{datasource_id}' version='18.1'>
<connection access_mode='readonly' authentication='auth-none' author-locale='en_US' class='excel-direct' filename='university_final_dataset_all_kpis.xlsx' sslmode=''>
<relation name='University_Data' table='[University_Data$]' type='table' />
</connection>
{''.join(twb_column(name, datatype) for name, datatype in fields)}
{calculated_fields}
</datasource>
</datasources>
<worksheets>{''.join(worksheet_xml)}{''.join(kpi_worksheet_xml)}</worksheets>
<dashboards>{''.join(dashboard_xml)}</dashboards>
<windows><window class='dashboard' name='University Overview'><cards /></window></windows>
</workbook>
"""
    return twb


def make_package():
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    make_storyboard()
    with ZipFile(TWBX_FILE, "w", ZIP_DEFLATED) as package:
        package.writestr("eduvision_prototype.twb", make_twb())
        package.write(DATASET, "university_final_dataset_all_kpis.xlsx")


if __name__ == "__main__":
    make_package()
    print(PDF_FILE)
    print(TWBX_FILE)