import sys
from pathlib import Path
from textwrap import dedent

from logger import Logger

logger = Logger(model_name="template_generator")

class Templates:
    def get_data_ingestion_template() -> str:
        '''Return the source code for data_ingestion.py.'''

        return dedent('''
            import os
            import sys
            import pandas as pd

            from dataclasses import dataclass
            from sklearn.model_selection import train_test_split

            from exception import CustomException
            from logger import Logger


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
                        # CHANGE HERE: Add source-specific reading logic
                        # if data_source is a file path or API response.
                        df = data_source

                        if not isinstance(df, pd.DataFrame):
                            raise TypeError("data_source must be a pandas DataFrame")

                        self.logger.info("Dataset received successfully")

                        # Create the output directory.
                        os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

                        # Save raw data.
                        df.to_csv(self.ingestion_config.raw_data_path, index=False)
                        self.logger.info("Raw data saved at %s", self.ingestion_config.raw_data_path)

                        # CHANGE HERE: Adjust test_size and random_state
                        # according to your project's requirements.
                        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

                        # Save training and testing data.
                        train_df.to_csv(self.ingestion_config.train_data_path, index=False)
                        test_df.to_csv(self.ingestion_config.test_data_path, index=False)
                        self.logger.info("Training data saved at %s", self.ingestion_config.train_data_path)
                        self.logger.info("Testing data saved at %s", self.ingestion_config.test_data_path)

                        self.logger.info("Data ingestion completed successfully")

                        return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)

                    except Exception as e:
                        self.logger.exception("Data ingestion failed")
                        raise CustomException(e, sys) from e
        ''').lstrip()

    def get_requirement_template() -> str:
        '''Return the content for requirements.txt.'''

        return dedent('''
            # Add your project dependencies here
            flask
            dvc
            pandas
            numpy
            scikit-learn
            python-dotenv
        ''').lstrip()

# Model Structure
def model_file_create(model_name: str):
    model_file_list = [
        # Model
        f"model/{model_name}/__init__.py",

        # Components
        f"model/{model_name}/components/__init__.py",
        f"model/{model_name}/components/data_ingestion.py",
        f"model/{model_name}/components/data_validation.py",
        f"model/{model_name}/components/data_transformation.py",
        f"model/{model_name}/components/model_trainer.py",
        f"model/{model_name}/components/model_evaluation.py",
        f"model/{model_name}/components/model_monitoring.py",

        # Pipelines
        f"model/{model_name}/pipelines/__init__.py",
        f"model/{model_name}/pipelines/training_pipeline.py",
        f"model/{model_name}/pipelines/prediction_pipeline.py",

        # Configuration
        f"model/{model_name}/config/__init__.py",
        f"model/{model_name}/config/configuration.py",

        # Utilities
        f"model/{model_name}/utils/__init__.py",
        f"model/{model_name}/utils/common.py",

        # Constants
        f"model/{model_name}/constants/__init__.py",
        f"model/{model_name}/constants/constants.py",

        # Root
        "app.py",
        "Dockerfile",
        ".dockerignore",
        ".gitignore",
        ".env",
        "requirements.txt",
        "pyproject.toml",
        "README.md",

        # Testing
        "tests/__init__.py",
        "tests/test_data.py",
        "tests/test_model.py",
        "tests/test_pipeline.py",

        # Configuration
        "config/config.yaml",
    ]

    # Create Files
    for filepath in model_file_list:
        filepath = Path(filepath)
        filedir = filepath.parent

        if filedir != Path("."):
            filedir.mkdir(parents=True, exist_ok=True)
        if not filepath.exists():
            filepath.touch()
            logger.info(f"Created file: {filepath}")
        elif filepath.stat().st_size == 0:
            logger.info(f"File already exists and is empty: {filepath}")
        else:
            logger.info(f"File already exists: {filepath}")

    data_ingestion_path = (Path(f"model/{model_name}/components/data_ingestion.py"))

    overwrite = False

    requirements_path = Path("requirements.txt")

    if requirements_path.exists() and requirements_path.stat().st_size == 0:
        requirements_content = Templates.get_requirement_template()
        requirements_path.write_text(requirements_content, encoding="utf-8")
        logger.info(f"Requirements template written to {requirements_path}")

    if (data_ingestion_path.exists() and data_ingestion_path.stat().st_size > 0):
        logger.warning(f"File {data_ingestion_path} already exists and is not empty.")
    else:
        template_code = Templates.get_data_ingestion_template()
        data_ingestion_path.write_text(template_code, encoding="utf-8")
        logger.info(f"Data ingestion template written to {data_ingestion_path}")



# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python template.py <model_name>")

    model_name = sys.argv[1].strip()

    if not model_name:
        raise ValueError("Model name cannot be empty.")

    model_file_create(model_name)