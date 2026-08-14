# Higher Education Performance Dashboard - Group 2

Welcome to the **Higher Education Performance Dashboard** project repository. This project focuses on analyzing, cleaning, and generating Key Performance Indicators (KPIs) for global universities using data from the QS World University Rankings and THE (Times Higher Education) World University Rankings.

## 🎯 Project Overview
This repository contains the complete data pipeline designed to integrate multiple university ranking datasets, clean the data to make it consistent, and generate targeted KPIs to be consumed by visualization tools (like Tableau or PowerBI).

## 🗂️ Project Structure
The project is modularized into a standard Data Science folder structure for maximum readability and maintainability.

```text
├── data/                                 # Datasets
│   ├── raw/                              # Original, immutable data dumps
│   │   ├── 2026 QS World University Rankings.csv
│   │   └── THE World University Rankings 2016-2026.csv
│   ├── interim/                          # Intermediate data that has been transformed
│   │   ├── university_raw_data.csv       # Merged dataset
│   │   └── university_cleaned.csv        # Cleaned dataset (missing values handled, standardized)
│   └── final/                            # Final dataset ready for visualization
│       └── university_final_dataset.xlsx # Contains generated KPIs
├── src/                                  # Source Code Modules
│   ├── module1_data_collection/          # Data Ingestion & Merging
│   │   └── data_collection.py
│   ├── module2_data_cleaning/            # Data Cleaning & Standardization
│   │   └── education_cleaning.ipynb
│   └── module3_kpi_generation/           # KPI Engineering
│       └── generate_education_kpis.py
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
```

## 🚀 Modules Breakdown

### Module 1: Data Collection (`src/module1_data_collection`)
Handles the initial data ingestion.
- Reads the raw QS and THE ranking datasets.
- Renames columns to align with a target schema.
- Standardizes university names.
- Merges the datasets on the university name and exports the result to `data/interim/university_raw_data.csv`.

### Module 2: Data Cleaning (`src/module2_data_cleaning`)
Handles data quality issues (implemented in a Jupyter Notebook for interactive exploration).
- Removes duplicate rows.
- Standardizes string columns (Names, Countries).
- Cleans and converts ranking metrics to proper numeric types.
- Imputes missing values (medians for numerical, 'Unknown' for categorical).
- Filters and aligns the dataset for dashboard consumption.
- Exports the cleaned dataset to `data/interim/university_cleaned.csv`.

### Module 3: KPI Generation (`src/module3_kpi_generation`)
Generates actionable metrics for dashboard visualization.
- **Global Ranking Score**: Average of QS and THE overall scores.
- **Research Impact Score**: Average of Citations and Research Quality.
- **Academic Reputation Score**: Normalized Academic Reputation.
- **Research Productivity Index**: Average of Research Environment and Citations per Faculty.
- Exports the final metrics to `data/final/university_final_dataset.xlsx`.

## 🛠️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/springboardmentorpl/Higher-Education-Performance-Dashboard-Group-2.git
   cd Higher-Education-Performance-Dashboard-Group-2
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Usage

To run the pipeline from scratch, execute the modules in sequence from the project root:

1. **Run Data Collection**:
   ```bash
   python src/module1_data_collection/data_collection.py
   ```
2. **Run Data Cleaning**:
   Open and execute all cells in `src/module2_data_cleaning/education_cleaning.ipynb` using Jupyter Notebook or your preferred IDE.
3. **Generate KPIs**:
   ```bash
   python src/module3_kpi_generation/generate_education_kpis.py
   ```

---
*Developed by Group 2.*