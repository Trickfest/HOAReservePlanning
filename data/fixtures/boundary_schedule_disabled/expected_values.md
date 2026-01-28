# Boundary Fixture: Schedule Expansion Disabled

Build:

```
python -m reserve build --scenario schedule_disabled --data-dir data/fixtures/boundary_schedule_disabled
```

Schedule checks:
- Only the header row should appear (no schedule items).

Forecast checks:
- `H2` (2025 end balance) = 600
- `H3` (2026 end balance) = 700
- `H4` (2027 end balance) = 800

Funding metrics (Sheet: Forecast):
- `I` (percent_funded) = beginning balance / fully funded balance (formula-driven).
- `J` (coverage_5yr) = beginning balance / sum of expenses for the next 5 years (formula-driven).

Checks:
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 3

Dashboard:
- `B2` (lowest reserve balance) = 600
- `B3` (ending balance final year) = 800
- `B4` (final forecast year) = 2027
