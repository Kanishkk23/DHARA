from typing import Any


def build_flood_features(
    weather: dict[str, Any],
    river: dict[str, Any] | None = None,
) -> dict[str, float | int | None]:
    """
    Convert raw environmental observations into model-ready features.

    This layer intentionally contains no prediction logic.
    Its job is to transform real observations into consistent
    numerical inputs for the FloodFlash ML model.
    """

    rainfall_24h = float(
        weather.get("rainfall_24h_mm", 0.0)
    )

    precipitation_now = float(
        weather.get("precipitation_mm", 0.0)
    )

    rain_now = float(
        weather.get("rain_mm", 0.0)
    )

    showers_now = float(
        weather.get("showers_mm", 0.0)
    )

    temperature = float(
        weather.get("temperature_c", 0.0)
    )

    humidity = float(
        weather.get("humidity_percent", 0.0)
    )

    river_level = None
    river_level_change = None

    if river is not None:
        raw_level = river.get("water_level_m")
        raw_change = river.get("level_change_m")

        if raw_level is not None:
            river_level = float(raw_level)

        if raw_change is not None:
            river_level_change = float(raw_change)

    features = {
        "rainfall_24h_mm": rainfall_24h,
        "precipitation_now_mm": precipitation_now,
        "rain_now_mm": rain_now,
        "showers_now_mm": showers_now,
        "temperature_c": temperature,
        "humidity_percent": humidity,
        "river_level_m": river_level,
        "river_level_change_m": river_level_change,
    }

    return features