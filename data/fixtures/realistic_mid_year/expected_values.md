# Realistic Fixture Expected Values (Mid Year)

Build:

```
python -m reserve build --scenario realistic_mid_year --data-dir data/fixtures/realistic_mid_year
```

Schedule checks (Sheet: Schedule):
- `A2` = 2025, `B2` = tree_pruning, `D2` = 12178.67 (displayed as 12,179)
- `A3` = 2026, `B3` = asphalt_resurface, `D3` = 114986.94 (displayed as 114,987)
- `A9` = 2032, `B9` = asphalt_resurface, `D9` = 137300.42 (displayed as 137,300)
- `A10` = 2032, `B10` = roof_replace, `D10` = 299564.56 (displayed as 299,565)
- `A12` = 2034, `B12` = exterior_paint, `D12` = 50319.61 (displayed as 50,320)
- `A13` = 2034, `B13` = tree_pruning, `D13` = 15890.40 (displayed as 15,890)

Forecast checks (Sheet: Forecast):
- `H2` (2025 end balance) = 281421.33 (displayed as 281,421)
- `H3` (2026 end balance) = 284262.82 (displayed as 284,263)
- `H5` (2028 end balance) = 474172.22 (displayed as 474,172)
- `H9` (2032 end balance) = 508418.43 (displayed as 508,418)
- `H11` (2034 end balance) = 653545.28 (displayed as 653,545)

Funding metrics (Sheet: Forecast):
- `I` (percent_funded) = beginning balance / fully funded balance (formula-driven).
- `J` (coverage_5yr) = beginning balance / sum of expenses for the next 5 years (formula-driven).

Checks (Sheet: Checks):
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 0

Dashboard:
- `B2` (lowest reserve balance) = 281421.33 (displayed as 281,421)
- `B3` (ending balance final year) = 653545.28 (displayed as 653,545)
- `B4` (final forecast year) = 2034
