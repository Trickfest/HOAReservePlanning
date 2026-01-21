# Repository Guidelines

## Project Structure & Module Organization
- `reserve/` contains the Python package (CLI, model logic, Excel writer).
- `data/` is the source-of-truth for inputs (`inputs.yaml`), components (`components.csv`), and contribution scenarios (`contributions/<scenario>.csv`).
- `tests/` holds unit tests (`test_model.py`).
- `dist/` contains generated workbooks (`HOA_Reserve_Planning_<scenario>.xlsx`) and is not committed.
- `pyproject.toml` defines dependencies (openpyxl, pyyaml, pytest optional).

## Build, Test, and Development Commands
- `python -m venv .venv` and `source .venv/bin/activate` to create a local env.
- `pip install -e .` installs dependencies for the CLI.
- `python -m reserve validate --scenario recommended` validates CSV/YAML inputs.
- `python -m reserve build --scenario recommended` generates the workbook in `dist/`.
- `python -m reserve build --scenario recommended --open` opens the workbook on macOS.
- `python -m reserve clean` removes generated workbooks.
- `python -m reserve fixture-check --all --clean` validates fixtures, verifies formulas/model values, and removes generated fixture workbooks.

## Coding Style & Naming Conventions
- Python: 4-space indentation, PEP 8 naming (snake_case for functions/vars, PascalCase for classes, UPPER_SNAKE for constants).
- Keep formulas Numbers-friendly: avoid whole-column references and advanced Excel-only functions; use bounded ranges from `FEATURES`.
- Keep sheet edits modular so sheets can be toggled without breaking other logic.
- Scenario files follow `data/contributions/<scenario>.csv` and must match the `--scenario` name.

## Testing Guidelines
- Framework: built-in `unittest`.
- Naming: test files `test_*.py`, test methods `test_*`.
- Run tests with `python -m unittest discover -s tests`.

## Fixtures & Validation
- Fixtures live under `data/fixtures/`; each fixture has `inputs.yaml`, `components.csv`, and `contributions/<scenario>.csv`.
- Expectations are stored in `expected_values.yaml` (machine) and `expected_values.md` (human).
- Use `--data-dir` with build/validate/fixture-check to target fixture data without touching `data/`.
- Duplicate contribution years warn; last value wins. Schedule rows exceeding `FEATURES.max_schedule_rows` fail validation.

## Data & Configuration Notes
- Update assumptions and feature toggles in `data/inputs.yaml` (e.g., `FEATURES.forecast_years`).
- Each contribution scenario must cover every forecast year; missing years should fail validation.
- Do not edit `dist/` by hand; regenerate via `python -m reserve build`.

## Commit & Pull Request Guidelines
- Git history currently shows only `Initial commit`; no established convention yet.
- Suggested commits: short, imperative messages (e.g., `Add checks sheet`).
- PRs should describe the scenario used, list data changes, and confirm the workbook was rebuilt.
