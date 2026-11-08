import sys
import json
import numpy as np

from exception import CustomException
from logger import Logger

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

# change
# model_name with the name of the current model
from model.model_name.constants import MODEL_NAME
from model.model_name.constants.directories import ARTIFACT_DIR
# change


class ModelEvaluation:

    METRICS_REGISTRY = {
        "r2": r2_score,
        "mae": mean_absolute_error,
        "mse": mean_squared_error,
    }

    LOWER_IS_BETTER = {
        "mae",
        "mse",
        "rmse"
    }

    def __init__(self):
        self.logger = Logger(model_name=MODEL_NAME)

    def __calculate_metrics(self, y_test, y_pred):
        metrics = {}

        try:
            for name, metric in self.METRICS_REGISTRY.items():
                metrics[name] = float(metric(y_test, y_pred))

            metrics["rmse"] = float(np.sqrt(mean_squared_error(y_test, y_pred)))
            return metrics
        except Exception as e:
            raise CustomException(f"Error calculating evaluation metrics: {e}", sys)

    def __save_evaluation(self, metrics):
        try:
            ARTIFACT_DIR.mkdir(parents=True,exist_ok=True)

            evaluation_path = ARTIFACT_DIR / "evaluation.json"

            with open(evaluation_path, "w", encoding="utf-8") as file:
                json.dump(metrics, file, indent=4)
        except Exception as e:
            raise CustomException(f"Error saving evaluation results: {e}", sys)

    def initiate(self, model, X_test, y_test):
        self.logger.info("Initializing model evaluation")

        try:
            # Generate predictions
            y_pred = model.predict(X_test)

            # Calculate evaluation metrics
            metrics = self.__calculate_metrics(y_test, y_pred)

            # Save evaluation results
            evaluation_path = self.__save_evaluation(metrics)

            self.logger.info("Model evaluation completed successfully")

            return {
                "metrics": metrics,
                "evaluation_path": evaluation_path
            }

        except Exception as e:
            self.logger.exception("Model evaluation failed")
            raise CustomException(f"Error during model evaluation: {e}", sys)