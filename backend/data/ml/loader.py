from pathlib import Path
import csv

from dataset import FloodTrainingRecord, validate_training_record


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_training_csv(
    file_path: str | Path,
) -> list[FloodTrainingRecord]:
    """
    Load FloodFlash historical training records from CSV.

    The CSV must contain the following columns:

        timestamp
        location_id
        latitude
        longitude
        rainfall_24h_mm
        rainfall_72h_mm
        temperature_c
        humidity_percent
        river_level_m
        river_level_change_m
        flood_observed

    No prediction is performed here.
    This module only loads and validates historical observations.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {path}"
        )

    records: list[FloodTrainingRecord] = []

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError(
                "Training CSV does not contain a header."
            )

        required_columns = {
            "timestamp",
            "location_id",
            "latitude",
            "longitude",
            "rainfall_24h_mm",
            "rainfall_72h_mm",
            "temperature_c",
            "humidity_percent",
            "river_level_m",
            "river_level_change_m",
            "flood_observed",
        }

        missing_columns = (
            required_columns
            - set(reader.fieldnames)
        )

        if missing_columns:
            raise ValueError(
                "Training CSV is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        for row_number, row in enumerate(
            reader,
            start=2,
        ):
            try:
                river_level = _optional_float(
                    row["river_level_m"]
                )

                river_change = _optional_float(
                    row["river_level_change_m"]
                )

                record = FloodTrainingRecord(
                    timestamp=row["timestamp"].strip(),
                    location_id=row["location_id"].strip(),
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    rainfall_24h_mm=float(
                        row["rainfall_24h_mm"]
                    ),
                    rainfall_72h_mm=float(
                        row["rainfall_72h_mm"]
                    ),
                    temperature_c=float(
                        row["temperature_c"]
                    ),
                    humidity_percent=float(
                        row["humidity_percent"]
                    ),
                    river_level_m=river_level,
                    river_level_change_m=river_change,
                    flood_observed=int(
                        row["flood_observed"]
                    ),
                )

                validate_training_record(record)

                records.append(record)

            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid training record on CSV "
                    f"row {row_number}: {exc}"
                ) from exc

    if not records:
        raise ValueError(
            "Training dataset contains no records."
        )

    return records


def _optional_float(
    value: str | None,
) -> float | None:
    """
    Convert an optional CSV value to float.

    Empty values are treated as missing observations.
    """

    if value is None:
        return None

    cleaned = value.strip()

    if cleaned == "":
        return None

    return float(cleaned)