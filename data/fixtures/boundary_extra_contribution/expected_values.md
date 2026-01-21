# Boundary Fixture: Extra Contribution Year

Validate (expect a warning, build should succeed):

```
python -m reserve validate --scenario extra_contribution --data-dir data/fixtures/boundary_extra_contribution
```

Expected validation warning:
- `Contribution years outside forecast window: 2027`

Build:

```
python -m reserve build --scenario extra_contribution --data-dir data/fixtures/boundary_extra_contribution
```

Forecast checks:
- `F2` (2025 end balance) = 100
- `F3` (2026 end balance) = 200

Checks:
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 2

Dashboard:
- `B2` (lowest reserve balance) = 100
- `B3` (ending balance final year) = 200
- `B4` (final forecast year) = 2026
