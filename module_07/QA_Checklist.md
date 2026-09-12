# QA Checklist - EduVision Dashboard

This document provides a comprehensive Quality Assurance (QA) checklist for the **Higher Education Performance Dashboard (EduVision)**. 

## 1. Data Accuracy & Integrity
- [ ] **Data Source Verification**: Ensure the dashboard connects to `university_final_dataset.xlsx` correctly.
- [ ] **Data Completeness**: Check that all universities from both QS and THE datasets are present without unintended omissions.
- [ ] **KPI Calculations**:
  - [ ] Global Ranking Score is correctly calculated (Average of QS and THE).
  - [ ] Research Impact Score is accurate (Citations and Research Quality).
  - [ ] Academic Reputation Score is properly normalized.
  - [ ] Research Productivity Index matches expected output.
- [ ] **Null Values**: Ensure nulls or missing values are handled gracefully (e.g., displaying "N/A" rather than breaking calculations).

## 2. Visual Elements & UI
- [ ] **Layout**: Dashboard layout matches the `dashboard_storyboard.pdf`.
- [ ] **Titles & Labels**: All charts have clear titles, axis labels, and legends.
- [ ] **Color Palette**: Consistent color scheme used across all charts (categorical/sequential colors are appropriate).
- [ ] **Formatting**: Numbers are formatted correctly (e.g., decimals, percentages).
- [ ] **Responsiveness**: Dashboard renders well on intended screen sizes (Desktop/Laptop).

## 3. Interactivity & Functionality
- [ ] **Filters**: Global filters (e.g., Country, Region, Year) apply correctly across all relevant sheets.
- [ ] **Actions/Highlights**: Selecting a university in one chart highlights or filters it in other charts.
- [ ] **Tooltips**: Tooltips are customized, clear, and display relevant context when hovering over data points.
- [ ] **Navigation**: Any buttons or navigation links function properly.

## 4. Performance
- [ ] **Load Time**: Dashboard loads within an acceptable timeframe (e.g., < 3-5 seconds).
- [ ] **Filter Responsiveness**: Dashboard updates quickly when filters are applied.
- [ ] **Extract Size**: (For `.twbx`) Ensure the data extract is optimized and not unnecessarily large.

## 5. Accessibility & UX
- [ ] **Color Contrast**: Colors are distinct enough for users with color vision deficiencies.
- [ ] **Font Size**: Text is legible without zooming.
- [ ] **Clarity**: The "story" of the dashboard is clear to a new user.

## 6. Deployment
- [ ] **Packaged Workbook**: `.twbx` file successfully saves and opens with all data intact (`EduVision_DV.twbx`).
- [ ] **Tableau Server/Public**: (If applicable) Dashboard publishes correctly without losing formatting or connections.
