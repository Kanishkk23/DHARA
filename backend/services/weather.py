from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherDataError(Exception):
    """Raised when live weather data cannot be retrieved or processed."""


def fetch_live_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch live/current weather and recent hourly precipitation
    for a geographic location.

    Data source:
    Open-Meteo Forecast API.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "showers,"
            "weather_code"
        ),
        "hourly": (
            "precipitation,"
            "rain,"
            "showers"
        ),
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "auto",
    }

    url = f"{OPEN_METEO_URL}?{urlencode(params)}"

    request = Request(
        url,
        headers={
            "User-Agent": "FloodFlash/0.1",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            if response.status != 200:
                raise WeatherDataError(
                    f"Weather provider returned HTTP {response.status}."
                )

            payload = json.loads(response.read().decode("utf-8"))

    except Exception as exc:
        raise WeatherDataError(
            f"Unable to retrieve live weather data: {exc}"
        ) from exc

    try:
        current = payload["current"]
        hourly = payload["hourly"]

        hourly_times = hourly["time"]
        hourly_precipitation = hourly["precipitation"]

        valid_precipitation = [
            float(value)
            for value in hourly_precipitation
            if value is not None
        ]

        rainfall_24h_mm = round(
            sum(valid_precipitation[-24:]),
            2,
        )

        return {
            "latitude": float(payload["latitude"]),
            "longitude": float(payload["longitude"]),
            "temperature_c": float(
                current["temperature_2m"]
            ),
            "humidity_percent": float(
                current["relative_humidity_2m"]
            ),
            "precipitation_mm": float(
                current["precipitation"]
            ),
            "rain_mm": float(
                current["rain"]
            ),
            "showers_mm": float(
                current["showers"]
            ),
            "weather_code": int(
                current["weather_code"]
            ),
            "rainfall_24h_mm": rainfall_24h_mm,
            "observation_time": current["time"],
            "source": "Open-Meteo",
            "fetched_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "hourly_points_available": len(
                hourly_times
            ),
        }

    except (KeyError, TypeError, ValueError, IndexError) as exc:
        raise WeatherDataError(
            f"Invalid weather provider response: {exc}"
        ) from exc