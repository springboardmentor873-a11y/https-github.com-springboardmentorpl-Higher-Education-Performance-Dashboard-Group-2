# EduVision_DV: Higher Education Performance Dashboard



---

## 1. Project Statement

**EduVision_DV** is a comprehensive higher education analytics suite designed to evaluate global university rankings, research productivity, student diversity, academic excellence, and country-level educational benchmarks.

By integrating data from **QS World University Rankings** and **Times Higher Education (THE) World University Rankings**, this project transforms raw educational metrics into actionable insights through an interactive Tableau dashboard suite.

---

## 2. Project Outcomes & Architecture

- **Unified Data Ingestion**: Cleaned and integrated global university performance datasets (`747` total institutions, top `50` composite benchmarking).
- **Automated Data Pipeline**: Python ETL scripts for merging, band-rank resolution, cleaning, and KPI calculation.
- **KPI Engineering**: 6 custom educational KPIs + Composite Overall KPI Score (0-100 scale).
- **Tableau Dashboard Suite**: 4 interconnected interactive dashboards (`University Overview`, `Research Analytics`, `Student Analytics`, `Country Comparison`).
- **Quality Assurance**: Evaluated with >99% data completeness and 100% KPI numerical accuracy.

---

## 3. Project Directory Structure

```
EduVision_DV/
│
├── README.md                           # Main Project Documentation & Deliverable Sitemap
├── education.py                        # Module 2: Data Cleaning & Transformation Script
├── data_collection.py                  # Module 1: Data Collection & Merging Script
├── generate_education_kpis.py          # Module 3: KPI Engineering & Dataset Export Script
│
├── scripts/                            # Pipeline Source Code Directory
│   ├── data_collection.py
│   ├── education.py
│   └── generate_education_kpis.py
│
├── data/                               # Data Artifacts Directory
│   ├── university_raw_data.csv         # Raw merged dataset
│   ├── university_cleaned.csv          # Cleaned dataset (>99% completeness)
│   ├── university_final_dataset.xlsx   # Tableau-optimized Excel dataset
│   └── university_final_dataset_top50.csv # Top 50 university KPI dataset
│
├── dashboard/                          # Tableau Workbooks Directory
│   ├── eduvision_prototype.twbx        # Module 4: Prototype Tableau Workbook
│   ├── eduvision_dashboard_v1.twbx     # Module 5: Overview & Research Workbook
│   └── EduVision_DV.twbx               # Module 6 & 8: Final Integrated Tableau Workbook
│
└── docs/                               # Project Documentation Directory
    ├── dashboard_storyboard.md         # Wireframes, layout specs & storyboard
    ├── EduVision_Analytics_Methodology.md # KPI formulas & analytical methodology
    ├── Dashboard_User_Guide.md         # Step-by-step dashboard user manual
    ├── QA_Checklist.md                 # Quality Assurance checklist
    └── Dashboard_Testing_Report.md     # Testing & empirical validation report
```

---

## 4. Module Implementation Summary

### Milestone 1: Data Collection & Preparation
- **Module 1: University Data Collection**: `data_collection.py` ingests QS & THE datasets, standardizing institution keys to generate `university_raw_data.csv`.
- **Module 2: Data Cleaning & Transformation**: `education.py` resolves rank bands (e.g. `601-650` -> `625.5`), removes duplicates, handles missing values, and achieves **99.35% dataset completeness** in `university_cleaned.csv`.

### Milestone 2: KPI Engineering & Prototyping
- **Module 3: Education KPI Engineering**: `generate_education_kpis.py` calculates Global Ranking Score, Research Impact Score, Teaching Quality Score, and Overall Composite KPI Score, exporting `university_final_dataset.xlsx` and `university_final_dataset_top50.csv`.
- **Module 4: Dashboard Planning & Prototyping**: Wireframes and layout storyboards created in `docs/dashboard_storyboard.md`; prototype packaged workbook saved in `eduvision_prototype.twbx`.

### Milestone 3: Dashboard Development & Integration
- **Module 5: University Overview & Research Analytics**: Built top ranking scorecards, publication impact charts, and scatter visualizations in `eduvision_dashboard_v1.twbx`.
- **Module 6: Student Analytics & Country Comparison**: Built international student choropleth map, faculty-to-student ratio charts, regional trend plots, and global navigation controls in `EduVision_DV.twbx`.

### Milestone 4: Testing & Delivery
- **Module 7: Testing & Validation**: Validated KPI formulas (0.00% error rate) and filter interactivity documented in `docs/QA_Checklist.md` and `docs/Dashboard_Testing_Report.md`.
- **Module 8: Documentation & Delivery**: Comprehensive sitemap, methodology guide, user manual, organized folder structure (`/scripts`, `/data`, `/dashboard`, `/docs`), and production-ready `EduVision_DV.twbx`.

---

## 5. Execution & How to Run

### 1. Run Data Processing Pipeline
To re-run the entire data cleaning and KPI generation pipeline from source:

```bash
# Step 1: Ingest and merge raw ranking datasets
python scripts/data_collection.py

# Step 2: Clean, resolve band ranks, and standardize names
python scripts/education.py

# Step 3: Calculate KPIs and generate final datasets
python scripts/generate_education_kpis.py
```

### 2. Launch Tableau Dashboards
Open `EduVision_DV.twbx` in **Tableau Desktop** or **Tableau Reader** to interact with the dashboards.

---

## 6. Tech Stack

- **Data Processing**: Python 3.9+, Pandas, NumPy, OpenPyXL, Regex
- **Visualization & BI**: Tableau Desktop / Tableau Public (`.twbx`)
- **Documentation**: Markdown, GitHub Flavored Markdown, LaTeX KaTeX
