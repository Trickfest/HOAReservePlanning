# Boundary Fixture: Spend Year Outside Forecast Window

Validate (expect a warning, build should succeed):

```
python -m reserve validate --scenario spend_year_outside --data-dir data/fixtures/boundary_spend_year_outside
```

Expected validation warning:
- `components.csv row 2: spend_year 2024 outside forecast window`

Build:

```
python -m reserve build --scenario spend_year_outside --data-dir data/fixtures/boundary_spend_year_outside
```

Schedule checks:
- `A2` = 2026, `B2` = paint, `D2` = 50
- No row for `old_gate` (outside the window)

Forecast checks:
- `H2` (2025 end balance) = 100
- `H3` (2026 end balance) = 150
- `H4` (2027 end balance) = 250
- `H5` (2028 end balance) = 350

Funding metrics (Sheet: Forecast):
- `I` (percent_funded) = beginning balance / fully funded balance (formula-driven).
- `J` (coverage_5yr) = beginning balance / sum of expenses for the next 5 years (formula-driven).

Checks:
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 3

Dashboard:
- `B2` (lowest reserve balance) = 100
- `B3` (ending balance final year) = 350
