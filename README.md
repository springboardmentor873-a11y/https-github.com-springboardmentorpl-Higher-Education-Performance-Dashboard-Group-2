# Higher Education Performance Dashboard - Group 2

Welcome to the **Higher Education Performance Dashboard** project repository. This project focuses on analyzing, cleaning, and generating Key Performance Indicators (KPIs) for global universities using data from the QS World University Rankings and THE (Times Higher Education) World University Rankings.

## 🎯 Project Overview
This repository contains the complete data pipeline designed to integrate multiple university ranking datasets, clean the data to make it consistent, and generate targeted KPIs to be consumed by visualization tools (like Tableau or PowerBI).

## 🗂️ Project Structure
The project is modularized into a standard Data Science folder structure for maximum readability and maintainability.

```text
├── module_01/                            # Data Ingestion & Merging
│   ├── 2026 QS World University Rankings.csv
│   ├── THE World University Rankings 2016-2026.csv
│   ├── data_collection.py
│   └── university_raw_data.csv
├── module_02/                            # Data Cleaning & Standardization
│   ├── education_cleaning.ipynb
│   └── university_cleaned.csv
├── module_03/                            # KPI Engineering
│   ├── generate_education_kpis.py
│   └── university_final_dataset.xlsx
├── module_04/                            # Storyboard
│   └── dashboard_storyboard.pdf
├── module_05/                            # Tableau Dashboard File
│   └── eduvision_dashboard_v1.twb
├── module_06/                            # Tableau Packaged Workbook
│   └── EduVision_DV.twbx
├── module_07/                            # Tableau Packaged Workbook
│   └── EduVision_DV.twbx
├── module_08/                            # Dashboard Presentation
│   └── EduVision_Dashboard_Presentation.pptx
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
```

## 🚀 Modules Breakdown

### Module 1: Data Collection (`module_01`)
Handles the initial data ingestion.
- Reads the raw QS and THE ranking datasets.
- Renames columns to align with a target schema.
- Standardizes university names.
- Merges the datasets on the university name and exports the result to `module_01/university_raw_data.csv`.

### Module 2: Data Cleaning (`module_02`)
Handles data quality issues (implemented in a Jupyter Notebook for interactive exploration).
- Removes duplicate rows.
- Standardizes string columns (Names, Countries).
- Cleans and converts ranking metrics to proper numeric types.
- Imputes missing values (medians for numerical, 'Unknown' for categorical).
- Filters and aligns the dataset for dashboard consumption.
- Exports the cleaned dataset to `module_02/university_cleaned.csv`.

### Module 3: KPI Generation (`module_03`)
Generates actionable metrics for dashboard visualization.
- **Global Ranking Score**: Average of QS and THE overall scores.
- **Research Impact Score**: Average of Citations and Research Quality.
- **Academic Reputation Score**: Normalized Academic Reputation.
- **Research Productivity Index**: Average of Research Environment and Citations per Faculty.
- Exports the final metrics to `module_03/university_final_dataset.xlsx`.

### Dashboard & Visualization
The visualization deliverables built on top of the final dataset are stored in their respective module directories:
- **`module_04/dashboard_storyboard.pdf`**: Exported PDF of the dashboard storyboard for presentations and quick viewing.
- **`module_05/eduvision_dashboard_v1.twb`**: Tableau Workbook containing the dashboard layout and sheets.
- **`module_06/EduVision_DV.twbx`** & **`module_07/EduVision_DV.twbx`**: Tableau Packaged Workbooks containing the dashboard along with the extracted dataset.
- **`module_08/EduVision_Dashboard_Presentation.pptx`**: PowerPoint presentation summarizing the insights.

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
   python module_01/data_collection.py
   ```
2. **Run Data Cleaning**:
   Open and execute all cells in `module_02/education_cleaning.ipynb` using Jupyter Notebook or your preferred IDE.
3. **Generate KPIs**:
   ```bash
   python module_03/generate_education_kpis.py
   ```

---
*Developed by Group 2.*