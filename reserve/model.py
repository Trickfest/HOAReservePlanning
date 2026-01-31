from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
from typing import Dict, Iterable, List

import yaml

from .constants import (
    DATA_DIR,
    DEFAULT_AUDIT_TOLERANCE_AMOUNT,
    DEFAULT_AUDIT_TOLERANCE_RATIO,
    DEFAULT_FEATURES,
    DEFAULT_SPEND_INFLATION_OFFSET,
    DEFAULT_SPEND_INFLATION_TIMING,
)


@dataclass
class Inputs:
    starting_year: int
    forecast_years: int
    beginning_reserve_balance: float
    inflation_rate: float
    investment_return_rate: float
    features: Dict[str, object]
    spend_inflation_timing: str = DEFAULT_SPEND_INFLATION_TIMING
    spend_inflation_offset: float = DEFAULT_SPEND_INFLATION_OFFSET
    audit_tolerance_amount: float = DEFAULT_AUDIT_TOLERANCE_AMOUNT
    audit_tolerance_ratio: float = DEFAULT_AUDIT_TOLERANCE_RATIO


@dataclass
class Component:
    id: str
    name: str
    category: str
    base_cost: float
    spend_year: int
    recurring: bool
    interval_years: int | None
    include: bool
    row_index: int


@dataclass
class ForecastRow:
    year: int
    begin_balance: float
    contributions: float
    interest: float
    expenses: float
    end_balance: float


def _require(data: Dict[str, object], key: str) -> object:
    if key not in data:
        raise ValueError(f"Missing required input: {key}")
    return data[key]


def _resolve_data_dir(data_dir: Path | None) -> Path:
    return data_dir if data_dir is not None else DATA_DIR


def _parse_spend_inflation_timing(value: str) -> float:
    normalized = value.strip().lower()
    if normalized == "start_of_year":
        return 0.0
    if normalized == "mid_year":
        return 0.5
    if normalized == "end_of_year":
        return 1.0
    raise ValueError(
        "spend_inflation_timing must be one of: start_of_year, mid_year, end_of_year"
    )


def load_inputs(path: Path | None = None, data_dir: Path | None = None) -> Inputs:
    if path is None:
        path = _resolve_data_dir(data_dir) / "inputs.yaml"
    raw = yaml.safe_load(path.read_text()) or {}

    features = DEFAULT_FEATURES.copy()
    raw_features = raw.get("FEATURES", {})
    if raw_features:
        features.update(raw_features)

    forecast_years = raw.get("forecast_years", features.get("forecast_years"))
    if forecast_years is None:
        forecast_years = DEFAULT_FEATURES["forecast_years"]
    features["forecast_years"] = int(forecast_years)

    starting_year = int(_require(raw, "starting_year"))
    beginning_reserve_balance = float(_require(raw, "beginning_reserve_balance"))
    inflation_rate = float(_require(raw, "inflation_rate"))
    investment_return_rate = float(_require(raw, "investment_return_rate"))

    spend_inflation_timing = str(
        raw.get("spend_inflation_timing", DEFAULT_SPEND_INFLATION_TIMING)
    )
    spend_inflation_offset = _parse_spend_inflation_timing(spend_inflation_timing)

    audit_tolerance_amount = float(
        raw.get("audit_tolerance_amount", DEFAULT_AUDIT_TOLERANCE_AMOUNT)
    )
    audit_tolerance_ratio = float(
        raw.get("audit_tolerance_ratio", DEFAULT_AUDIT_TOLERANCE_RATIO)
    )

    return Inputs(
        starting_year=starting_year,
        forecast_years=int(features["forecast_years"]),
        beginning_reserve_balance=beginning_reserve_balance,
        inflation_rate=inflation_rate,
        investment_return_rate=investment_return_rate,
        audit_tolerance_amount=audit_tolerance_amount,
        audit_tolerance_ratio=audit_tolerance_ratio,
        features=features,
        spend_inflation_timing=spend_inflation_timing,
        spend_inflation_offset=spend_inflation_offset,
    )


def load_components(path: Path | None = None, data_dir: Path | None = None) -> List[Component]:
    if path is None:
        path = _resolve_data_dir(data_dir) / "components.csv"
    required = [
        "id",
        "name",
        "category",
        "base_cost",
        "spend_year",
        "recurring",
        "interval_years",
        "include",
    ]
    components: List[Component] = []
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("components.csv is missing a header row")
        missing = [col for col in required if col not in reader.fieldnames]
        if missing:
            raise ValueError(f"components.csv missing columns: {', '.join(missing)}")

        for row in reader:
            raw_id = (row.get("id") or "").strip()
            raw_name = (row.get("name") or "").strip()
            if not raw_id and not raw_name:
                continue

            recurring_flag = (row.get("recurring") or "").strip().upper()
            include_flag = (row.get("include") or "").strip().upper()

            interval_raw = (row.get("interval_years") or "").strip()
            interval_val = int(interval_raw) if interval_raw else None

            row_index = len(components) + 2
            component = Component(
                id=raw_id,
                name=raw_name,
                category=(row.get("category") or "").strip(),
                base_cost=float((row.get("base_cost") or 0) or 0),
                spend_year=int((row.get("spend_year") or 0) or 0),
                recurring=recurring_flag == "Y",
                interval_years=interval_val,
                include=include_flag == "Y",
                row_index=row_index,
            )
            components.append(component)

    return components


def load_contributions(
    scenario: str, contributions_dir: Path | None = None, data_dir: Path | None = None
) -> Dict[int, float]:
    if contributions_dir is None:
        contributions_dir = _resolve_data_dir(data_dir) / "contributions"
    path = contributions_dir / f"{scenario}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Scenario file not found: {path}")

    contributions: Dict[int, float] = {}
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"{path.name} is missing a header row")
        required = ["year", "contribution"]
        missing = [col for col in required if col not in reader.fieldnames]
        if missing:
            raise ValueError(f"{path.name} missing columns: {', '.join(missing)}")

        for row in reader:
            year_raw = (row.get("year") or "").strip()
            if not year_raw:
                continue
            year = int(year_raw)
            contribution = float((row.get("contribution") or 0) or 0)
            contributions[year] = contribution

    return contributions


def compute_forecast(
    inputs: Inputs,
    contributions: Dict[int, float],
    schedule_expenses: Dict[int, float],
) -> List[ForecastRow]:
    rows: List[ForecastRow] = []
    begin_balance = inputs.beginning_reserve_balance
    start_year = inputs.starting_year
    end_year = start_year + inputs.forecast_years - 1

    for year in range(start_year, end_year + 1):
        contribution = contributions.get(year, 0.0)
        interest = begin_balance * inputs.investment_return_rate
        expenses = schedule_expenses.get(year, 0.0)
        end_balance = begin_balance + contribution + interest - expenses
        rows.append(
            ForecastRow(
                year=year,
                begin_balance=begin_balance,
                contributions=contribution,
                interest=interest,
                expenses=expenses,
                end_balance=end_balance,
            )
        )
        begin_balance = end_balance

    return rows


def expenses_by_year(schedule_items: Iterable["ScheduleItem"]) -> Dict[int, float]:
    totals: Dict[int, float] = {}
    for item in schedule_items:
        totals[item.year] = totals.get(item.year, 0.0) + item.nominal_expense
    return totals


# Import placed at end to avoid a circular import for typing.
from .schedule import ScheduleItem  # noqa: E402
