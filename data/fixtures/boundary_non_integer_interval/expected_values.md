# Boundary Fixture: Non-Integer Interval

Validate (expected to fail):

```
python -m reserve validate --scenario non_integer_interval --data-dir data/fixtures/boundary_non_integer_interval
```

Expected validation error:
- `components.csv row 2: interval_years must be an integer`
