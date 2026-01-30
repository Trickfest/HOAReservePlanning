from __future__ import annotations

import platform
import subprocess
from pathlib import Path

from . import excel
from .constants import DIST_DIR
from .schedule import expand_schedule
from .validate import ValidationError, ValidationResult, validate_scenario


def build_workbook(
    scenario: str,
    open_file: bool = False,
    data_dir: Path | None = None,
    inputs_path: Path | None = None,
    components_path: Path | None = None,
) -> tuple[Path, ValidationResult]:
    result, inputs, components, contributions = validate_scenario(
        scenario,
        data_dir=data_dir,
        inputs_path=inputs_path,
        components_path=components_path,
    )
    if result.errors:
        raise ValidationError(result)

    if inputs.features.get("enable_schedule_expansion", True):
        schedule_items = expand_schedule(components, inputs)
    else:
        schedule_items = []

    workbook = excel.build_workbook(
        inputs=inputs,
        components=components,
        schedule_items=schedule_items,
        contributions=contributions,
        scenario=scenario,
    )

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DIST_DIR / f"HOA_Reserve_Planning_{scenario}.xlsx"
    workbook.save(output_path)

    if open_file and platform.system() == "Darwin":
        subprocess.run(["open", str(output_path)], check=False)

    return output_path, result
