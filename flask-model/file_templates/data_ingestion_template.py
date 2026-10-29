import os
import sys
from exception import CustomException
from logger import Logger
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.logger = Logger(model_name="data_ingestion")

    def initiate_data_ingestion(self, data_source):
        self.logger.info("Starting data ingestion process")

        try:
            # Read the dataset
            df = data_source
            self.logger.info(f"Dataset read successfully from {data_source}")

            # Create artifacts directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path), exist_ok=True)

            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            self.logger.info(f"Raw data saved at {self.ingestion_config.raw_data_path}.")

            # Split the dataset into training and testing sets
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

            # Save training and testing data
            train_df.to_csv(self.ingestion_config.train_data_path, index=False)
            test_df.to_csv(self.ingestion_config.test_data_path, index=False)
            self.logger.info(f"Training data saved at {self.ingestion_config.train_data_path}.")
            self.logger.info(f"Testing data saved at {self.ingestion_config.test_data_path}.")

            self.logger.info("Data ingestion process completed successfully")

            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
        except Exception as e:
            raise CustomException(e, sys)