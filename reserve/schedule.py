from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .model import Component, Inputs


@dataclass
class ScheduleItem:
    year: int
    component_id: str
    component_name: str
    base_cost: float
    component_row: int
    nominal_expense: float


def expand_schedule(components: List[Component], inputs: Inputs) -> List[ScheduleItem]:
    start_year = inputs.starting_year
    end_year = start_year + inputs.forecast_years - 1
    schedule: List[ScheduleItem] = []
    inflation_offset = inputs.spend_inflation_offset

    for component in components:
        if not component.include:
            continue

        years: List[int] = []
        if component.recurring:
            interval = component.interval_years or 0
            if interval <= 0:
                continue
            year = component.spend_year
            while year <= end_year:
                if year >= start_year:
                    years.append(year)
                year += interval
        else:
            if start_year <= component.spend_year <= end_year:
                years.append(component.spend_year)

        for year in years:
            nominal = component.base_cost * (
                (1 + inputs.inflation_rate) ** (year - start_year + inflation_offset)
            )
            schedule.append(
                ScheduleItem(
                    year=year,
                    component_id=component.id,
                    component_name=component.name,
                    base_cost=component.base_cost,
                    component_row=component.row_index,
                    nominal_expense=nominal,
                )
            )

    schedule.sort(key=lambda item: (item.year, item.component_id))
    return schedule
