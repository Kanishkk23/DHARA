"""
FloodFlash - ML Target Engineering

Creates a future high-water prediction target from real CWC observations.

Target:
    1 = station reaches its historical 95th-percentile river level
        within the next 6 hours
    0 = otherwise

The threshold is calculated separately for every monitoring station.

Input:
    data/processed/cwc_ml_features.csv

Output:
    data/processed/cwc_training_dataset.csv
"""

from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict, deque


FORECAST_HOURS = 6
HIGH_WATER_PERCENTILE = 0.95


def percentile(values: list[float], percentile_value: float) -> float:
    """Calculate a linear-interpolated percentile."""

    if not values:
        raise ValueError("Cannot calculate percentile from empty data.")

    ordered = sorted(values)

    position = (len(ordered) - 1) * percentile_value

    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)

    fraction = position - lower

    return (
        ordered[lower]
        + (ordered[upper] - ordered[lower]) * fraction
    )


def parse_float(value: str) -> float | None:
    try:
        if value is None or value.strip() == "":
            return None

        return float(value)

    except (ValueError, TypeError):
        return None


def read_dataset(
    input_path: str,
) -> tuple[list[dict[str, str]], dict[str, list[float]]]:

    print("\nReading ML feature dataset...")

    rows: list[dict[str, str]] = []

    station_levels: dict[str, list[float]] = defaultdict(list)

    with open(
        input_path,
        "r",
        encoding="utf-8",
        newline="",
    ) as source:

        reader = csv.DictReader(source)

        for row in reader:

            station = row["station"].strip()

            level = parse_float(
                row["river_level_m"]
            )

            if not station or level is None:
                continue

            rows.append(row)

            station_levels[station].append(level)

    return rows, station_levels


def build_targets(
    input_path: str,
    output_path: str,
) -> None:

    print("=" * 70)
    print("FLOODFLASH ML TARGET ENGINEERING")
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

    rows, station_levels = read_dataset(
        input_path
    )

    print(
        f"\nRows loaded: {len(rows):,}"
    )

    print(
        f"Stations found: {len(station_levels)}"
    )

    # ---------------------------------------------------------
    # Calculate station-specific high-water thresholds.
    # ---------------------------------------------------------

    thresholds: dict[str, float] = {}

    for station, levels in station_levels.items():

        thresholds[station] = percentile(
            levels,
            HIGH_WATER_PERCENTILE,
        )

    print("\nStation thresholds:")

    for station in sorted(thresholds):

        print(
            f"  {station}: "
            f"{thresholds[station]:.4f} m"
        )

    # ---------------------------------------------------------
    # Group rows by station.
    # ---------------------------------------------------------

    station_rows: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:

        station = row["station"].strip()

        station_rows[station].append(row)

    # ---------------------------------------------------------
    # Prepare output columns.
    # ---------------------------------------------------------

    original_columns = list(rows[0].keys())

    output_columns = original_columns + [
        "high_water_threshold_m",
        "future_max_level_6h_m",
        "flood_target",
    ]

    total_rows = 0
    positive_rows = 0
    negative_rows = 0
    skipped_rows = 0

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline="",
    ) as destination:

        writer = csv.DictWriter(
            destination,
            fieldnames=output_columns,
        )

        writer.writeheader()

        # -----------------------------------------------------
        # Process each station independently.
        # -----------------------------------------------------

        for station, station_data in station_rows.items():

            threshold = thresholds[station]

            levels = []

            for row in station_data:

                level = parse_float(
                    row["river_level_m"]
                )

                if level is None:
                    levels.append(None)
                else:
                    levels.append(level)

            # Future six-hour maximum.

            future_window = deque(
                maxlen=FORECAST_HOURS
            )

            # Because the CWC data is hourly, the next
            # six observations represent approximately
            # the next six hours.

            for index, row in enumerate(station_data):

                current_level = levels[index]

                if current_level is None:
                    skipped_rows += 1
                    continue

                future_window.clear()

                end_index = min(
                    index + 1 + FORECAST_HOURS,
                    len(levels),
                )

                for future_index in range(
                    index + 1,
                    end_index,
                ):

                    future_level = levels[future_index]

                    if future_level is not None:
                        future_window.append(
                            future_level
                        )

                if not future_window:

                    # There is no future observation available,
                    # so this row cannot be used as a supervised
                    # training example.
                    skipped_rows += 1
                    continue

                future_max_level = max(
                    future_window
                )

                target = int(
                    future_max_level >= threshold
                )

                output_row = dict(row)

                output_row[
                    "high_water_threshold_m"
                ] = f"{threshold:.6f}"

                output_row[
                    "future_max_level_6h_m"
                ] = f"{future_max_level:.6f}"

                output_row[
                    "flood_target"
                ] = str(target)

                writer.writerow(output_row)

                total_rows += 1

                if target == 1:
                    positive_rows += 1
                else:
                    negative_rows += 1

    print("\n" + "=" * 70)
    print("TARGET ENGINEERING COMPLETE")
    print("=" * 70)

    print(
        f"\nTraining rows:       {total_rows:,}"
    )

    print(
        f"High-water events:  {positive_rows:,}"
    )

    print(
        f"Normal events:      {negative_rows:,}"
    )

    print(
        f"Skipped rows:       {skipped_rows:,}"
    )

    if total_rows > 0:

        positive_percentage = (
            positive_rows / total_rows
        ) * 100

        print(
            f"\nPositive target rate: "
            f"{positive_percentage:.2f}%"
        )

    print(
        f"\nForecast horizon: "
        f"{FORECAST_HOURS} hours"
    )

    print(
        f"High-water threshold: "
        f"{HIGH_WATER_PERCENTILE * 100:.0f}th percentile"
    )

    print(
        f"\nTraining dataset:"
        f"\n{output_path}"
    )

    print("\n" + "=" * 70)


def main() -> None:

    if len(sys.argv) != 3:

        print(
            "\nUsage:\n"
            "python data/ml/target_engineering.py "
            "INPUT.csv OUTPUT.csv\n"
        )

        raise SystemExit(1)

    input_path = sys.argv[1]

    output_path = sys.argv[2]

    build_targets(
        input_path,
        output_path,
    )


if __name__ == "__main__":
    main()