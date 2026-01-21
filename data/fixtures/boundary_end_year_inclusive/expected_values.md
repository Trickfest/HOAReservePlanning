# Boundary Fixture: End Year Inclusive

Build:

```
python -m reserve build --scenario end_year_inclusive --data-dir data/fixtures/boundary_end_year_inclusive
```

Schedule checks:
- Includes expenses in both 2025 and 2027 (start and end years).

Forecast checks:
- `F2` (2025 end balance) = 850
- `F3` (2026 end balance) = 850
- `F4` (2027 end balance) = 600

Checks:
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 1

Dashboard:
- `B2` (lowest reserve balance) = 600
- `B3` (ending balance final year) = 600
- `B4` (final forecast year) = 2027
