# # Higher Education Performance Dashboard

## 📊 Project Overview

The **Higher Education Performance Dashboard (EduVision)** is a data analytics project focused on analyzing global university performance using university ranking data from **QS World University Rankings** and **Times Higher Education (THE)**.

The project involves collecting, cleaning, and combining university ranking datasets, engineering key performance indicators (KPIs), and developing interactive dashboards to analyze university, research, student, and country-level performance.

---

## 🎯 Project Objectives

* Collect global university ranking data from QS and Times Higher Education (THE).
* Clean and standardize data from different ranking sources.
* Combine datasets into a structured analytical dataset.
* Engineer meaningful education performance KPIs.
* Analyze university rankings, research performance, academic reputation, student metrics, and country-level performance.
* Develop interactive dashboards using Tableau.

---

## 🛠️ Technologies Used

* Python
* Pandas
* Jupyter Notebook
* CSV
* Excel
* Tableau
* Git & GitHub

---

# 📁 Project Structure

```text
Higher-Education-Performance-Dashboard/
│
├── Data/
│   ├── 2026_QS.csv
│   └── 2026_THE.csv
│
├── Output/
│   ├── university_cleaned.csv
│   ├── university_raw_data.csv
│   └── university_final_dataset.xlsx
│
├── data_collection.py
├── education_cleaning.ipynb
├── generate_education_kpis.py
└── README.md
```

---

# 🚀 Project Modules

## Module 1 — Data Collection

University ranking data was collected from two major ranking sources:

* QS World University Rankings
* Times Higher Education (THE)

### Files

* `Data/2026_QS.csv`
* `Data/2026_THE.csv`
* `data_collection.py`

---

## Module 2 — Data Cleaning & Preparation

The QS and THE datasets were cleaned and standardized into a unified analytical dataset.

### Key Results

* **Total Records:** 3,695
* **Total Columns:** 43
* **THE Records:** 2,191
* **QS Records:** 1,504
* **Duplicate Rows:** 0
* **Missing University Names:** 0
* **Missing Country Names:** 0

The datasets contain different metrics for QS and THE. Therefore, missing values are retained where a metric is not applicable to a particular ranking source.

### Outputs

* `Output/university_cleaned.csv`
* `Output/university_raw_data.csv`

---

## Module 3 — KPI Engineering

Six education performance KPIs were engineered from the cleaned dataset.

### 1. Global Ranking Score

Measures the overall university performance using available QS and THE overall ranking scores.

### 2. Research Impact Score

Measures research quality and impact using:

* QS Citations per Faculty Score
* THE Research Quality

### 3. Faculty-to-Student Ratio

Calculated using:

```text
Faculty-to-Student Ratio = 1 / Students-to-Staff Ratio
```

Measures faculty availability relative to the student population.

### 4. International Student Percentage

Uses THE international student percentage data to measure international student presence and diversity.

### 5. Academic Reputation Score

Uses the QS Academic Reputation Score to evaluate academic reputation.

### 6. Research Productivity Index

Calculated using:

```text
Research Productivity Index =
(Research Environment + Research Quality) / 2
```

Measures research environment and research quality together.

### Module 3 Files

* `generate_education_kpis.py`
* `Output/university_final_dataset.xlsx`

---

## 📈 Planned Dashboards

The project will include four interactive Tableau dashboards:

### 1. University Overview

Analyze overall university performance, rankings, academic reputation, and institutional comparisons.

### 2. Research Analytics

Analyze research impact, research productivity, and citation performance.

### 3. Student Analytics

Analyze international student percentage, faculty-to-student ratio, and student-related metrics.

### 4. Country Comparison

Compare higher education performance across countries and regions.

---

## 🔄 Project Workflow

```text
Data Collection
      ↓
Data Cleaning & Preparation
      ↓
KPI Engineering
      ↓
Dashboard Planning & Prototyping
      ↓
Dashboard Development
      ↓
Dashboard Integration & Finalization
```

---

## 📌 Current Project Status

| Module                                          | Status         |
| ----------------------------------------------- | -------------- |
| Module 1 — Data Collection                      | ✅ Completed    |
| Module 2 — Data Cleaning & Preparation          | ✅ Completed    |
| Module 3 — KPI Engineering                      | ✅ Completed    |
| Module 4 — Dashboard Planning & Prototyping     | 🚧 In Progress |
| Module 5 — Dashboard Development                | ⏳ Pending      |
| Module 6 — Dashboard Integration & Finalization | ⏳ Pending      |

---

## 👤 Contributor

**Vishal Patel**

Branch: `Vishal-Patel`

---
