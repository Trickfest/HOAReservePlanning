# Boundary Fixture: Negative Balances

Build:

```
python -m reserve build --scenario negative_balance --data-dir data/fixtures/boundary_negative_balance
```

Schedule checks:
- `A2` = 2025, `B2` = major_repair, `D2` = 2000

Forecast checks:
- `H2` (2025 end balance) = -1000
- `H3` (2026 end balance) = -1000
- `H4` (2027 end balance) = -1000

Funding metrics (Sheet: Forecast):
- `I` (percent_funded) = beginning balance / fully funded balance (formula-driven).
- `J` (coverage_5yr) = beginning balance / sum of expenses for the next 5 years (formula-driven).

Checks:
- `B2` (negative balance years) = 3
- `B3` (zero expense years) = 2

Dashboard:
- `B2` (lowest reserve balance) = -1000
- `B3` (ending balance final year) = -1000
- `B4` (final forecast year) = 2027
