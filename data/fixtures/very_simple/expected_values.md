# Very Simple Fixture Expected Values

Build:

```
python -m reserve build --scenario very_simple --data-dir data/fixtures/very_simple
```

Schedule checks (Sheet: Schedule):
- `A2` = 2036, `B2` = roof, `D2` = 1000000

Forecast checks (Sheet: Forecast):
- `H2` (2026 end balance) = 100000
- `H12` (2036 end balance) = 100000

Funding metrics (Sheet: Forecast):
- `I` (percent_funded) = beginning balance / fully funded balance (formula-driven).
- `J` (coverage_5yr) = beginning balance / sum of expenses for the next 5 years (formula-driven).

Checks (Sheet: Checks):
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 10

Dashboard:
- `B2` (lowest reserve balance) = 100000
- `B3` (ending balance final year) = 100000
- `B4` (final forecast year) = 2036
