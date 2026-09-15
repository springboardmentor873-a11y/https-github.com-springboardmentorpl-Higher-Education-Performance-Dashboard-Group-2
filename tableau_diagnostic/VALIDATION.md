# Static Validation

## Preserved Package

| Check | Result | Evidence |
|---|---|---|
| ZIP package readable | PASS | Preserved package opened with the standard ZIP reader |
| TWB exists | PASS | `eduvision_prototype.twb` |
| Excel datasource exists | PASS | `university_final_dataset_all_kpis.xlsx` |
| XML well formed | PASS | Python `xml.etree.ElementTree` parsed the TWB |
| Worksheets preserved | PASS | 36 |
| Dashboards preserved | PASS | 4 |
| KPI calculated fields present | PASS | 4 calculated datasource fields |
| Worksheet references valid | PASS | 36 worksheet names parsed |
| Dashboard zone references valid | PASS | All zones resolve to worksheet names |
| Raw field references valid | PASS | 0 missing datasource fields after qualified-name normalization |
| Dataset modified | PASS | Dataset was only read from the package |

## Structural Failures Preventing Repair Claim

| Check | Result | Evidence |
|---|---|---|
| 2026.2 worksheet wrapper model | FAIL | Direct legacy table bodies; no required `simple-id` elements |
| 2026.2 dashboard model | FAIL | Legacy dashboard child structure; no required dashboard identifiers |
| Worksheet aggregation coverage | FAIL | 15 aggregation nodes for 36 worksheets |
| 2026.2 pane encoding model | FAIL | Generic `encoding attr/field` nodes rather than named encoding elements |
| Window model | FAIL | One window containing `cards`, not the dashboard window sequence |
| Live Tableau open | NOT TESTED | Tableau Desktop/Public is unavailable |

## Conclusion

The package is statically inventoried and validated for preservation and reference integrity, but it is not repaired. Live Tableau opening cannot be claimed.