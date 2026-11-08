import sys
from exception import CustomException
from logger import Logger

import pandas as pd

# change
#model_name with the name of the current model
from model.model_name.constants import MODEL_NAME
# change


class ValidationPipeline:

    def __init__(self):
        self.logger = Logger(model_name="data_validation")

        self.steps = [
            getattr(self, name)
            for name, method in self.__class__.__dict__.items()
            if getattr(method, "_is_registered", False)
        ]

    @staticmethod
    def register(func):
        func._is_registered = True
        return func

    # Row validation operations

    @register
    def duplicate_rows(self, df):
        df.drop_duplicates(inplace=True)

    @register
    def drop_missing_rows(self, df):
        df.dropna(how="all", inplace=True)

    @register
    def reset_index(self, df):
        df.reset_index(drop=True, inplace=True)

    # Column validation operations

    @register
    def drop_missing_columns(self, df):
        df.dropna(axis=1, how="all", inplace=True)

    # Execute pipeline

    def run(self, df):

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        df = df.copy()

        total_steps = len(self.steps)

        self.logger.info(f"Starting data validation | Total steps: {total_steps}")

        for index, step in enumerate(self.steps, start=1):
            step(df)
            self.logger.info(f"[Step {index}/{total_steps}] Successfully completed: {step.__name__}")

        return df


class DataValidation:

    def __init__(self):
        self.logger = Logger(model_name="data_validation")

    def initiate(self, data: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Starting data validation component")

        try:
            pipeline = ValidationPipeline()

            validated_data = pipeline.run(data)

            self.logger.info(f"Data validation completed successfully | Shape: {validated_data.shape}")

            return validated_data

        except Exception as e:
            self.logger.exception("Data validation failed")
            raise CustomException(e, sys)