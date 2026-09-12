"""Shared, auditable configuration for the EduVision 2026 data pipeline."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard" / "EduVision_Final"

REPORTING_YEAR = 2026

NORMALIZED_COLUMNS = ["QS_Rank_Normalized", "THE_Rank_Normalized"]

KPI_COLUMNS = [
    "KPI_Global_Ranking_Score",
    "KPI_Research_Impact_Score",
    "KPI_Faculty_to_Student_Ratio",
    "KPI_International_Student_Percentage",
    "KPI_Academic_Reputation_Score",
    "KPI_Research_Productivity_Index",
]

REQUIRED_SOURCE_COLUMNS = [
    "Rank_QS",
    "Rank_THE",
    "Name",
    "Country",
    "Region",
    "Year",
    "Academic_Reputation_Score",
    "Citations_per_Faculty_Score",
    "Students_to_Staff_Ratio",
    "International_Students",
    "Research_Environment",
    "Research_Quality",
    "Industry_Impact",
    "International_Research_Network_Score",
]

TEXT_COLUMNS = ["Name", "Country", "Region", "Size", "Focus", "Research", "Status"]

COUNTRY_ALIASES = {
    "USA": "United States",
    "U.S.A.": "United States",
    "United States of America": "United States",
    "UK": "United Kingdom",
    "U.K.": "United Kingdom",
    "Republic of Korea": "South Korea",
}

KPI_DEFINITIONS = [
    {
        "field": "KPI_Global_Ranking_Score",
        "label": "Global Ranking Score",
        "formula": "AVERAGE(QS_Rank_Normalized, THE_Rank_Normalized)",
        "source_columns": "QS_Rank_Normalized; THE_Rank_Normalized",
        "scale": "0-100",
        "interpretation": "Higher scores represent stronger combined QS and THE rank performance.",
    },
    {
        "field": "KPI_Research_Impact_Score",
        "label": "Research Impact Score",
        "formula": "0.35*Citation Score + 0.45*Research Quality + 0.20*Industry Impact",
        "source_columns": "Citations_per_Faculty_Score; Research_Quality; Industry_Impact",
        "scale": "0-100",
        "interpretation": "Measures research influence using citations, research quality and industry impact.",
    },
    {
        "field": "KPI_Faculty_to_Student_Ratio",
        "label": "Faculty-to-Student Ratio",
        "formula": "1 / Students_to_Staff_Ratio",
        "source_columns": "Students_to_Staff_Ratio",
        "scale": "Decimal or percentage",
        "interpretation": "Represents academic staff availability per student.",
    },
    {
        "field": "KPI_International_Student_Percentage",
        "label": "International Student Percentage",
        "formula": "International_Students * 100",
        "source_columns": "International_Students",
        "scale": "Percentage points",
        "interpretation": "Converts the supplied international-student share into percentage points.",
    },
    {
        "field": "KPI_Academic_Reputation_Score",
        "label": "Academic Reputation Score",
        "formula": "Academic_Reputation_Score",
        "source_columns": "Academic_Reputation_Score",
        "scale": "0-100",
        "interpretation": "Retains the supplied QS academic-reputation score without modification.",
    },
    {
        "field": "KPI_Research_Productivity_Index",
        "label": "Research Productivity Index",
        "formula": "0.30*Research Quality + 0.25*Research Environment + 0.20*Citation Score + 0.15*Research Network + 0.10*Industry Impact",
        "source_columns": "Research_Quality; Research_Environment; Citations_per_Faculty_Score; International_Research_Network_Score; Industry_Impact",
        "scale": "0-100",
        "interpretation": "Proxy for research productivity; publication counts are not present in the source.",
    },
]

REQUIRED_DASHBOARD_PAGES = [
    "University Overview",
    "Research Analytics",
    "Student Analytics",
    "Country Comparison",
]

ALL_DASHBOARD_PAGES = REQUIRED_DASHBOARD_PAGES + ["Executive Command Center"]

BLOCKED_VISUAL_TYPES = {
    "azureMap",
    "filledMap",
    "map",
    "qnaVisual",
    "aiNarratives",
    "keyDriversVisual",
}
