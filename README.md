# HOA Reserve Planning Model

This project generates a .xlsx reserve planning workbook from simple text files.  The .xlsx is also works with Apple Numbers.

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

## Funding metrics in the Forecast sheet

The Forecast tab now includes two funding metrics, calculated with Excel formulas:

Fully funded balance definition:
- The sum of each component’s funded portion, where funded portion is the inflated current cost multiplied by the fraction of useful life that has elapsed (linear funding).

Examples (starting year 2026):
- Recurring example: Roof replacement costs $100,000 today, inflation 3%, interval 10 years. In year 2030 (4 years after 2026), inflated cost is $100,000 × 1.03^4 ≈ $112,551. If 4 of 10 years have elapsed, funded portion is 4/10 × $112,551 ≈ $45,020.
- Non-recurring example: Paint project costs $20,000 today, inflation 3%, spend year 2031 (5 years from 2026). In year 2029 (3 years after 2026), inflated cost is $20,000 × 1.03^3 ≈ $21,855. Funded fraction is 3/5, so funded portion ≈ $13,113.
- Generic formula: `inflated_cost = base_cost * (1 + inflation_rate)^(year - starting_year)`.

- `percent_funded`: beginning-of-year balance divided by the fully funded balance.
- `coverage_5yr`: beginning-of-year balance divided by the sum of expenses for the next 5 years.
  - Near the end of the forecast, the window shrinks to the remaining years.

Interpretation (rule of thumb):
- `coverage_5yr` > 1.0 means the beginning-of-year balance can cover more than the next 5 years of expenses; < 1.0 means it cannot.
- `percent_funded` at 100% means the reserve is fully funded; below 100% indicates underfunded, above 100% indicates a surplus relative to the target.

Fully funded balance assumptions:
- Recurring components fund linearly across their interval (`interval_years`).
- Non-recurring components fund linearly from the starting year to their `spend_year`.
- Costs are inflated to the forecast year using the inflation rate.

The Forecast tab also includes:
- `cumulative_contributions`: running total of contributions.
- `cumulative_interest`: running total of interest.

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
- Funding metric formulas return blank when the denominator is zero (no fully funded target or no expenses in the 5-year window).

## Tests

```bash
python -m unittest discover -s tests
```
