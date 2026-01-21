# Boundary Fixture: Interval One

Build:

```
python -m reserve build --scenario interval_one --data-dir data/fixtures/boundary_interval_one
```

Schedule checks:
- Expenses occur every year (2025, 2026, 2027).

Forecast checks:
- `F2` (2025 end balance) = 0
- `F3` (2026 end balance) = 0
- `F4` (2027 end balance) = 0

Checks:
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 0

Dashboard:
- `B2` (lowest reserve balance) = 0
- `B3` (ending balance final year) = 0
- `B4` (final forecast year) = 2027
