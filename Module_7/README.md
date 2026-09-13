# https-github.com-springboardmentorpl-Higher-Education-Performance-Dashboard-Group-2

# 🎓 EduVision – Higher Education Performance Dashboard

## 📌 Project Overview

**EduVision** is a data analytics and visualization project designed to analyze **higher education performance of universities and countries**.

The project combines university ranking data, cleans and transforms the data using **Python**, calculates important **Education KPIs**, and presents the results through **interactive Tableau dashboards**.

---

## 🎯 Objectives

* Analyze university performance using ranking and academic indicators.
* Compare research performance across universities.
* Analyze student-related indicators.
* Compare higher education performance across countries.
* Create interactive and user-friendly Tableau dashboards.
* Support easy comparison and decision-making through data visualization.

---

## 📊 KPIs Used

The project includes the following key performance indicators:

* **Global Ranking Score**
* **Research Impact Score**
* **Faculty-to-Student Ratio**
* **International Student Percentage**
* **Academic Reputation Score**
* **Research Productivity Index**

---

## 🔄 Project Workflow

```text
Raw Datasets
     ↓
Data Cleaning
     ↓
Data Transformation
     ↓
Dataset Merging
     ↓
KPI Engineering
     ↓
Final Dataset
     ↓
Tableau Visualization
     ↓
Interactive Dashboards
```

---

## 🧹 Data Cleaning

Python was used for data preprocessing.

Main techniques include:

* Removing duplicate records
* Removing empty rows and columns
* Standardizing column names
* Removing extra spaces
* Handling invalid/missing values
* Converting required columns into numeric format
* Removing duplicate university records

---

## 📈 KPI Engineering

The cleaned dataset was used to create the required education KPIs.

### Global Ranking Score

Converts university ranking into a score where a **better rank receives a higher score**.

### Research Impact Score

Uses the available **Citations per Faculty** indicator.

### Faculty-to-Student Ratio

Uses the available **Faculty Student Ratio score** from the dataset.

### International Student Percentage

Uses the available **International Student Score** because raw international-student and total-student counts were not available.

### Academic Reputation Score

Uses the available **Academic Reputation score**.

### Research Productivity Index

Calculated using available research-related indicators such as:

* Citations per Faculty
* Research Environment
* Research Quality

---

# 📊 Tableau Dashboards

The project contains **four interactive dashboards**.

## 1. 🎓 University Overview

Provides an overall view of university performance.

### Includes:

* Global Ranking
* Research Impact
* Academic Reputation
* International Student Percentage
* Faculty-to-Student Ratio
* Research Productivity
* Top university comparisons
* Country-level analysis

---

## 2. 🔬 Research Analytics

Focuses specifically on research performance.

### Includes:

* Research Impact
* Research Productivity
* Citations per Faculty
* Research Quality
* Research Environment
* Top research institutions
* Research comparisons

---

## 3. 👩‍🎓 Student Analytics

Focuses on student-related indicators.

### Includes:

* International Student Percentage
* Faculty-to-Student Ratio
* University comparisons
* Country comparisons
* International Students vs Academic Reputation

---

## 4. 🌍 Country Comparison

Compares higher education performance across countries.

### Includes:

* University distribution
* Global Ranking Score
* Research Impact
* Academic Reputation
* International Student Percentage
* Research Productivity
* Country-level comparisons

---

## 🎛️ Filters and Navigation

Interactive features include:

* **Country Filter**
* **University Filter**
* **Rank Filter**
* Dashboard navigation buttons
* Interactive chart selections

Navigation allows users to move between:

```text
University Overview
        ↕
Research Analytics
        ↕
Student Analytics
        ↕
Country Comparison
```

---

## 🛠️ Technologies Used

### Data Processing

* Python
* Pandas
* NumPy
* Scikit-learn

### Visualization

* Tableau

### Data Format

* CSV
* Excel

---

## 📁 Project Deliverables

```text
📁 EduVision
│
├── 📄 README.md
├── 🐍 Data Cleaning Python Script
├── 🐍 KPI Engineering Python Script
├── 📊 university_final_dataset.xlsx
└── 📈 eduvision_dashboard_v1.twbx
```

---

## 🚀 Final Outcome

EduVision provides an **interactive higher education analytics platform** that helps users understand university performance from four perspectives:

**University → Research → Students → Country**

The project transforms raw ranking data into meaningful KPIs and interactive visualizations that make higher education performance easier to analyze and compare.
