from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
INPUTS_FILE = DATA_DIR / "inputs.yaml"
COMPONENTS_FILE = DATA_DIR / "components.csv"
CONTRIBUTIONS_DIR = DATA_DIR / "contributions"
DIST_DIR = ROOT_DIR / "dist"

DEFAULT_FEATURES = {
    "forecast_years": 40,
    "enable_checks": True,
    "enable_dashboard": True,
    "enable_schedule_expansion": True,
    "max_components_rows": 500,
    "max_schedule_rows": 10000,
}
