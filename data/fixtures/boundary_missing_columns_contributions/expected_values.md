# Fixture Expected Values: Boundary Missing Columns Contributions

- Scenario: `missing_columns_contributions`
- Fixture data: `data/fixtures/boundary_missing_columns_contributions`
- Machine-readable source: `data/fixtures/boundary_missing_columns_contributions/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario missing_columns_contributions --data-dir data/fixtures/boundary_missing_columns_contributions
python -m reserve fixture-check --scenario missing_columns_contributions --data-dir data/fixtures/boundary_missing_columns_contributions
```

## Validation Expectations

Expected errors:
- `missing_columns_contributions.csv missing columns: contribution`

Expected warnings:
- None

Because validation is expected to fail, fixture-check stops after comparing validation output and does not generate workbook or model checks for this fixture.

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
