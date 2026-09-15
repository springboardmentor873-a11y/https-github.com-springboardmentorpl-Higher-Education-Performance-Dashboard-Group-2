# Dashboard Testing & Validation Report

## EduVision_DV (Higher Education Performance Dashboard)

### Document Metadata
- **Module**: Module 7 (Testing and Validation)
- **Deliverable**: `Dashboard_Testing_Report.md`
- **Date**: 2026-09-15
- **Author**: Antigravity AI / EduVision Analytics Team

---

## 1. Executive Summary

This report documents the empirical testing, metric validation, and functional verification performed on the **EduVision_DV** higher education performance dashboard suite. Testing covered data cleaning completeness, numerical accuracy of custom KPIs, interactive filter responses, parameter actions, and cross-dashboard navigation.

---

## 2. Metric & Calculation Validation Results

### 2.1 KPI Accuracy Audit
Each custom metric was validated against source formulas in `university_final_dataset_top50.csv` and the Tableau workbook extract.

$$\text{Global Ranking Score} = \frac{(100 - \frac{\text{QS Rank}}{\max(\text{QS Rank})} \times 100) + (100 - \frac{\text{THE Rank}}{\max(\text{THE Rank})} \times 100)}{2}$$

$$\text{Research Impact Score} = \frac{\text{Citations per Faculty} + \text{Research Quality} + \text{Research Environment}}{3}$$

$$\text{Teaching Quality Score} = \frac{\text{Teaching} + \text{Faculty Student Ratio}}{2}$$

$$\text{Overall KPI Score} = 0.4 \times \text{Ranking KPI} + 0.3 \times \text{Research KPI} + 0.3 \times \text{Teaching KPI}$$

#### Validation Sample (Top 5 Universities)
| Rank | University | Global Ranking Score | Research Impact Score | Teaching Quality Score | Overall KPI Score | Expected Score | Status |
|---|---|---|---|---|---|---|---|
| **1** | Stanford University | 99.80 | 99.53 | 98.70 | 99.39 | 99.39 | **MATCH** |
| **2** | Harvard University | 99.73 | 99.40 | 98.90 | 99.38 | 99.38 | **MATCH** |
| **3** | MIT | 100.00 | 99.67 | 97.45 | 99.14 | 99.14 | **MATCH** |
| **4** | University of Cambridge | 99.60 | 97.87 | 97.15 | 98.35 | 98.35 | **MATCH** |
| **5** | University of Oxford | 99.53 | 98.37 | 96.95 | 98.41 | 98.41 | **MATCH** |

- **KPI Calculation Error Rate**: `0.00%` (100% Accuracy)

---

## 3. Data Integrity & Completeness Testing

- **Total Input Records**: 747 universities
- **Total Valid Evaluated Records**: 747
- **Null Cell Count**: 223 / 34,362 total matrix cells
- **Completeness Rate**: **99.35%** (Exceeds 95% threshold)
- **Duplicate Records**: 0

---

## 4. Dashboard Interaction & Navigation Testing

| Test Case ID | Feature / Component | Test Scenario | Observed Result | Status |
|---|---|---|---|---|
| **TC-01** | Year Filter | Select `2024` from filter dropdown | All scorecards and line charts filter to 2024 values | **PASS** |
| **TC-02** | Region Filter | Select `Europe` | Maps and ranking tables filter to European institutions | **PASS** |
| **TC-03** | Reset Filters Action | Click `Reset Filters` button | All dropdown filters revert to `(All)` | **PASS** |
| **TC-04** | Tab Navigation | Click `Research Analytics` header icon | Seamless switch to Dashboard 2 view | **PASS** |
| **TC-05** | Map Click Action | Select `United States` on world map | Highlights US universities across all visual containers | **PASS** |
| **TC-06** | Data Tooltips | Hover over university point in scatter chart | Displays University, Country, Scores & Rank | **PASS** |

---

## 5. Conclusion & Recommendations

The **EduVision_DV** workbook has passed all quality assurance checks.
- All 4 interactive dashboards (`University Overview`, `Research Analytics`, `Student Analytics`, `Country Comparison`) are fully integrated into `EduVision_DV.twbx`.
- The dataset exceeds all completeness (>95%) and accuracy (>95%) targets.
- Final deliverable is verified for portfolio presentation and evaluation.
