import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def model_file_create(model_name:str):
    model_file_list = [
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

        # Core
        f"model/{model_name}/exception.py",
        f"model/{model_name}/logger.py",

        # Root
        "app.py",
        "Dockerfile",
        ".dockerignore",
        ".gitignore",
        ".env.example",
        "requirements.txt",
        "setup.py",
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
    for filepath in model_file_list:
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)
        if filedir != "":
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Creating directory: {filedir} for the {filename}")
            print(f"Creating directory: {filedir} for the {filename}")
        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, "w") as f:
                logging.info(f"Creating empty file: {filepath}")
                pass
        else:
            logging.info(f"{filepath} already exists and is not empty")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python template.py <model_name>"
        )
    model_name = sys.argv[1].strip()
    if not model_name:
        raise ValueError("Model name cannot be empty.")
    model_file_create(model_name)