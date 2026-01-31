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

Reserve planning balances near-term cash needs with long-term component funding. The Forecast tab reports both so you can see liquidity and funding adequacy year by year.

Glossary (Forecast tab terms):
- **Inflated cost**: `inflated_cost = base_cost * (1 + inflation_rate)^(year - starting_year)`; the exponent is the number of years after the starting year.
- **Fully funded balance (FFB)**: the sum of each component’s funded portion, where funded portion is the inflated current cost multiplied by the fraction of useful life elapsed (linear funding). Recurring items use `interval_years`; non-recurring items fund linearly from `starting_year` to `spend_year`.
- **Useful life**: the time (in years) over which a component is expected to be used before replacement. For recurring items this is `interval_years`; for non-recurring items it is `spend_year - starting_year`.
- **percent_funded**: beginning-of-year balance ÷ FFB. Around 100% means fully funded; below 100% indicates underfunded, above 100% indicates surplus relative to target.
- **coverage_5yr**: beginning-of-year balance ÷ sum of expenses for the next 5 years. > 1.0 means you can cover more than 5 years of expenses; < 1.0 means you cannot. Near the end of the forecast, the window shrinks to remaining years.
- **cumulative_contributions**: running total of contributions to date.
- **cumulative_interest**: running total of interest to date.

Examples (starting year 2026):
- Recurring example: Roof replacement costs $100,000 today, inflation 3%, interval 10 years. In year 2030 (4 years after 2026), inflated cost is $100,000 × 1.03^4 ≈ $112,551. If 4 of 10 years have elapsed, funded portion is 4/10 × $112,551 ≈ $45,020.
- Non-recurring example: Paint project costs $20,000 today, inflation 3%, spend year 2031 (5 years from 2026). In year 2029 (3 years after 2026), inflated cost is $20,000 × 1.03^3 ≈ $21,855. Funded fraction is 3/5, so funded portion ≈ $13,113.

## Calculation Details

### How Forecast expenses are calculated
The Forecast tab gets its yearly expenses from the Schedule tab. For each year, it sums all schedule rows whose year matches the Forecast year. In plain terms: **“total scheduled expenses for this year.”** This keeps the Forecast math simple and ensures the Schedule sheet is the single source of truth for timing.

### Percent funded: how it is computed
For each year, **percent_funded** is:
```
beginning of year balance ÷ fully funded balance
```
The fully funded balance is computed by:
1. Inflating component costs to the current forecast year.
2. For recurring items, funding linearly across the interval (age ÷ interval).
3. For non-recurring items, funding linearly from the starting year to the spend year.
If there is no fully funded target for a year, the cell is left blank.

### Recurring vs. non-recurring: why it matters
Recurring items “reset” after each replacement cycle. That means a roof that gets replaced every 20 years starts a new 20‑year funding cycle after each replacement. Modeling it as multiple non‑recurring rows would overlap those cycles and **overstate** the fully funded balance, which makes percent_funded look artificially low.

As a rule of thumb:
- Use **recurring** for the same component repeating on a regular interval.
- Use **multiple non‑recurring** rows only when timing or scope changes meaningfully.

## Run a build for a specific scenario

```bash
python -m reserve build --scenario recommended
```

Optional macOS open:

```bash
python -m reserve build --scenario recommended --open
```

Optional overrides for inputs/components (paths can be outside `data/`):

```bash
python -m reserve build --scenario recommended --inputs path/to/inputs.yaml --components path/to/components.csv
```

## Where to edit inputs, components, and contributions

- Global assumptions and feature flags: `data/inputs.yaml`
- Reserve components: `data/components.csv`
- Contributions (one file per scenario): `data/contributions/<scenario>.csv`

You can override `inputs.yaml` or `components.csv` at runtime with `--inputs` and `--components` on `build` or `validate`. Contributions still come from `--data-dir` (or `data/` by default).

## Input settings

- `starting_year`: first year of the forecast.
- `beginning_reserve_balance`: opening reserve balance (dollars).
- `inflation_rate`: annual inflation rate (decimal, e.g., `0.03`).
- `investment_return_rate`: annual investment return rate (decimal, e.g., `0.02`).
- `spend_inflation_timing`: how to time inflation on spend years. Allowed values are `start_of_year`, `mid_year`, and `end_of_year` (default `end_of_year`).
- `audit_tolerance_amount`: absolute tolerance for dollar columns (default `0.01`).
- `audit_tolerance_ratio`: tolerance for ratio columns like `percent_funded` and `coverage_5yr` (default `0.0001`, or 0.01%).
- `FEATURES.forecast_years`: forecast horizon in years.
- `FEATURES.enable_checks`: include the Checks sheet.
- `FEATURES.enable_dashboard`: include the Dashboard sheet.
- `FEATURES.enable_schedule_expansion`: expand recurring components into Schedule rows.
- `FEATURES.enable_audit`: include audit columns and summary checks (debug).
- `FEATURES.max_components_rows`: max rows reserved for Components.
- `FEATURES.max_schedule_rows`: max rows reserved for Schedule.

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
python -m reserve build --scenario realistic_end_of_year --data-dir data/fixtures/realistic_end_of_year
```

Automated fixture checks:

```bash
python -m reserve fixture-check --scenario simple --data-dir data/fixtures/simple
python -m reserve fixture-check --scenario realistic_end_of_year --data-dir data/fixtures/realistic_end_of_year
python -m reserve fixture-check --all
python -m reserve fixture-check --all --clean
```

Expected checks are documented in:
- `data/fixtures/simple/expected_values.md`
- `data/fixtures/realistic_end_of_year/expected_values.md`
- `data/fixtures/realistic_start_of_year/expected_values.md`
- `data/fixtures/realistic_mid_year/expected_values.md`

Machine-readable expectations live in:
- `data/fixtures/**/expected_values.yaml`

`fixture-check` builds workbooks, verifies formula text and model values, prints a summary, and can remove generated workbooks with `--clean`.

Additional boundary fixtures live under `data/fixtures/boundary_*`.

## Validation notes

- Duplicate contribution years are reported as warnings; the last value wins.
- If expanded schedule rows exceed `FEATURES.max_schedule_rows`, validation fails so formulas stay in-bounds.
- Funding metric formulas return blank when the denominator is zero (no fully funded target or no expenses in the 5-year window).

## Audit settings (debug)

- When `FEATURES.enable_audit` is `true`, the Forecast sheet adds hidden expected-value columns and visible audit flag columns, plus a summary at the end of the Checks sheet. Audit flags display `FAIL` when out of tolerance.
- Audit flags use `audit_tolerance_amount` and `audit_tolerance_ratio` from `inputs.yaml`.
- Audit flags are intended for build-time validation; if you edit values directly in the workbook, expect audit failures until you regenerate from the source files.
- Treat enable_audit as something akin to a "debug=Y" flag.  

## Tests

```bash
python -m unittest discover -s tests
```
