# Fixture Expected Values: Boundary Non Integer Interval

- Scenario: `non_integer_interval`
- Fixture data: `data/fixtures/boundary_non_integer_interval`
- Machine-readable source: `data/fixtures/boundary_non_integer_interval/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario non_integer_interval --data-dir data/fixtures/boundary_non_integer_interval
python -m reserve fixture-check --scenario non_integer_interval --data-dir data/fixtures/boundary_non_integer_interval
```

## Validation Expectations

Expected errors:
- `components.csv row 2: interval_years must be an integer`

Expected warnings:
- None

Because validation is expected to fail, fixture-check stops after comparing validation output and does not generate workbook or model checks for this fixture.

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
