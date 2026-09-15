# Dashboard Planning & Storyboard Specification

## EduVision_DV (Higher Education Performance Dashboard)

### Document Metadata
- **Project Name**: EduVision_DV
- **Module**: Module 4 (Dashboard Planning & Wireframing)
- **Deliverable**: `dashboard_storyboard.md` / `dashboard_storyboard.pdf`
- **Target Audience**: Academic Administrators, Education Consultants, Policymakers, Researchers, Students

---

## 1. Executive Summary & Design Architecture

The EduVision_DV suite is designed as a 4-tier interactive analytics system delivering key insights across global university rankings, research productivity, student demographics, and country-level benchmarks.

### Architecture Overview
```
+---------------------------------------------------------------------------------+
|                                 GLOBAL FILTERS                                  |
|   Year (2024) | Region (All) | Country (All) | Subject Area (All) | Reset Filters|
+---------------------------------------------------------------------------------+
|                                KPI CARDS RIBBON                                 |
|  Top Ranking  | Total Unis | Avg Overall Score | Int'l Students % | Faculty Ratio |
+---------------------------------------------------------------------------------+
|                                                                                 |
|  +-----------------------------------+   +-----------------------------------+  |
|  |           VISUAL PANEL 1          |   |           VISUAL PANEL 2          |  |
|  |  (Top Universities / Map / Rank)  |   |  (Trend Lines / Distribution)     |  |
|  +-----------------------------------+   +-----------------------------------+  |
|                                                                                 |
|  +-----------------------------------+   +-----------------------------------+  |
|  |           VISUAL PANEL 3          |   |           VISUAL PANEL 4          |  |
|  |  (Bar Charts / Breakdown)         |   |  (Scatter / Regional Comparison)  |  |
|  +-----------------------------------+   +-----------------------------------+  |
+---------------------------------------------------------------------------------+
```

---

## 2. Dashboard Layout Wireframes & Storyboard

### Dashboard 1: University Overview
- **Purpose**: High-level executive view of top global universities, overall rankings, and reputation benchmarks.
- **Layout Grid**: 2x2 Grid with Top KPI Header Ribbon.
- **Components**:
  1. **Top 10 Universities by Global Ranking**: Sorted horizontal bar chart with rank badges.
  2. **Top 10 Universities by Overall Score Trend**: Multi-line trend chart comparing scores across evaluation years.
  3. **Universities by Region**: Donut chart displaying regional market share (North America, Europe, Asia, Oceania, South America).
  4. **Publications by Top 5 Universities**: Bar chart showing institutional publication volume.
  5. **Academic Reputation Score by Region**: Grouped bar visualization.
  6. **Faculty to Student Ratio by Region**: Vertical bar chart highlighting teaching intensity.

### Dashboard 2: Research Analytics
- **Purpose**: Deep dive into institutional research output, citations, citations per faculty, and global impact.
- **Layout Grid**: 3-column split view with performance scatter plots.
- **Components**:
  1. **Research Impact vs. Citations per Faculty**: Quadrant scatter chart for research efficiency.
  2. **Top 10 Research Institutions**: Sorted bar chart by Research KPI Score.
  3. **Research KPI by Region**: Comparative regional bar chart.
  4. **Citations per Faculty by Country**: Geo-heat breakdown.
  5. **University Research Detail Table**: Detailed data table with research quality score drill-down.

### Dashboard 3: Student Analytics
- **Purpose**: Evaluation of international diversity, faculty-to-student ratios, and student enrollment trends.
- **Layout Grid**: Geographical map header + split bar panels.
- **Components**:
  1. **International Students % by Region (Choropleth Map)**: World map highlighting international student concentration.
  2. **Faculty-to-Student Ratio Breakdown**: Bar chart comparing faculty accessibility across regions.
  3. **Student Diversity & International Outlook**: Dual-axis plot comparing international students vs. international outlook scores.
  4. **Top 10 Universities by Student Diversity**: Bar list of top diverse institutions.

### Dashboard 4: Country Comparison
- **Purpose**: Macro-level country benchmarking across academic metrics, research impact, and industry income.
- **Layout Grid**: Benchmarking panel + multi-metric comparative bar charts.
- **Components**:
  1. **Country Performance Benchmark**: Comparative score matrix by country.
  2. **Average QS Score by Country**: Bar chart ranking countries by mean university score.
  3. **Citations per Faculty by Country**: Bar chart comparing national research impact.
  4. **Industry Income & Innovation Score by Country**: Horizontal bar chart comparing industry partnership metrics.
  5. **Regional Education Trends**: Trend graph over time by geographic area.

---

## 3. Interactive Filters, Navigation & Actions

### Global Filters
- **Year Filter**: Dropdown filter (Single select / All).
- **Region Filter**: Multi-select dropdown (`North America`, `Europe`, `Asia`, `Oceania`, `South America`).
- **Country Filter**: Multi-select dropdown dynamically dependent on selected region.
- **Subject Area Filter**: Dropdown filter.

### Dashboard Actions & Interactivity
- **URL Navigation Buttons**: Top navigation bar linking `Overview`, `Research Analytics`, `Student Analytics`, `Country Comparison`, and `About`.
- **Hover Tooltips**: Formatted rich tooltips displaying exact score, global rank, country, and comparative delta vs prior year.
- **Filter Action**: Clicking a country on the world map highlights that country's institutions across all other charts on the dashboard.
- **Highlight Action**: Hovering over a university in the ranking table highlights its position in scatter plots and trend graphs.
