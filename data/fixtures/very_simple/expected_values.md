# Fixture Expected Values: Very Simple

- Scenario: `very_simple`
- Fixture data: `data/fixtures/very_simple`
- Machine-readable source: `data/fixtures/very_simple/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario very_simple --data-dir data/fixtures/very_simple
python -m reserve build --scenario very_simple --data-dir data/fixtures/very_simple
python -m reserve fixture-check --scenario very_simple --data-dir data/fixtures/very_simple
```

## Validation Expectations

Expected errors:
- None

Expected warnings:
- None

## Workbook Value Checks

- `Forecast!C2` expected `100000`

## Workbook Formula Checks

- `Forecast!B2` expected `=Inputs!$B$3`
- `Forecast!D2` expected `=C2`
- `Forecast!D3` expected `=D2+C3`
- `Forecast!F2` expected `=E2`
- `Forecast!F3` expected `=F2+E3`
- `Forecast!G2` expected `=SUMIFS(Schedule!$D$2:$D$21,Schedule!$A$2:$A$21,A2)`
- `Forecast!I2` expected `=IF(SUM(Funding!$C$2:$C$11)=0,"",B2/(SUM(Funding!$C$2:$C$11)))`
- `Forecast!J2` expected `=IF(SUM(G2:INDEX($G$2:$G$12,MIN(2+4,12)-1))=0,"",B2/SUM(G2:INDEX($G$2:$G$12,MIN(2+4,12)-1)))`
- `Schedule!D2` expected `=Components!$D$2*(1+Inputs!$B$4)^(A2-Inputs!$B$2+1)`
- `Dashboard!B4` expected `=Forecast!$A$12`

## Model Schedule Checks

- year `2036`, component `roof`, nominal expense `1000000`

## Model Forecast Checks

- year `2026`, end balance `100000`
- year `2036`, end balance `100000`

## Model Count Checks

- forecast years: `11`
- negative balance years: `0`
- schedule items: `1`
- zero expense years: `10`

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
