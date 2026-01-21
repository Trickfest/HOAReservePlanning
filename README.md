# HOA Reserve Planning Model

This project generates a .xlsx reserve planning workbook from simple text files.  The .xlsx is Apple Numbers-friendly.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m reserve validate --scenario recommended
python -m reserve build --scenario recommended
```

Workbook output:

```
dist/HOA_Reserve_Planning_<scenario>.xlsx
```

## Run a build for a specific scenario

```bash
python -m reserve build --scenario recommended
```

Optional macOS open:

```bash
python -m reserve build --scenario recommended --open
```

## Where to edit inputs, components, and contributions

- Global assumptions and feature flags: `data/inputs.yaml`
- Reserve components: `data/components.csv`
- Contributions (one file per scenario): `data/contributions/<scenario>.csv`

## How to add a new component

1. Open `data/components.csv`.
2. Add a new row with a unique `id` and set `include` to `Y`.
3. For recurring items, set `recurring` to `Y` and provide `interval_years`.
4. Rebuild the workbook.

## How to add a new contribution scenario

1. Create `data/contributions/<scenario>.csv` with columns `year,contribution`.
2. Provide a contribution value for every forecast year.
3. Run `python -m reserve validate --scenario <scenario>`.
4. Build with `python -m reserve build --scenario <scenario>`.

## Fixtures for verification

Use the fixture datasets to verify spreadsheet outputs without touching the main data files.

```bash
python -m reserve build --scenario simple --data-dir data/fixtures/simple
python -m reserve build --scenario realistic --data-dir data/fixtures/realistic
```

Automated fixture checks:

```bash
python -m reserve fixture-check --scenario simple --data-dir data/fixtures/simple
python -m reserve fixture-check --scenario realistic --data-dir data/fixtures/realistic
python -m reserve fixture-check --all
python -m reserve fixture-check --all --clean
```

Expected checks are documented in:
- `data/fixtures/simple/expected_values.md`
- `data/fixtures/realistic/expected_values.md`

Machine-readable expectations live in:
- `data/fixtures/**/expected_values.yaml`

`fixture-check` builds workbooks, verifies formula text and model values, prints a summary, and can remove generated workbooks with `--clean`.

Additional boundary fixtures live under `data/fixtures/boundary_*`.

## Validation notes

- Duplicate contribution years are reported as warnings; the last value wins.
- If expanded schedule rows exceed `FEATURES.max_schedule_rows`, validation fails so formulas stay in-bounds.

## Tests

```bash
python -m unittest discover -s tests
```
