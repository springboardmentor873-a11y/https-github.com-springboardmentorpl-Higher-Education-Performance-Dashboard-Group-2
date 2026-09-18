# Education Analytics Methodology

## 1. Project Overview

EduVision is a higher-education analytics project that combines QS World University Rankings 2026 and Times Higher Education (THE) World University Rankings 2026 data to create an integrated university performance analysis.

The methodology follows a structured data pipeline from source collection through validation and dashboard delivery.

---

## 2. Data Collection

The project begins with two ranking datasets:

- QS World University Rankings 2026
- Times Higher Education (THE) World University Rankings 2026

The source data is collected and converted into analysis-ready datasets during Module 1.

The collected datasets provide university ranking, academic, research, faculty, student, and internationalization-related information.

---

## 3. Data Cleaning and Transformation

The collected datasets undergo cleaning and transformation before they are used for analysis.

The main activities include:

- Standardizing university names.
- Cleaning text and categorical fields.
- Handling encoding issues.
- Preparing ranking and score fields for analysis.
- Matching universities between QS and THE datasets.
- Reviewing uncertain university matches.
- Validating final matches.
- Creating the cleaned merged dataset.

The final matching process produced 1,008 university records for the KPI engineering stage.

---

## 4. University Matching

QS and THE records are matched to create a unified university-level dataset.

The project used multiple matching approaches, including:

- Exact name and country matching.
- Fuzzy matching for high-confidence matches.
- Manual review and approval for remaining cases.

Country consistency was validated as part of the matching process.

---

## 5. KPI Engineering

After data integration, six project-defined KPIs are engineered.

The KPIs are:

1. Global Ranking Score
2. Research Impact Score
3. Faculty-to-Student Ratio
4. International Student Percentage
5. Academic Reputation Score
6. Research Productivity Index

The KPI calculations combine selected QS and THE indicators where applicable.

The resulting Tableau-facing dataset contains 1,008 university records and eight fields:

- University
- Country
- Global Ranking Score
- Research Impact Score
- Faculty-to-Student Ratio
- International Student Percentage
- Academic Reputation Score
- Research Productivity Index

---

## 6. Dashboard Development

The engineered KPI dataset is used to develop the EduVision Tableau dashboards.

The integrated workbook contains four dashboards:

- Overview Dashboard
- Research Dashboard
- Student analysis Dashboard
- Comparison Dashboard

Each dashboard focuses on a different analytical perspective while using the common university-level dataset.

---

## 7. Dashboard Interaction Design

The dashboards support interactive analysis through features such as:

- Filters
- University selection
- Highlighting
- Tooltips
- Dashboard navigation
- Comparison views
- Reset controls

These interactions allow users to move from high-level university performance to detailed research, student, and comparative analysis.

---

## 8. Testing and Validation

Testing is performed in Module 7 using both automated and manual validation.

### Automated Validation

The automated validation checks:

- Final KPI dataset existence.
- Expected row count.
- Duplicate university records.
- Required KPI columns.
- KPI missing-value checks.
- KPI numeric validation.
- KPI range validation.
- Availability of ranking-related fields.
- Integrated Tableau workbook existence.
- Expected dashboard structure.

Result:

**13 automated checks passed and 0 failed.**

### Manual Dashboard Validation

The four dashboards were manually tested for their expected interaction and behavior.

Result:

- Overview Dashboard: 5/5 PASS
- Research Dashboard: 5/5 PASS
- Student analysis Dashboard: 5/5 PASS
- Comparison Dashboard: 5/5 PASS

Total manual dashboard checks:

**20/20 PASS**

Overall Module 7 validation:

**33/33 checks passed.**

---

## 9. Final Data Flow

The complete project methodology can be summarized as:

QS 2026 + THE 2026
- Data Collection
- Data Cleaning & Transformation
- University Matching
- KPI Engineering
- Tableau Dashboard Development
- Testing & Validation
- Documentation & Project Delivery

---

## 10. Final Analytical Dataset

The primary Tableau-facing dataset is:

Module 3 - Education KPI Engineering/output/university_kpis.csv

This dataset contains 1,008 university records and the six project-defined KPIs used by the EduVision dashboards.

The full KPI dataset is also maintained as:

Module 3 - Education KPI Engineering/output/university_kpi_dataset.csv

The full dataset contains the supporting university-level fields used during KPI engineering and validation.

---

## 11. Methodology Note

The analytical metrics created in EduVision are project-defined KPIs intended for educational analytics and university comparison.

They should not be interpreted as official QS or THE ranking methodologies.
