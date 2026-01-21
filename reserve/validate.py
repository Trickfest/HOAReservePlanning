from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Dict, List, Tuple

from .constants import DATA_DIR
from .model import Component, Inputs, load_components, load_inputs
from .schedule import expand_schedule


@dataclass
class ValidationResult:
    errors: List[str]
    warnings: List[str]


class ValidationError(Exception):
    def __init__(self, result: ValidationResult) -> None:
        super().__init__("Validation failed")
        self.result = result


def validate_scenario(
    scenario: str,
    data_dir: Path | None = None,
) -> Tuple[ValidationResult, Inputs, List[Component], Dict[int, float]]:
    errors: List[str] = []
    warnings: List[str] = []

    try:
        inputs = load_inputs(data_dir=data_dir)
    except Exception as exc:  # pragma: no cover - fatal parse issues
        errors.append(str(exc))
        result = ValidationResult(errors, warnings)
        raise ValidationError(result) from exc

    components_path = (data_dir or DATA_DIR) / "components.csv"
    component_errors, component_warnings = _validate_components_csv(
        components_path, inputs
    )
    errors.extend(component_errors)
    warnings.extend(component_warnings)

    if component_errors:
        components = []
    else:
        try:
            components = load_components(data_dir=data_dir)
        except Exception as exc:
            errors.append(str(exc))
            components = []

    contributions, contrib_errors, contrib_warnings = _load_contributions_for_validation(
        scenario, data_dir
    )
    errors.extend(contrib_errors)
    warnings.extend(contrib_warnings)

    if not contrib_errors:
        contrib_errors, contrib_warnings = _validate_contributions(inputs, contributions)
        errors.extend(contrib_errors)
        warnings.extend(contrib_warnings)

    if (
        not errors
        and components
        and inputs.features.get("enable_schedule_expansion", True)
    ):
        max_schedule_rows = int(inputs.features.get("max_schedule_rows", 10000))
        schedule_items = expand_schedule(components, inputs)
        if len(schedule_items) > max_schedule_rows:
            errors.append(
                f"Schedule rows {len(schedule_items)} exceed max_schedule_rows {max_schedule_rows}"
            )

    result = ValidationResult(errors, warnings)
    return result, inputs, components, contributions


def _validate_components_csv(path: Path, inputs: Inputs) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    required = {
        "id",
        "name",
        "category",
        "base_cost",
        "spend_year",
        "recurring",
        "interval_years",
        "include",
    }

    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            errors.append("components.csv is missing a header row")
            return errors, warnings

        missing = [col for col in sorted(required) if col not in reader.fieldnames]
        if missing:
            errors.append(f"components.csv missing columns: {', '.join(missing)}")
            return errors, warnings

        start_year = inputs.starting_year
        end_year = start_year + inputs.forecast_years - 1

        for row_number, row in enumerate(reader, start=2):
            raw_id = (row.get("id") or "").strip()
            raw_name = (row.get("name") or "").strip()
            if not raw_id and not raw_name:
                continue

            recurring = (row.get("recurring") or "").strip().upper()
            include = (row.get("include") or "").strip().upper()

            if recurring not in {"Y", "N"}:
                errors.append(
                    f"components.csv row {row_number}: recurring must be Y or N"
                )
            if include not in {"Y", "N"}:
                errors.append(f"components.csv row {row_number}: include must be Y or N")

            spend_year_raw = (row.get("spend_year") or "").strip()
            if spend_year_raw:
                try:
                    spend_year = int(spend_year_raw)
                    if spend_year < start_year or spend_year > end_year:
                        warnings.append(
                            f"components.csv row {row_number}: spend_year {spend_year} outside forecast window"
                        )
                except ValueError:
                    errors.append(
                        f"components.csv row {row_number}: spend_year must be an integer"
                    )
            else:
                errors.append(
                    f"components.csv row {row_number}: spend_year is required"
                )

            interval_raw = (row.get("interval_years") or "").strip()
            if recurring == "Y":
                if not interval_raw:
                    errors.append(
                        f"components.csv row {row_number}: interval_years required for recurring items"
                    )
                else:
                    try:
                        interval = int(interval_raw)
                        if interval <= 0:
                            errors.append(
                                f"components.csv row {row_number}: interval_years must be > 0"
                            )
                    except ValueError:
                        errors.append(
                            f"components.csv row {row_number}: interval_years must be an integer"
                        )

    return errors, warnings


def _load_contributions_for_validation(
    scenario: str, data_dir: Path | None
) -> Tuple[Dict[int, float], List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    contributions: Dict[int, float] = {}

    contributions_dir = (data_dir or DATA_DIR) / "contributions"
    path = contributions_dir / f"{scenario}.csv"
    if not path.exists():
        errors.append(f"Scenario file not found: {path}")
        return contributions, errors, warnings

    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            errors.append(f"{path.name} is missing a header row")
            return contributions, errors, warnings

        required = {"year", "contribution"}
        missing = [col for col in sorted(required) if col not in reader.fieldnames]
        if missing:
            errors.append(f"{path.name} missing columns: {', '.join(missing)}")
            return contributions, errors, warnings

        seen_years: set[int] = set()
        duplicate_years: set[int] = set()

        for row_number, row in enumerate(reader, start=2):
            year_raw = (row.get("year") or "").strip()
            if not year_raw:
                continue
            try:
                year = int(year_raw)
            except ValueError:
                errors.append(
                    f"{path.name} row {row_number}: year must be an integer"
                )
                continue

            if year in seen_years:
                duplicate_years.add(year)
            seen_years.add(year)

            contribution_raw = (row.get("contribution") or "").strip()
            if contribution_raw == "":
                contribution = 0.0
            else:
                try:
                    contribution = float(contribution_raw)
                except ValueError:
                    errors.append(
                        f"{path.name} row {row_number}: contribution must be a number"
                    )
                    continue
            contributions[year] = contribution

        if duplicate_years:
            dup_list = ", ".join(str(year) for year in sorted(duplicate_years))
            warnings.append(f"Duplicate contribution years: {dup_list}")

    return contributions, errors, warnings


def _validate_contributions(
    inputs: Inputs, contributions: Dict[int, float]
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    start_year = inputs.starting_year
    end_year = start_year + inputs.forecast_years - 1

    missing_years = [
        year for year in range(start_year, end_year + 1) if year not in contributions
    ]
    if missing_years:
        errors.append(
            "Missing contributions for years: "
            + ", ".join(str(year) for year in missing_years)
        )

    extra_years = sorted(year for year in contributions if year < start_year or year > end_year)
    if extra_years:
        warnings.append(
            "Contribution years outside forecast window: "
            + ", ".join(str(year) for year in extra_years)
        )

    return errors, warnings
