# Tableau Build Guide for EduVision

This guide is extracted from the final design state in `dashboard/build_module4.py` and is meant to be a manual build reference for reconstructing the four dashboards natively in Tableau Public’s UI.

Important scope note:
- This document intentionally does not attempt to generate or repair any `.twb` or `.twbx` file.
- The purpose is to preserve the verified design decisions that were captured in the last working module script, including worksheet order, KPI-card layout, action wiring, and aggregation/grain rules.
- The workbook design was validated structurally in the existing project artifacts, but the actual Tableau engine rendering and action wiring remain a manual UI step.

## Shared design conventions and calculated fields

These are the exact calculated-field patterns already embedded in the module logic and should be recreated in Tableau as native calculated fields before building the worksheets:

1. `Top Country by Average Global Score`
   - Formula: `IF RANK(AVG([Global_Ranking_Score])) = 1 THEN [Country] END`
   - Used as a string field for the Country Comparison KPI card.
   - The KPI card itself should be built as a single-value worksheet and display the field with `ATTR(...)`.

2. `stats_number_students (log)`
   - Formula: `LOG([stats_number_students])`
   - Required for the enrollment binning logic.

3. `Enrollment Bin Label`
   - Formula:
     `IF [stats_number_students (log)] < LOG(10000) THEN "< 10,000" ELSEIF [stats_number_students (log)] < LOG(25000) THEN "10,000-25,000" ELSEIF [stats_number_students (log)] < LOG(50000) THEN "25,000-50,000" ELSEIF [stats_number_students (log)] < LOG(100000) THEN "50,000-100,000" ELSE "100,000+" END`
   - This is the readable bucket label shown to viewers. The underlying logic remains log-domain, but the user-facing bins are real enrollment units.

4. `Region Coverage`
   - Formula: `"N/A (no Region column)"`
   - This is the placeholder string for the University Overview KPI card because the shipped dataset does not contain a usable region field.

## Dashboard 1: University Overview

Subtitle: `Rankings, reputation, and global context`

### Build order

1. Worksheet: `University Overview - Top 10 universities`
   - Chart/mark type: Bar
   - Rows: `University`
   - Columns: `Global_Ranking_Score`
   - Aggregation: `AVG(Global_Ranking_Score)` is the intended score axis; the view is additionally Top-N filtered to the top 10 universities.
   - Top-N filter: `University` Top 10 by `AVG([Global_Ranking_Score])`
   - Sort: descending by `Global_Ranking_Score`
   - Grain: university-level detail
   - Notes: label field is `University`

2. Worksheet: `University Overview - Global score distribution`
   - Chart/mark type: Map
   - Rows: `Country`
   - Columns: `Global_Ranking_Score`
   - Aggregation: `AVG(Global_Ranking_Score)`
   - Top-N filter: none
   - Grain: country-level aggregated view
   - Notes: this is the country map/symbol view for the dashboard; country selections are intended to drive the rest of the dashboard filters

3. Worksheet: `University Overview - Reputation vs. ranking`
   - Chart/mark type: Circle (scatter)
   - Rows: `Academic_Reputation_KPI`
   - Columns: `Global_Ranking_Score`
   - Aggregation: standard Tableau aggregation of the two score measures; effectively the score measures are aggregated as averages on the axes
   - Detail: `University`
   - Grain: university-level detail
   - Notes: this is the scatter plot that should behave as the primary exploration sheet for university-level reputation vs. ranking

4. Worksheet: `University Overview - Global score histogram`
   - Chart/mark type: Bar
   - Rows: `Global_Ranking_Score (bin)`
   - Columns: `Number of Records`
   - Bin: `Global_Ranking_Score` binned in 5-point increments
   - Aggregation: histogram count (`Number of Records`)
   - Grain: university-level raw distribution, binned by score

5. Worksheet: `University Overview - University comparison`
   - Chart/mark type: Text table
   - Rows: `University`
   - Columns: all KPI columns in the comparison table
   - Aggregation: no explicit rollup; this is a detail table at university grain
   - Filters: `University` categorical filter is included in the design
   - Grain: university-level detail
   - Notes: the table includes `University` plus KPI fields such as `Global_Ranking_Score`, `Academic_Excellence_Score`, and `Research_Impact_Score`

### KPI cards (single-value worksheets)

Build these as small single-value worksheets, not captions.

1. `University Overview - KPI - Total Universities`
   - Formula/aggregation: `COUNTD(University)`

2. `University Overview - KPI - Average Global Score`
   - Formula/aggregation: `AVG(Global_Ranking_Score)`

3. `University Overview - KPI - Countries Represented`
   - Formula/aggregation: `COUNTD(Country)`

4. `University Overview - KPI - Region Coverage`
   - Formula/aggregation: string field `Region Coverage`
   - Exact display value: `N/A (no Region column)`

### Dashboard actions

Action matrix for University Overview:

- `Top 10 universities` -> `University comparison` on `University` as a filter
- `Top 10 universities` -> `Reputation vs. ranking` on `University` as a highlight
- `Reputation vs. ranking` -> `University comparison` on `University` as a filter
- `Reputation vs. ranking` -> `Top 10 universities` on `University` as a highlight
- `Global score distribution` -> `University comparison` on `Country` as a filter
- `Global score distribution` -> `Top 10 universities` on `Country` as a filter
- `Global score distribution` -> `Reputation vs. ranking` on `Country` as a filter
- `University comparison` -> `Top 10 universities` on `University` as a highlight
- `University comparison` -> `Reputation vs. ranking` on `University` as a highlight

### Grain summary

- `Top 10 universities`: university-level
- `Global score distribution`: country-level aggregate
- `Reputation vs. ranking`: university-level
- `Global score histogram`: university-level distribution, binned
- `University comparison`: university-level detail
- KPI cards: single-value aggregates (or a placeholder string for region coverage)

---

## Dashboard 2: Research Analytics

Subtitle: `Research impact, citations, and productivity`

### Build order

1. Worksheet: `Research Analytics - Top research institutions`
   - Chart/mark type: Bar
   - Rows: `University`
   - Columns: `Research_Impact_Score`
   - Aggregation: `AVG(Research_Impact_Score)` on the bar axis
   - Top-N filter: `University` Top 10 by `AVG([Research_Impact_Score])`
   - Sort: descending by `Research_Impact_Score`
   - Grain: university-level detail

2. Worksheet: `Research Analytics - Productivity profile`
   - Chart/mark type: Circle (scatter)
   - Rows: `Research_Productivity_Index`
   - Columns: `Research_Impact_Score`
   - Aggregation: standard Tableau aggregation of both score measures
   - Detail: `University`
   - Grain: university-level detail
   - Notes: this is the research productivity profile scatter

3. Worksheet: `Research Analytics - Citations by institution`
   - Chart/mark type: Bar
   - Rows: `University`
   - Columns: `scores_citations`
   - Aggregation: `AVG(scores_citations)` on the bar axis
   - Top-N filter: `University` Top 15 by `AVG([scores_citations])`
   - Sort: descending by `scores_citations`
   - Grain: university-level detail

4. Worksheet: `Research Analytics - Research score distribution`
   - Chart/mark type: Bar
   - Rows: `scores_research (bin)`
   - Columns: `Number of Records`
   - Bin: `scores_research` binned in 5-point increments
   - Aggregation: histogram count (`Number of Records`)
   - Grain: university-level distribution, binned

5. Worksheet: `Research Analytics - Research benchmark table`
   - Chart/mark type: Text table
   - Rows: `Country`
   - Columns: `University`, `Research_Productivity_Index`, and the research KPI fields in the table layout
   - Aggregation: no explicit rollup; the table is a detail list with country and university rows
   - Grain: mixed country-level + university-level table detail
   - Notes: the worksheet retains `Country` and `University` together with the research KPI columns

### KPI cards (single-value worksheets)

1. `Research Analytics - KPI - Research Impact`
   - Formula/aggregation: `AVG(Research_Impact_Score)`

2. `Research Analytics - KPI - Productivity Index`
   - Formula/aggregation: `AVG(Research_Productivity_Index)`

3. `Research Analytics - KPI - Citations`
   - Formula/aggregation: `AVG(scores_citations)`

4. `Research Analytics - KPI - Research Score`
   - Formula/aggregation: `AVG(scores_research)`

### Dashboard actions

- `Top research institutions` -> `Productivity profile` on `University` as a highlight
- `Top research institutions` -> `Citations by institution` on `University` as a filter
- `Top research institutions` -> `Research benchmark table` on `University` as a filter
- `Citations by institution` -> `Productivity profile` on `University` as a highlight
- `Citations by institution` -> `Top research institutions` on `University` as a filter
- `Citations by institution` -> `Research benchmark table` on `University` as a filter
- `Productivity profile` -> `Citations by institution` on `University` as a filter
- `Productivity profile` -> `Research benchmark table` on `University` as a filter
- `Productivity profile` -> `Top research institutions` on `University` as a highlight
- `Research benchmark table` -> `Top research institutions` on `Country` as a filter
- `Research benchmark table` -> `Citations by institution` on `Country` as a filter
- `Research benchmark table` -> `Productivity profile` on `Country` as a filter

### Grain summary

- `Top research institutions`: university-level
- `Productivity profile`: university-level
- `Citations by institution`: university-level
- `Research score distribution`: university-level distribution, binned
- `Research benchmark table`: mixed detail table with country and university rows

---

## Dashboard 3: Student Analytics

Subtitle: `International reach, enrollment, and faculty capacity`

### Build order

1. Worksheet: `Student Analytics - International student reach`
   - Chart/mark type: Bar
   - Rows: `Country`
   - Columns: `International_Student_Percentage`
   - Aggregation: `AVG(International_Student_Percentage)`
   - Sort: descending by `International_Student_Percentage`
   - Grain: country-level aggregated view

2. Worksheet: `Student Analytics - Enrollment vs. faculty ratio`
   - Chart/mark type: Circle (scatter)
   - Rows: `stats_number_students`
   - Columns: `Faculty_to_Student_Ratio`
   - Aggregation: standard Tableau aggregation of the two measure fields
   - Detail: `University`
   - Grain: university-level detail
   - Notes: this scatter is the enrollment vs. faculty-ratio view

3. Worksheet: `Student Analytics - Gender composition`
   - Chart/mark type: Bar (100% stacked)
   - Rows: `Country`
   - Columns: `female_percentage` and `male_percentage` as stacked composition fields
   - Aggregation: `AVG(female_percentage)` and `AVG(male_percentage)`
   - Stack fields: `female_percentage`, `male_percentage`
   - Grain: country-level aggregated composition
   - Notes: this is the country-level 100% stacked bar chart that displays gender composition by average values

4. Worksheet: `Student Analytics - Enrollment distribution`
   - Chart/mark type: Bar
   - Rows: `Enrollment Bin Label`
   - Columns: `Number of Records`
   - Bin/label logic: `LOG([stats_number_students])` -> bucket labels `< 10,000`, `10,000-25,000`, `25,000-50,000`, `50,000-100,000`, `100,000+`
   - Aggregation: histogram count (`Number of Records`)
   - Grain: university-level raw distribution mapped into readable real-unit bins

5. Worksheet: `Student Analytics - Student profile table`
   - Chart/mark type: Text table
   - Rows: `University`
   - Columns: `Country`, `International_Student_Percentage`, `Faculty_to_Student_Ratio`, `stats_number_students`
   - Aggregation: no explicit rollup; this is a detail table at university grain
   - Grain: university-level detail

### KPI cards (single-value worksheets)

1. `Student Analytics - KPI - Average International Students`
   - Formula/aggregation: `AVG(International_Student_Percentage)`

2. `Student Analytics - KPI - Average Faculty-to-Student Ratio`
   - Formula/aggregation: `AVG(Faculty_to_Student_Ratio)`

3. `Student Analytics - KPI - Total Enrolled Students`
   - Formula/aggregation: `SUM(stats_number_students)`

4. `Student Analytics - KPI - Universities with Enrollment`
   - Formula/aggregation: `COUNT(stats_number_students)`

### Dashboard actions

- `International student reach` -> `Student profile table` on `Country` as a filter
- `International student reach` -> `Gender composition` on `Country` as a filter
- `International student reach` -> `Enrollment vs. faculty ratio` on `Country` as a highlight
- `International student reach` -> `Enrollment distribution` on `Country` as a filter
- `Enrollment vs. faculty ratio` -> `Student profile table` on `University` as a filter
- `Enrollment vs. faculty ratio` -> `Gender composition` on `Country` as a filter
- `Gender composition` -> `Enrollment vs. faculty ratio` on `Country` as a highlight
- `Student profile table` -> `International student reach` on `Country` as a filter
- `Student profile table` -> `Gender composition` on `Country` as a filter

### Grain summary

- `International student reach`: country-level aggregated
- `Enrollment vs. faculty ratio`: university-level detail
- `Gender composition`: country-level aggregated stacked composition
- `Enrollment distribution`: university-level distribution, bucketed into real-unit labels
- `Student profile table`: university-level detail

---

## Dashboard 4: Country Comparison

Subtitle: `Benchmark countries and regional patterns`

### Build order

1. Worksheet: `Country Comparison - Country ranking comparison`
   - Chart/mark type: Bar
   - Rows: `Country`
   - Columns: `Global_Ranking_Score`
   - Aggregation: `AVG(Global_Ranking_Score)`
   - Sort: descending by `Global_Ranking_Score`
   - Grain: country-level aggregate only
   - Notes: this is the dashboard’s primary ranked-country benchmark view

2. Worksheet: `Country Comparison - Benchmark profile`
   - Chart/mark type: Bar
   - Rows: `Country`
   - Columns: selected KPI averages (country-level benchmark measures)
   - Aggregation: `AVG` of the selected KPI measures
   - Grain: country-level aggregate
   - Notes: `Benchmark profile` is the grouped bar view with multiple country-level KPI averages

3. Worksheet: `Country Comparison - Country KPI comparison`
   - Chart/mark type: Bar
   - Rows: `Country`
   - Columns: `Global_Ranking_Score` and `Research_Impact_Score`
   - Aggregation: `AVG(Global_Ranking_Score)`, `AVG(Research_Impact_Score)`
   - Grain: country-level aggregate

4. Worksheet: `Country Comparison - Country distribution`
   - Chart/mark type: Map
   - Rows: `Country`
   - Columns: `Research_Impact_Score`
   - Aggregation: `AVG(Research_Impact_Score)`
   - Grain: country-level aggregate

5. Worksheet: `Country Comparison - Benchmark detail`
   - Chart/mark type: Text table
   - Rows: `Country`
   - Columns: institution count plus KPI averages
   - Aggregation: country-level aggregate table
   - Grain: country-level aggregate only
   - Notes: this is the detail table for country benchmarks; it must not expose the raw 3,382-row university detail

### KPI cards (single-value worksheets)

1. `Country Comparison - KPI - Total Countries`
   - Formula/aggregation: `COUNTD(Country)`

2. `Country Comparison - KPI - Top Country by Global Score`
   - Formula/aggregation: `ATTR([Top Country by Average Global Score])`
   - Exact underlying calculated field: `IF RANK(AVG([Global_Ranking_Score])) = 1 THEN [Country] END`

3. `Country Comparison - KPI - Average Global Score`
   - Formula/aggregation: `AVG(Global_Ranking_Score)`

4. `Country Comparison - KPI - Average Research Impact`
   - Formula/aggregation: `AVG(Research_Impact_Score)`

### Dashboard actions

All actions in Country Comparison are filters, not highlights.

- `Country ranking comparison` -> `Benchmark profile` on `Country` as a filter
- `Country ranking comparison` -> `Country KPI comparison` on `Country` as a filter
- `Country ranking comparison` -> `Country distribution` on `Country` as a filter
- `Country ranking comparison` -> `Benchmark detail` on `Country` as a filter
- `Benchmark profile` -> `Country ranking comparison` on `Country` as a filter
- `Benchmark profile` -> `Country KPI comparison` on `Country` as a filter
- `Benchmark profile` -> `Country distribution` on `Country` as a filter
- `Benchmark profile` -> `Benchmark detail` on `Country` as a filter
- `Country KPI comparison` -> `Country ranking comparison` on `Country` as a filter
- `Country KPI comparison` -> `Benchmark profile` on `Country` as a filter
- `Country KPI comparison` -> `Country distribution` on `Country` as a filter
- `Country KPI comparison` -> `Benchmark detail` on `Country` as a filter
- `Country distribution` -> `Country ranking comparison` on `Country` as a filter
- `Country distribution` -> `Benchmark profile` on `Country` as a filter
- `Country distribution` -> `Country KPI comparison` on `Country` as a filter
- `Country distribution` -> `Benchmark detail` on `Country` as a filter
- `Benchmark detail` -> `Country ranking comparison` on `Country` as a filter
- `Benchmark detail` -> `Benchmark profile` on `Country` as a filter
- `Benchmark detail` -> `Country KPI comparison` on `Country` as a filter
- `Benchmark detail` -> `Country distribution` on `Country` as a filter

### Grain summary

- All Country Comparison worksheets are country-level aggregate views.
- This dashboard must not show the raw 3,382-row university extract.
- The design explicitly aggregates metrics by country and uses the Country field as the dashboard-wide filter.

---

## Final reconstruction checklist for Tableau Public

1. Create the calculated fields first:
   - `Top Country by Average Global Score`
   - `stats_number_students (log)`
   - `Enrollment Bin Label`
   - `Region Coverage`

2. Build the four dashboard tabs in this order:
   - University Overview
   - Research Analytics
   - Student Analytics
   - Country Comparison

3. Build each dashboard’s worksheets in the exact order shown above.

4. Build each KPI card as a single-value worksheet, not a text caption.

5. Wire actions exactly as listed above, using the rule already established in the source logic:
   - `highlight` for any action targeting a scatter plot
   - `filter` for all other actions

6. Keep the grain consistent with the design:
   - University Overview, Research Analytics, and Student Analytics contain a mix of university-level and country-level views.
   - Country Comparison must remain country-level aggregate only.

7. Do not attempt to serialize the workbook back to XML. Use this guide as the authoritative manual reconstruction reference.
