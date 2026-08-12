# University Rankings Data Analysis — Milestone 1

## Internship Project — Data Collection and Preparation

This project focuses on collecting, cleaning, standardizing, integrating, and validating university ranking data from the **QS World University Rankings 2026** and **Times Higher Education (THE) World University Rankings 2026**.

The project was completed as part of **Milestone 1: Data Collection and Preparation**.

---

## 🎯 Objectives

The main objectives of this milestone are:

- Collect QS World University Rankings 2026 data
- Collect THE World University Rankings 2026 data
- Collect university performance indicators
- Clean and preprocess the datasets
- Remove and validate duplicate universities
- Standardize university names
- Standardize country names
- Normalize ranking and performance metrics
- Integrate QS and THE university data
- Validate the quality of the merged dataset
- Create a Tableau-ready dataset
- Achieve more than 95% dataset completeness

---

## 📊 Datasets

### 1. QS World University Rankings 2026

The QS dataset contains university ranking information and performance indicators such as:

- QS 2026 Rank
- Previous Rank
- Academic Reputation
- Employer Reputation
- Faculty/Student Ratio
- Citations per Faculty
- International Faculty Ratio
- International Student Ratio
- International Research Network
- Employment Outcomes
- Sustainability
- Overall Score
- Country/Territory
- Region
- University characteristics

### 2. Times Higher Education World University Rankings 2026

The THE dataset contains indicators including:

- THE Rank
- University Name
- Country
- Student Population
- Students-to-Staff Ratio
- International Students
- Female-to-Male Ratio
- Overall Score
- Teaching
- Research Environment
- Research Quality
- Industry Impact
- International Outlook

---

## 🔄 Data Processing Pipeline

```text
QS 2026 Dataset ──────┐
                      │
                      ├──> Data Collection
                      │
THE 2026 Dataset ─────┘
                      │
                      ↓
               Data Cleaning
                      │
                      ↓
          Name & Country Standardization
                      │
                      ↓
             Ranking Normalization
                      │
                      ↓
          Controlled University Matching
                      │
                      ↓
             Match Validation
                      │
                      ↓
            Dataset Integration
                      │
                      ↓
          Final Data Quality Audit
                      │
                      ↓
             Tableau-Ready Dataset