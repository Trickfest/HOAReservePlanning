# Boundary Fixture: Non-Integer Spend Year

Validate (expected to fail):

```
python -m reserve validate --scenario non_integer_spend_year --data-dir data/fixtures/boundary_non_integer_spend_year
```

Expected validation error:
- `components.csv row 2: spend_year must be an integer`
