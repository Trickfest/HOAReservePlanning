# Boundary Fixture: Missing Columns (Components)

Validate (expected to fail):

```
python -m reserve validate --scenario missing_columns_components --data-dir data/fixtures/boundary_missing_columns_components
```

Expected validation error:
- `components.csv missing columns: include`

Funding metrics:
- Not applicable because validation fails and no workbook is generated.
