from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .build import build_workbook
from .constants import DIST_DIR
from .fixture_check import find_fixtures, load_fixture, run_fixture
from .validate import ValidationError, validate_scenario


def _print_validation(result) -> None:
    for warning in result.warnings:
        sys.stderr.write(f"WARNING: {warning}\n")
    for error in result.errors:
        sys.stderr.write(f"ERROR: {error}\n")


def _clean_dist() -> int:
    if not DIST_DIR.exists():
        return 0
    removed = 0
    for path in DIST_DIR.glob("*.xlsx"):
        path.unlink()
        removed += 1
    return removed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="reserve")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build the workbook")
    build_parser.add_argument("--scenario", required=True)
    build_parser.add_argument("--open", action="store_true")
    build_parser.add_argument("--data-dir")
    build_parser.add_argument(
        "--inputs",
        help="Path to inputs.yaml (overrides --data-dir)",
    )
    build_parser.add_argument(
        "--components",
        help="Path to components.csv (overrides --data-dir)",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate inputs")
    validate_parser.add_argument("--scenario", required=True)
    validate_parser.add_argument("--data-dir")
    validate_parser.add_argument(
        "--inputs",
        help="Path to inputs.yaml (overrides --data-dir)",
    )
    validate_parser.add_argument(
        "--components",
        help="Path to components.csv (overrides --data-dir)",
    )

    fixture_parser = subparsers.add_parser(
        "fixture-check", help="Verify fixture workbooks"
    )
    fixture_parser.add_argument("--scenario")
    fixture_parser.add_argument("--data-dir")
    fixture_parser.add_argument("--all", action="store_true")
    fixture_parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove generated fixture workbooks",
    )

    subparsers.add_parser("clean", help="Remove generated workbooks")

    args = parser.parse_args(argv)

    if args.command == "build":
        try:
            data_dir = Path(args.data_dir) if args.data_dir else None
            inputs_path = Path(args.inputs) if args.inputs else None
            components_path = Path(args.components) if args.components else None
            output_path, result = build_workbook(
                args.scenario,
                open_file=args.open,
                data_dir=data_dir,
                inputs_path=inputs_path,
                components_path=components_path,
            )
        except ValidationError as exc:
            _print_validation(exc.result)
            return 1
        _print_validation(result)
        sys.stdout.write(f"Wrote {output_path}\n")
        return 0

    if args.command == "validate":
        try:
            data_dir = Path(args.data_dir) if args.data_dir else None
            inputs_path = Path(args.inputs) if args.inputs else None
            components_path = Path(args.components) if args.components else None
            result, _, _, _ = validate_scenario(
                args.scenario,
                data_dir=data_dir,
                inputs_path=inputs_path,
                components_path=components_path,
            )
        except ValidationError as exc:
            _print_validation(exc.result)
            return 1
        _print_validation(result)
        return 1 if result.errors else 0

    if args.command == "clean":
        removed = _clean_dist()
        sys.stdout.write(f"Removed {removed} workbook(s).\n")
        return 0

    if args.command == "fixture-check":
        if args.all:
            fixtures = find_fixtures()
        else:
            if args.data_dir:
                data_dir = Path(args.data_dir)
                expected_path = data_dir / "expected_values.yaml"
                if not expected_path.exists():
                    sys.stderr.write(
                        f"ERROR: Missing {expected_path}\n"
                    )
                    return 1
                fixture = load_fixture(expected_path)
                if args.scenario and args.scenario != fixture.scenario:
                    sys.stderr.write(
                        f"ERROR: Scenario mismatch. expected {fixture.scenario}\n"
                    )
                    return 1
                fixtures = [fixture]
            else:
                if not args.scenario:
                    sys.stderr.write(
                        "ERROR: Provide --scenario or --all.\n"
                    )
                    return 1
                fixtures = [
                    fixture
                    for fixture in find_fixtures()
                    if fixture.scenario == args.scenario
                ]
                if not fixtures:
                    sys.stderr.write(
                        f"ERROR: No fixture found for scenario {args.scenario}\n"
                    )
                    return 1
                if len(fixtures) > 1:
                    sys.stderr.write(
                        f"ERROR: Multiple fixtures found for scenario {args.scenario}\n"
                    )
                    return 1

        failed_count = 0
        generated: list[Path] = []
        for fixture in fixtures:
            result = run_fixture(fixture)
            if result.output_path:
                generated.append(result.output_path)
            if result.issues:
                failed_count += 1
                sys.stderr.write(
                    f"FAIL fixture {fixture.name} ({fixture.scenario})\n"
                )
                for issue in result.issues:
                    sys.stderr.write(f" - {issue}\n")
            else:
                sys.stdout.write(
                    f"OK fixture {fixture.name} ({fixture.scenario})\n"
                )
                if result.warnings:
                    sys.stderr.write(
                        f"WARN fixture {fixture.name} ({fixture.scenario})\n"
                    )
                    for warning in result.warnings:
                        sys.stderr.write(f" - {warning}\n")
        total = len(fixtures)
        passed_count = total - failed_count
        sys.stdout.write(
            f"Fixture summary: {passed_count} passed, {failed_count} failed, {total} total.\n"
        )

        if args.clean and generated:
            removed = 0
            for path in sorted(set(generated)):
                if path.exists():
                    path.unlink()
                    removed += 1
            sys.stdout.write(f"Removed {removed} fixture workbook(s).\n")

        return 1 if failed_count else 0

    return 1
