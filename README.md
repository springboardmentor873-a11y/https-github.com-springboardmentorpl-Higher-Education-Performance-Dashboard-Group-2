# EduVision Higher Education Performance Dashboard

EduVision is a Tableau-ready education analytics project combining QS World University Rankings 2024 and Times Higher Education World University Rankings 2024. It produces cleaned university data, derived education KPIs, four interactive dashboard views, and a packaged Tableau workbook.

## Project Contents

```text
scripts/       Data collection, cleaning, KPI generation, and Module 7 validation
data/raw/      Source QS, THE, and merged raw extracts
data/processed Cleaned CSV and final KPI-bearing XLSX datasets
dashboard/     Tableau workbook package, storyboard, and QA reports
docs/          Project, methodology, dashboard, and delivery documentation
outputs/       Generated visualization outputs
```

The main deliverables are [dashboard/eduvision_prototype.twbx](dashboard/eduvision_prototype.twbx), [data/processed/university_final_dataset_all_kpis.xlsx](data/processed/university_final_dataset_all_kpis.xlsx), and the documentation in [docs/project_documentation.md](docs/project_documentation.md).

## Setup

1. Create or activate a Python 3.10+ environment.
2. Install dependencies:

	```powershell
	python -m pip install -r requirements.txt
	```

3. Run the data pipeline when rebuilding from source:

	```powershell
	python scripts/data_collection.py
	python scripts/data_cleaning.py
	python scripts/generate_education_kpis.py
	```

4. Build the Tableau package:

	```powershell
	python dashboard/build_module4.py
	```

5. Run structural and independent-data QA:

	```powershell
	python scripts/module7_validation.py
	```

## Open the Dashboard

Open `dashboard/eduvision_prototype.twbx` in Tableau Desktop or Tableau Public. The workbook contains University Overview, Research Analytics, Student Analytics, and Country Comparison tabs. Country is the shared dashboard filter. Tableau was not installed in the development environment, so the workbook has been verified structurally and through independent XLSX calculations, but not opened in a live Tableau engine; see [dashboard/module7_dashboard_testing_report.md](dashboard/module7_dashboard_testing_report.md).

## Documentation

Read [docs/project_documentation.md](docs/project_documentation.md) for data sources, exact KPI formulas, dashboard behavior, methodology, QA status, and Tableau Public delivery steps.