# Dashboard Testing Report

**Project Name**: Higher Education Performance Dashboard (EduVision)
**Date of Testing**: [Insert Date]
**Tested By**: [Insert Tester Name]
**Dashboard Version**: v1.0
**Target Environment**: Tableau Desktop / Tableau Reader

---

## 1. Executive Summary
Provide a brief summary of the testing phase. Mention if the dashboard is ready for production, or if there are critical issues holding up the release.

**Status**: [Pass / Fail / Pass with Conditions]

---

## 2. Test Execution Details

### 2.1 Data Validation Tests
| Test Case ID | Description | Expected Result | Actual Result | Status (Pass/Fail) | Notes/Jira ID |
|---|---|---|---|---|---|
| TC-D01 | Verify dataset source | Dashboard points to `university_final_dataset.xlsx` | | | |
| TC-D02 | Validate total record count | Record count matches expected row count in final data | | | |
| TC-D03 | KPI: Global Ranking Score | Values match manual calculations | | | |
| TC-D04 | KPI: Research Impact | Values match manual calculations | | | |

### 2.2 UI & Visualization Tests
| Test Case ID | Description | Expected Result | Actual Result | Status (Pass/Fail) | Notes/Jira ID |
|---|---|---|---|---|---|
| TC-U01 | Dashboard dimensions | Renders properly at expected resolution | | | |
| TC-U02 | Chart titles and labels | All text is visible, spelled correctly, and formatted | | | |
| TC-U03 | Tooltip content | Tooltips display clean, relevant information without raw variable names | | | |
| TC-U04 | Color consistency | University/Region colors are consistent across all charts | | | |

### 2.3 Functional & Interactivity Tests
| Test Case ID | Description | Expected Result | Actual Result | Status (Pass/Fail) | Notes/Jira ID |
|---|---|---|---|---|---|
| TC-F01 | Country/Region Filter | Modifying filter correctly updates all linked visuals | | | |
| TC-F02 | Highlight Actions | Clicking a university on a scatter plot highlights it on the bar charts | | | |
| TC-F03 | Clear Filters | Reverting/clearing filters resets the dashboard to default view | | | |

---

## 3. Defect Tracking

Log any issues discovered during testing below.

| Defect ID | Description | Severity (High/Med/Low) | Status (Open/Resolved) | Steps to Reproduce |
|---|---|---|---|---|
| BUG-001 | Example: Text overlaps in tooltip on small screens | Low | Open | Hover over small cluster in scatter plot |
| | | | | |

---

## 4. Performance Metrics
- **Average Load Time**: [e.g., 2.4 seconds]
- **Filter Apply Delay**: [e.g., < 1 second]

## 5. Sign-off

| Name | Role | Date | Signature |
|---|---|---|---|
| [Name] | QA Lead | [Date] | |
| [Name] | Project Manager | [Date] | |
