# EduVision: Higher Education Performance Dashboard

## 📌 Project Overview
This project aims to develop a comprehensive higher education analytics dashboard suite. By leveraging publicly available datasets, this project transforms raw educational data into actionable insights through interactive Tableau dashboards. It enables students, academic researchers, university administrators, and policymakers to evaluate institutional performance, compare universities globally, analyze research output, and identify global education trends.

## 🎯 Problem Statement
Higher education data is spread across different ranking sources, making it difficult to objectively compare universities, analyze research performance, understand student diversity, and identify global trends. EduVision bridges this gap by providing one connected dashboard suite that cleans, standardizes, and unifies this data.

## 🗄️ Data Sources
The dashboard is powered by two major global ranking datasets:
*   **QS World University Rankings 2026** (Top 1500)
*   **THE World University Rankings 2016–2024** 

## 🛠️ Tools & Technologies Used
*   **Data Processing & Cleaning:** Python (Pandas, NumPy)
*   **Data Visualization & Dashboarding:** Tableau Desktop
*   **Version Control & Repository:** GitHub

## ⚙️ Techniques & Methodology
The project followed an 8-week, 4-milestone methodology:
1.  **Data Collection:** Merged ranking datasets into a common structure.
2.  **Data Cleaning & Transformation:** Handled missing values, removed duplicates, and standardized university and country names using Python.
3.  **KPI Engineering:** Calculated normalized, multi-dimensional metrics to evaluate educational performance.
4.  **Dashboard Development:** Designed layouts, interactive filters, drill-downs, and dashboard actions in Tableau.
5.  **Testing & Integration:** Connected four independent views into one cohesive `.twbx` workbook.

## 📊 Key Performance Indicators (KPIs) Engineered
To provide a standardized evaluation across different ranking systems, the following six core KPIs were engineered:
1.  **Global Ranking Score (GRS):** Derived from QS and THE Overall Scores.
2.  **Research Impact Score (RIS):** Derived from available research indicators.
3.  **Faculty-Student Ratio Score (FSR):** Standardized metric for teaching capacity.
4.  **International Student Percentage (ISP):** Mapped from International Students Score.
5.  **Academic Reputation Score (ARS):** Based on QS Academic Reputation and THE Overall Score proxy.
6.  **Research Productivity Index (RPI):** Calculated using Citations per Faculty and International Research Network data.

## 🖥️ Dashboard Suite Modules
The final output is a unified Tableau workbook consisting of four interconnected dashboards:
1.  **University Overview:** Analyzes top university rankings, global distribution, academic reputation, and institutional comparisons.
2.  **Research Analytics:** Highlights citation performance, research productivity trends, and top research institutions globally.
3.  **Student Analytics:** Visualizes international student participation, faculty-to-student ratios, and regional student diversity.
4.  **Country Comparison:** Benchmarks country-level education performance and regional education trends.

## 📄 Project Documents & References
The following foundational documents were referenced and utilized to build the project scope, layouts, and logic:
*   `EduVision_Presentation (1).pptx`: Project pitch and high-level architectural overview.
*   `HEP.pdf`: Detailed project statement, milestones, evaluation criteria, and technical stack.
*   `dashboard_storyboard.pdf`: Initial wireframes and layout designs for the Tableau dashboards.
