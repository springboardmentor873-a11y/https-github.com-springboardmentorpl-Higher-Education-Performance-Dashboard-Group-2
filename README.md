# 🎓 EduVision DV — Higher Education Performance Dashboard

> An interactive Tableau dashboard suite for analyzing global university rankings, research performance, student diversity, academic reputation, and country-level higher education trends.

---

## 📌 Project Overview

**EduVision DV** is a comprehensive **Higher Education Performance Dashboard** developed to transform raw global university data into meaningful, interactive, and decision-ready insights.

The project integrates publicly available higher education datasets, including university ranking and performance indicators, and processes them using **Python, Pandas, and NumPy** before visualizing the results through **Tableau**.

The final solution consists of **four interconnected interactive dashboards**:

1. 🏛️ University Overview
2. 🔬 Research Analytics
3. 🎓 Student Analytics
4. 🌍 Country Comparison

The dashboard suite enables users to compare universities and countries based on ranking performance, research impact, academic reputation, student population, internationalization, and other educational indicators.

---
🔄 Project Workflow
Step 1 — Data Collection

University ranking and performance datasets are collected from publicly available sources.

The collected information includes indicators related to:
University rankings
Academic reputation
Research performance
Student population
International students
Faculty/student ratio
Country
Regional information 

Step 2 — Data Cleaning & Transformation

Python is used to prepare the raw data for analysis.

Major preprocessing operations include:
Removing duplicate records
Handling missing values
Standardizing university names
Standardizing country names
Normalizing numerical indicators
Converting inconsistent data formats
Merging related datasets
Preparing Tableau-ready data

Target:
Dataset completeness above 95% with less than 2% missing values after cleaning.

Step 3 — KPI Engineering

Six major education performance KPIs are generated:
Global Ranking Score
Research Impact Score
Faculty-to-Student Ratio
International Student Percentage
Academic Reputation Score
Research Productivity Index

These KPIs convert raw educational indicators into comparable performance measures.

Step 4 — Tableau Dashboard Development

The processed dataset is imported into Tableau.

Interactive dashboards are developed using:
Charts
KPI cards
Maps
Treemaps
Scatter plots
Bar charts
Filters
Parameters
Dashboard actions
Comparative visualizations

Step 5 — Dashboard Integration

The four dashboards are integrated into a single Tableau workbook.

Users can navigate between:

University Overview
        ↓
Research Analytics
        ↓
Student Analytics
        ↓
Country Comparison

Global filters and dashboard interactions help users explore the data efficiently.

📊 Dashboards
1. 🏛️ University Overview

The University Overview Dashboard provides an executive-level summary of global university performance.

Key KPIs
Global Ranking Score
Research Impact Score
Academic Reputation Score
International Student Percentage
Visualizations
Top Universities by Global Ranking Score
Top 10 Universities based on QS and THE Rankings
Academic Reputation Analysis
Institutional Comparison
Global University Distribution

Purpose
This dashboard helps users quickly understand:

Which universities perform highly
How universities compare across ranking systems
Academic reputation across regions
Global distribution of universities
Institutional performance differences

2. 🔬 Research Analytics

The Research Analytics Dashboard focuses on university research performance.

Key KPIs
Research Impact Score
Research Productivity Index
Research Quality
Industry Impact
Visualizations
Research Impact Comparison
Top Research Institutions by Research Impact
Top Universities by Research Productivity
Top Universities by Research Quality
Research Environment Analysis
Research Quality Trend

Purpose
The dashboard helps identify:

High-impact research institutions
Universities with strong research productivity
Research quality differences
Relationship between research productivity and impact
Institutions with strong research environments

3. 🎓 Student Analytics

The Student Analytics Dashboard focuses on student population and diversity.

Key KPIs
International Student Percentage
Total Students
Female Students Percentage
Student-to-Staff Ratio
Visualizations
International Student Analysis
Faculty-to-Student Ratio Analysis
Enrollment Comparison
Student Distribution
Student Diversity Trends

Purpose
This dashboard enables users to analyze:

Student population
International student participation
Gender distribution
Faculty-to-student ratios
Enrollment differences
Student diversity

4. 🌍 Country Comparison

The Country Comparison Dashboard provides country-level benchmarking of higher education performance.

Key Metrics
Global Ranking Score
Academic Reputation
International Student Percentage
University Count
Research Impact Score
Faculty-to-Student Ratio
Visualizations
Country Comparison by Global Ranking Score
Country Comparison by Academic Reputation
Country International Students
University Count by Country
Education Performance Benchmarking
Top Performing Countries by Research Impact
Global University Distribution
Purpose
The dashboard helps users:

Compare countries
Identify high-performing education systems
Analyze university concentration
Compare research impact
Analyze international student participation
Benchmark education performance

📈 Key Performance Indicators
KPI	Description
Global Ranking Score	Represents the overall ranking/performance score of a university or country.
Research Impact Score	Measures the influence and impact of university research.
Faculty-to-Student Ratio	Indicates teaching capacity by comparing faculty numbers with student population.
International Student Percentage	Represents the proportion of international students within the student population.
Academic Reputation Score	Represents academic reputation based on available ranking indicators.
Research Productivity Index	Represents research output/productivity using available research indicators.

🧹 Data Cleaning

The raw university datasets are transformed into a standardized analytical dataset.

Cleaning Operations
Raw Dataset
    ↓
Remove Duplicates
    ↓
Handle Missing Values
    ↓
Standardize University Names
    ↓
Standardize Country Names
    ↓
Normalize Metrics
    ↓
Merge Datasets
    ↓
Final Tableau Dataset

Data Quality Goals
Dataset completeness: 95%+
Missing values: Less than 2%
Consistent university naming
Consistent country naming
Valid numerical indicators
Tableau-compatible dataset

🧮 KPI Engineering

The project creates six major analytical indicators.

1. Global Ranking Score

Used to compare overall university performance and ranking position.

2. Research Impact Score

Used to evaluate the influence of university research.

3. Faculty-to-Student Ratio

Used to understand teaching capacity and student-to-faculty balance.

4. International Student Percentage

Used to measure internationalization and student diversity.

5. Academic Reputation Score

Used to compare academic reputation among universities and countries.

6. Research Productivity Index

Used to compare research output/productivity among institutions.

🛠️ Technology Stack
Area	Technology
Data Collection	Python
Data Processing	Pandas, NumPy
Data Cleaning	Python, Jupyter Notebook
KPI Engineering	Python
Data Storage	CSV, Excel
Visualization	Tableau Desktop 
Dashboard Integration	Tableau Filters, Parameters, Actions

Documentation	Markdown, GitHub
📁 Project Structure

Recommended GitHub repository structure:

EduVision-DV/
│
├── README.md
│
├── data/
│   ├── university_raw_data.csv
│   ├── university_cleaned.csv
│   └── university_final_dataset.xlsx
│
├── scripts/
│   ├── data_collection.py
│   └── generate_education_kpis.py
│
├── notebooks/
│   └── education_cleaning.ipynb
│
├── dashboard/
│   └── EduVision_DV.twbx
│
├── screenshots/
│   ├── university_overview.png
│   ├── research_analytics.png
│   ├── student_analytics.png
│   └── country_comparison.png
│
└── docs/
    ├── dashboard_storyboard.pdf
    ├── dashboard_testing_report.pdf
    └── project_documentation.pdf

🎛️ Interactive Features
The Tableau dashboard suite provides multiple interactive capabilities.
Filters
Users can filter information based on:
University
Country
QS Region
Other available dimensions
Dashboard Navigation

Users can move between the four major analytical dashboards.
Comparative Analysis

Users can compare:
Universities
Countries
Ranking scores
Research performance
Student populations
Academic reputation
Drill-Down Exploration

Charts and dashboard interactions allow users to explore detailed information from high-level KPIs.

👥 Target Users

EduVision DV can be useful for:

🎓 Students
Compare universities
Understand university rankings
Explore international student presence
Analyze institutional performance

👨‍🏫 Academic Researchers
Study research performance
Compare research impact
Analyze academic reputation
Identify high-performing research institutions

🏛️ University Administrators
Benchmark institutional performance
Identify strengths and weaknesses
Compare research productivity
Analyze student diversity

🏛️ Policymakers
Compare higher education systems
Analyze country-level performance
Identify education trends
Support evidence-based policy decisions

📊 Education Consultants
Compare institutions
Analyze global education trends
Support university selection and benchmarking

📊 Expected Project Outcomes
The project delivers:

A unified higher education analytics solution
Cleaned and standardized educational datasets
Six engineered education KPIs
Four interactive Tableau dashboards
University-level performance analysis
Research performance analysis
Student diversity analysis
Country-level education benchmarking
Global university distribution analysis
Interactive filtering and dashboard navigation
A single integrated Tableau workbook

🧪 Testing & Validation

The dashboard is validated across multiple dimensions.

Data Validation
Check duplicate records
Check missing values
Verify university names
Verify country names
Validate numerical fields
KPI Validation
Verify KPI calculations
Compare calculated values with source indicators
Check aggregation behavior
Dashboard Testing
Test filters
Test dashboard navigation
Test interactive actions
Test visualizations
Check labels and values
Verify dashboard responsiveness
Target Quality
KPI Accuracy:        > 95%
Dataset Completeness: > 95%
Major Dashboard Issues: 0

📅 Project Milestones
Milestone 1 — Data Collection & Preparation

Modules
University Data Collection
Data Cleaning & Transformation
Deliverables
university_raw_data.csv
data_collection.py
university_cleaned.csv
education_cleaning.ipynb

Milestone 2 — KPI Engineering & Dashboard Planning

Modules
Education KPI Engineering
Dashboard Planning & Prototyping
Deliverables
university_final_dataset.xlsx
generate_education_kpis.py
Dashboard storyboard
Tableau prototype

Milestone 3 — Dashboard Development

Modules
University Overview
Research Analytics
Student Analytics
Country Comparison
Dashboard Integration
Deliverables
EduVision_DV.twbx

Milestone 4 — Testing & Delivery

Modules
Testing & Validation
Documentation & Project Delivery
Deliverables
QA checklist
Dashboard testing report
Project documentation
GitHub repository
Tableau workbook

▶️ How to Use the Project
Step 1 — Clone the Repository
git clone https://github.com/<your-username>/EduVision-DV.git

Step 2 — Install Python Dependencies
pip install pandas numpy jupyter

Step 3 — Prepare the Dataset
Place the raw university dataset inside:
data/

Step 4 — Run Data Processing
Run the data collection and cleaning scripts:
python scripts/data_collection.py

Then perform the cleaning and transformation process using:
notebooks/education_cleaning.ipynb

Step 5 — Generate KPIs
python scripts/generate_education_kpis.py

Step 6 — Open Tableau Workbook
Open:
dashboard/EduVision_DV.twbx
using Tableau Desktop.

📦 Final Deliverable
The primary project deliverable is:
EduVision_DV.twbx

The workbook contains four interconnected dashboards:

┌──────────────────────────────┐
│      University Overview     │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│       Research Analytics     │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│        Student Analytics     │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│       Country Comparison     │
└──────────────────────────────┘

🏆 Project Highlights
📊 4 Interactive Tableau Dashboards
📈 6 Education Performance KPIs
🌍 Global University Analysis
🏛️ University Ranking Comparison
🔬 Research Performance Analytics
🎓 Student Diversity Analytics
🌎 Country-Level Benchmarking
🗺️ Global University Distribution
🧹 Python-Based Data Cleaning
🔄 Integrated Tableau Workbook
📋 Interactive Filters and Dashboard Actions
🎓 Skills Demonstrated

This project demonstrates practical skills in:

Data Analytics
Data Cleaning
Exploratory Data Analysis
Python
Pandas
NumPy
KPI Engineering
Tableau
Data Visualization
Dashboard Design
Interactive Analytics
Data Integration
Education Analytics
Data Storytelling

📄 Project Information
Information	Details
Project Name:	EduVision DV
Project Type: Data Analytics & Visualization
Domain:	Higher Education Analytics
Primary Tool:	Tableau
Programming Language:	Python
Data Processing:	Pandas, NumPy
Dashboards	4
KPIs	6
Final Output	Tableau Workbook (.twbx)
Repository	GitHub

⭐ Conclusion

EduVision DV demonstrates how data analytics and interactive visualization can transform complex higher education datasets into meaningful insights.

By integrating university rankings, research indicators, student statistics, and country-level metrics, the project provides a unified platform for understanding global higher education performance.

The four-dashboard architecture enables users to move from institution-level performance to research analytics, student analytics, and country-level benchmarking.

👩‍💻 Author

Developed by Aishwarya Todkari
Computer Engineering Student
Project: EduVision DV — Higher Education Performance Dashboard

🙏 Thank You
