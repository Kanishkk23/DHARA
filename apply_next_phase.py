from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
API = ROOT / 'backend' / 'api.py'
PRED = ROOT / 'backend' / 'data' / 'ml' / 'predict.py'


def replace_once(path, old, new, label):
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly 1 match, found {count}')
    path.write_text(text.replace(old, new), encoding='utf-8')


def main():
    if not API.exists() or not PRED.exists():
        raise RuntimeError('Run this script from the FloodFlash project root.')

    api_backup = API.with_suffix('.py.nextphase-backup')
    pred_backup = PRED.with_suffix('.py.nextphase-backup')
    shutil.copy2(API, api_backup)
    shutil.copy2(PRED, pred_backup)

    try:
        replace_once(
            PRED,
            '''        self.risk_classes = saved_data.get(\n            "risk_classes",\n            None\n        )\n\n        self.station_thresholds = saved_data.get(\n''',
            '''        self.risk_classes = saved_data.get(\n            "risk_classes",\n            saved_data.get("classes", None)\n        )\n\n        self.evaluation = saved_data.get(\n            "evaluation",\n            None\n        )\n\n        self.station_thresholds = saved_data.get(\n''',
            'predict.py model metadata',
        )

        replace_once(
            PRED,
            '''        self.feature_importances = getattr(\n            self.model,\n            "feature_importances_",\n            None\n        )\n''',
            '''        self.feature_importances = saved_data.get(\n            "feature_importance",\n            getattr(\n                self.model,\n                "feature_importances_",\n                None\n            )\n        )\n''',
            'predict.py feature importance',
        )

        replace_once(
            PRED,
            '''        importance_values = list(\n            self.feature_importances\n        )\n\n        if len(importance_values) != len(self.features):\n\n            return {\n                "available": False,\n                "method": "Random Forest feature importance",\n                "top_factors": []\n            }\n\n        factors = []\n\n        for feature, importance in zip(\n            self.features,\n            importance_values\n        ):\n\n            importance = float(importance)\n''',
            '''        if isinstance(self.feature_importances, dict):\n            importance_by_feature = {\n                str(key): float(value)\n                for key, value in self.feature_importances.items()\n            }\n        else:\n            importance_values = list(self.feature_importances)\n\n            if len(importance_values) != len(self.features):\n                return {\n                    "available": False,\n                    "method": "Random Forest feature importance",\n                    "top_factors": []\n                }\n\n            importance_by_feature = dict(\n                zip(self.features, importance_values)\n            )\n\n        factors = []\n\n        for feature in self.features:\n\n            importance = float(\n                importance_by_feature.get(feature, 0.0)\n            )\n''',
            'predict.py XAI compatibility',
        )

        replace_once(
            PRED,
            '''            "prediction":\n                round(\n                    prediction,\n                    4\n                ),\n\n            "risk_probability":\n''',
            '''            "prediction":\n                round(\n                    prediction,\n                    4\n                ),\n\n            "prediction_class":\n                prediction,\n\n            "risk_probability":\n''',
            'predict.py prediction class',
        )

        old_eval = '''@app.get("/model/evaluation")\ndef model_evaluation():\n\n    return {\n        "status": "unavailable",\n        "message": (\n            "Actual model evaluation requires "\n            "the training/test dataset or evaluation "\n            "file. The current model file alone does "\n            "not contain ground-truth test labels."\n        ),\n        "metrics": {\n            "accuracy": None,\n            "precision": None,\n            "recall": None,\n            "f1_score": None,\n            "roc_auc": None,\n        },\n        "required_data": [\n            "training dataset",\n            "test dataset",\n            "ground truth labels",\n        ],\n    }\n'''
        new_eval = '''@app.get("/model/evaluation")\ndef model_evaluation():\n    """Return evaluation metrics stored with the trained model."""\n\n    if predictor is None:\n        return {\n            "status": "error",\n            "message": "Prediction model is unavailable",\n        }\n\n    evaluation = getattr(predictor, "evaluation", None)\n\n    if not isinstance(evaluation, dict):\n        return {\n            "status": "unavailable",\n            "message": "No evaluation metadata is stored in the model package.",\n            "metrics": {\n                "accuracy": None,\n                "precision": None,\n                "recall": None,\n                "f1_score": None,\n                "roc_auc": None,\n            },\n        }\n\n    return {\n        "status": "success",\n        "source": "Stored model evaluation from training run",\n        "task": evaluation.get("task"),\n        "forecast_hours": evaluation.get("forecast_hours", get_forecast_hours()),\n        "training_samples": evaluation.get("training_samples"),\n        "testing_samples": evaluation.get("testing_samples"),\n        "total_samples": evaluation.get("total_samples"),\n        "metrics": {\n            "accuracy": evaluation.get("accuracy"),\n            "precision": evaluation.get("precision"),\n            "recall": evaluation.get("recall"),\n            "f1_score": evaluation.get("f1", evaluation.get("f1_score")),\n            "roc_auc": evaluation.get("roc_auc"),\n        },\n        "confusion_matrix": evaluation.get("confusion_matrix"),\n        "classification_report": evaluation.get("classification_report"),\n    }\n'''
        replace_once(API, old_eval, new_eval, 'api.py evaluation endpoint')

        subprocess.run(
            [sys.executable, '-m', 'py_compile', str(API), str(PRED)],
            check=True,
        )

        print('SUCCESS: FloodFlash next phase applied.')
        print(f'Backup: {api_backup}')
        print(f'Backup: {pred_backup}')
        print('No frontend files were changed.')
        print('Next: restart backend and test /health, /predict, /model/evaluation.')

    except Exception:
        shutil.copy2(api_backup, API)
        shutil.copy2(pred_backup, PRED)
        raise


if __name__ == '__main__':
    main()
