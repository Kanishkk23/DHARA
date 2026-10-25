from pathlib import Path
import csv
import sys
from datetime import datetime


REQUIRED_COLUMNS = {
    "Station",
    "State",
    "District",
    "River",
    "Basin",
    "Latitude",
    "Longitude",
    "Data Acquisition Time",
    "River Water Level Telemetry Hourly (meter)",
}


def clean_value(value: str | None) -> str:
    if value is None:
        return ""

    return value.strip()


def parse_float(value: str | None) -> float | None:
    value = clean_value(value)

    if value in {"", "-", "--", "NA", "N/A", "null", "None"}:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def parse_timestamp(value: str | None) -> str | None:
    value = clean_value(value)

    if not value:
        return None

    formats = (
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
    )

    for fmt in formats:
        try:
            parsed = datetime.strptime(value, fmt)

            return parsed.isoformat()

        except ValueError:
            continue

    return None


def process_cwc_file(
    input_file: str | Path,
    output_file: str | Path,
) -> None:

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        raise FileNotFoundError(
            f"CWC file not found: {input_path}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 70)
    print("FLOODFLASH CWC PROCESSOR")
    print("=" * 70)

    print(f"\nInput:")
    print(input_path)

    print(f"\nOutput:")
    print(output_path)

    previous_levels: dict[str, float] = {}

    total_rows = 0
    valid_rows = 0
    skipped_rows = 0

    output_columns = [
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
    ]

    with input_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as source:

        reader = csv.DictReader(source)

        if reader.fieldnames is None:
            raise ValueError(
                "The CWC CSV does not contain column headers."
            )

        missing_columns = (
            REQUIRED_COLUMNS
            - set(reader.fieldnames)
        )

        if missing_columns:
            raise ValueError(
                "The CWC CSV is missing required columns:\n"
                + "\n".join(
                    f"- {column}"
                    for column in sorted(missing_columns)
                )
            )

        with output_path.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as destination:

            writer = csv.DictWriter(
                destination,
                fieldnames=output_columns,
            )

            writer.writeheader()

            for row in reader:

                total_rows += 1

                station = clean_value(
                    row.get("Station")
                )

                timestamp = parse_timestamp(
                    row.get("Data Acquisition Time")
                )

                latitude = parse_float(
                    row.get("Latitude")
                )

                longitude = parse_float(
                    row.get("Longitude")
                )

                river_level = parse_float(
                    row.get(
                        "River Water Level Telemetry Hourly (meter)"
                    )
                )

                if (
                    not station
                    or timestamp is None
                    or latitude is None
                    or longitude is None
                    or river_level is None
                ):
                    skipped_rows += 1
                    continue

                previous_level = previous_levels.get(
                    station
                )

                if previous_level is None:
                    river_change = None
                else:
                    river_change = (
                        river_level
                        - previous_level
                    )

                previous_levels[station] = river_level

                writer.writerow(
                    {
                        "station": station,
                        "state": clean_value(
                            row.get("State")
                        ),
                        "district": clean_value(
                            row.get("District")
                        ),
                        "river": clean_value(
                            row.get("River")
                        ),
                        "basin": clean_value(
                            row.get("Basin")
                        ),
                        "latitude": latitude,
                        "longitude": longitude,
                        "timestamp": timestamp,
                        "river_level_m": river_level,
                        "river_level_change_m": (
                            ""
                            if river_change is None
                            else river_change
                        ),
                    }
                )

                valid_rows += 1

    print("\nProcessing complete.")

    print(f"\nTotal source rows: {total_rows:,}")

    print(f"Valid rows:        {valid_rows:,}")

    print(f"Skipped rows:      {skipped_rows:,}")

    print(
        f"\nStations detected: {len(previous_levels):,}"
    )

    print(
        f"\nProcessed file:"
        f"\n{output_path}"
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":

    if len(sys.argv) != 3:

        print(
            "\nUsage:"
        )

        print(
            "python data/ml/cwc_processor.py "
            "INPUT.csv OUTPUT.csv"
        )

        raise SystemExit(1)

    process_cwc_file(
        sys.argv[1],
        sys.argv[2],
    )