# Simple Fixture Expected Values

Build:

```
python -m reserve build --scenario simple --data-dir data/fixtures/simple
```

Schedule checks (Sheet: Schedule):
- `A2` = 2026, `B2` = paving_seal, `D2` = 200
- `A3` = 2027, `B3` = entry_gate, `D3` = 500
- `A4` = 2028, `B4` = paving_seal, `D4` = 200

Forecast checks (Sheet: Forecast):
- `F2` (2025 end balance) = 1400
- `F3` (2026 end balance) = 1640
- `F4` (2027 end balance) = 1604
- `F5` (2028 end balance) = 1864.4 (displayed as 1,864)
- `F6` (2029 end balance) = 2350.84 (displayed as 2,351)

Checks (Sheet: Checks):
- `B2` (negative balance years) = 0
- `B3` (zero expense years) = 2

Dashboard:
- `B2` (lowest reserve balance) = 1400
- `B3` (ending balance final year) = 2350.84 (displayed as 2,351)
