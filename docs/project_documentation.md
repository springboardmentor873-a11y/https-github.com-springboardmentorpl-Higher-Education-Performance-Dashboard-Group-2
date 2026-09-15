# EduVision Higher Education Performance Dashboard

## 1. Project Overview

EduVision is an education analytics project for comparing university ranking performance, research strength, student composition, enrollment, and country-level benchmarks. The delivered Tableau workbook contains four dashboards:

- University Overview
- Research Analytics
- Student Analytics
- Country Comparison

The workbook is [dashboard/eduvision_prototype.twbx](../dashboard/eduvision_prototype.twbx). Its data source is [data/processed/university_final_dataset_all_kpis.xlsx](../data/processed/university_final_dataset_all_kpis.xlsx).

## 2. Data Sources and Merge

The project uses the 2024 editions of:

- QS World University Rankings: `data/raw/qs_rankings_2024.csv`
- Times Higher Education World University Rankings: `data/raw/the_rankings_2024.csv`

`data_collection.py` selects the ranking, institution, country, overall score, academic, research, internationalization, student, and staffing fields from both sources. It standardizes the source names to a common schema, lowercases and trims university and country names, removes punctuation and parenthetical text from university names, and performs an outer merge on `University` and `Country`. The merged extract is written to `data/raw/university_raw_data.csv`.

`data_cleaning.py` removes duplicate rows, cleans text fields, converts QS/THE rank and score ranges to numeric midpoints, removes commas from enrollment counts, converts international-student percentages to numeric values, and splits `stats_female_male_ratio` into `female_percentage` and `male_percentage`. The cleaned result is `data/processed/university_cleaned.csv`.

The final KPI dataset is `data/processed/university_final_dataset_all_kpis.xlsx`. The outer merge preserves institutions found in either ranking source; missing source values remain missing and are excluded from averages by the row-wise calculations described below.

## 3. KPI Definitions

Unless stated otherwise, row-wise averages use the available non-null component values and are rounded to two decimal places.

| KPI field | Exact definition |
|---|---|
| `Global_Ranking_Score` | `ROUND(AVERAGE(Overall_QS, Overall_THE), 2)`, ignoring a missing source score. If only one score exists, that score is used. |
| `Academic_Excellence_Score` | `ROUND(AVERAGE(Academic Reputation Score, Faculty Student Score, Citations per Faculty Score, scores_teaching, scores_research, scores_citations), 2)`, ignoring missing components. |
| `Research_Impact_Score` | `ROUND(AVERAGE(scores_citations, Citations per Faculty Score, International Research Network Score), 2)`, ignoring missing components. |
| `Faculty_to_Student_Ratio` | Direct mapping of cleaned THE `stats_student_staff_ratio`. It is not recalculated or inverted. |
| `International_Student_Percentage` | Direct mapping of cleaned THE `stats_pc_intl_students`, with percent signs removed and the value stored numerically from 0 to 100. |
| `Academic_Reputation_KPI` | Direct mapping of QS `Academic Reputation Score`. |
| `Research_Productivity_Index` | `ROUND(AVERAGE(scores_research, Citations per Faculty Score, International Research Network Score), 2)`, ignoring missing components. |

The Tableau workbook uses these fields as measures with live aggregations. For example, dashboard KPI cards use `AVG(Global_Ranking_Score)`, `AVG(Research_Impact_Score)`, `SUM(stats_number_students)`, or `COUNTD(University)` as appropriate. The Country Comparison Top Country card uses the calculated field `IF RANK(AVG([Global_Ranking_Score])) = 1 THEN [Country] END` with `ATTR` in its single-value worksheet.

The formulas are implemented in `scripts/generate_education_kpis.py`, not only inferred from the output. The generator reads `university_cleaned.csv`, writes the seven fields in the shipped column order, and produces both `university_final_dataset_all_kpis.xlsx` and the legacy `university_final_dataset.xlsx` filename. An end-to-end rerun was compared against the pre-change shipped workbook: 3,382 rows, 32 columns, and zero differing data cells.

Formula verification used the generator's CSV input representation, where both `Global_Ranking_Score` and `Academic_Excellence_Score` match 3,382 of 3,382 rows. Re-reading the exported XLSX as binary floats creates two tie-rounding differences for Global Ranking only; the regenerated workbook still matches the shipped workbook value-for-value because it uses the same CSV-to-XLSX calculation path.

## 4. Dashboard Guide

### University Overview

- **Top 10 universities:** horizontal bar chart of universities ranked by `Global_Ranking_Score`; a Top 10 University filter limits the view.
- **Global score distribution:** country-level map/symbol view using `Global_Ranking_Score`.
- **Reputation vs. ranking:** scatter plot using `Academic_Reputation_KPI` and `Global_Ranking_Score`, with University detail.
- **Global score histogram:** distribution of `Global_Ranking_Score` using its real Tableau bin field.
- **University comparison:** detail table containing University and KPI fields.

The Country filter applies across the dashboard. Selecting a country in the distribution view filters the Top 10 chart, scatter plot, and comparison table. Selecting or highlighting universities connects the Top 10, scatter, and comparison views.

### Research Analytics

- **Top research institutions:** Top 10 horizontal bar chart ranked by `Research_Impact_Score`.
- **Productivity profile:** scatter plot of `Research_Productivity_Index` against `Research_Impact_Score`, with University detail.
- **Citations by institution:** Top 15 bar chart ranked by `scores_citations`.
- **Research score distribution:** histogram of binned `scores_research`.
- **Research benchmark table:** Country, University, and research KPI detail.

The Country filter applies to all views. University selections and highlights connect the Top 10, citations, productivity, and benchmark table views; benchmark-table country selections filter the research charts.

### Student Analytics

- **International student reach:** country-level sorted bar chart of `AVG(International_Student_Percentage)`.
- **Enrollment vs. faculty ratio:** scatter plot of enrollment versus `Faculty_to_Student_Ratio`, with University detail.
- **Gender composition:** country-level 100-percent stacked bar chart using average female and male percentages.
- **Enrollment distribution:** enrollment distribution using a calculated log field and readable real-unit buckets.
- **Student profile table:** University, Country, international-student, faculty-ratio, and enrollment fields.

Country is the shared filter. Country selections connect the reach, gender, enrollment, and profile views. University selections from the enrollment-ratio and profile views connect back to the student charts.

### Country Comparison

- **Country ranking comparison:** countries ranked by `AVG(Global_Ranking_Score)`.
- **Benchmark profile:** grouped country bars for selected average KPI measures.
- **Country KPI comparison:** grouped country comparison of average global score and research impact.
- **Country distribution:** country map using average research impact.
- **Benchmark detail:** country, institution count, and KPI averages.

Country is the dashboard-wide filter. Country ranking, benchmark profile, KPI comparison, map, and detail selections are connected through the verified filter-action matrix.

## 5. Enrollment Methodology

Enrollment is highly concentrated below 100,000 students. The original coarse `10,000-100,000` range contained 1,571 of 2,671 non-null records (58.82%), so it was split using data-driven real-unit breakpoints:

- `< 10,000`
- `10,000-25,000`
- `25,000-50,000`
- `50,000-100,000`
- `100,000+`

The workbook defines `LOG([stats_number_students])` as a Tableau calculated field. The displayed `Enrollment Bin Label` compares that calculated log value against `LOG(10000)`, `LOG(25000)`, `LOG(50000)`, and `LOG(100000)`. This preserves the log-domain comparison while exposing real enrollment units to viewers. The earlier non-standard `<bin scale='log'>` construct and its orphaned size-20 enrollment bin were removed.

## 6. Validation and Known Limitation

Module 7 validation is implemented in `scripts/module7_validation.py`. It performs XML parsing, worksheet and KPI-zone checks, independent calculations directly from the source XLSX XML, Top-N direct-sort comparisons, exact Tableau field-reference checks, action source/target/field resolution, and education-metric range checks. The generated reports are:

- [QA checklist](../dashboard/module7_qa_checklist.md)
- [Dashboard testing report](../dashboard/module7_dashboard_testing_report.md)

The workbook was **not opened in Tableau Desktop or Tableau Public** because neither application was available in the development environment. Therefore repair prompts, live rendering, Tableau calculation execution, and visual blank/broken states remain engine-level limitations. Structural XML and independent data checks are rigorous substitutes, but they are not equivalent to opening the workbook in Tableau.

The workbook XML was subsequently repaired after Tableau load attempts reported schema errors. Worksheet rows, columns, panes, marks, repository revisions, dashboard zones, and windows now use the expected Tableau hierarchy. The rejected custom `class='top'`, `scale`/bin, dashboard layout, storyboard, and hand-authored action constructs were removed. Top-N views are encoded as valid categorical University member filters in the packaged XML, with member lists generated from the verified direct-sort results. The generator retains the verified 50-action source/target matrix for implementation in Tableau, but no action nodes are currently serialized because the earlier invented action schema prevented the workbook from loading. The regenerated package passes structural XML QA but still needs the documented real Tableau open/render check and action-wiring validation.

## 7. GitHub and Tableau Public Delivery

The repository is organized as:

```text
/scripts       Collection, cleaning, KPI generation, and validation scripts
/data/raw      QS, THE, and merged raw extracts
/data/processed Cleaned and final KPI datasets
/dashboard     Tableau workbook, storyboard, and QA reports
/docs          Project and delivery documentation
/outputs       Generated visualization outputs
```

To publish to Tableau Public, a user with Tableau access would:

1. Install or open Tableau Desktop/Public.
2. Open `dashboard/eduvision_prototype.twbx`.
3. Resolve any local data-path prompt by selecting the included final XLSX if Tableau requests it.
4. Inspect all four dashboard tabs and confirm representative charts render.
5. Sign in to Tableau Public and choose **Save to Tableau Public**.
6. Set workbook title, description, visibility, and extract/refresh options.
7. Publish and record the public URL in the project README or delivery notes.

No Tableau Public deployment was performed for this project.
