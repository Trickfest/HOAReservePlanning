# Boundary Fixture: Missing Contribution Year

Validate (expected to fail):

```
python -m reserve validate --scenario missing_contribution --data-dir data/fixtures/boundary_missing_contribution
```

Expected validation error:
- `Missing contributions for years: 2026`

Notes:
- Build should fail until the missing year is added.

Funding metrics:
- Not applicable because validation fails and no workbook is generated.
