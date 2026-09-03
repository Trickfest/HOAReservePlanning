# Fixture Expected Values: Realistic Start Of Year

- Scenario: `realistic_start_of_year`
- Fixture data: `data/fixtures/realistic_start_of_year`
- Machine-readable source: `data/fixtures/realistic_start_of_year/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario realistic_start_of_year --data-dir data/fixtures/realistic_start_of_year
python -m reserve build --scenario realistic_start_of_year --data-dir data/fixtures/realistic_start_of_year
python -m reserve fixture-check --scenario realistic_start_of_year --data-dir data/fixtures/realistic_start_of_year
```

## Validation Expectations

Expected errors:
- None

Expected warnings:
- None

## Workbook Value Checks

- `Forecast!C2` expected `110000`

## Workbook Formula Checks

- `Forecast!B2` expected `=Inputs!$B$3`
- `Schedule!D2` expected `=Components!$D$7*(1+Inputs!$B$4)^(A2-Inputs!$B$2)`
- `Dashboard!B4` expected `=Forecast!$A$11`
- `Forecast!G2` expected `=SUMIFS(Schedule!$D$2:$D$501,Schedule!$A$2:$A$501,A2)`
- `Forecast!D2` expected `=C2`
- `Forecast!F2` expected `=E2`
- `Forecast!I2` expected `=IF(SUM(Funding!$C$2:$C$101)=0,"",B2/(SUM(Funding!$C$2:$C$101)))`
- `Forecast!J2` expected `=IF(SUM(G2:INDEX($G$2:$G$11,MIN(2+4,11)-1))=0,"",B2/SUM(G2:INDEX($G$2:$G$11,MIN(2+4,11)-1)))`
- `Forecast!D3` expected `=D2+C3`
- `Forecast!F3` expected `=F2+E3`

## Model Schedule Checks

- year `2025`, component `tree_pruning`, nominal expense `12000.0`
- year `2032`, component `roof_replace`, nominal expense `295169.72770196886`, tolerance `0.01`
- year `2034`, component `tree_pruning`, nominal expense `15657.278205950939`, tolerance `0.01`

## Model Forecast Checks

- year `2025`, end balance `282580.0`
- year `2032`, end balance `521963.2584538943`, tolerance `0.01`
- year `2034`, end balance `670932.935330551`, tolerance `0.01`

## Model Count Checks

- forecast years: `10`
- negative balance years: `0`
- schedule items: `12`
- zero expense years: `0`

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
