# KPI Definitions

## Overview

The EduVision project defines six project-specific Key Performance Indicators (KPIs) using data from the QS World University Rankings 2026 and Times Higher Education (THE) World University Rankings 2026.

These KPIs were engineered to support university performance, research, student, and country-level analysis in the EduVision dashboards.

> **Important:** The KPI formulas below are project-defined calculations. They are not official QS or THE ranking formulas.

---

## 1. Global Ranking Score

### Purpose

Measures overall university performance using the QS and THE overall scores.

### Formula

Global Ranking Score =

(QS Overall Score + THE Overall Score) / 2

### Range

0–100

### Dashboard Usage

- Overview Dashboard
- Comparison Dashboard

---

## 2. Research Impact Score

### Purpose

Measures research impact using citations performance and THE research quality.

### Formula

Research Impact Score =

(QS Citations per Faculty Score + THE Research Quality Score) / 2

### Range

0–100

### Dashboard Usage

- Research Dashboard
- Comparison Dashboard

---

## 3. Faculty-to-Student Ratio

### Purpose

Provides a project-defined measure combining QS faculty-to-student ratio performance with the THE ratio percentile.

### Formula

Faculty-to-Student Ratio =

(QS Faculty-Student Ratio Score + THE Ratio Percentile × 100) / 2

### Range

0–100

### Dashboard Usage

- Comparison Dashboard
- Student analysis Dashboard

---

## 4. International Student Percentage

### Purpose

Measures the proportion of international students at a university.

### Formula

International Student Percentage =

THE International Students × 100

### Range

0–100

### Dashboard Usage

- Student analysis Dashboard
- Comparison Dashboard

---

## 5. Academic Reputation Score

### Purpose

Represents the academic reputation score provided by QS.

### Formula

Academic Reputation Score =

QS Academic Reputation Score

### Range

0–100

### Dashboard Usage

- Overview Dashboard
- Comparison Dashboard

---

## 6. Research Productivity Index

### Purpose

Provides a project-defined research productivity measure using QS citations performance and two THE research indicators.

### Formula

Research Productivity Index =

(QS Citations per Faculty Score + THE Research Environment Score + THE Research Quality Score) / 3

### Range

0–100

### Dashboard Usage

- Research Dashboard
- Comparison Dashboard

---

## KPI Summary

| KPI | Range | Primary Dashboard |
|------|--------|-------------------|
| Global Ranking Score | 0–100 | Overview Dashboard |
| Research Impact Score | 0–100 | Research Dashboard |
| Faculty-to-Student Ratio | 0–100 | Comparison Dashboard |
| International Student Percentage | 0–100 | Student analysis Dashboard |
| Academic Reputation Score | 0–100 | Overview Dashboard |
| Research Productivity Index | 0–100 | Research Dashboard |

## Final KPI Dataset

The final Tableau-facing dataset containing these six KPIs is:

Module 3 - Education KPI Engineering/output/university_kpis.csv

The dataset contains 1,008 university records and no missing values in the six KPI fields.
