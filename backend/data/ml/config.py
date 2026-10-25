from pathlib import Path


# ---------------------------------------------------------
# FloodFlash ML paths
# ---------------------------------------------------------

ML_DIR = Path(__file__).resolve().parent

DATA_DIR = ML_DIR.parent / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODEL_DIR = ML_DIR / "models"


# ---------------------------------------------------------
# Dataset configuration
# ---------------------------------------------------------

TARGET_COLUMN = "flood_observed"

FEATURE_COLUMNS = (
    "rainfall_24h_mm",
    "rainfall_72h_mm",
    "temperature_c",
    "humidity_percent",
    "river_level_m",
    "river_level_change_m",
)


# ---------------------------------------------------------
# Training configuration
# ---------------------------------------------------------

TEST_SIZE = 0.20

RANDOM_STATE = 42

MINIMUM_TRAINING_ROWS = 100


# ---------------------------------------------------------
# Supported official data sources
# ---------------------------------------------------------

CWC_RIVER_SOURCE = (
    "National Water Data Portal - "
    "CWC River Water Level Telemetry"
)

CWC_RAINFALL_SOURCE = (
    "National Water Data Portal - "
    "CWC Rainfall Telemetry"
)

IMD_RAINFALL_SOURCE = (
    "Open Government Data Platform - "
    "India Meteorological Department"
)


def create_ml_directories() -> None:
    """
    Create the directories required by the ML pipeline.
    """

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )