# Boundary Fixture: Recurring Missing Interval

Validate (expected to fail):

```
python -m reserve validate --scenario missing_interval --data-dir data/fixtures/boundary_missing_interval
```

Expected validation error:
- `components.csv row 2: interval_years required for recurring items`

Notes:
- Build should fail until interval_years is provided.

Funding metrics:
- Not applicable because validation fails and no workbook is generated.
