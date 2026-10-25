from datetime import datetime, timezone
from typing import Optional


class RiverDataError(Exception):
    """Raised when river-level data cannot be retrieved or validated."""


def get_river_observation(
    station_name: str,
    river_name: str,
    latitude: float,
    longitude: float,
    water_level_m: Optional[float] = None,
    previous_level_m: Optional[float] = None,
) -> dict:
    """
    Normalize a river observation for FloodFlash.

    The function is intentionally separated from the API route so that
    an official CWC/India-WRIS machine-readable data source can be
    connected without changing the rest of the application.

    water_level_m and previous_level_m are optional during development.
    They will be populated by the real hydrological data connector.
    """

    if not station_name.strip():
        raise RiverDataError("River station name is required.")

    if not river_name.strip():
        raise RiverDataError("River name is required.")

    if not -90 <= latitude <= 90:
        raise RiverDataError("Invalid station latitude.")

    if not -180 <= longitude <= 180:
        raise RiverDataError("Invalid station longitude.")

    if water_level_m is not None and water_level_m < 0:
        raise RiverDataError("Water level cannot be negative.")

    if previous_level_m is not None and previous_level_m < 0:
        raise RiverDataError("Previous water level cannot be negative.")

    level_change_m = None

    if (
        water_level_m is not None
        and previous_level_m is not None
    ):
        level_change_m = round(
            water_level_m - previous_level_m,
            3,
        )

    return {
        "station_name": station_name,
        "river_name": river_name,
        "latitude": latitude,
        "longitude": longitude,
        "water_level_m": water_level_m,
        "previous_level_m": previous_level_m,
        "level_change_m": level_change_m,
        "data_status": (
            "OBSERVED"
            if water_level_m is not None
            else "AWAITING_LIVE_FEED"
        ),
        "source": "CWC / India-WRIS",
        "observed_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }