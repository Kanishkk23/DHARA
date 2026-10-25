from pathlib import Path
import csv
import sys


def inspect_csv(file_path: str) -> None:
    """
    Inspect an official CSV dataset before it enters
    the FloodFlash processing pipeline.

    This does NOT modify the dataset.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    print("\n" + "=" * 70)
    print("FLOODFLASH DATASET INSPECTOR")
    print("=" * 70)

    print(f"\nFile:")
    print(path)

    print(f"\nSize:")
    print(f"{path.stat().st_size / 1024 / 1024:.2f} MB")

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:

        reader = csv.reader(csv_file)

        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError(
                "The CSV file is empty."
            )

        print("\nColumns:")
        for index, column in enumerate(headers, start=1):
            print(f"  {index}. {column}")

        print("\nFirst 5 records:")
        print("-" * 70)

        for row_number, row in enumerate(
            reader,
            start=1,
        ):
            print(row)

            if row_number >= 5:
                break

    print("\n" + "=" * 70)
    print("Inspection complete.")
    print("=" * 70)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "\nUsage:"
        )

        print(
            "python inspect_data.py "
            "path/to/file.csv\n"
        )

        raise SystemExit(1)

    inspect_csv(sys.argv[1])