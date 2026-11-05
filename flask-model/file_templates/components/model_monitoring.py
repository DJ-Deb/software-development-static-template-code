import sys
import json
import numpy as np
import pandas as pd

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


class ModelMonitoring:

    def __init__(self):
        self.logger = Logger(model_name=MODEL_NAME)

        self.psi_threshold = 0.2

    def __prediction_monitoring(self, predictions):

        try:
            predictions = np.asarray(predictions, dtype=float)

            if predictions.size == 0:
                raise ValueError("Predictions cannot be empty.")

            if not np.isfinite(predictions).all():
                raise ValueError("Predictions contain non-finite values.")

            return {
                "total_predictions": int(len(predictions)),
                "mean_prediction": float(np.mean(predictions)),
                "min_prediction": float(np.min(predictions)),
                "max_prediction": float(np.max(predictions)),
                "std_prediction": float(np.std(predictions))
            }

        except Exception as e:
            raise CustomException(f"Error during prediction monitoring: {e}", sys)

    def __calculate_psi(self, reference, current, bins=10):

        try:
            reference = pd.to_numeric(pd.Series(reference), errors="coerce").dropna().to_numpy()

            current = pd.to_numeric(pd.Series(current), errors="coerce").dropna().to_numpy()

            if len(reference) == 0 or len(current) == 0:
                raise ValueError("Reference and current data must contain valid values.")

            # Use reference data to establish bin boundaries
            breakpoints = np.unique(np.quantile(reference, np.linspace(0, 1, bins + 1)))

            # Constant reference feature
            if len(breakpoints) < 2:
                return 0.0 if np.all(current == reference[0]) else float("inf")

            # Extend boundaries to include all possible values
            breakpoints[0] = -np.inf
            breakpoints[-1] = np.inf

            reference_counts, _ = np.histogram(reference, bins=breakpoints)

            current_counts, _ = np.histogram(current, bins=breakpoints)

            # Calculate distributions
            epsilon = 1e-6

            reference_pct = (reference_counts / len(reference))

            current_pct = (current_counts / len(current))

            reference_pct = np.clip(reference_pct, epsilon, None)

            current_pct = np.clip(current_pct, epsilon, None)

            # Normalize after smoothing
            reference_pct /= reference_pct.sum()
            current_pct /= current_pct.sum()

            psi = np.sum((current_pct - reference_pct) * np.log(current_pct / reference_pct))

            return float(psi)

        except Exception as e:
            raise CustomException(f"Error calculating PSI: {e}", sys)

    def __data_drift_monitoring(self, reference_data, current_data):

        try:
            if not isinstance(reference_data, pd.DataFrame):
                raise TypeError("Reference data must be a DataFrame.")

            if not isinstance(current_data, pd.DataFrame):
                raise TypeError("Current data must be a DataFrame.")

            drift_results = {}

            common_columns = reference_data.columns.intersection(current_data.columns)

            if len(common_columns) == 0:
                raise ValueError("No common features found.")

            for column in common_columns:

                if (pd.api.types.is_numeric_dtype(reference_data[column]) and pd.api.types.is_numeric_dtype(current_data[column])):

                    psi = self.__calculate_psi(reference_data[column], current_data[column])

                    drift_results[column] = {
                        "psi": psi,
                        "drift_detected": psi >= self.psi_threshold
                    }

                else:
                    drift_results[column] = {
                        "drift_detected": None,
                        "message": "Categorical drift not implemented."
                    }

            return drift_results

        except Exception as e:
            raise CustomException(f"Error during data drift monitoring: {e}", sys)

    def __performance_monitoring(self, y_true, y_pred):

        try:
            if len(y_true) != len(y_pred):
                raise ValueError("Actual and predicted values must have equal lengths.")

            metrics = {
                "r2": float(r2_score(y_true, y_pred)),
                "mae": float(mean_absolute_error(y_true, y_pred)),
                "mse": float(mean_squared_error(y_true, y_pred)),
                "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred)))
            }

            return metrics

        except Exception as e:
            raise CustomException(f"Error during performance monitoring: {e}", sys)

    def initiate(self, reference_data, current_data, model, y_true=None):
        self.logger.info("Initializing model monitoring")

        try:
            # Generate predictions using raw features
            predictions = model.predict(current_data)

            # Prediction monitoring
            prediction_report = self.__prediction_monitoring(predictions)

            # Data drift monitoring
            drift_report = self.__data_drift_monitoring(reference_data, current_data)

            # Model performance monitoring
            performance_report = None

            if y_true is not None:
                performance_report = self.__performance_monitoring(y_true, predictions)

            # Prepare monitoring report
            report = {
                "model_name": MODEL_NAME,
                "prediction_monitoring": prediction_report,
                "data_drift_monitoring": drift_report,
                "model_performance_monitoring": performance_report
            }

            # Save report
            report_path = self.__save_report(report)

            self.logger.info(
                "Model monitoring completed successfully"
            )

            return {
                "report": report,
                "report_path": report_path
            }

        except Exception as e:
            self.logger.exception("Model monitoring failed")
            raise CustomException(f"Error during model monitoring: {e}", sys)