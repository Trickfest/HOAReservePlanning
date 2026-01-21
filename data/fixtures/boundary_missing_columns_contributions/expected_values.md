# Boundary Fixture: Missing Columns (Contributions)

Validate (expected to fail):

```
python -m reserve validate --scenario missing_columns_contributions --data-dir data/fixtures/boundary_missing_columns_contributions
```

Expected validation error:
- `missing_columns_contributions.csv missing columns: contribution`
