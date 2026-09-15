# Module 7 QA Checklist

| Check | Result | Evidence |
|---|---|---|
| TWBX XML parse | PASS | The packaged workbook XML is well-formed. |
| Tableau engine open/render | FAIL / LIMITATION | Tableau Desktop/Public is unavailable; engine-level opening and rendering remain unverified. |
| Dashboard and worksheet inventory | PASS | Found 4 dashboards and 36 worksheets. |
| 16 KPI worksheet zones | PASS | KPI zones use the repaired dashboard/zones schema. |
| KPI aggregation bindings | FAIL / LIMITATION | Validated 16 live KPI worksheet bindings. |
| Enrollment log labels | PASS | IF [stats_number_students (log)] < LOG(10000) THEN "< 10,000" ELSEIF [stats_number_students (log)] < LOG(25000) THEN "10,000-25,000" ELSEIF [stats_number_students (log)] < LOG(50000) THEN "25,000-50,000" ELSEIF [stats_number_students (log)] < LOG(100000) THEN "50,000-100,000" ELSE "100,000+" END |
| No orphan enrollment bin | PASS | No unsupported enrollment bin element remains. |
| Top-N filters and exact ordering | FAIL / LIMITATION | Validated categorical member filters and descending sort fields for Top 10, Top 10, and Top 15. |
| Dashboard action resolution | FAIL / LIMITATION | The invalid hand-authored action XML was removed to make the workbook loadable; the generator still contains the 50-action source/target matrix, but no actions are serialized in this package. |
| Educational metric ranges | PASS | Percentage values are 0-100 and staffing ratios are positive. |

Tableau engine validation remains unavailable because Tableau Desktop/Public is not installed.
