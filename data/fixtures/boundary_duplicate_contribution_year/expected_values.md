# Boundary Fixture: Duplicate Contribution Year

Validate (expect a warning, build should succeed):

```
python -m reserve validate --scenario duplicate_contribution_year --data-dir data/fixtures/boundary_duplicate_contribution_year
```

Expected validation warning:
- `Duplicate contribution years: 2025`

Build:

```
python -m reserve build --scenario duplicate_contribution_year --data-dir data/fixtures/boundary_duplicate_contribution_year
```

Forecast checks:
- `F2` (2025 end balance) = 150
- `F3` (2026 end balance) = 350

Funding metrics (Sheet: Forecast):
- `G` (percent_funded) = beginning balance / fully funded balance (formula-driven).
- `H` (coverage_5yr) = beginning balance / sum of expenses for the next 5 years (formula-driven).

Checks:
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 2

Dashboard:
- `B2` (lowest reserve balance) = 150
- `B3` (ending balance final year) = 350
- `B4` (final forecast year) = 2026
