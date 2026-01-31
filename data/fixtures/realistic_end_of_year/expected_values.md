# Realistic Fixture Expected Values (End of Year)

Build:

```
python -m reserve build --scenario realistic_end_of_year --data-dir data/fixtures/realistic_end_of_year
```

Schedule checks (Sheet: Schedule):
- `A2` = 2025, `B2` = tree_pruning, `D2` = 12360 (displayed as 12,360)
- `A3` = 2026, `B3` = asphalt_resurface, `D3` = 116699 (displayed as 116,699)
- `A9` = 2032, `B9` = asphalt_resurface, `D9` = 139344.71 (displayed as 139,345)
- `A10` = 2032, `B10` = roof_replace, `D10` = 304024.82 (displayed as 304,025)
- `A12` = 2034, `B12` = exterior_paint, `D12` = 51068.82 (displayed as 51,069)
- `A13` = 2034, `B13` = tree_pruning, `D13` = 16127.00 (displayed as 16,127)

Forecast checks (Sheet: Forecast):
- `H2` (2025 end balance) = 281240 (displayed as 281,240)
- `H3` (2026 end balance) = 282365.80 (displayed as 282,366)
- `H5` (2028 end balance) = 471379.05 (displayed as 471,379)
- `H9` (2032 end balance) = 497797.64 (displayed as 497,798)
- `H11` (2034 end balance) = 640435.73 (displayed as 640,436)

Funding metrics (Sheet: Forecast):
- `I` (percent_funded) = beginning balance / fully funded balance (formula-driven).
- `J` (coverage_5yr) = beginning balance / sum of expenses for the next 5 years (formula-driven).

Checks (Sheet: Checks):
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 0

Dashboard:
- `B2` (lowest reserve balance) = 281240 (displayed as 281,240)
- `B3` (ending balance final year) = 640435.73 (displayed as 640,436)
- `B4` (final forecast year) = 2034
