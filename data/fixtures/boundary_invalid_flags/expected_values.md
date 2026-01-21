# Boundary Fixture: Invalid Flags

Validate (expected to fail):

```
python -m reserve validate --scenario invalid_flags --data-dir data/fixtures/boundary_invalid_flags
```

Expected validation errors:
- `components.csv row 2: recurring must be Y or N`
- `components.csv row 2: include must be Y or N`
