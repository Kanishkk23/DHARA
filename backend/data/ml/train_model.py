"""
FloodFlash - CWC River Level ML Model Training

Trains a real machine-learning model using processed
Central Water Commission river-level observations.
"""

from pathlib import Path
import csv
import math
import pickle
from collections import defaultdict

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "processed" / "cwc_ml_features.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_FILE = MODEL_DIR / "flood_risk_model.pkl"


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# How far ahead the model predicts.
FORECAST_HOURS = 6

# Number of rows to process at once.
CHUNK_SIZE = 50_000


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def safe_float(value):
    """Convert a CSV value to float safely."""

    try:
        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        return float(value)

    except (ValueError, TypeError):
        return None


def calculate_risk_target(current_level, future_level):
    """
    Create a continuous flood-risk target.

    This is NOT a random value.

    The target is based on the observed future change
    in river level.

    Larger future rises = higher risk.
    """

    if current_level is None or future_level is None:
        return None

    rise = future_level - current_level

    # Convert river-level rise into a bounded risk score.
    #
    # 0.0  = very low
    # 1.0  = very high

    risk = 0.5 + (rise * 5.0)

    return max(0.0, min(1.0, risk))


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_dataset():
    """
    Load the processed CWC dataset and create training
    examples using future river levels.
    """

    print("=" * 70)
    print("FLOODFLASH ML DATA PREPARATION")
    print("=" * 70)

    print(f"\nInput file:")
    print(INPUT_FILE)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"\nDataset not found:\n{INPUT_FILE}\n\n"
            "Make sure feature engineering has been completed first."
        )

    rows = []

    # We first group observations by station.
    station_rows = defaultdict(list)

    print("\nReading dataset...")

    with INPUT_FILE.open("r", encoding="utf-8", newline="") as file:

        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=1):

            station = row.get("station")

            timestamp = row.get("timestamp")

            river_level = safe_float(row.get("river_level_m"))

            if not station or not timestamp or river_level is None:
                continue

            station_rows[station].append(
                {
                    "timestamp": timestamp,
                    "river_level_m": river_level,
                    "row": row,
                }
            )

            if row_number % CHUNK_SIZE == 0:
                print(f"Read {row_number:,} rows...")

    print(f"\nStations loaded: {len(station_rows)}")

    # -----------------------------------------------------
    # CREATE FUTURE TARGET
    # -----------------------------------------------------

    print("\nCreating future flood-risk targets...")

    feature_names = [
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

    for station, station_data in station_rows.items():

        # Dataset is already chronological, but sort again
        # to make future prediction alignment reliable.

        station_data.sort(key=lambda x: x["timestamp"])

        for index, current in enumerate(station_data):

            future_index = index + FORECAST_HOURS

            if future_index >= len(station_data):
                break

            future = station_data[future_index]

            current_level = current["river_level_m"]
            future_level = future["river_level_m"]

            target = calculate_risk_target(
                current_level,
                future_level,
            )

            if target is None:
                continue

            features = []

            valid = True

            for feature_name in feature_names:

                value = safe_float(
                    current["row"].get(feature_name)
                )

                if value is None:
                    valid = False
                    break

                features.append(value)

            if not valid:
                continue

            rows.append(
                (
                    features,
                    target,
                )
            )

    print(f"\nTraining examples created: {len(rows):,}")

    return rows, feature_names


# ---------------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------------

def train_model():

    rows, feature_names = load_dataset()

    if len(rows) < 100:
        raise RuntimeError(
            "Not enough valid training examples."
        )

    X = [row[0] for row in rows]

    y = [row[1] for row in rows]

    print("\nFeature count:", len(feature_names))

    print("\nFeatures:")

    for number, name in enumerate(feature_names, start=1):
        print(f"{number:2}. {name}")

    print("\nSplitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    print(f"Training samples: {len(X_train):,}")
    print(f"Testing samples:  {len(X_test):,}")

    # -----------------------------------------------------
    # RANDOM FOREST
    # -----------------------------------------------------

    print("\nTraining Random Forest model...")

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=18,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    print("Model training complete.")

    # -----------------------------------------------------
    # EVALUATION
    # -----------------------------------------------------

    print("\nEvaluating model...")

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    mse = mean_squared_error(
        y_test,
        predictions,
    )

    rmse = math.sqrt(mse)

    r2 = r2_score(
        y_test,
        predictions,
    )

    print("\nMODEL PERFORMANCE")
    print("=" * 50)

    print(f"MAE :  {mae:.6f}")
    print(f"RMSE:  {rmse:.6f}")
    print(f"R²  :  {r2:.6f}")

    # -----------------------------------------------------
    # FEATURE IMPORTANCE
    # -----------------------------------------------------

    print("\nFEATURE IMPORTANCE")
    print("=" * 50)

    importance = list(
        zip(
            feature_names,
            model.feature_importances_,
        )
    )

    importance.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    for name, score in importance:
        print(f"{name:25} {score:.4f}")

    # -----------------------------------------------------
    # SAVE MODEL
    # -----------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_package = {
        "model": model,
        "features": feature_names,
        "forecast_hours": FORECAST_HOURS,
    }

    with MODEL_FILE.open("wb") as file:

        pickle.dump(
            model_package,
            file,
        )

    print("\n" + "=" * 70)
    print("MODEL TRAINING COMPLETE")
    print("=" * 70)

    print(f"\nModel saved to:")
    print(MODEL_FILE)

    print("\nThe model is now ready for prediction.")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    train_model()