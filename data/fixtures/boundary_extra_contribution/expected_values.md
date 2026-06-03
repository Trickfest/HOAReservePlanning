# Fixture Expected Values: Boundary Extra Contribution

- Scenario: `extra_contribution`
- Fixture data: `data/fixtures/boundary_extra_contribution`
- Machine-readable source: `data/fixtures/boundary_extra_contribution/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario extra_contribution --data-dir data/fixtures/boundary_extra_contribution
python -m reserve build --scenario extra_contribution --data-dir data/fixtures/boundary_extra_contribution
python -m reserve fixture-check --scenario extra_contribution --data-dir data/fixtures/boundary_extra_contribution
```

## Validation Expectations

Expected errors:
- None

Expected warnings:
- `Contribution years outside forecast window: 2027`

## Workbook Value Checks

- `Forecast!C2` expected `100`

## Workbook Formula Checks

- `Forecast!B2` expected `=Inputs!$B$3`
- `Dashboard!B4` expected `=Forecast!$A$3`
- `Forecast!G2` expected `=SUMIFS(Schedule!$D$2:$D$51,Schedule!$A$2:$A$51,A2)`
- `Forecast!D2` expected `=C2`
- `Forecast!F2` expected `=E2`
- `Forecast!I2` expected `=IF(SUM(Funding!$C$2:$C$11)=0,"",B2/(SUM(Funding!$C$2:$C$11)))`
- `Forecast!J2` expected `=IF(SUM(G2:INDEX($G$2:$G$3,MIN(2+4,3)-1))=0,"",B2/SUM(G2:INDEX($G$2:$G$3,MIN(2+4,3)-1)))`
- `Forecast!D3` expected `=D2+C3`
- `Forecast!F3` expected `=F2+E3`

## Model Forecast Checks

- year `2025`, end balance `100`
- year `2026`, end balance `200`

## Model Count Checks

- forecast years: `2`
- negative balance years: `0`
- schedule items: `0`
- zero expense years: `2`

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
