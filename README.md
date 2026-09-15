# EduVision_DV - Higher Education Performance Dashboard 📊

## 📌 Project Overview

EduVision_DV is a comprehensive Higher Education Performance Dashboard project designed to analyze university rankings, research performance, student diversity, academic excellence, and global education trends.

The project uses university ranking datasets such as QS World University Rankings and Times Higher Education World University Rankings. The data is cleaned, transformed, and converted into useful education KPIs before being visualized through interactive Tableau dashboards.

The final project consists of four interconnected dashboards:

- 🎓 University Overview
- 🔬 Research Analytics
- 👨‍🎓 Student Analytics
- 🌍 Country Comparison

## 🎯 Project Objectives

- Analyze university rankings and performance.
- Compare universities across countries and regions.
- Analyze research performance and impact.
- Study student diversity and international students.
- Develop meaningful higher education KPIs.
- Build interactive Tableau dashboards.
- Provide country-level education benchmarking.

---

# 🔄 Project Workflow

Data Collection
↓
Data Cleaning & Transformation
↓
KPI Engineering
↓
Dashboard Planning
↓
Dashboard Development
↓
Dashboard Integration
↓
Testing & Validation
↓
Documentation & Delivery

---

# 📚 Project Modules

## Module 1 - University Data Collection

### Tasks

- Download QS Ranking datasets.
- Download World University Ranking datasets.
- Collect university performance indicators.
- Merge ranking datasets into a common structure.

### Deliverables

- `university_raw_data.csv`
- `data_collection.py`

### Outcome

A complete and integrated university dataset is prepared for further processing.

---

## Module 2 - Data Cleaning & Transformation

### Tasks

- Remove duplicate records.
- Standardize university names.
- Standardize country names.
- Normalize ranking metrics.
- Create Tableau-ready datasets.

### Deliverables

- `university_cleaned.csv`
- `education_cleaning.ipynb`

### Outcome

The raw data is cleaned, standardized, and prepared for KPI engineering and visualization.

---

## Module 3 - Education KPI Engineering

### Tasks

Calculate the following education KPIs:

- Global Ranking Score
- Research Impact Score
- Faculty-to-Student Ratio
- International Student Percentage
- Academic Reputation Score
- Research Productivity Index

### Deliverables

- `university_final_dataset.xlsx`
- `generate_education_kpis.py`

### Outcome

The required education KPIs are calculated and the final dataset is optimized for Tableau.

---

## Module 4 - Dashboard Planning & Prototyping

### Tasks

Design dashboard layouts for:

- University Overview
- Research Analytics
- Student Analytics
- Country Comparison

Define:

- Filters
- Navigation
- Dashboard actions
- Interactive comparisons

### Deliverables

- `dashboard_storyboard.pdf`

### Outcome

Dashboard designs and prototype functionality are prepared before development.

---

## Module 5 - Dashboard Development

### University Overview

The University Overview dashboard focuses on:

- Top university rankings
- Global university distribution
- Academic reputation analysis
- University performance trends
- Institutional comparison

### Research Analytics

The Research Analytics dashboard focuses on:

- Publications analysis
- Citation performance
- Research productivity trends
- Top research institutions
- Research impact comparison

### Deliverable

- `University Overview.twbx`
- `Research Analytics.twbx`


### Outcome

Interactive University Overview and Research Analytics dashboards are developed and ranking metrics are validated.

---

## Module 6 - Dashboard Integration

### Student Analytics

The Student Analytics dashboard focuses on:

- International student analysis
- Faculty-to-student ratio analysis
- Student diversity trends
- Enrollment comparisons
- Student distribution analysis

### Country Comparison

The Country Comparison dashboard focuses on:

- Country ranking comparison
- Education performance benchmarking
- Regional education trends
- Top performing countries

### Dashboard Integration

The dashboards are integrated using:

- Global filters
- Navigation controls
- Parameter actions
- Dashboard linking

### Deliverable

- `Student Analytics.twbx`
- `Country Comparision.twbx`

### Outcome

All dashboards are integrated into a unified Tableau workbook with working navigation and filters.

---

## Module 7 - Testing & Validation

### Tasks

- Validate KPI calculations.
- Verify ranking calculations.
- Test dashboard interactions.
- Validate educational metrics.

### Deliverables

- `QA Checklist`
- `Dashboard Testing Report`

### Outcome

The dashboards and KPI calculations are tested to ensure accuracy and proper functionality.

---

## Module 8 - Documentation & Project Delivery

### Tasks

Prepare project documentation including:

- Dataset sources
- KPI definitions
- Dashboard guide
- Education analytics methodology

### Project Organization

```text
/scripts
/data
/dashboard
/docs
