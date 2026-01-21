from __future__ import annotations

from typing import Dict, List

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

from .model import Component, Inputs
from .schedule import ScheduleItem

HEADER_FILL = PatternFill(fill_type="solid", fgColor="D9D9D9")
INPUT_FILL = PatternFill(fill_type="solid", fgColor="FFF2CC")
BOLD_FONT = Font(bold=True)

INPUT_ROWS = {
    "starting_year": 2,
    "beginning_reserve_balance": 3,
    "inflation_rate": 4,
    "investment_return_rate": 5,
}
FEATURE_ROWS = {
    "forecast_years": 8,
    "enable_checks": 9,
    "enable_dashboard": 10,
    "enable_schedule_expansion": 11,
    "max_components_rows": 12,
    "max_schedule_rows": 13,
}


def build_workbook(
    inputs: Inputs,
    components: List[Component],
    schedule_items: List[ScheduleItem],
    contributions: Dict[int, float],
    scenario: str,
) -> Workbook:
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    _write_readme_sheet(ws, scenario)

    inputs_ws = wb.create_sheet("Inputs")
    _write_inputs_sheet(inputs_ws, inputs)

    components_ws = wb.create_sheet("Components")
    _write_components_sheet(components_ws, inputs, components)

    schedule_ws = wb.create_sheet("Schedule")
    _write_schedule_sheet(schedule_ws, inputs, schedule_items)

    forecast_ws = wb.create_sheet("Forecast")
    _write_forecast_sheet(forecast_ws, inputs, contributions)

    if inputs.features.get("enable_checks", True):
        checks_ws = wb.create_sheet("Checks")
        _write_checks_sheet(checks_ws, inputs)
    else:
        checks_ws = wb.create_sheet("Checks")
        checks_ws["A1"] = "Checks disabled by FEATURES.enable_checks"

    if inputs.features.get("enable_dashboard", True):
        dashboard_ws = wb.create_sheet("Dashboard")
        _write_dashboard_sheet(dashboard_ws, inputs)
    else:
        dashboard_ws = wb.create_sheet("Dashboard")
        dashboard_ws["A1"] = "Dashboard disabled by FEATURES.enable_dashboard"

    return wb


def _style_header(ws, num_cols: int) -> None:
    for col in range(1, num_cols + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = HEADER_FILL
        cell.font = BOLD_FONT
        cell.alignment = Alignment(horizontal="left")


def _write_readme_sheet(ws, scenario: str) -> None:
    ws["A1"] = "HOA Reserve Planning Workbook"
    ws["A2"] = f"Scenario: {scenario}"
    ws["A3"] = "Generated from data/inputs.yaml, data/components.csv, and data/contributions/*.csv"
    ws["A4"] = "Edit source files and rebuild for versioned changes."
    ws["A6"] = "Sheets: Inputs, Components, Schedule, Forecast, Checks, Dashboard"
    ws.column_dimensions["A"].width = 90


def _write_inputs_sheet(ws, inputs: Inputs) -> None:
    ws.append(["Input", "Value", "Notes"])
    _style_header(ws, 3)

    rows = [
        ("starting_year", inputs.starting_year, "First year of the forecast"),
        ("beginning_reserve_balance", inputs.beginning_reserve_balance, "Opening reserve balance"),
        ("inflation_rate", inputs.inflation_rate, "Annual inflation rate"),
        ("investment_return_rate", inputs.investment_return_rate, "Annual investment return"),
    ]

    for label, value, note in rows:
        ws.append([label, value, note])

    ws.append(["", "", ""])
    ws.append(["FEATURES", "", "Toggle optional behavior"])
    ws.append(["forecast_years", inputs.forecast_years, "Forecast horizon in years"])
    ws.append([
        "enable_checks",
        bool(inputs.features.get("enable_checks", True)),
        "Include the Checks sheet",
    ])
    ws.append([
        "enable_dashboard",
        bool(inputs.features.get("enable_dashboard", True)),
        "Include the Dashboard sheet",
    ])
    ws.append([
        "enable_schedule_expansion",
        bool(inputs.features.get("enable_schedule_expansion", True)),
        "Generate recurring schedule rows",
    ])
    ws.append([
        "max_components_rows",
        int(inputs.features.get("max_components_rows", 500)),
        "Max rows reserved for Components",
    ])
    ws.append([
        "max_schedule_rows",
        int(inputs.features.get("max_schedule_rows", 10000)),
        "Max rows reserved for Schedule",
    ])

    for row in range(2, 6):
        cell = ws.cell(row=row, column=2)
        cell.fill = INPUT_FILL

    for row in range(8, 14):
        cell = ws.cell(row=row, column=2)
        cell.fill = INPUT_FILL

    ws.cell(row=INPUT_ROWS["starting_year"], column=2).number_format = "0"
    ws.cell(row=INPUT_ROWS["beginning_reserve_balance"], column=2).number_format = "#,##0"
    ws.cell(row=INPUT_ROWS["inflation_rate"], column=2).number_format = "0.00%"
    ws.cell(row=INPUT_ROWS["investment_return_rate"], column=2).number_format = "0.00%"

    ws.cell(row=FEATURE_ROWS["forecast_years"], column=2).number_format = "0"
    ws.cell(row=FEATURE_ROWS["max_components_rows"], column=2).number_format = "0"
    ws.cell(row=FEATURE_ROWS["max_schedule_rows"], column=2).number_format = "0"

    ws.freeze_panes = "A2"
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 60


def _write_components_sheet(ws, inputs: Inputs, components: List[Component]) -> None:
    headers = [
        "id",
        "name",
        "category",
        "base_cost",
        "spend_year",
        "recurring",
        "interval_years",
        "include",
    ]
    ws.append(headers)
    _style_header(ws, len(headers))

    max_rows = int(inputs.features.get("max_components_rows", 500))
    for row in range(2, 2 + max_rows):
        for col in range(1, len(headers) + 1):
            ws.cell(row=row, column=col).fill = INPUT_FILL

    for component in components:
        row = component.row_index
        ws.cell(row=row, column=1, value=component.id)
        ws.cell(row=row, column=2, value=component.name)
        ws.cell(row=row, column=3, value=component.category)
        ws.cell(row=row, column=4, value=component.base_cost)
        ws.cell(row=row, column=5, value=component.spend_year)
        ws.cell(row=row, column=6, value="Y" if component.recurring else "N")
        ws.cell(row=row, column=7, value=component.interval_years or "")
        ws.cell(row=row, column=8, value="Y" if component.include else "N")

    for row in range(2, 2 + max_rows):
        ws.cell(row=row, column=4).number_format = "#,##0"
        ws.cell(row=row, column=5).number_format = "0"
        ws.cell(row=row, column=7).number_format = "0"

    ws.freeze_panes = "A2"
    widths = [16, 28, 18, 14, 12, 10, 14, 10]
    for idx, width in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + idx)].width = width


def _write_schedule_sheet(ws, inputs: Inputs, schedule_items: List[ScheduleItem]) -> None:
    headers = ["year", "component_id", "component_name", "nominal_expense"]
    ws.append(headers)
    _style_header(ws, len(headers))

    start_row = 2
    inflation_cell = f"Inputs!$B${INPUT_ROWS['inflation_rate']}"
    start_year_cell = f"Inputs!$B${INPUT_ROWS['starting_year']}"

    for idx, item in enumerate(schedule_items, start=start_row):
        ws.cell(row=idx, column=1, value=item.year)
        ws.cell(row=idx, column=2, value=item.component_id)
        ws.cell(row=idx, column=3, value=item.component_name)

        base_cost_cell = f"Components!$D${item.component_row}"
        formula = f"={base_cost_cell}*(1+{inflation_cell})^(A{idx}-{start_year_cell})"
        cell = ws.cell(row=idx, column=4, value=formula)
        cell.number_format = "#,##0"

    ws.freeze_panes = "A2"
    widths = [8, 16, 32, 16]
    for idx, width in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + idx)].width = width


def _write_forecast_sheet(ws, inputs: Inputs, contributions: Dict[int, float]) -> None:
    headers = [
        "year",
        "begin_balance",
        "contributions",
        "interest",
        "expenses",
        "end_balance",
    ]
    ws.append(headers)
    _style_header(ws, len(headers))

    start_year = inputs.starting_year
    forecast_years = inputs.forecast_years
    max_schedule_rows = int(inputs.features.get("max_schedule_rows", 10000))
    schedule_end_row = 1 + max_schedule_rows

    for offset in range(forecast_years):
        row = 2 + offset
        year = start_year + offset
        ws.cell(row=row, column=1, value=year)

        if row == 2:
            begin_formula = f"=Inputs!$B${INPUT_ROWS['beginning_reserve_balance']}"
        else:
            begin_formula = f"=F{row - 1}"
        ws.cell(row=row, column=2, value=begin_formula)

        contribution_value = contributions.get(year, 0.0)
        contrib_cell = ws.cell(row=row, column=3, value=contribution_value)
        contrib_cell.fill = INPUT_FILL

        interest_formula = f"=B{row}*Inputs!$B${INPUT_ROWS['investment_return_rate']}"
        ws.cell(row=row, column=4, value=interest_formula)

        expenses_formula = (
            f"=SUMIFS(Schedule!$D$2:$D${schedule_end_row},"
            f"Schedule!$A$2:$A${schedule_end_row},A{row})"
        )
        ws.cell(row=row, column=5, value=expenses_formula)

        end_formula = f"=B{row}+C{row}+D{row}-E{row}"
        ws.cell(row=row, column=6, value=end_formula)

    for row in range(2, 2 + forecast_years):
        for col in range(2, 7):
            ws.cell(row=row, column=col).number_format = "#,##0"

    ws.freeze_panes = "A2"
    widths = [8, 18, 16, 16, 16, 18]
    for idx, width in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + idx)].width = width


def _write_checks_sheet(ws, inputs: Inputs) -> None:
    forecast_years = inputs.forecast_years
    end_row = 1 + forecast_years

    ws.append(["Check", "Value"])
    _style_header(ws, 2)

    ws.append([
        "Years with negative ending balance",
        f"=COUNTIF(Forecast!$F$2:$F${end_row},\"<0\")",
    ])
    ws.append([
        "Years with zero expenses",
        f"=COUNTIF(Forecast!$E$2:$E${end_row},0)",
    ])

    ws.append(["", ""])
    ws.append(["Negative balance years", ""])
    ws.append(["Year", ""])

    start_list_row = ws.max_row + 1
    for offset in range(forecast_years):
        forecast_row = 2 + offset
        formula = f"=IF(Forecast!$F${forecast_row}<0,Forecast!$A${forecast_row},\"\")"
        ws.cell(row=start_list_row + offset, column=1, value=formula)

    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 18
    ws.freeze_panes = "A2"


def _write_dashboard_sheet(ws, inputs: Inputs) -> None:
    forecast_years = inputs.forecast_years
    end_row = 1 + forecast_years

    ws.append(["Metric", "Value"])
    _style_header(ws, 2)

    ws.append([
        "Lowest reserve balance",
        f"=MIN(Forecast!$F$2:$F${end_row})",
    ])
    ws.append([
        "Ending balance (final year)",
        f"=Forecast!$F${end_row}",
    ])
    ws.append([
        "Final forecast year",
        f"=Forecast!$A${end_row}",
    ])

    for row in range(2, 5):
        ws.cell(row=row, column=2).number_format = "#,##0"

    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 18
    ws.freeze_panes = "A2"
