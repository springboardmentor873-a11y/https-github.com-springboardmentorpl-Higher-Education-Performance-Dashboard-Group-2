# Education Analytics Methodology Guide

## EduVision_DV (Higher Education Performance Dashboard)

### Document Metadata
- **Module**: Module 8 (Documentation and Project Delivery)
- **Deliverable**: `EduVision_Analytics_Methodology.md`
- **Scope**: Data collection methodology, cleaning algorithms, KPI engineering formulas, composite weighting models, and Tableau visualization standards.

---

## 1. Introduction & Methodology Framework

The **EduVision_DV** analytics methodology provides a standardized, objective framework for benchmarking global higher education institutions across international ranking frameworks (QS World University Rankings and Times Higher Education Rankings).

```
   RAW RANKING DATASETS (QS + THE)
                 │
                 ▼
    MODULE 1: DATA COLLECTION
    - Load QS CSV & THE Excel files
    - Normalize text casing & university matching keys
                 │
                 ▼
   MODULE 2: CLEANING & TRANSFORMATION
    - Standardize institution & country names
    - Convert rank bands (e.g. '601-650') to float midpoints
    - Verify completeness (>95%)
                 │
                 ▼
     MODULE 3: KPI ENGINEERING
    - Compute Global Ranking Score (0-100)
    - Compute Research Impact Score (0-100)
    - Compute Teaching Quality Score (0-100)
    - Compute Overall Composite KPI Score (0-100)
                 │
                 ▼
  MODULES 4-6: TABLEAU DASHBOARD SUITE
    - University Overview
    - Research Analytics
    - Student Analytics
    - Country Comparison
```

---

## 2. Dataset Sources & Ingestion

### Primary Data Sources
1. **QS World University Rankings (2026)**:
   - Evaluates Academic Reputation, Employer Reputation, Citations per Faculty, Faculty-Student Ratio, International Students, and Sustainability.
2. **Times Higher Education (THE) World University Rankings (2026)**:
   - Evaluates Teaching, Research Environment, Research Quality (Citations), Industry Impact, and International Outlook.

---

## 3. Data Cleaning & Transformation Standard

### 3.1 Duplicate Resolution
Institutions are matched using normalized lower-case text keys. Duplicate instances are purged based on primary QS institution naming.

### 3.2 Rank Band Resolution
Rankings often report institutions in range bands rather than discrete integers (e.g. "601-650" or "801-1000"). To enable mathematical operations, these ranges are resolved into numeric midpoints using regular expression pattern matching:

$$\text{Midpoint Rank} = \frac{\text{Lower Bound} + \text{Upper Bound}}{2}$$

---

## 4. KPI Engineering & Mathematical Models

To evaluate university performance holistically, 6 core KPIs and 1 Composite Overall Score are calculated:

### 4.1 Global Ranking Score
Quantifies global standing by normalizing QS and THE rank positions onto a 0-100 relative score scale:

$$\text{QS Norm} = 100 - \left(\frac{\text{QS Rank}}{\max(\text{QS Rank})} \times 100\right)$$

$$\text{THE Norm} = 100 - \left(\frac{\text{THE Rank}}{\max(\text{THE Rank})} \times 100\right)$$

$$\text{Global Ranking Score} = \frac{\text{QS Norm} + \text{THE Norm}}{2}$$

### 4.2 Research Impact Score
Measures institution-wide research output, quality, and citation efficiency:

$$\text{Research Impact Score} = \frac{\text{Citations per Faculty} + \text{Research Quality} + \text{Research Environment}}{3}$$

### 4.3 Teaching Quality Score
Evaluates instructional commitment and staff availability:

$$\text{Teaching Quality Score} = \frac{\text{Teaching Score} + \text{Faculty-Student Ratio Score}}{2}$$

### 4.4 Overall Composite KPI Score
Combines the three core pillars with weighted priorities:

$$\text{Overall KPI Score} = 0.40 \times \text{Global Ranking Score} + 0.30 \times \text{Research Impact Score} + 0.30 \times \text{Teaching Quality Score}$$

### 4.5 Performance Category Classification
Institutions are categorized based on their Overall KPI Score:
- **Excellent**: $\text{Overall KPI Score} \ge 90.0$
- **Very Good**: $75.0 \le \text{Overall KPI Score} < 90.0$
- **Good**: $60.0 \le \text{Overall KPI Score} < 75.0$
- **Average**: $\text{Overall KPI Score} < 60.0$

---

## 5. Tableau Data Source Optimization

The resulting dataset (`university_final_dataset.xlsx` / `university_final_dataset_top50.csv`) contains 25 standardized fields structured specifically for high-performance Tableau calculations, LOD expressions, parameter actions, and cross-filtering.
