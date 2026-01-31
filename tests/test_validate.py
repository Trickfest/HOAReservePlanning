import csv
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from reserve.cli import main as cli_main
from reserve.model import Component, Inputs, compute_forecast, expenses_by_year, load_inputs
from reserve.schedule import expand_schedule
from reserve.validate import validate_scenario


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def write_inputs(
    path: Path,
    starting_year: int = 2025,
    forecast_years: int = 2,
    beginning_reserve_balance: float = 0.0,
    inflation_rate: float = 0.0,
    investment_return_rate: float = 0.0,
    spend_inflation_timing: str | None = None,
    enable_schedule_expansion: bool = True,
    max_schedule_rows: int = 20,
) -> None:
    content = (
        f"starting_year: {starting_year}\n"
        f"beginning_reserve_balance: {beginning_reserve_balance}\n"
        f"inflation_rate: {inflation_rate}\n"
        f"investment_return_rate: {investment_return_rate}\n"
    )
    if spend_inflation_timing is not None:
        content += f"spend_inflation_timing: {spend_inflation_timing}\n"
    content += (
        "FEATURES:\n"
        f"  forecast_years: {forecast_years}\n"
        "  enable_checks: true\n"
        "  enable_dashboard: true\n"
        f"  enable_schedule_expansion: {str(enable_schedule_expansion).lower()}\n"
        "  max_components_rows: 50\n"
        f"  max_schedule_rows: {max_schedule_rows}\n"
    )
    path.write_text(content)


class ValidationTests(unittest.TestCase):
    def test_spend_inflation_timing_variants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            inputs_path = data_dir / "inputs.yaml"

            for timing, offset in (
                ("start_of_year", 0.0),
                ("mid_year", 0.5),
                ("end_of_year", 1.0),
            ):
                write_inputs(
                    inputs_path,
                    forecast_years=1,
                    spend_inflation_timing=timing,
                )
                inputs = load_inputs(path=inputs_path)
                self.assertEqual(inputs.spend_inflation_timing, timing)
                self.assertAlmostEqual(inputs.spend_inflation_offset, offset, places=6)

    def test_validate_with_override_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "data"
            data_dir.mkdir()
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )

            alt_dir = root / "alt"
            alt_dir.mkdir()
            inputs_path = alt_dir / "inputs.yaml"
            components_path = alt_dir / "components.csv"
            write_inputs(inputs_path, forecast_years=1, starting_year=2025)
            write_csv(
                components_path,
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["roof", "Roof", "General", 1000, 2025, "N", "", "Y"]],
            )

            result, inputs, components, contributions = validate_scenario(
                "scenario",
                data_dir=data_dir,
                inputs_path=inputs_path,
                components_path=components_path,
            )

            self.assertEqual(result.errors, [])
            self.assertEqual(inputs.starting_year, 2025)
            self.assertEqual(len(components), 1)
            self.assertIn(2025, contributions)

    def test_default_audit_tolerances(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            inputs = load_inputs(data_dir=data_dir)
            self.assertAlmostEqual(inputs.audit_tolerance_amount, 0.01, places=4)
            self.assertAlmostEqual(inputs.audit_tolerance_ratio, 0.0001, places=6)
            self.assertEqual(inputs.spend_inflation_timing, "end_of_year")
            self.assertAlmostEqual(inputs.spend_inflation_offset, 1.0, places=6)

    def test_invalid_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["bad", "Bad", "General", 100, 2025, "maybe", "", "yes"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "components.csv row 2: recurring must be Y or N", result.errors
            )
            self.assertIn(
                "components.csv row 2: include must be Y or N", result.errors
            )

    def test_non_integer_spend_year(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=2)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["bad_year", "Bad", "General", 100, "202A", "N", "", "Y"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0], [2026, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "components.csv row 2: spend_year must be an integer", result.errors
            )

    def test_non_integer_interval(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=2)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["bad_int", "Bad", "General", 100, 2025, "Y", "3.5", "Y"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0], [2026, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "components.csv row 2: interval_years must be an integer", result.errors
            )

    def test_missing_base_cost(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["item", "Item", "General", "", 2025, "N", "", "Y"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "components.csv row 2: base_cost is required", result.errors
            )

    def test_non_numeric_base_cost(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["item", "Item", "General", "abc", 2025, "N", "", "Y"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "components.csv row 2: base_cost must be a number", result.errors
            )

    def test_base_cost_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )

            cases = [
                (0, "components.csv row 2: base_cost must be > 0"),
                (-5, "components.csv row 2: base_cost must be > 0"),
                (10000001, "components.csv row 2: base_cost must be <= 10000000"),
            ]
            for value, expected in cases:
                write_csv(
                    data_dir / "components.csv",
                    [
                        "id",
                        "name",
                        "category",
                        "base_cost",
                        "spend_year",
                        "recurring",
                        "interval_years",
                        "include",
                    ],
                    [["item", "Item", "General", value, 2025, "N", "", "Y"]],
                )
                result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
                self.assertIn(expected, result.errors)

    def test_nonrecurring_interval_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["item", "Item", "General", 100, 2025, "N", "N/A", "Y"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )
            result, _, components, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertEqual(result.errors, [])
            self.assertIsNone(components[0].interval_years)

    def test_missing_columns_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                ],
                [["item", "Item", "General", 100, 2025, "N", ""]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn("components.csv missing columns: include", result.errors)

    def test_missing_columns_contributions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=1)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["item", "Item", "General", 100, 2025, "N", "", "Y"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "amount"],
                [[2025, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "scenario.csv missing columns: contribution", result.errors
            )

    def test_duplicate_contribution_year_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(data_dir / "inputs.yaml", forecast_years=2)
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 100], [2025, 150], [2026, 200]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "Duplicate contribution years: 2025", result.warnings
            )
            self.assertEqual(result.errors, [])

    def test_max_schedule_rows_exceeded(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            write_inputs(
                data_dir / "inputs.yaml",
                forecast_years=3,
                max_schedule_rows=2,
            )
            write_csv(
                data_dir / "components.csv",
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["annual", "Annual", "General", 10, 2025, "Y", 1, "Y"]],
            )
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0], [2026, 0], [2027, 0]],
            )
            result, _, _, _ = validate_scenario("scenario", data_dir=data_dir)
            self.assertIn(
                "Schedule rows 3 exceed max_schedule_rows 2", result.errors
            )


class ScheduleAndForecastTests(unittest.TestCase):
    def test_schedule_inclusive_end_year(self) -> None:
        inputs = Inputs(
            starting_year=2025,
            forecast_years=3,
            beginning_reserve_balance=0.0,
            inflation_rate=0.0,
            investment_return_rate=0.0,
            features={},
        )
        components = [
            Component(
                id="recurring",
                name="Recurring",
                category="General",
                base_cost=100.0,
                spend_year=2023,
                recurring=True,
                interval_years=2,
                include=True,
                row_index=2,
            )
        ]
        schedule = expand_schedule(components, inputs)
        years = [item.year for item in schedule]
        self.assertEqual(years, [2025, 2027])

    def test_schedule_interval_one(self) -> None:
        inputs = Inputs(
            starting_year=2025,
            forecast_years=3,
            beginning_reserve_balance=0.0,
            inflation_rate=0.0,
            investment_return_rate=0.0,
            features={},
        )
        components = [
            Component(
                id="annual",
                name="Annual",
                category="General",
                base_cost=10.0,
                spend_year=2025,
                recurring=True,
                interval_years=1,
                include=True,
                row_index=2,
            )
        ]
        schedule = expand_schedule(components, inputs)
        years = [item.year for item in schedule]
        self.assertEqual(years, [2025, 2026, 2027])

    def test_forecast_negative_contributions(self) -> None:
        inputs = Inputs(
            starting_year=2025,
            forecast_years=2,
            beginning_reserve_balance=1000.0,
            inflation_rate=0.0,
            investment_return_rate=0.05,
            features={},
        )
        components = []
        schedule_items = expand_schedule(components, inputs)
        expenses = expenses_by_year(schedule_items)
        contributions = {2025: -100.0, 2026: -100.0}
        rows = compute_forecast(inputs, contributions, expenses)
        self.assertAlmostEqual(rows[0].end_balance, 950.0, places=2)
        self.assertAlmostEqual(rows[1].end_balance, 897.5, places=2)


class CliTests(unittest.TestCase):
    def test_validate_cli_with_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "data"
            data_dir.mkdir()
            write_csv(
                data_dir / "contributions" / "scenario.csv",
                ["year", "contribution"],
                [[2025, 0]],
            )

            alt_dir = root / "alt"
            alt_dir.mkdir()
            inputs_path = alt_dir / "inputs.yaml"
            components_path = alt_dir / "components.csv"
            write_inputs(inputs_path, forecast_years=1, starting_year=2025)
            write_csv(
                components_path,
                [
                    "id",
                    "name",
                    "category",
                    "base_cost",
                    "spend_year",
                    "recurring",
                    "interval_years",
                    "include",
                ],
                [["roof", "Roof", "General", 1000, 2025, "N", "", "Y"]],
            )

            out = io.StringIO()
            err = io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                exit_code = cli_main(
                    [
                        "validate",
                        "--scenario",
                        "scenario",
                        "--data-dir",
                        str(data_dir),
                        "--inputs",
                        str(inputs_path),
                        "--components",
                        str(components_path),
                    ]
                )
            self.assertEqual(exit_code, 0)

    def test_validate_cli_invalid_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            inputs_path = data_dir / "inputs.yaml"
            inputs_path.write_text(
                "beginning_reserve_balance: 0\n"
                "inflation_rate: 0\n"
                "investment_return_rate: 0\n"
                "FEATURES:\n"
                "  forecast_years: 1\n"
            )
            out = io.StringIO()
            err = io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                exit_code = cli_main(
                    [
                        "validate",
                        "--scenario",
                        "scenario",
                        "--data-dir",
                        str(data_dir),
                        "--inputs",
                        str(inputs_path),
                    ]
                )
            self.assertEqual(exit_code, 1)
            self.assertIn("Missing required input: starting_year", err.getvalue())

    def test_fixture_check_missing_expected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            (data_dir / "contributions").mkdir(parents=True, exist_ok=True)
            out = io.StringIO()
            err = io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                exit_code = cli_main(
                    ["fixture-check", "--data-dir", str(data_dir)]
                )
            self.assertEqual(exit_code, 1)
            self.assertIn("Missing", err.getvalue())

    def test_fixture_check_all(self) -> None:
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            exit_code = cli_main(["fixture-check", "--all", "--clean"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Fixture summary", out.getvalue())


if __name__ == "__main__":
    unittest.main()
