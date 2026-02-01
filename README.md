# HOA Reserve Planning Model

This project is a command-line reserve planning tool that turns simple text inputs into a multi-sheet .xlsx workbook for HOA reserve forecasting. It generates the Schedule, Forecast, Checks, and Dashboard tabs from your inputs and works in both Excel and Apple Numbers.

This tool is designed for HOAs (and similar associations) that want a transparent, repeatable reserve study workflow. You describe your components, timing, and funding assumptions in plain text files, and the app generates a spreadsheet with formulas so you can explore scenarios without rebuilding the model by hand.

The generated workbook separates **timing (Schedule)** from **cash flow (Forecast)** and includes diagnostics (Checks) plus optional audit flags to help spot inconsistencies. The intent is to make the math auditable and the inputs version-controlled, while still producing a familiar spreadsheet output.

If you’re new to reserve planning, the Forecast tab provides funding metrics like percent funded and 5‑year coverage to help assess adequacy. The app doesn’t replace professional judgement — it makes the assumptions explicit and easy to revise.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m reserve validate --scenario recommended
python -m reserve build --scenario recommended
```

What each command does:

- `python -m venv .venv`: create a local virtual environment.
- `source .venv/bin/activate`: activate the virtual environment in your shell.
- `pip install -e .`: install the package and dependencies in editable mode.
- `python -m reserve validate --scenario recommended`: validate inputs/components/contributions for the scenario.
- `python -m reserve build --scenario recommended`: generate the workbook in `dist/`.

Workbook output:

```
dist/HOA_Reserve_Planning_recommended.xlsx
```

## Solution architecture overview

The project is a small command‑line application that reads structured text inputs, calculates schedules and forecasts, and writes a spreadsheet with formulas. The workflow is:

1. **Inputs** (`inputs.yaml`, `components.csv`, `contributions/<scenario>.csv`) define assumptions, components, and yearly funding.
2. **Model & validation** load and validate the inputs, expand recurring components into a Schedule, and compute the forecast model used for checks and audit expectations.
3. **Workbook generation** writes the Excel file with multiple sheets (Inputs, Components, Schedule, Forecast, Checks, Dashboard), formulas, and formatting.
4. **Verification** uses fixtures (`fixture-check`) to compare expected formulas/values against generated workbooks.

Key ideas:
- The Schedule sheet is the single source of truth for expense timing.
- The Forecast sheet derives expenses from the Schedule and calculates balances and funding metrics.
- The Checks sheet summarizes health metrics and optional audit results.
- The generated workbook is intended for review and light “what‑if” edits; structural changes should be made in the source files and rebuilt.

## Funding metrics in the Forecast sheet

Reserve planning balances near-term cash needs with long-term component funding. The Forecast tab reports both so you can see liquidity and funding adequacy year by year.

Glossary (Forecast tab terms):
- **Inflated cost**: `inflated_cost = base_cost * (1 + inflation_rate)^(year - starting_year + spend_inflation_offset)`; the exponent is the number of years after the starting year plus the timing offset (start_of_year = 0.0, mid_year = 0.5, end_of_year = 1.0; default is end_of_year).
- **Fully funded balance (FFB)**: the sum of each component’s funded portion, where funded portion is the inflated current cost multiplied by the fraction of useful life elapsed (linear funding). Recurring items use `interval_years`; non-recurring items fund linearly from `starting_year` to `spend_year`.
- **Useful life**: the time (in years) over which a component is expected to be used before replacement. For recurring items this is `interval_years`; for non-recurring items it is `spend_year - starting_year`.
- **percent_funded**: beginning-of-year balance ÷ FFB. Around 100% means fully funded; below 100% indicates underfunded, above 100% indicates surplus relative to target.
- **coverage_5yr**: beginning-of-year balance ÷ sum of expenses for the next 5 years. > 1.0 means you can cover more than 5 years of expenses; < 1.0 means you cannot. Near the end of the forecast, the window shrinks to remaining years.
- **cumulative_contributions**: running total of contributions to date.
- **cumulative_interest**: running total of interest to date.

Examples (starting year 2026, spend_inflation_timing = end_of_year so offset = 1.0):
- Recurring example: Roof replacement costs $100,000 today, inflation 3%, interval 10 years. In year 2030 (4 years after 2026), inflated cost is $100,000 × 1.03^5 ≈ $115,927. If 4 of 10 years have elapsed, funded portion is 4/10 × $115,927 ≈ $46,371.
- Non-recurring example: Paint project costs $20,000 today, inflation 3%, spend year 2031 (5 years from 2026). In year 2029 (3 years after 2026), inflated cost is $20,000 × 1.03^4 ≈ $22,511. Funded fraction is 3/5, so funded portion ≈ $13,507.

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


## Audit settings (debug)

- When `FEATURES.enable_audit` is `true`, the Forecast sheet adds hidden expected-value columns and visible audit flag columns, plus a summary at the end of the Checks sheet. Audit flags display `FAIL` when out of tolerance.
- Audit flags use `audit_tolerance_amount` and `audit_tolerance_ratio` from `inputs.yaml`.
- Audit flags are intended for build-time validation; if you edit values directly in the workbook, expect audit failures until you regenerate from the source files.
- Treat enable_audit as something akin to a "debug=Y" flag.  


## Validation notes

- Duplicate contribution years are reported as warnings; the last value wins.
- If expanded schedule rows exceed `FEATURES.max_schedule_rows`, validation fails so formulas stay in-bounds.
- Funding metric formulas return blank when the denominator is zero (no fully funded target or no expenses in the 5-year window).
- Interest is calculated on the beginning-of-year balance only; contributions made in the same year do not earn interest until the following year (worst-case assumption).


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


## Unit Tests

```bash
python -m unittest discover -s tests
```

Unit tests are small, fast checks focused on core Python behavior: input parsing/validation, schedule expansion, forecast math, and CLI wiring. They run in-memory and avoid spreadsheet generation, which keeps them quick and reliable for regression detection. The limitation is they don’t validate the final Excel formulas or workbook rendering; that coverage is handled by fixtures (`fixture-check`) instead.

## Fixture Tests

Use the fixture datasets to verify spreadsheet outputs without touching the main data files.  Fixture tests validate the end-to-end workbook output: they build spreadsheets from known inputs and compare key cell formulas and computed values against expected snapshots. This catches regression in Excel logic and formatting that unit tests can’t see. The tradeoff is they’re slower, generate files, and are only as comprehensive as the fixtures you maintain.

The `expected_values.md` files are human-readable notes that explain the expected results and assumptions. They are not read by the test runner; `fixture-check` uses `expected_values.yaml` as the machine-readable source of truth.

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

## Appendix: Additional Reference

### CLI command summary
- `build`: generate a workbook for a scenario.
- `validate`: validate inputs/components/contributions for a scenario.
- `fixture-check`: build fixtures and compare workbook outputs to expectations.
- `clean`: remove generated workbooks from `dist/`.

Common flags:
- `--scenario`: scenario name (matches `data/contributions/<scenario>.csv`).
- `--data-dir`: base directory for data files.
- `--inputs`: path to an alternate `inputs.yaml`.
- `--components`: path to an alternate `components.csv`.
- `--open`: open the generated workbook (macOS).

### CSV format examples
`components.csv`:
```csv
id,name,category,base_cost,spend_year,recurring,interval_years,include
roof,Roof,General,1000000,2036,N,,Y
pool,Pool,Exterior,250000,2030,Y,5,Y
```

`contributions.csv`:
```csv
year,contribution
2026,50000
2027,51500
```

Notes:
- `recurring` and `include` accept `Y` or `N`.
- `interval_years` is required when `recurring = Y`.

### Troubleshooting common warnings
- **spend_year outside forecast window**: increase `FEATURES.forecast_years` or adjust the component’s `spend_year`.
- **duplicate contribution years**: the last value wins; remove duplicates if unintended.

### Spreadsheet limitations
- Formulas use bounded ranges to stay Numbers-friendly and avoid whole-column references.
- Audit flags show `FAIL` text rather than conditional formatting because Numbers ignores some conditional rules.

### Regeneration reminder
`dist/` is generated output. After editing inputs or CSVs, rerun `python -m reserve build --scenario <scenario>` to regenerate the workbook.

### What you can edit in a generated workbook
The workbook is intended for quick what‑if checks, but most of the structure is generated from the source files.

Safe to edit for quick what‑ifs (no rebuild required):
- Forecast contributions (Forecast column C).
- Component `base_cost` (formulas reference it directly).

Requires a rebuild to be correct:
- Inputs (`starting_year`, rates, `spend_inflation_timing`, features, audit tolerances).
- Any timing changes (`spend_year`, `recurring`, `interval_years`) or adding/removing components.
- Changing the component `include` flag (Schedule rows won’t update without a rebuild).
- Forecast horizon (`FEATURES.forecast_years`) or schedule expansion toggles.

Rule of thumb: edit **contributions and costs** in the workbook; edit **structure/timing/assumptions** in the source files and rebuild.

Note: if `FEATURES.enable_audit` is enabled, changing contributions or component costs in the workbook will cause audit flags to show `FAIL` because expected values were generated at build time. Rebuild to clear audit failures.
