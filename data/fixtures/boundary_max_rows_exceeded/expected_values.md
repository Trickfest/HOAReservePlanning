# Fixture Expected Values: Boundary Max Rows Exceeded

- Scenario: `max_rows_exceeded`
- Fixture data: `data/fixtures/boundary_max_rows_exceeded`
- Machine-readable source: `data/fixtures/boundary_max_rows_exceeded/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario max_rows_exceeded --data-dir data/fixtures/boundary_max_rows_exceeded
python -m reserve fixture-check --scenario max_rows_exceeded --data-dir data/fixtures/boundary_max_rows_exceeded
```

## Validation Expectations

Expected errors:
- `Schedule rows 3 exceed max_schedule_rows 2`

Expected warnings:
- None

Because validation is expected to fail, fixture-check stops after comparing validation output and does not generate workbook or model checks for this fixture.

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
