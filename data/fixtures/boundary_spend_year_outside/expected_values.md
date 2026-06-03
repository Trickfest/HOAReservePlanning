# Fixture Expected Values: Boundary Spend Year Outside

- Scenario: `spend_year_outside`
- Fixture data: `data/fixtures/boundary_spend_year_outside`
- Machine-readable source: `data/fixtures/boundary_spend_year_outside/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario spend_year_outside --data-dir data/fixtures/boundary_spend_year_outside
python -m reserve build --scenario spend_year_outside --data-dir data/fixtures/boundary_spend_year_outside
python -m reserve fixture-check --scenario spend_year_outside --data-dir data/fixtures/boundary_spend_year_outside
```

## Validation Expectations

Expected errors:
- None

Expected warnings:
- `components.csv row 2: spend_year 2024 outside forecast window`

## Workbook Value Checks

- `Forecast!C2` expected `100`

## Workbook Formula Checks

- `Forecast!B2` expected `=Inputs!$B$3`
- `Schedule!D2` expected `=Components!$D$3*(1+Inputs!$B$4)^(A2-Inputs!$B$2+1)`
- `Dashboard!B4` expected `=Forecast!$A$5`
- `Forecast!G2` expected `=SUMIFS(Schedule!$D$2:$D$51,Schedule!$A$2:$A$51,A2)`
- `Forecast!D2` expected `=C2`
- `Forecast!F2` expected `=E2`
- `Forecast!I2` expected `=IF(SUM(Funding!$C$2:$C$21)=0,"",B2/(SUM(Funding!$C$2:$C$21)))`
- `Forecast!J2` expected `=IF(SUM(G2:INDEX($G$2:$G$5,MIN(2+4,5)-1))=0,"",B2/SUM(G2:INDEX($G$2:$G$5,MIN(2+4,5)-1)))`
- `Forecast!D3` expected `=D2+C3`
- `Forecast!F3` expected `=F2+E3`

## Model Schedule Checks

- year `2026`, component `paint`, nominal expense `50`

## Model Forecast Checks

- year `2025`, end balance `100`
- year `2026`, end balance `150`
- year `2028`, end balance `350`

## Model Count Checks

- forecast years: `4`
- negative balance years: `0`
- schedule items: `1`
- zero expense years: `3`

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
