# Module 7 Dashboard Testing Report

## Engine Availability

Tableau Desktop/Public was not available. The workbook has now been rewritten to the expected Tableau XML hierarchy, but it still requires a real Tableau engine check for repair prompts and rendering.

## Top-N Validation

- **Top 10 universities**: `Global_Ranking_Score` raw field maps to expected sort `[none:Global_Ranking_Score:qk]`; actual sort `[none:Global_Ranking_Score:qk]`; identity/order result: FAIL.
  Direct sort: massachusetts institute of technology, university of oxford, university of cambridge, harvard university, stanford university, imperial college london, eth zurich - swiss federal institute of technology, eth zurich, university of california berkeley, tsinghua university
  Categorical filter members: massachusetts institute of technology, university of oxford, university of cambridge, harvard university, stanford university, imperial college london, eth zurich - swiss federal institute of technology, eth zurich, university of california berkeley, tsinghua university
- **Top research institutions**: `Research_Impact_Score` raw field maps to expected sort `[none:Research_Impact_Score:qk]`; actual sort `[none:Research_Impact_Score:qk]`; identity/order result: FAIL.
  Direct sort: harvard university, stanford university, vita-salute san raffaele university, humanitas university, massachusetts institute of technology, université psl, charité - universitätsmedizin berlin, king’s college london, chinese university of hong kong, the university of chicago
  Categorical filter members: harvard university, stanford university, vita-salute san raffaele university, humanitas university, massachusetts institute of technology, université psl, charité - universitätsmedizin berlin, king’s college london, chinese university of hong kong, the university of chicago
- **Citations by institution**: `scores_citations` raw field maps to expected sort `[none:scores_citations:qk]`; actual sort `[none:scores_citations:qk]`; identity/order result: FAIL.
  Direct sort: massachusetts institute of technology, stanford university, harvard university, university of california berkeley, university of oxford, carnegie mellon university, princeton university, imperial college london, ucl, vita-salute san raffaele university, university of washington, humanitas university, university of cambridge, queen mary university of london, northwestern university
  Categorical filter members: massachusetts institute of technology, stanford university, harvard university, university of california berkeley, university of oxford, carnegie mellon university, princeton university, imperial college london, ucl, vita-salute san raffaele university, university of washington, humanitas university, university of cambridge, queen mary university of london, northwestern university

## Structural Result

- Worksheets: 36; dashboards: 4; KPI zones: 16; serialized actions: 0.
- The generator retains the verified 50-action source/target matrix, but invalid hand-authored action XML was removed from the package because it caused Tableau schema errors.
- Unsupported custom `<bin>`, `class='top'`, dashboard `<layout>`, storyboard, and invalid action structures were removed.
- Residual limitation: no real Tableau engine/rendering check was possible; dashboard action wiring must be recreated or validated in Tableau.
