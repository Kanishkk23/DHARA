import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# ============================================================
# FLOODFLASH REAL RIVER DATA CONNECTOR
# ============================================================
#
# Primary source:
# National Water Data Portal / Assam river telemetry
#
# Secondary source:
# CWC / National Water Data Portal
#
# The connector is deliberately separated from the ML model.
# This allows us to change the data provider without changing
# predict.py.
# ============================================================


# ------------------------------------------------------------
# Known Assam monitoring stations
# ------------------------------------------------------------

STATIONS = {
    "guwahati": {
        "name": "Guwahati DC Court",
        "river": "Brahmaputra",
        "district": "Kamrup",
        "latitude": 26.194722,
        "longitude": 91.743056,
        "danger_level_m": 49.68,
        "warning_level_m": 48.68,
        "hfl_m": 51.46,
    },

    "dibrugarh": {
        "name": "Dibrugarh",
        "river": "Brahmaputra",
        "district": "Dibrugarh",
        "latitude": 27.4728,
        "longitude": 94.9120,
        "danger_level_m": 105.70,
        "warning_level_m": 104.70,
        "hfl_m": 106.48,
    },

    "jorhat": {
        "name": "Neamatighat",
        "river": "Brahmaputra",
        "district": "Jorhat",
        "latitude": 26.7509,
        "longitude": 94.2037,
        "danger_level_m": 85.04,
        "warning_level_m": 84.04,
        "hfl_m": 87.37,
    },

    "tezpur": {
        "name": "Tezpur",
        "river": "Brahmaputra",
        "district": "Sonitpur",
        "latitude": 26.6528,
        "longitude": 92.7926,
        "danger_level_m": 65.23,
        "warning_level_m": 64.23,
        "hfl_m": 66.59,
    },

    "silchar": {
        "name": "Silchar",
        "river": "Barak",
        "district": "Cachar",
        "latitude": 24.8333,
        "longitude": 92.7789,
        "danger_level_m": None,
        "warning_level_m": None,
        "hfl_m": None,
    },
}


# ============================================================
# ENVIRONMENT VARIABLE SUPPORT
# ============================================================

# If later we obtain the exact NWDP API endpoint, put it in:
#
# MAC/Linux:
# export NWDP_RIVER_API_URL="..."
#
# Windows:
# set NWDP_RIVER_API_URL="..."
#
# The code will automatically use it.

NWDP_RIVER_API_URL = os.getenv(
    "NWDP_RIVER_API_URL"
)


# ============================================================
# HTTP HELPER
# ============================================================

def fetch_json(url, timeout=10):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
                "FloodFlash/2.0"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=timeout
    ) as response:

        return json.loads(
            response.read().decode(
                "utf-8"
            )
        )


# ============================================================
# NORMALIZE NUMBER
# ============================================================

def number(value):

    try:

        if value is None:
            return None

        return float(value)

    except Exception:

        return None


# ============================================================
# PARSE POSSIBLE API RECORD
# ============================================================

def extract_records(data):

    if isinstance(data, list):
        return data

    if not isinstance(data, dict):
        return []

    possible_keys = [
        "data",
        "records",
        "results",
        "items",
        "observations",
        "features"
    ]

    for key in possible_keys:

        value = data.get(key)

        if isinstance(value, list):
            return value

    return []


# ============================================================
# FIND WATER LEVEL FIELD
# ============================================================

def extract_water_level(record):

    if not isinstance(record, dict):
        return None

    possible_fields = [
        "water_level",
        "water_level_m",
        "river_level",
        "river_level_m",
        "level",
        "rwl",
        "RWL",
        "waterLevel",
        "Water Level",
        "Water_Level"
    ]

    for field in possible_fields:

        if field in record:

            value = number(
                record[field]
            )

            if value is not None:
                return value

    return None


# ============================================================
# FIND TIMESTAMP
# ============================================================

def extract_timestamp(record):

    if not isinstance(record, dict):
        return None

    possible_fields = [
        "timestamp",
        "datetime",
        "date_time",
        "date",
        "time",
        "Date",
        "DateTime"
    ]

    for field in possible_fields:

        if field in record:

            value = record[field]

            if value:
                return str(value)

    return None


# ============================================================
# LIVE API INGESTION
# ============================================================

def get_api_observations(
    location_id,
    hours=25
):

    if not NWDP_RIVER_API_URL:

        return []

    station = STATIONS.get(
        location_id
    )

    if station is None:

        return []

    try:

        params = {
            "station":
                station["name"],

            "location":
                station["name"],

            "river":
                station["river"],

            "district":
                station["district"],

            "hours":
                hours
        }

        separator = (
            "&"
            if "?" in NWDP_RIVER_API_URL
            else "?"
        )

        url = (
            NWDP_RIVER_API_URL
            + separator
            + urllib.parse.urlencode(
                params
            )
        )

        data = fetch_json(
            url
        )

        records = extract_records(
            data
        )

        observations = []

        for record in records:

            level = extract_water_level(
                record
            )

            timestamp = extract_timestamp(
                record
            )

            if level is None:
                continue

            observations.append({
                "timestamp":
                    timestamp
                    or datetime.now().isoformat(),

                "water_level_m":
                    level
            })

        observations.sort(
            key=lambda x:
            x["timestamp"]
        )

        return observations

    except Exception as e:

        print(
            "NWDP river API error:",
            e
        )

        return []


# ============================================================
# BUILD MODEL FEATURES
# ============================================================

def build_features(
    observations
):

    if not observations:

        return None

    levels = [
        number(
            item["water_level_m"]
        )
        for item in observations
    ]

    levels = [
        x for x in levels
        if x is not None
    ]

    if not levels:

        return None

    current = levels[-1]

    # --------------------------------------------------------
    # Calculate changes
    # --------------------------------------------------------

    def delta(hours):

        if len(levels) <= hours:
            return (
                levels[-1]
                - levels[0]
            )

        return (
            levels[-1]
            - levels[-1 - hours]
        )

    delta_3 = delta(3)
    delta_6 = delta(6)
    delta_24 = delta(24)

    # --------------------------------------------------------
    # Rolling means
    # --------------------------------------------------------

    def mean(hours):

        values = levels[-hours:]

        if not values:
            return current

        return sum(values) / len(values)

    mean_3 = mean(3)
    mean_6 = mean(6)
    mean_24 = mean(24)

    # --------------------------------------------------------
    # Standard deviation
    # --------------------------------------------------------

    def std(values):

        if len(values) <= 1:
            return 0.0

        avg = sum(values) / len(values)

        variance = sum(
            (x - avg) ** 2
            for x in values
        ) / len(values)

        return variance ** 0.5

    std_3 = std(
        levels[-3:]
    )

    std_6 = std(
        levels[-6:]
    )

    std_24 = std(
        levels[-24:]
    )

    # --------------------------------------------------------
    # Hourly rate/change
    # --------------------------------------------------------

    changes = []

    for i in range(
        1,
        len(levels)
    ):

        changes.append(
            levels[i]
            - levels[i - 1]
        )

    def change_mean(hours):

        values = changes[-hours:]

        if not values:
            return 0.0

        return sum(values) / len(values)

    change_3 = change_mean(3)
    change_6 = change_mean(6)
    change_24 = change_mean(24)

    now = datetime.now()

    return {

        "river_level_m":
            current,

        "river_level_change_m":
            changes[-1]
            if changes
            else 0.0,

        "level_mean_3h":
            mean_3,

        "level_mean_6h":
            mean_6,

        "level_mean_24h":
            mean_24,

        "level_std_3h":
            std_3,

        "level_std_6h":
            std_6,

        "level_std_24h":
            std_24,

        "level_delta_3h":
            delta_3,

        "level_delta_6h":
            delta_6,

        "level_delta_24h":
            delta_24,

        "change_mean_3h":
            change_3,

        "change_mean_6h":
            change_6,

        "change_mean_24h":
            change_24,

        "hour":
            now.hour,

        "day_of_week":
            now.weekday(),

        "month":
            now.month
    }


# ============================================================
# MAIN FUNCTION
# ============================================================

def get_real_river_data(
    location_id
):

    station = STATIONS.get(
        location_id
    )

    if station is None:

        raise ValueError(
            f"Unknown river station: "
            f"{location_id}"
        )

    observations = (
        get_api_observations(
            location_id
        )
    )

    # --------------------------------------------------------
    # Only return real river data if we actually received it.
    # --------------------------------------------------------

    if observations:

        features = build_features(
            observations
        )

        if features:

            return {
                "available": True,

                "live": True,

                "source":
                    "National Water Data Portal / Assam telemetry API",

                "station":
                    station,

                "observations":
                    observations,

                "features":
                    features
            }

    # --------------------------------------------------------
    # No API configured yet.
    #
    # IMPORTANT:
    # Do NOT generate fake river readings.
    # --------------------------------------------------------

    return {
        "available": False,

        "live": False,

        "source":
            "No live river API configured",

        "station":
            station,

        "observations": [],

        "features": None,

        "message":
            (
                "Configure NWDP_RIVER_API_URL "
                "with the official river telemetry "
                "API endpoint."
            )
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = get_real_river_data(
        "guwahati"
    )

    print(
        json.dumps(
            result,
            indent=2,
            default=str
        )
    )