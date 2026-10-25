"""
FloodFlash - CWC Feature Engineering

Converts processed CWC river observations into ML-ready features.

Input:
    data/processed/cwc_river_observations.csv

Output:
    data/processed/cwc_ml_features.csv
"""

from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict, deque
from datetime import datetime


WINDOWS = {
    "3h": 3,
    "6h": 6,
    "24h": 24,
}


def parse_float(value: str) -> float | None:
    try:
        if value is None or value.strip() == "":
            return None
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_timestamp(value: str) -> datetime | None:
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue

    return None


def mean(values: deque[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def standard_deviation(values: deque[float]) -> float:
    if len(values) < 2:
        return 0.0

    avg = mean(values)

    variance = sum(
        (value - avg) ** 2
        for value in values
    ) / len(values)

    return variance ** 0.5


def build_features(input_path: str, output_path: str) -> None:
    print("=" * 70)
    print("FLOODFLASH CWC FEATURE ENGINEERING")
    print("=" * 70)

    print(f"\nInput:")
    print(input_path)

    print(f"\nOutput:")
    print(output_path)

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"\nInput dataset not found:\n{input_path}"
        )

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    # History is maintained separately for every station.
    histories = defaultdict(
        lambda: {
            "levels": deque(maxlen=24),
            "changes": deque(maxlen=24),
        }
    )

    rows_read = 0
    rows_written = 0
    skipped_rows = 0

    fieldnames = [
        "station",
        "state",
        "district",
        "river",
        "basin",
        "latitude",
        "longitude",
        "timestamp",

        "river_level_m",
        "river_level_change_m",

        "level_mean_3h",
        "level_mean_6h",
        "level_mean_24h",

        "level_std_3h",
        "level_std_6h",
        "level_std_24h",

        "level_delta_3h",
        "level_delta_6h",
        "level_delta_24h",

        "change_mean_3h",
        "change_mean_6h",
        "change_mean_24h",

        "hour",
        "day_of_week",
        "month",
    ]

    with open(
        input_path,
        "r",
        encoding="utf-8",
        newline="",
    ) as source:

        reader = csv.DictReader(source)

        required_columns = {
            "station",
            "state",
            "district",
            "river",
            "basin",
            "latitude",
            "longitude",
            "timestamp",
            "river_level_m",
            "river_level_change_m",
        }

        missing = required_columns - set(reader.fieldnames or [])

        if missing:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(sorted(missing))
            )

        with open(
            output_path,
            "w",
            encoding="utf-8",
            newline="",
        ) as destination:

            writer = csv.DictWriter(
                destination,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for row in reader:
                rows_read += 1

                station = row["station"].strip()

                timestamp = parse_timestamp(
                    row["timestamp"]
                )

                river_level = parse_float(
                    row["river_level_m"]
                )

                river_change = parse_float(
                    row["river_level_change_m"]
                )

                latitude = parse_float(
                    row["latitude"]
                )

                longitude = parse_float(
                    row["longitude"]
                )

                if (
                    not station
                    or timestamp is None
                    or river_level is None
                    or latitude is None
                    or longitude is None
                ):
                    skipped_rows += 1
                    continue

                if river_change is None:
                    river_change = 0.0

                history = histories[station]

                previous_levels = history["levels"]
                previous_changes = history["changes"]

                current_level = river_level

                # Calculate rolling statistics including
                # the current observation.
                level_values_3h = deque(
                    list(previous_levels)[-2:]
                    + [current_level]
                )

                level_values_6h = deque(
                    list(previous_levels)[-5:]
                    + [current_level]
                )

                level_values_24h = deque(
                    list(previous_levels)[-23:]
                    + [current_level]
                )

                change_values_3h = deque(
                    list(previous_changes)[-2:]
                    + [river_change]
                )

                change_values_6h = deque(
                    list(previous_changes)[-5:]
                    + [river_change]
                )

                change_values_24h = deque(
                    list(previous_changes)[-23:]
                    + [river_change]
                )

                level_delta_3h = (
                    current_level
                    - level_values_3h[0]
                    if len(level_values_3h) > 1
                    else 0.0
                )

                level_delta_6h = (
                    current_level
                    - level_values_6h[0]
                    if len(level_values_6h) > 1
                    else 0.0
                )

                level_delta_24h = (
                    current_level
                    - level_values_24h[0]
                    if len(level_values_24h) > 1
                    else 0.0
                )

                output_row = {
                    "station": station,
                    "state": row["state"].strip(),
                    "district": row["district"].strip(),
                    "river": row["river"].strip(),
                    "basin": row["basin"].strip(),

                    "latitude": f"{latitude:.8f}",
                    "longitude": f"{longitude:.8f}",

                    "timestamp": timestamp.isoformat(),

                    "river_level_m": f"{current_level:.6f}",
                    "river_level_change_m": f"{river_change:.6f}",

                    "level_mean_3h": f"{mean(level_values_3h):.6f}",
                    "level_mean_6h": f"{mean(level_values_6h):.6f}",
                    "level_mean_24h": f"{mean(level_values_24h):.6f}",

                    "level_std_3h": f"{standard_deviation(level_values_3h):.6f}",
                    "level_std_6h": f"{standard_deviation(level_values_6h):.6f}",
                    "level_std_24h": f"{standard_deviation(level_values_24h):.6f}",

                    "level_delta_3h": f"{level_delta_3h:.6f}",
                    "level_delta_6h": f"{level_delta_6h:.6f}",
                    "level_delta_24h": f"{level_delta_24h:.6f}",

                    "change_mean_3h": f"{mean(change_values_3h):.6f}",
                    "change_mean_6h": f"{mean(change_values_6h):.6f}",
                    "change_mean_24h": f"{mean(change_values_24h):.6f}",

                    "hour": timestamp.hour,
                    "day_of_week": timestamp.weekday(),
                    "month": timestamp.month,
                }

                writer.writerow(output_row)

                rows_written += 1

                # Add current observation to station history.
                history["levels"].append(current_level)
                history["changes"].append(river_change)

                if rows_read % 100_000 == 0:
                    print(
                        f"Processed {rows_read:,} rows..."
                    )

    print("\n" + "=" * 70)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 70)

    print(f"\nRows read:      {rows_read:,}")
    print(f"Rows written:   {rows_written:,}")
    print(f"Rows skipped:   {skipped_rows:,}")

    print(
        f"\nStations processed: {len(histories)}"
    )

    print(
        f"\nML feature file:\n{output_path}"
    )

    print("\nFeatures created:")
    print("  • Current river level")
    print("  • River-level change")
    print("  • 3-hour rolling statistics")
    print("  • 6-hour rolling statistics")
    print("  • 24-hour rolling statistics")
    print("  • Level change over 3/6/24 hours")
    print("  • Temporal features")

    print("\n" + "=" * 70)


def main() -> None:
    if len(sys.argv) != 3:
        print(
            "\nUsage:\n"
            "python data/ml/feature_engineering.py "
            "INPUT.csv OUTPUT.csv\n"
        )
        raise SystemExit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    build_features(
        input_path,
        output_path,
    )


if __name__ == "__main__":
    main()