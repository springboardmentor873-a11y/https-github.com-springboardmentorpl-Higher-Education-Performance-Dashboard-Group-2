# Dataset Sources

## Overview

The EduVision project uses higher-education ranking data from the QS World University Rankings 2026 and the Times Higher Education (THE) World University Rankings 2026.

## 1. QS World University Rankings 2026

**Source:** QS World University Rankings 2026

**Role in the project:**
- Provides university ranking information.
- Provides QS overall scores.
- Provides academic reputation information.
- Provides faculty-to-student ratio information.
- Provides citations-per-faculty information used in research-related KPI calculations.

## 2. Times Higher Education World University Rankings 2026

**Source:** Times Higher Education (THE) World University Rankings 2026

**Role in the project:**
- Provides university ranking information.
- Provides THE overall scores.
- Provides student population information.
- Provides students-to-staff ratio information.
- Provides international student information.
- Provides research quality and research environment information.

## 3. Data Processing

The source datasets were collected, cleaned, matched, validated, and transformed before being used for KPI engineering and dashboard development.

The final Tableau-facing KPI dataset is:

Module 3 - Education KPI Engineering/output/university_kpis.csv

It contains 1,008 university records and the six project-defined education KPIs used by the EduVision dashboards.

## 4. Data Usage

The QS and THE datasets are used as source data for analysis and KPI engineering. The composite KPIs created in this project are project-defined calculations and should not be interpreted as official QS or THE metrics.

## 5. Data Lineage

QS 2026 + THE 2026
- Data Collection
- Data Cleaning & Transformation
- University Matching
- KPI Engineering
- Dashboard Development
- Testing & Validation
- Final Documentation & Delivery
