# Fixture Expected Values: Boundary Invalid Flags

- Scenario: `invalid_flags`
- Fixture data: `data/fixtures/boundary_invalid_flags`
- Machine-readable source: `data/fixtures/boundary_invalid_flags/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario invalid_flags --data-dir data/fixtures/boundary_invalid_flags
python -m reserve fixture-check --scenario invalid_flags --data-dir data/fixtures/boundary_invalid_flags
```

## Validation Expectations

Expected errors:
- `components.csv row 2: recurring must be Y or N`
- `components.csv row 2: include must be Y or N`

Expected warnings:
- None

Because validation is expected to fail, fixture-check stops after comparing validation output and does not generate workbook or model checks for this fixture.

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
