import logging
from pathlib import Path
from datetime import datetime

# Log Configuration
BASE_DIR = Path(__file__).resolve().parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logger Factory
def get_logger(model_name: str) -> logging.Logger:
    logger = logging.getLogger(model_name)

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Log File
    log_file = LOG_DIR / (
        f"{model_name}_"
        f"{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    # Handlers
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(name)s | "
        "%(levelname)s | "
        "%(filename)s:%(lineno)d | "
        "%(message)s"
    )

    # Apply Formatter
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add Handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    return logger