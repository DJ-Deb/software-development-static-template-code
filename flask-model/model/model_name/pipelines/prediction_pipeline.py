import sys
import joblib
import pandas as pd

from exception import CustomException
from logger import Logger

# change
from model.model_name.constants import MODEL_NAME
from model.model_name.constants.directories import ARTIFACT_DIR
# change


class PredictionPipeline:

    def __init__(self):
        self.logger = Logger(model_name=MODEL_NAME)

    def __load_model(self):

        try:
            model_path = ARTIFACT_DIR / "trained_model.joblib"

            if not model_path.exists():
                raise FileNotFoundError(f"Model not found: {model_path}")

            return joblib.load(model_path)

        except Exception as e:
            raise CustomException(f"Error loading model: {e}", sys)

    def __validate_input(self, data, model):

        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        if data.empty:
            raise ValueError("Input data cannot be empty.")

        expected_columns = list(model.named_steps["preprocessor"].feature_names_in_)

        missing_columns = [
            column for column in expected_columns
            if column not in data.columns
        ]

        unexpected_columns = [
            column for column in data.columns
            if column not in expected_columns
        ]

        if missing_columns or unexpected_columns:
            raise ValueError(f"Missing columns: {missing_columns}; " f"Unexpected columns: {unexpected_columns}")

        return data[expected_columns]

    def initiate(self, data):
        self.logger.info("Starting prediction pipeline")

        try:

            # Load trained pipeline
            model = self.__load_model()

            # Validate and arrange input columns
            data = self.__validate_input(data, model)

            # Automatic preprocessing + prediction
            predictions = model.predict(data)

            result = pd.DataFrame({
                "prediction": predictions
            })

            self.logger.info("Prediction completed successfully")

            return result

        except Exception as e:
            self.logger.exception("Prediction pipeline failed")
            raise CustomException(f"Error during prediction: {e}", sys)