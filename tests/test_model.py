import unittest

from reserve.model import Component, Inputs, compute_forecast, expenses_by_year
from reserve.schedule import expand_schedule


class ModelTests(unittest.TestCase):
    def test_expand_schedule_recurring(self) -> None:
        inputs = Inputs(
            starting_year=2025,
            forecast_years=12,
            beginning_reserve_balance=0.0,
            inflation_rate=0.0,
            investment_return_rate=0.0,
            features={},
        )
        components = [
            Component(
                id="roof",
                name="Roof",
                category="Building",
                base_cost=1000.0,
                spend_year=2025,
                recurring=True,
                interval_years=5,
                include=True,
                row_index=2,
            )
        ]

        schedule = expand_schedule(components, inputs)
        years = [item.year for item in schedule]
        self.assertEqual(years, [2025, 2030, 2035])

    def test_forecast_math(self) -> None:
        inputs = Inputs(
            starting_year=2025,
            forecast_years=3,
            beginning_reserve_balance=1000.0,
            inflation_rate=0.0,
            investment_return_rate=0.1,
            features={},
        )
        components = [
            Component(
                id="paint",
                name="Paint",
                category="Exterior",
                base_cost=100.0,
                spend_year=2026,
                recurring=False,
                interval_years=None,
                include=True,
                row_index=2,
            )
        ]
        schedule_items = expand_schedule(components, inputs)
        expenses = expenses_by_year(schedule_items)
        contributions = {2025: 200.0, 2026: 200.0, 2027: 200.0}
        rows = compute_forecast(inputs, contributions, expenses)

        self.assertAlmostEqual(rows[-1].end_balance, 1883.0, places=2)


if __name__ == "__main__":
    unittest.main()
