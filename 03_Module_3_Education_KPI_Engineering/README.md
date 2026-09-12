# Module 3 – Education KPI Engineering

## EduVision_DV | Higher Education Performance Dashboard

### 1. Module Overview

Module 3 focuses on **engineering the key higher-education performance KPIs** from the cleaned university dataset produced in Module 2.

The objective is to transform the standardized data into a set of measurable indicators that quantify university and country-level performance, ready for use in dashboard design and visualization.

---

### 2. Module Objectives

The main objectives of Module 3 are:

- Load the cleaned dataset from Module 2.
- Define and calculate the required education KPIs.
- Aggregate KPI values at the university and country level.
- Validate KPI calculations for accuracy and consistency.
- Produce a final, KPI-enriched dataset for dashboard development.

---

### 3. Input Dataset

The primary input for this module is the cleaned dataset generated during Module 2.

```
Module 2
    ↓
university_cleaned.csv
    ↓
Module 3 – Education KPI Engineering
```

---

### 4. KPI Engineering Process

The KPI engineering workflow follows these major steps:

```
Load Cleaned University Data
        ↓
Define KPI Formulas
        ↓
Calculate Ranking-Based KPIs
        ↓
Calculate Performance-Based KPIs
        ↓
Aggregate KPIs by University / Country
        ↓
Validate KPI Results
        ↓
Generate Final Education Dataset
```

---

### 5. Implementation

The KPI engineering process is documented in a Python script:

```
scripts/
└── generate_education_kpis.py
```

The script contains the logic used to calculate and compile the education KPIs from the cleaned dataset.

---

### 6. Module Deliverable

The main output of Module 3 is:

```
data/
└── university_final_dataset.xlsx
```

This dataset contains the cleaned university data enriched with the calculated KPIs, and will be used as input for **Module 4 – Dashboard Planning & Prototyping**.

---

### 7. Repository Structure

```
03_Module_3_Education_KPI_Engineering/
│
├── README.md
│
├── data/
│   └── university_final_dataset.xlsx
│
└── scripts/
    └── generate_education_kpis.py
```

---

### 8. Expected Evaluation

According to the project requirements, Module 3 is evaluated based on:

| Evaluation Area      | Target                          |
|-----------------------|----------------------------------|
| KPI Accuracy          | Correctly calculated per formula |
| KPI Coverage          | All six required KPIs present    |
| Data Consistency      | Aligned with cleaned dataset     |
| Output                | Dashboard-ready dataset          |

---

### 9. Technology Used

| Area                     | Technology       |
|--------------------------|-------------------|
| Programming              | Python            |
| Data Processing          | Pandas            |
| Numerical Processing     | NumPy             |
| Development Environment  | Script-based (.py)|
| Input Format             | CSV               |
| Output Format            | XLSX              |

---

### 10. Module Outcome

At the completion of Module 3, the cleaned university dataset from Module 2 is enriched with the six required education KPIs, producing a final analytical dataset ready for dashboard planning and visualization.

The final dataset is passed to:

**Module 4 – Dashboard Planning & Prototyping**

for storyboard design and prototype development.

---

### 11. Next Module

➡️ **Module 4 – Dashboard Planning & Prototyping**

The next module focuses on planning the dashboard story and building an early Tableau prototype using the final KPI dataset.