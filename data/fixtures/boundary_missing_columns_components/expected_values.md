# Fixture Expected Values: Boundary Missing Columns Components

- Scenario: `missing_columns_components`
- Fixture data: `data/fixtures/boundary_missing_columns_components`
- Machine-readable source: `data/fixtures/boundary_missing_columns_components/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario missing_columns_components --data-dir data/fixtures/boundary_missing_columns_components
python -m reserve fixture-check --scenario missing_columns_components --data-dir data/fixtures/boundary_missing_columns_components
```

## Validation Expectations

Expected errors:
- `components.csv missing columns: include`

Expected warnings:
- None

Because validation is expected to fail, fixture-check stops after comparing validation output and does not generate workbook or model checks for this fixture.

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
