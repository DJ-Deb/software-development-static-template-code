import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def model_file_create(model_name:str):
    model_file_list = [
        f"model/{model_name}/__init__.py",
        f"model/{model_name}/components/__init__.py",
        f"model/{model_name}/components/data_ingestion.py",
        f"model/{model_name}/components/data_transformation.py",
        f"model/{model_name}/components/model_trainer.py",
        f"model/{model_name}/components/model_monitoring.py",
        f"model/{model_name}/pipelines/__init__.py",
        f"model/{model_name}/pipelines/prediction_pipeline.py",
        f"model/{model_name}/pipelines/training_pipeline.py",
        f"model/{model_name}/exception.py",
        f"model/{model_name}/logger.py",
        f"model/{model_name}/utils.py",
        f"model/{model_name}/exception.py",
        "app.py",
        "Dockerfile",
        "requirements.txt",
        "setup.py"
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
            logging.info(f"{filepath} is already empty")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python template.py <model_name>"
        )
    model_name = sys.argv[1].strip()
    if not model_name:
        raise ValueError("Model name cannot be empty.")
    model_file_create(model_name)
