import os
import sys
from exception import CustomException
from logger import Logger

from dataclasses import dataclass

import pandas as pd

# change
#model_name with the name of the current model
from model.model_name.constants import MODEL_NAME
from model.model_name.constants.directories import ARTIFACT_DIR
#change


@dataclass
class DataIngestionConfig:
    raw_data_path: str = ARTIFACT_DIR/"raw.csv"

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.logger = Logger(model_name=MODEL_NAME)

    def initiate(self, data: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Starting data ingestion process")

        try:
            # Read the dataset
            df = data
            self.logger.info(f"Dataset read successfully from {data}")

            # Create artifacts directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            self.logger.info(f"Raw data saved at {self.ingestion_config.raw_data_path}.")

            self.logger.info("Data ingestion process completed successfully")

            return df
        except Exception as e:
            self.logger.exception("Data Ingestion failed")
            raise CustomException(e, sys)