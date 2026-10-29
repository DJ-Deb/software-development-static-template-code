import logging
from pathlib import Path
from datetime import datetime


# LOG CONFIGURATION
BASE_DIR = Path(__file__).resolve().parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# LOGGER CLASS
class Logger:
    """
        Reusable logger class for project components.\n
        Initializes a logger for the specified model or component.\n
        logger = Logger(model_name)\n
        model_name should be a string such as "data_ingestion", "training", or "prediction".\n
        USAGE:\n
        \tlogger.info("info message")\n
        \tlogger.error("error message")\n
        \tlogger.debug("debug message")\n
        \tlogger.warning("warning message")\n
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

        # Initialize the actual Python logger
        self.logger = self.get_logger(model_name)

    @staticmethod
    def get_logger(model_name: str) -> logging.Logger:
        """Create or retrieve a configured Python logger."""

        logger = logging.getLogger(model_name)
        logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Create a daily log file
        log_file = LOG_DIR / (
            f"{model_name}_"
            f"{datetime.now().strftime('%Y-%m-%d')}.log"
        )

        # Create handlers
        file_handler = logging.FileHandler(log_file, encoding="utf-8")

        console_handler = logging.StreamHandler()

        # Define log format
        formatter = logging.Formatter(
            "%(asctime)s | "
            "%(name)s | "
            "%(levelname)s | "
            "%(filename)s:%(lineno)d | "
            "%(message)s"
        )

        # Apply formatting
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Attach handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger


    # LOGGING METHODS
    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def exception(self, message: str) -> None:
        # Use inside an exception handler to include the traceback.
        self.logger.exception(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)
