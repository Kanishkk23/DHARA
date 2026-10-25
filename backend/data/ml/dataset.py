from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FloodTrainingRecord:
    """
    One historical observation used for ML training.

    The record represents environmental conditions at a location
    and the corresponding observed flood outcome.
    """

    timestamp: str

    location_id: str

    latitude: float
    longitude: float

    rainfall_24h_mm: float
    rainfall_72h_mm: float

    temperature_c: float
    humidity_percent: float

    river_level_m: Optional[float]
    river_level_change_m: Optional[float]

    flood_observed: int


REQUIRED_FEATURES = (
    "rainfall_24h_mm",
    "rainfall_72h_mm",
    "temperature_c",
    "humidity_percent",
    "river_level_m",
    "river_level_change_m",
)


TARGET_COLUMN = "flood_observed"


def validate_training_record(
    record: FloodTrainingRecord,
) -> None:
    """
    Validate one historical ML training record.
    """

    if not record.timestamp:
        raise ValueError("timestamp is required.")

    if not record.location_id:
        raise ValueError("location_id is required.")

    if not -90 <= record.latitude <= 90:
        raise ValueError("Invalid latitude.")

    if not -180 <= record.longitude <= 180:
        raise ValueError("Invalid longitude.")

    if record.rainfall_24h_mm < 0:
        raise ValueError(
            "rainfall_24h_mm cannot be negative."
        )

    if record.rainfall_72h_mm < 0:
        raise ValueError(
            "rainfall_72h_mm cannot be negative."
        )

    if not 0 <= record.humidity_percent <= 100:
        raise ValueError(
            "humidity_percent must be between 0 and 100."
        )

    if record.river_level_m is not None:
        if record.river_level_m < 0:
            raise ValueError(
                "river_level_m cannot be negative."
            )

    if record.flood_observed not in (0, 1):
        raise ValueError(
            "flood_observed must be either 0 or 1."
        )


def record_to_features(
    record: FloodTrainingRecord,
) -> dict[str, float]:
    """
    Convert a validated training record into ML features.

    Missing river observations are represented as 0 for the initial
    feature matrix. The final pipeline may use a more sophisticated
    missing-value strategy once real station coverage is established.
    """

    validate_training_record(record)

    return {
        "rainfall_24h_mm": record.rainfall_24h_mm,
        "rainfall_72h_mm": record.rainfall_72h_mm,
        "temperature_c": record.temperature_c,
        "humidity_percent": record.humidity_percent,
        "river_level_m": (
            record.river_level_m
            if record.river_level_m is not None
            else 0.0
        ),
        "river_level_change_m": (
            record.river_level_change_m
            if record.river_level_change_m is not None
            else 0.0
        ),
    }