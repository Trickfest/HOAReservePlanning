# Realistic Fixture Expected Values

Build:

```
python -m reserve build --scenario realistic --data-dir data/fixtures/realistic
```

Schedule checks (Sheet: Schedule):
- `A2` = 2025, `B2` = tree_pruning, `D2` = 12000
- `A3` = 2026, `B3` = asphalt_resurface, `D3` = 113300
- `A9` = 2032, `B9` = asphalt_resurface, `D9` = 135286.13 (displayed as 135,286)
- `A10` = 2032, `B10` = roof_replace, `D10` = 295169.73 (displayed as 295,170)
- `A12` = 2034, `B12` = exterior_paint, `D12` = 49581.38 (displayed as 49,581)
- `A13` = 2034, `B13` = tree_pruning, `D13` = 15657.28 (displayed as 15,657)

Forecast checks (Sheet: Forecast):
- `F2` (2025 end balance) = 281600
- `F3` (2026 end balance) = 286132
- `F5` (2028 end balance) = 476924.40 (displayed as 476,924)
- `F9` (2032 end balance) = 518883.41 (displayed as 518,883)
- `F11` (2034 end balance) = 666462.50 (displayed as 666,463)

Checks (Sheet: Checks):
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 0

Dashboard:
- `B2` (lowest reserve balance) = 281600
- `B3` (ending balance final year) = 666462.50 (displayed as 666,463)
- `B4` (final forecast year) = 2034
