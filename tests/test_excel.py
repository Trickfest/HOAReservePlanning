import unittest

from reserve import excel
from reserve.model import Component, Inputs
from reserve.schedule import expand_schedule


def _expected_percent_funded_formula(
    row: int, forecast_years: int, max_components_rows: int
) -> str:
    start_year_cell = f"Inputs!$B${excel.INPUT_ROWS['starting_year']}"
    inflation_cell = f"Inputs!$B${excel.INPUT_ROWS['inflation_rate']}"
    year_cell = f"A{row}"

    components_end_row = 1 + max_components_rows
    base_cost_range = f"Components!$D$2:$D${components_end_row}"
    spend_year_range = f"Components!$E$2:$E${components_end_row}"
    recurring_range = f"Components!$F$2:$F${components_end_row}"
    interval_range = f"Components!$G$2:$G${components_end_row}"
    include_range = f"Components!$H$2:$H${components_end_row}"

    inflation_factor = f"(1+{inflation_cell})^({year_cell}-{start_year_cell})"

    years_to_next = (
        f"IF({year_cell}<={spend_year_range},"
        f"{spend_year_range}-{year_cell},"
        f"{spend_year_range}+CEILING(({year_cell}-{spend_year_range})/"
        f"IF({interval_range}>0,{interval_range},1),1)"
        f"*{interval_range}-{year_cell})"
    )
    recurring_age = f"{interval_range}-{years_to_next}"
    recurring_fraction = (
        f"IF({interval_range}<=0,0,"
        f"IF({recurring_age}<=0,0,{recurring_age}/{interval_range}))"
    )

    nonrecurring_fraction = (
        f"IF({year_cell}>{spend_year_range},0,"
        f"IF({spend_year_range}-{start_year_cell}<=0,1,"
        f"({year_cell}-{start_year_cell})/({spend_year_range}-{start_year_cell})))"
    )

    sum_recurring = (
        f"SUMPRODUCT(--({include_range}=\"Y\"),--({recurring_range}=\"Y\"),"
        f"{base_cost_range},{recurring_fraction})"
    )
    sum_nonrecurring = (
        f"SUMPRODUCT(--({include_range}=\"Y\"),--({recurring_range}<>\"Y\"),"
        f"{base_cost_range},{nonrecurring_fraction})"
    )

    fully_funded = f"{inflation_factor}*({sum_recurring}+{sum_nonrecurring})"
    return f"=IF({fully_funded}=0,\"\",B{row}/({fully_funded}))"


def _expected_coverage_formula(row: int, forecast_years: int) -> str:
    end_row = 1 + forecast_years
    coverage_sum = (
        f"SUM(G{row}:INDEX($G$2:$G${end_row},MIN({row}+4,{end_row})-1))"
    )
    return f"=IF({coverage_sum}=0,\"\",B{row}/{coverage_sum})"


def _expected_expenses_formula(row: int, max_schedule_rows: int) -> str:
    schedule_end_row = 1 + max_schedule_rows
    return (
        f"=SUMIFS(Schedule!$D$2:$D${schedule_end_row},"
        f"Schedule!$A$2:$A${schedule_end_row},A{row})"
    )


class ExcelTests(unittest.TestCase):
    def test_forecast_formulas(self) -> None:
        inputs = Inputs(
            starting_year=2025,
            forecast_years=3,
            beginning_reserve_balance=1000.0,
            inflation_rate=0.02,
            investment_return_rate=0.01,
            features={"max_components_rows": 20, "max_schedule_rows": 50},
        )
        components = [
            Component(
                id="roof",
                name="Roof",
                category="Building",
                base_cost=1000.0,
                spend_year=2026,
                recurring=False,
                interval_years=None,
                include=True,
                row_index=2,
            )
        ]
        schedule_items = expand_schedule(components, inputs)
        contributions = {2025: 0.0, 2026: 0.0, 2027: 0.0}

        wb = excel.build_workbook(
            inputs=inputs,
            components=components,
            schedule_items=schedule_items,
            contributions=contributions,
            scenario="test",
        )

        forecast_ws = wb["Forecast"]
        headers = [cell.value for cell in forecast_ws[1]]
        self.assertEqual(
            headers,
            [
                "year",
                "begin_balance",
                "contributions",
                "cumulative_contributions",
                "interest",
                "cumulative_interest",
                "expenses",
                "end_balance",
                "percent_funded",
                "coverage_5yr",
            ],
        )

        self.assertEqual(
            forecast_ws["D2"].value,
            "=C2",
        )
        self.assertEqual(
            forecast_ws["D3"].value,
            "=D2+C3",
        )
        self.assertEqual(
            forecast_ws["F2"].value,
            "=E2",
        )
        self.assertEqual(
            forecast_ws["F3"].value,
            "=F2+E3",
        )
        self.assertEqual(
            forecast_ws["G2"].value,
            _expected_expenses_formula(2, inputs.features["max_schedule_rows"]),
        )
        self.assertEqual(
            forecast_ws["I2"].value,
            _expected_percent_funded_formula(
                2, inputs.forecast_years, inputs.features["max_components_rows"]
            ),
        )
        self.assertEqual(
            forecast_ws["J2"].value,
            _expected_coverage_formula(2, inputs.forecast_years),
        )

        self.assertEqual(forecast_ws["I2"].number_format, "0.00%")
        self.assertEqual(forecast_ws["J2"].number_format, "0.00")


if __name__ == "__main__":
    unittest.main()
