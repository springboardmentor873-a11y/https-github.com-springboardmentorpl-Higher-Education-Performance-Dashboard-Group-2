# Root Cause

## Root Cause

The package is a hand-authored legacy TWB whose worksheet and dashboard document structures do not conform to the official 2026.2 workbook schema. The rejection is structural and cascades from malformed parent content models; changing isolated attributes such as simple-id, pane class, mark class, or aggregation cannot repair it.

## Evidence

- Workbook reports version='18.1', original-version='2024.2', source-build='2024.2.0'; these values are not, by themselves, evidence that version 18.1 must be changed.
- All 36 worksheets contain a direct table body with child order `view, style, panes, rows, cols`, but the official 2026.2 schema requires each workbook worksheet wrapper to contain a repository location, a visual specification, and a required `simple-id`.
- The worksheet visual specification requires `view` to contain an `aggregation` element after its view specification. This package has 15 worksheet-level aggregation elements for 36 worksheets.
- Every pane uses `<mark class=...>` and `<encoding attr=... field=...>`, while the official 2026.2 pane model requires the mark and uses named mark-encoding elements such as `<color column=...>`.
- Each dashboard uses child order `repository-location, style, size, zones`, while the official dashboard model requires a size/options element, optional datasource/dependencies, zones, and a required dashboard `simple-id`.
- The package contains 1 window and its child is `cards`; the official dashboard window model requires `viewpoints`, `active`, optional preview settings, grid options, and optional simple-id.
- The document-format-change-manifest is empty. The official guidance recommends `<ManifestByVersion />` for direct authoring, but an empty manifest is secondary to the malformed worksheet/dashboard content models.

## Official Schema Reference

- Tableau official schemas: https://github.com/tableau/tableau-document-schemas
- Target schema: `schemas/2026_2/twb_2026.2.0.xsd`
- The repository documents TWB version compatibility and distinguishes syntactic XSD validation from semantic Tableau loadability.

## Secondary Problems

- 0 referenced field names are not declared as datasource columns: none.
- The package has 0 root-level action nodes, but the 2026.2 action content model expects an `actions` wrapper and nested legacy action structure.
- The generated datasource omits the metadata records and other structures normally emitted by Tableau, so XSD compliance alone would not establish semantic loadability.

## Cascading Errors

Errors such as `no declaration found for element rows`, `cols`, and `mark`, plus missing `class`, `revision`, or `aggregation`, are expected consequences when Tableau enters the wrong content model after the malformed worksheet parent. Treating them as independent repairs explains why earlier attribute-level changes did not converge.

## Previous Repair Mistakes

- The visible workspace contains only `dashboard/eduvision_prototype.twbx`; the requested fixed_final and other repair variants are absent, so their exact edits cannot be audited.
- Existing project documentation says invalid action XML, bins, layout, and storyboard structures were removed without a Tableau engine check. Those removals may reduce individual errors but cannot turn a hand-authored legacy worksheet body into a valid 2026.2 document model.

## Recommended Repair

Do not patch the current TWB element-by-element. Recreate a minimal workbook in Tableau 2026.2.2 (or obtain a genuine 2026.2 TWB), then transplant datasource fields and worksheet/dashboard definitions using that workbook's exact wrapper, child order, identifiers, and action syntax. Until such a reference workbook is available, a full repair preserving all 36 worksheets and 4 dashboards would be speculative.

## Validation Boundary

Tableau Desktop/Public is not installed in this environment, and no fixed_final package was supplied. This report is static diagnosis only; it does not claim that the current or any repaired package opens in Tableau.
