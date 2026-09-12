# Module 2 – Data Cleaning & Transformation

## EduVision_DV | Higher Education Performance Dashboard

### 1. Module Overview

Module 2 focuses on **cleaning, standardizing, and transforming the raw university ranking data** collected in Module 1.

The objective is to improve data quality and consistency so that the resulting dataset can be used reliably for **KPI engineering and Tableau dashboard development**.

---

### 2. Module Objectives

The main objectives of Module 2 are:

- Remove duplicate university records.
- Standardize university names.
- Standardize country names.
- Normalize ranking metrics.
- Handle missing and inconsistent values.
- Transform the raw dataset into a structured format.
- Prepare a Tableau-ready dataset for the next stages of the project.

---

### 3. Input Dataset

The primary input for this module is the raw dataset generated during Module 1.

```
Module 1
    ↓
university_raw_data.csv
    ↓
Module 2 – Data Cleaning & Transformation
```

The raw data contains university ranking and performance information collected from the QS World University Rankings and Times Higher Education World University Rankings.

---

### 4. Data Cleaning Process

The cleaning workflow follows these major steps:

```
Load Raw University Data
        ↓
Inspect Dataset
        ↓
Remove Duplicate Records
        ↓
Standardize University Names
        ↓
Standardize Country Names
        ↓
Handle Missing Values
        ↓
Normalize Ranking Metrics
        ↓
Validate Cleaned Data
        ↓
Generate Tableau-Ready Dataset
```

---

### 5. Cleaning and Transformation Tasks

#### 5.1 Duplicate Removal
Duplicate records are identified and removed to avoid repeated university entries and inaccurate analysis.

#### 5.2 University Name Standardization
University names are standardized to improve consistency when comparing and integrating records from different ranking sources.

#### 5.3 Country Name Standardization
Country names are standardized so that universities belonging to the same country are grouped correctly during country-level analysis.

#### 5.4 Ranking Metric Normalization
Ranking-related fields are processed into consistent formats to support comparison and analysis across the collected datasets.

#### 5.5 Missing Value Handling
Missing and unavailable values are examined during the cleaning process to improve the quality of the final analytical dataset without incorrectly replacing unavailable information.

#### 5.6 Tableau-Ready Transformation
After cleaning and transformation, the dataset is structured so that it can be used for KPI engineering and Tableau visualizations.

---

### 6. Implementation

The data cleaning and transformation process is documented in a Jupyter Notebook:

```
notebooks/
└── education_cleaning.ipynb
```

The notebook contains the data preparation workflow used to transform the collected university data.

---

### 7. Module Deliverable

The main output of Module 2 is:

```
data/
└── university_cleaned.csv
```

This dataset contains the cleaned and standardized university information that will be used as input for **Module 3 – Education KPI Engineering**.

---

### 8. Repository Structure

```
02_Module_2_Data_Cleaning_Transformation/
│
├── README.md
│
├── data/
│   └── university_cleaned.csv
│
└── notebooks/
    └── education_cleaning.ipynb
```

---

### 9. Expected Evaluation

According to the project requirements, Module 2 is evaluated based on:

| Evaluation Area   | Target                     |
|--------------------|----------------------------|
| Missing Values     | Less than 2%               |
| Ranking Indicators | Consistent                 |
| Data Quality       | Clean and standardized     |
| Output             | Tableau-ready dataset      |

---

### 10. Technology Used

| Area                     | Technology       |
|--------------------------|-------------------|
| Programming              | Python            |
| Data Processing          | Pandas            |
| Numerical Processing     | NumPy             |
| Development Environment  | Jupyter Notebook  |
| Input Format             | CSV               |
| Output Format            | CSV               |

---

### 11. Module Outcome

At the completion of Module 2, the raw university ranking data from Module 1 is transformed into a cleaned and standardized dataset suitable for further analytical processing.

The cleaned dataset is passed to:

**Module 3 – Education KPI Engineering**

for calculation of the required higher-education performance KPIs.

---

### 12. Next Module

➡️ **Module 3 – Education KPI Engineering**

The next module focuses on calculating the six required education KPIs and preparing the final dataset for Tableau analysis.