# Fixture Expected Values: Boundary Non Integer Spend Year

- Scenario: `non_integer_spend_year`
- Fixture data: `data/fixtures/boundary_non_integer_spend_year`
- Machine-readable source: `data/fixtures/boundary_non_integer_spend_year/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario non_integer_spend_year --data-dir data/fixtures/boundary_non_integer_spend_year
python -m reserve fixture-check --scenario non_integer_spend_year --data-dir data/fixtures/boundary_non_integer_spend_year
```

## Validation Expectations

Expected errors:
- `components.csv row 2: spend_year must be an integer`

Expected warnings:
- None

Because validation is expected to fail, fixture-check stops after comparing validation output and does not generate workbook or model checks for this fixture.

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
