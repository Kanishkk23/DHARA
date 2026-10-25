"""
FloodFlash V2 - Time-Aware Flood Risk Model

Trains a real Random Forest classification model using
processed Central Water Commission river-level observations.

The trained model package also stores REAL evaluation
metrics and feature importance for the FloodFlash API.
"""

from pathlib import Path
import csv
import pickle
from collections import defaultdict
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cwc_ml_features.csv"
)

MODEL_DIR = BASE_DIR / "models"

MODEL_FILE = (
    MODEL_DIR
    / "flood_risk_model_v2.pkl"
)


# ============================================================
# CONFIGURATION
# ============================================================

FORECAST_HOURS = 6


# ============================================================
# MODEL FEATURES
# ============================================================

FEATURES = [

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


# ============================================================
# SAFE FLOAT
# ============================================================

def safe_float(value):

    try:

        if value is None:
            return None

        value = str(value).strip()

        if not value:
            return None

        return float(value)

    except (ValueError, TypeError):

        return None


# ============================================================
# TIMESTAMP
# ============================================================

def parse_timestamp(value):

    try:

        return datetime.fromisoformat(value)

    except (ValueError, TypeError):

        return None


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("=" * 70)
    print("FLOODFLASH V2 - LOADING CWC DATA")
    print("=" * 70)

    print(
        f"\nInput file:\n{INPUT_FILE}"
    )

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n{INPUT_FILE}"
        )

    stations = defaultdict(list)

    with INPUT_FILE.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row_number, row in enumerate(
            reader,
            start=1
        ):

            station = row.get(
                "station"
            )

            timestamp = parse_timestamp(
                row.get("timestamp")
            )

            if not station or timestamp is None:

                continue

            river_level = safe_float(
                row.get(
                    "river_level_m"
                )
            )

            if river_level is None:

                continue

            features = []

            valid = True

            for feature in FEATURES:

                value = safe_float(
                    row.get(feature)
                )

                if value is None:

                    valid = False

                    break

                features.append(value)

            if not valid:

                continue

            stations[station].append(
                {
                    "timestamp": timestamp,

                    "river_level": river_level,

                    "features": features,
                }
            )

            if row_number % 100_000 == 0:

                print(
                    f"Read {row_number:,} rows..."
                )

    print(
        f"\nStations loaded: "
        f"{len(stations)}"
    )

    return stations


# ============================================================
# CREATE TRAINING DATA
# ============================================================

def create_training_data(stations):

    print(
        "\nCreating time-aware training data..."
    )

    all_timestamps = []

    for station_rows in stations.values():

        for row in station_rows:

            all_timestamps.append(
                row["timestamp"]
            )

    if len(all_timestamps) < 100:

        raise RuntimeError(
            "Not enough timestamped observations."
        )

    all_timestamps.sort()

    split_index = int(
        len(all_timestamps) * 0.80
    )

    split_index = min(
        split_index,
        len(all_timestamps) - 1
    )

    split_time = all_timestamps[
        split_index
    ]

    print(
        "\nChronological split:"
    )

    print(
        "Training data before:",
        split_time
    )

    # ========================================================
    # CALCULATE STATION THRESHOLDS
    # ONLY USING TRAINING PERIOD
    # ========================================================

    station_levels = defaultdict(list)

    for station, rows in stations.items():

        rows.sort(
            key=lambda x:
            x["timestamp"]
        )

        for row in rows:

            if row["timestamp"] < split_time:

                station_levels[
                    station
                ].append(
                    row["river_level"]
                )

    thresholds = {}

    for station, levels in station_levels.items():

        if len(levels) < 20:

            continue

        levels.sort()

        p80_index = int(
            len(levels) * 0.80
        )

        p90_index = int(
            len(levels) * 0.90
        )

        p95_index = int(
            len(levels) * 0.95
        )

        thresholds[station] = {

            "moderate": levels[
                min(
                    p80_index,
                    len(levels) - 1
                )
            ],

            "high": levels[
                min(
                    p90_index,
                    len(levels) - 1
                )
            ],

            "critical": levels[
                min(
                    p95_index,
                    len(levels) - 1
                )
            ],
        }

    print(
        f"\nThresholds calculated for "
        f"{len(thresholds)} stations."
    )

    # ========================================================
    # CREATE TRAIN / TEST EXAMPLES
    # ========================================================

    training_rows = []

    testing_rows = []

    for station, rows in stations.items():

        if station not in thresholds:

            continue

        rows.sort(
            key=lambda x:
            x["timestamp"]
        )

        station_thresholds = (
            thresholds[station]
        )

        for index, current in enumerate(
            rows
        ):

            future_index = (
                index + FORECAST_HOURS
            )

            if future_index >= len(rows):

                break

            future = rows[
                future_index
            ]

            target_level = (
                future["river_level"]
            )

            # ------------------------------------------------
            # Four-class flood-risk target
            # ------------------------------------------------

            if target_level >= station_thresholds[
                "critical"
            ]:

                target = 3

            elif target_level >= station_thresholds[
                "high"
            ]:

                target = 2

            elif target_level >= station_thresholds[
                "moderate"
            ]:

                target = 1

            else:

                target = 0

            example = (
                current["features"],
                target
            )

            if current["timestamp"] < split_time:

                training_rows.append(
                    example
                )

            else:

                testing_rows.append(
                    example
                )

    print(
        f"\nTraining examples: "
        f"{len(training_rows):,}"
    )

    print(
        f"Testing examples: "
        f"{len(testing_rows):,}"
    )

    return (
        training_rows,
        testing_rows,
        thresholds,
    )


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model():

    stations = load_data()

    (
        training_rows,
        testing_rows,
        thresholds,
    ) = create_training_data(
        stations
    )

    if len(training_rows) < 100:

        raise RuntimeError(
            "Not enough training examples."
        )

    if len(testing_rows) < 20:

        raise RuntimeError(
            "Not enough testing examples."
        )

    # ========================================================
    # PREPARE DATA
    # ========================================================

    X_train = [
        row[0]
        for row in training_rows
    ]

    y_train = [
        row[1]
        for row in training_rows
    ]

    X_test = [
        row[0]
        for row in testing_rows
    ]

    y_test = [
        row[1]
        for row in testing_rows
    ]

    # ========================================================
    # TRAIN RANDOM FOREST
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "TRAINING RANDOM FOREST CLASSIFIER"
    )

    print(
        "=" * 70
    )

    model = RandomForestClassifier(

        n_estimators=120,

        max_depth=18,

        min_samples_leaf=5,

        class_weight="balanced",

        random_state=42,

        n_jobs=-1,
    )

    model.fit(
        X_train,
        y_train
    )

    print(
        "\nTraining complete."
    )

    # ========================================================
    # PREDICTIONS
    # ========================================================

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )

    # ========================================================
    # CLASSIFICATION METRICS
    # ========================================================

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    # ========================================================
    # ROC-AUC
    # ========================================================

    try:

        roc_auc = roc_auc_score(
            y_test,
            probabilities,
            multi_class="ovr",
            average="weighted"
        )

    except ValueError:

        roc_auc = None

    # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=[
            0,
            1,
            2,
            3
        ]
    )

    confusion_matrix_data = {

        "labels": [
            "LOW",
            "MODERATE",
            "HIGH",
            "CRITICAL"
        ],

        "matrix":
            matrix.tolist(),
    }

    # ========================================================
    # CLASSIFICATION REPORT
    # ========================================================

    report = classification_report(
        y_test,
        predictions,
        labels=[
            0,
            1,
            2,
            3
        ],
        target_names=[
            "LOW",
            "MODERATE",
            "HIGH",
            "CRITICAL"
        ],
        output_dict=True,
        zero_division=0
    )

    # ========================================================
    # FEATURE IMPORTANCE
    # ========================================================

    print(
        "\nFEATURE IMPORTANCE"
    )

    print(
        "=" * 50
    )

    importance = list(
        zip(
            FEATURES,
            model.feature_importances_
        )
    )

    importance.sort(
        key=lambda x:
        x[1],
        reverse=True
    )

    feature_importance = {}

    for name, score in importance:

        score = float(score)

        feature_importance[
            name
        ] = score

        print(
            f"{name:25} "
            f"{score:.4f}"
        )

    # ========================================================
    # PRINT PERFORMANCE
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "FLOODFLASH V2 MODEL PERFORMANCE"
    )

    print(
        "=" * 70
    )

    print(
        f"\nAccuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    if roc_auc is not None:

        print(
            f"ROC-AUC  : {roc_auc:.4f}"
        )

    else:

        print(
            "ROC-AUC  : unavailable"
        )

    print(
        "\nClassification report:"
    )

    print(
        classification_report(
            y_test,
            predictions,
            labels=[
                0,
                1,
                2,
                3
            ],
            target_names=[
                "LOW",
                "MODERATE",
                "HIGH",
                "CRITICAL"
            ],
            zero_division=0
        )
    )

    print(
        "\nConfusion matrix:"
    )

    print(
        matrix
    )

    # ========================================================
    # EVALUATION PACKAGE
    # ========================================================

    evaluation = {

        "task": "four_class_flood_risk_classification",

        "forecast_hours":
            FORECAST_HOURS,

        "training_samples":
            len(X_train),

        "testing_samples":
            len(X_test),

        "total_samples":
            len(X_train) + len(X_test),

        "accuracy":
            float(accuracy),

        "precision":
            float(precision),

        "recall":
            float(recall),

        "f1":
            float(f1),

        "roc_auc":
            (
                float(roc_auc)
                if roc_auc is not None
                else None
            ),

        "confusion_matrix":
            confusion_matrix_data,

        "classification_report":
            report,
    }

    # ========================================================
    # SAVE MODEL
    # ========================================================

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    package = {

        "model":
            model,

        "features":
            FEATURES,

        "thresholds":
            thresholds,

        "forecast_hours":
            FORECAST_HOURS,

        "classes": {

            0: "LOW",

            1: "MODERATE",

            2: "HIGH",

            3: "CRITICAL",
        },

        "evaluation":
            evaluation,

        "feature_importance":
            feature_importance,
    }

    with MODEL_FILE.open(
        "wb"
    ) as file:

        pickle.dump(
            package,
            file
        )

    # ========================================================
    # COMPLETE
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "FLOODFLASH V2 MODEL COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        f"\nModel saved to:\n{MODEL_FILE}"
    )

    print(
        "\nSaved inside model:"
    )

    print(
        "✓ Random Forest classifier"
    )

    print(
        "✓ 17 model features"
    )

    print(
        "✓ Station thresholds"
    )

    print(
        "✓ Four risk classes"
    )

    print(
        "✓ Accuracy"
    )

    print(
        "✓ Precision"
    )

    print(
        "✓ Recall"
    )

    print(
        "✓ F1 Score"
    )

    print(
        "✓ ROC-AUC"
    )

    print(
        "✓ Confusion matrix"
    )

    print(
        "✓ Classification report"
    )

    print(
        "✓ Feature importance"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    train_model()