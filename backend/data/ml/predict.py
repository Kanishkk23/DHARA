import os
import pickle
import pandas as pd


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "models",
    "flood_risk_model_v2.pkl"
)


# ============================================================
# FLOOD RISK PREDICTOR V2
# ============================================================

class FloodRiskPredictor:

    def __init__(self):

        with open(MODEL_PATH, "rb") as f:
            saved_data = pickle.load(f)

        self.model = saved_data["model"]
        self.features = saved_data["features"]

        self.forecast_hours = saved_data.get(
            "forecast_hours",
            6
        )

        self.risk_classes = saved_data.get(
            "risk_classes",
            saved_data.get("classes", None)
        )

        self.evaluation = saved_data.get(
            "evaluation",
            None
        )

        self.station_thresholds = saved_data.get(
            "station_thresholds",
            {}
        )

        # Real Random Forest feature importance
        self.feature_importances = saved_data.get(
            "feature_importance",
            getattr(
                self.model,
                "feature_importances_",
                None
            )
        )

        print("=" * 60)
        print("FLOODFLASH V2 MODEL LOADED")
        print("=" * 60)

        print(f"Model path     : {MODEL_PATH}")
        print(f"Model features : {len(self.features)}")
        print(f"Forecast hours : {self.forecast_hours}")
        print(f"Risk classes   : {self.risk_classes}")

        if self.feature_importances is not None:
            print("Feature XAI   : AVAILABLE")
        else:
            print("Feature XAI   : NOT AVAILABLE")


    # ========================================================
    # REAL XAI
    # ========================================================

    def get_xai(self, features: dict):

        if self.feature_importances is None:

            return {
                "available": False,
                "method": "Random Forest feature importance",
                "top_factors": []
            }

        if isinstance(self.feature_importances, dict):
            importance_by_feature = {
                str(key): float(value)
                for key, value in self.feature_importances.items()
            }
        else:
            importance_values = list(self.feature_importances)

            if len(importance_values) != len(self.features):
                return {
                    "available": False,
                    "method": "Random Forest feature importance",
                    "top_factors": []
                }

            importance_by_feature = dict(
                zip(self.features, importance_values)
            )

        factors = []

        for feature in self.features:

            importance = float(
                importance_by_feature.get(feature, 0.0)
            )

            factors.append({

                "feature": feature,

                "importance": round(
                    importance,
                    6
                ),

                "importance_percent": round(
                    importance * 100,
                    2
                ),

                "value": features.get(
                    feature
                )
            })

        # Highest-impact features first
        factors.sort(
            key=lambda x: x["importance"],
            reverse=True
        )

        # Top 5
        top_factors = factors[:5]

        return {

            "available": True,

            "method":
                "Random Forest feature importance",

            "total_features":
                len(self.features),

            "top_factors":
                top_factors
        }


    # ========================================================
    # PREDICTION
    # ========================================================

    def predict(self, features: dict):

        # ----------------------------------------------------
        # Validate features
        # ----------------------------------------------------

        data = {}

        for feature in self.features:

            if feature not in features:

                raise ValueError(
                    f"Missing required feature: {feature}"
                )

            data[feature] = features[feature]


        # ----------------------------------------------------
        # Preserve exact training feature order
        # ----------------------------------------------------

        df = pd.DataFrame(
            [data],
            columns=self.features
        )


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        prediction = self.model.predict(df)[0]

        prediction = int(prediction)


        # ----------------------------------------------------
        # CLASS PROBABILITIES
        # ----------------------------------------------------

        probabilities = {}

        if hasattr(
            self.model,
            "predict_proba"
        ):

            proba = self.model.predict_proba(df)[0]

            classes = self.model.classes_

            for class_value, probability in zip(
                classes,
                proba
            ):

                class_name = self.get_class_name(
                    class_value
                )

                probabilities[class_name] = round(
                    float(probability) * 100,
                    2
                )


        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        risk_level = self.get_class_name(
            prediction
        )


        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        if probabilities:

            confidence = max(
                probabilities.values()
            )

        else:

            confidence = 0.0


        # ----------------------------------------------------
        # ALERT STATUS
        # ----------------------------------------------------

        if risk_level == "CRITICAL":

            alert_status = "ALERT"

        elif risk_level == "HIGH":

            alert_status = "WARNING"

        elif risk_level == "MODERATE":

            alert_status = "WATCH"

        else:

            alert_status = "NORMAL"


        # ----------------------------------------------------
        # REAL XAI
        # ----------------------------------------------------

        xai = self.get_xai(
            features
        )


        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return {

            "prediction":
                round(
                    prediction,
                    4
                ),

            "prediction_class":
                prediction,

            "risk_probability":
                round(
                    probabilities.get(
                        risk_level,
                        0.0
                    ),
                    2
                ),

            "risk_level":
                risk_level,

            "alert_status":
                alert_status,

            "forecast_hours":
                self.forecast_hours,

            "model_confidence":
                round(
                    confidence,
                    2
                ),

            "class_probabilities":
                probabilities,

            "xai":
                xai
        }


    # ========================================================
    # CLASS NAME
    # ========================================================

    def get_class_name(
        self,
        class_value
    ):

        class_mapping = {

            0: "LOW",

            1: "MODERATE",

            2: "HIGH",

            3: "CRITICAL"
        }

        try:

            class_value = int(
                class_value
            )

        except (
            ValueError,
            TypeError
        ):

            return str(
                class_value
            )

        return class_mapping.get(
            class_value,
            str(class_value)
        )


# ================================================================
# TEST
# ================================================================

if __name__ == "__main__":

    predictor = FloodRiskPredictor()


    sample = {

        "river_level_m": 4.0,

        "river_level_change_m": 0.1,

        "level_mean_3h": 4.0,

        "level_mean_6h": 4.0,

        "level_mean_24h": 4.0,

        "level_std_3h": 0.01,

        "level_std_6h": 0.02,

        "level_std_24h": 0.03,

        "level_delta_3h": 0.1,

        "level_delta_6h": 0.15,

        "level_delta_24h": 0.2,

        "change_mean_3h": 0.03,

        "change_mean_6h": 0.04,

        "change_mean_24h": 0.05,

        "hour": 12,

        "day_of_week": 2,

        "month": 8
    }


    result = predictor.predict(
        sample
    )


    print()
    print("=" * 60)
    print("FLOODFLASH V2 RISK PREDICTION")
    print("=" * 60)

    print(
        f"Prediction       : "
        f"{result['prediction']}"
    )

    print(
        f"Risk Probability : "
        f"{result['risk_probability']}%"
    )

    print(
        f"Risk Level       : "
        f"{result['risk_level']}"
    )

    print(
        f"Alert Status     : "
        f"{result['alert_status']}"
    )

    print(
        f"Forecast Hours   : "
        f"{result['forecast_hours']}"
    )

    print(
        f"Model Confidence : "
        f"{result['model_confidence']}%"
    )


    # ============================================================
    # CLASS PROBABILITIES
    # ============================================================

    print()
    print("=" * 60)
    print("CLASS PROBABILITIES")
    print("=" * 60)

    for (
        class_name,
        probability
    ) in result[
        "class_probabilities"
    ].items():

        print(
            f"{class_name:10} : "
            f"{probability}%"
        )


    # ============================================================
    # REAL XAI
    # ============================================================

    print()
    print("=" * 60)
    print("REAL XAI")
    print("=" * 60)

    xai = result["xai"]

    print(
        f"XAI Available : "
        f"{xai['available']}"
    )

    print(
        f"XAI Method    : "
        f"{xai['method']}"
    )

    print(
        f"Total Features: "
        f"{xai.get('total_features', 0)}"
    )

    print()

    for index, factor in enumerate(
        xai["top_factors"],
        start=1
    ):

        print(
            f"{index}. "
            f"{factor['feature']} "
            f"→ "
            f"{factor['importance_percent']}% "
            f"importance "
            f"(value: {factor['value']})"
        )

    print("=" * 60)