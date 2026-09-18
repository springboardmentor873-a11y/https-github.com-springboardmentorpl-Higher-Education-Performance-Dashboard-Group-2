# EduVision - Final Project Documentation

## 1. Project Title

**Higher Education Performance Dashboard - EduVision**

## 2. Project Objective

The objective of EduVision is to transform higher-education ranking data into an interactive analytics solution that allows users to explore university performance across overall ranking, research, student, academic reputation, and comparative indicators.

The project integrates QS World University Rankings 2026 and Times Higher Education (THE) World University Rankings 2026 data.

## 3. Project Modules

The project was completed through eight structured modules.

### Module 1 - University Data Collection

Collected the QS 2026 and THE 2026 source datasets and prepared the raw data for further processing.

### Module 2 - Data Cleaning & Transformation

Cleaned, standardized, matched, reviewed, and validated university records to create an integrated university dataset.

### Module 3 - Education KPI Engineering

Created six project-defined education KPIs and produced the final KPI datasets used for dashboard development.

### Module 4 - Dashboard Planning & Prototyping

Created dashboard storyboards and planned the structure, navigation, filters, interactions, and analytical views for EduVision.

### Module 5 - Build University Overview & Research Analytics

Developed the Overview Dashboard and Research Dashboard in Tableau.

### Module 6 - Build Student Analytics & Country Comparison

Developed the Student analysis Dashboard and Comparison Dashboard in Tableau.

### Module 7 - Testing & Validation

Performed automated data and workbook validation together with manual dashboard testing.

Validation result: 13 automated checks passed, 20 manual dashboard checks passed, and 33 total validation checks passed.

### Module 8 - Documentation and Project Delivery

Prepared the project documentation, methodology, KPI definitions, dashboard guide, source information, and final project handover materials.

## 4. Final Dashboards

The integrated EduVision Tableau workbook contains four dashboards:

1. Overview Dashboard
2. Research Dashboard
3. Student analysis Dashboard
4. Comparison Dashboard

## 5. Final KPI Dataset

The primary Tableau-facing dataset is:

Module 3 - Education KPI Engineering/output/university_kpis.csv`n
Dataset characteristics:

- 1,008 university records
- 8 fields
- 6 project-defined KPIs
- 0 missing values across the six KPI fields
- 0 duplicate university records

The six KPIs are:

1. Global Ranking Score
2. Research Impact Score
3. Faculty-to-Student Ratio
4. International Student Percentage
5. Academic Reputation Score
6. Research Productivity Index

## 6. Integrated Tableau Workbook

The main integrated Tableau workbook is:

EduVision.twb`n
It contains all four project dashboards and represents the final integrated dashboard solution.

## 7. Documentation Set

The Module 8 documentation contains:

- Dataset_Sources.md - source datasets and data lineage.
- KPI_Definitions.md - definitions, formulas, ranges, and dashboard usage of the six KPIs.
- Dashboard_Guide.md - dashboard purposes, key information, interactions, and recommended workflow.
- Education_Analytics_Methodology.md - end-to-end analytical methodology and validation approach.
- Final_Project_Documentation.md - overall project summary and final handover information.

## 8. Repository Structure

The repository is organized into module-wise project folders:

- Module 1 - University Data Collection/
- Module 2 - Data Cleaning & Transformation/
- Module 3 - Education KPI Engineering/
- Module 4 - Dashboard Planning & Prototyping/
- Module 5 - Build University Overview & Research Analytics/
- Module 6 - Build Student Analytics & Country Comparison/
- Module 7 - Testing & Validation/
- Module 8 - Documentation and Project Delivery/

## 9. Final Project Workflow

Data Collection
? Data Cleaning & Transformation
? University Matching
? KPI Engineering
? Dashboard Planning
? Dashboard Development
? Testing & Validation
? Documentation & Project Delivery

## 10. Project Outcome

EduVision provides an integrated Tableau-based analytical solution for exploring university performance using ranking, research, student, academic reputation, and comparative indicators.

The final project combines structured data engineering, KPI development, dashboard design, interactive analytics, validation, and project documentation into a single workflow.

## 11. Handover Information

The project repository contains the module-wise implementation and supporting project artifacts.

The final documentation should be read together with the Module 3 KPI datasets, the integrated EduVision.twb Tableau workbook, the Module 7 QA checklist and validation artifacts, and the Module 4 dashboard planning storyboard.

These artifacts together provide the data, analytical logic, dashboard implementation, testing evidence, and documentation required to understand and review the EduVision project.

## 12. Important Notes

The six KPIs used by EduVision are project-defined analytical metrics. They are not official QS or THE ranking formulas.

The project uses QS and THE 2026 datasets as source data and applies its own data integration, transformation, KPI engineering, and dashboard methodology.

