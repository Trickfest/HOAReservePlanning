# Fixture Expected Values: Boundary Missing Contribution

- Scenario: `missing_contribution`
- Fixture data: `data/fixtures/boundary_missing_contribution`
- Machine-readable source: `data/fixtures/boundary_missing_contribution/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario missing_contribution --data-dir data/fixtures/boundary_missing_contribution
python -m reserve fixture-check --scenario missing_contribution --data-dir data/fixtures/boundary_missing_contribution
```

## Validation Expectations

Expected errors:
- `Missing contributions for years: 2026`

Expected warnings:
- None

Because validation is expected to fail, fixture-check stops after comparing validation output and does not generate workbook or model checks for this fixture.

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
