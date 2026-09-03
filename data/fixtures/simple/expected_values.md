# Fixture Expected Values: Simple

- Scenario: `simple`
- Fixture data: `data/fixtures/simple`
- Machine-readable source: `data/fixtures/simple/expected_values.yaml`

## Commands

```bash
python -m reserve validate --scenario simple --data-dir data/fixtures/simple
python -m reserve build --scenario simple --data-dir data/fixtures/simple
python -m reserve fixture-check --scenario simple --data-dir data/fixtures/simple
```

## Validation Expectations

Expected errors:
- None

Expected warnings:
- None

## Workbook Value Checks

- `Forecast!C2` expected `300`

## Workbook Formula Checks

- `Forecast!B2` expected `=Inputs!$B$3`
- `Schedule!D2` expected `=Components!$D$2*(1+Inputs!$B$4)^(A2-Inputs!$B$2+1)`
- `Dashboard!B4` expected `=Forecast!$A$6`
- `Forecast!G2` expected `=SUMIFS(Schedule!$D$2:$D$201,Schedule!$A$2:$A$201,A2)`
- `Forecast!D2` expected `=C2`
- `Forecast!F2` expected `=E2`
- `Forecast!I2` expected `=IF(SUM(Funding!$C$2:$C$51)=0,"",B2/(SUM(Funding!$C$2:$C$51)))`
- `Forecast!J2` expected `=IF(SUM(G2:INDEX($G$2:$G$6,MIN(2+4,6)-1))=0,"",B2/SUM(G2:INDEX($G$2:$G$6,MIN(2+4,6)-1)))`
- `Forecast!D3` expected `=D2+C3`
- `Forecast!F3` expected `=F2+E3`
- `Funding!C2` expected `=IF(Components!$A2="",0,IF(Components!$H2<>"Y",0,Components!$D2*(1+Inputs!$B$4)^(C$1-Inputs!$B$2+1)*IF(Components!$F2="Y",IF(Components!$G2<=0,0,IF(IF(Components!$G2<=0,0,IF((C$1-Components!$E2)>=0,IF(MOD((C$1-Components!$E2),Components!$G2)=0,Components!$G2,MOD((C$1-Components!$E2),Components!$G2)),Components!$G2+(C$1-Components!$E2)))<=0,0,(IF(Components!$G2<=0,0,IF((C$1-Components!$E2)>=0,IF(MOD((C$1-Components!$E2),Components!$G2)=0,Components!$G2,MOD((C$1-Components!$E2),Components!$G2)),Components!$G2+(C$1-Components!$E2))))/Components!$G2)),IF(C$1>Components!$E2,0,IF(Components!$E2-Inputs!$B$2<=0,1,(C$1-Inputs!$B$2)/(Components!$E2-Inputs!$B$2))))))`
- `Funding!C3` expected `=IF(Components!$A3="",0,IF(Components!$H3<>"Y",0,Components!$D3*(1+Inputs!$B$4)^(C$1-Inputs!$B$2+1)*IF(Components!$F3="Y",IF(Components!$G3<=0,0,IF(IF(Components!$G3<=0,0,IF((C$1-Components!$E3)>=0,IF(MOD((C$1-Components!$E3),Components!$G3)=0,Components!$G3,MOD((C$1-Components!$E3),Components!$G3)),Components!$G3+(C$1-Components!$E3)))<=0,0,(IF(Components!$G3<=0,0,IF((C$1-Components!$E3)>=0,IF(MOD((C$1-Components!$E3),Components!$G3)=0,Components!$G3,MOD((C$1-Components!$E3),Components!$G3)),Components!$G3+(C$1-Components!$E3))))/Components!$G3)),IF(C$1>Components!$E3,0,IF(Components!$E3-Inputs!$B$2<=0,1,(C$1-Inputs!$B$2)/(Components!$E3-Inputs!$B$2))))))`

## Model Schedule Checks

- year `2026`, component `paving_seal`, nominal expense `200`
- year `2027`, component `entry_gate`, nominal expense `500`
- year `2028`, component `paving_seal`, nominal expense `200`

## Model Forecast Checks

- year `2025`, end balance `1415.0`
- year `2029`, end balance `2387.8565`, tolerance `0.01`

## Model Count Checks

- forecast years: `5`
- negative balance years: `0`
- schedule items: `3`
- zero expense years: `2`

## Source Of Truth

These notes are generated from `expected_values.yaml`. The fixture runner uses the YAML file for assertions; this Markdown file is for human review.
