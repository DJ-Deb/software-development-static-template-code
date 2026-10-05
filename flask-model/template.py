import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

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
        ".env.example",
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
            logging.info(f"Created file: {filepath}")
        elif filepath.stat().st_size == 0:
            logging.info(f"File already exists and is empty: {filepath}")
        else:
            logging.info(f"File already exists: {filepath}")

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python template.py <model_name>")

    model_name = sys.argv[1].strip()

    if not model_name:
        raise ValueError("Model name cannot be empty.")

    model_file_create(model_name)