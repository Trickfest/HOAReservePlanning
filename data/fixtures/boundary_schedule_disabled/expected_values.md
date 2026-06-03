# Fixture Expected Values: Boundary Schedule Disabled

- Scenario: `schedule_disabled`
- Fixture data: `data/fixtures/boundary_schedule_disabled`
- Machine-readable source: `data/fixtures/boundary_schedule_disabled/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario schedule_disabled --data-dir data/fixtures/boundary_schedule_disabled
python -m reserve build --scenario schedule_disabled --data-dir data/fixtures/boundary_schedule_disabled
python -m reserve fixture-check --scenario schedule_disabled --data-dir data/fixtures/boundary_schedule_disabled
```

## Validation Expectations

Expected errors:
- None

Expected warnings:
- None

## Workbook Value Checks

- `Forecast!C2` expected `100`

## Workbook Formula Checks

- `Forecast!B2` expected `=Inputs!$B$3`
- `Dashboard!B4` expected `=Forecast!$A$4`
- `Forecast!G2` expected `=SUMIFS(Schedule!$D$2:$D$51,Schedule!$A$2:$A$51,A2)`
- `Forecast!D2` expected `=C2`
- `Forecast!F2` expected `=E2`
- `Forecast!I2` expected `=IF(SUM(Funding!$C$2:$C$21)=0,"",B2/(SUM(Funding!$C$2:$C$21)))`
- `Forecast!J2` expected `=IF(SUM(G2:INDEX($G$2:$G$4,MIN(2+4,4)-1))=0,"",B2/SUM(G2:INDEX($G$2:$G$4,MIN(2+4,4)-1)))`
- `Forecast!D3` expected `=D2+C3`
- `Forecast!F3` expected `=F2+E3`

## Model Forecast Checks

- year `2025`, end balance `600`
- year `2027`, end balance `800`

## Model Count Checks

- forecast years: `3`
- negative balance years: `0`
- schedule items: `0`
- zero expense years: `3`

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
