# Boundary Fixture: Max Schedule Rows Exceeded

Validate (expected to fail):

```
python -m reserve validate --scenario max_rows_exceeded --data-dir data/fixtures/boundary_max_rows_exceeded
```

Expected validation error:
- `Schedule rows 3 exceed max_schedule_rows 2`

Funding metrics:
- Not applicable because validation fails and no workbook is generated.
